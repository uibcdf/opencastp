"""Audit printed CASTp orthospheres against complete native region domains.

This developer tool reads trusted local geometry snapshots and original external
archives. It does not qualify areas, volumes, per-atom contributions or individual
mouths. The four-decimal tolerance is fixed independently of observed failures.
Run from the repository with ``python -m devtools.audit_castp_orthospheres``.
"""

import argparse
import hashlib
import json
import pickle
import subprocess
import sys
from collections import Counter, defaultdict
from importlib import metadata
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
from scipy.spatial import cKDTree

from opencastp._core.components import build_castp_feature_records

TOLERANCE_ANGSTROM = 0.00005001


def compare_spheres(expected: np.ndarray, actual: np.ndarray) -> dict:
    """Require a bijection of center/radius rows in explicit angstrom units.

    Parameters
    ----------
    expected, actual : array-like, shape (n, 4)
        Printed and calculated x/y/z/radius values. Negative radii, invalid
        shapes and nonfinite numbers are rejected; duplicate rows remain.

    Returns
    -------
    dict
        Maximum one-to-one matches, errors and unmatched row indices. A pass
        only certifies this comparison, not complete server equivalence.

    Raises
    ------
    ValueError
        If either array has invalid shape, values or radii.
    """
    expected, actual = (
        np.asarray(expected, dtype=float),
        np.asarray(actual, dtype=float),
    )
    for array in (expected, actual):
        if array.ndim != 2 or array.shape[1] != 4:
            raise ValueError("Orthospheres must have shape (n, 4)")
        if not np.all(np.isfinite(array)) or np.any(array[:, 3] < 0):
            raise ValueError(
                "Orthospheres must have finite values and nonnegative radii"
            )
    rows, columns = [], []
    if len(actual):
        candidates = cKDTree(actual[:, :3]).query_ball_point(
            expected[:, :3], TOLERANCE_ANGSTROM, p=np.inf
        )
        for i, neighbors in enumerate(candidates):
            for j in neighbors:
                if abs(expected[i, 3] - actual[j, 3]) <= TOLERANCE_ANGSTROM:
                    rows.append(i)
                    columns.append(j)
    pairs = []
    if rows:
        graph = csr_matrix(
            (np.ones(len(rows)), (rows, columns)), shape=(len(expected), len(actual))
        )
        matching = maximum_bipartite_matching(graph, perm_type="column")
        for i, j in enumerate(matching):
            if j >= 0:
                pairs.append(
                    dict(
                        server_index=i,
                        native_index=int(j),
                        center_max_absolute_error_angstrom=float(
                            np.max(np.abs(expected[i, :3] - actual[j, :3]))
                        ),
                        radius_absolute_error_angstrom=float(
                            abs(expected[i, 3] - actual[j, 3])
                        ),
                    )
                )
    missing = sorted(set(range(len(expected))) - {row["server_index"] for row in pairs})
    extra = sorted(set(range(len(actual))) - {row["native_index"] for row in pairs})
    return dict(
        server_spheres=len(expected),
        native_spheres=len(actual),
        matched_spheres=len(pairs),
        missing=missing,
        extra=extra,
        pairs=pairs,
        tolerance_angstrom=TOLERANCE_ANGSTROM,
        passed=not missing and not extra,
        complete_server_equivalence=False,
    )


def audit_geometry(archive_path: Path, geometry) -> dict:
    """Pair region memberships before auditing every exported supporting sphere.

    Numerical geometry is supplied independently of archive result labels.
    This checks a geometric bijection; it does not independently recompute
    atom contacts or identify individual mouth triangles.
    """
    from devtools.compare_castp_servers import read_archive

    _pdb, reference = read_archive(archive_path)
    with ZipFile(archive_path) as handle:
        names = [name for name in handle.namelist() if name.endswith(".bulb.json")]
        if len(names) != 1:
            raise ValueError("Expected exactly one bulb JSON file")
        raw = handle.read(names[0])
    bulbs = json.loads(raw)
    if not isinstance(bulbs, list) or set(r["server_id"] for r in reference) != set(
        range(1, len(bulbs) + 1)
    ):
        raise ValueError("Bulb arrays and region IDs differ")
    features = build_castp_feature_records(
        geometry, probe_radius=1.4, pocket_definition="castp3"
    )

    def key(item):
        return item["feature_type"], tuple(sorted(item["atom_indices"]))

    expected_counts = Counter(map(key, reference))
    actual_counts = Counter(map(key, features))
    buckets = defaultdict(list)
    for feature in features:
        buckets[key(feature)].append(feature)
    rows = []
    for target in reference:
        candidates = buckets[key(target)]
        if len(candidates) != 1 or expected_counts[key(target)] != 1:
            rows.append(
                dict(
                    server_id=target["server_id"],
                    passed=False,
                    error="missing or ambiguous region membership",
                )
            )
            continue
        feature = candidates[0]
        indices = np.array(feature["tetrahedron_indices"], dtype=int)
        centers = geometry.mesh.simplex_centers[indices]
        powers = geometry.mesh.simplex_power_values[indices]
        if not np.all(np.isfinite(powers)) or np.any(powers < 0):
            rows.append(
                dict(
                    server_id=target["server_id"],
                    passed=False,
                    error="invalid native orthosphere power",
                )
            )
            continue
        spheres = np.column_stack((centers, np.sqrt(powers)))
        exported = bulbs[target["server_id"] - 1]
        expected = np.array(
            [[*(b["c"][axis] for axis in "xyz"), b["r"]] for b in exported], dtype=float
        ).reshape((-1, 4))
        row = compare_spheres(expected, spheres)
        row.update(server_id=target["server_id"], feature_type=target["feature_type"])
        # Counts and error maxima preserve evidence without republishing centers.
        row["max_center_error_angstrom"] = max(
            (p["center_max_absolute_error_angstrom"] for p in row["pairs"]), default=0
        )
        row["max_radius_error_angstrom"] = max(
            (p["radius_absolute_error_angstrom"] for p in row["pairs"]), default=0
        )
        del row["pairs"]
        rows.append(row)
    return dict(
        case=archive_path.stem,
        completed=True,
        passed=expected_counts == actual_counts and all(r["passed"] for r in rows),
        server_regions=len(reference),
        native_regions=len(features),
        exact_memberships=sum((expected_counts & actual_counts).values()),
        server_spheres=sum(len(group) for group in bulbs),
        native_spheres=sum(len(f["tetrahedron_indices"]) for f in features),
        matched_spheres=sum(r.get("matched_spheres", 0) for r in rows),
        archive_sha256=hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        bulb_sha256=hashlib.sha256(raw).hexdigest(),
        regions=rows,
    )


def main() -> int:
    """Audit trusted developer caches without reading server geometry as input."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", type=Path, required=True)
    parser.add_argument(
        "--geometry-cache-dir",
        type=Path,
        required=True,
        help="Trusted local caches from the four-field metric collector; pickle is not a public input format",
    )
    parser.add_argument("--cases", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.cases) != len(set(args.cases)):
        parser.error("Cases must be unique")
    root = Path(__file__).resolve().parents[1]
    report = dict(
        scope="complete region orthosphere sets on specified cases; no independent atom-contact or mouth audit",
        completed=False,
        complete_server_equivalence=False,
        cases=[],
        python=sys.version.split()[0],
        versions={
            name: metadata.version(name) for name in ("opencastp", "numpy", "scipy")
        },
        source_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        source_sha256={
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (
                Path(__file__),
                root / "src/opencastp/_core/geometry.py",
                root / "src/opencastp/_core/components.py",
                root / "src/opencastp/_core/weighted_mesh.py",
            )
        },
    )
    for case in args.cases:
        try:
            path = (
                args.geometry_cache_dir / f"opencastp_all_metric_{case}_geometry.pickle"
            )
            geometry = pickle.loads(path.read_bytes())
            item = audit_geometry(args.archive_dir / f"{case}.zip", geometry)
            item["prepared_coordinate_sha256"] = hashlib.sha256(
                geometry.atom_coordinates.tobytes()
            ).hexdigest()
            item["prepared_expanded_radius_sha256"] = hashlib.sha256(
                geometry.atom_radii.tobytes()
            ).hexdigest()
        except Exception as error:
            item = dict(
                case=case,
                completed=False,
                passed=False,
                error=f"{type(error).__name__}: {error}",
            )
        report["cases"].append(item)
        print(
            case,
            item["completed"],
            item["passed"],
            item.get("matched_spheres"),
            "/",
            item.get("server_spheres"),
            flush=True,
        )
    report["completed"] = all(c["completed"] for c in report["cases"])
    report["passed"] = all(c["passed"] for c in report["cases"])
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
