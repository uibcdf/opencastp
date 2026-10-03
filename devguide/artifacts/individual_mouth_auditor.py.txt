"""Audit individual mouths with explicit limits on the server reference.

The graph reference partitions fixed mouth seeds through connected tetrahedral
fans around open edges. It calls neither the native Fnext walk nor its union
routine. Filtration, pocket domains, seeds and numerical mouth integration
remain shared; this is an independent partition check, not a second engine.
"""

import argparse
import hashlib
import json
import math
import pickle
import subprocess
import sys
from collections import Counter, defaultdict
from importlib import metadata
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MOUTH_FIELDS = (
    ("solvent_accessible_mouth_area", "area_sa", "angstrom**2"),
    ("molecular_surface_mouth_area", "area_ms", "angstrom**2"),
    ("solvent_accessible_mouth_perimeter", "perimeter_sa", "angstrom"),
    ("molecular_surface_mouth_perimeter", "perimeter_ms", "angstrom"),
)


def partition_edge_fans(
    tetrahedra: np.ndarray,
    neighbors: np.ndarray,
    active_tetrahedra: set[int],
    seeds: list[tuple[int, tuple[int, int, int]]],
    shape_edges: set[tuple[int, int]],
) -> list[frozenset[tuple[int, int, int]]]:
    """Partition boundary triangles using active tetrahedral edge-fan graphs.

    Tetrahedral neighbors are opposite the correspondingly positioned vertex.
    Seeds carry their pocket-side owner. Shape edges block mouth connectivity.
    Input filtration and seeds are trusted scientific inputs; malformed array
    shapes, owners, duplicate triangles and non-boundary seeds are rejected.
    No face ordering or mouth ID is used for comparison.
    """
    tetrahedra = np.asarray(tetrahedra)
    neighbors = np.asarray(neighbors)
    if (
        tetrahedra.ndim != 2
        or tetrahedra.shape[1] != 4
        or neighbors.shape != tetrahedra.shape
    ):
        raise ValueError("Tetrahedra and neighbor arrays must both be N by 4")
    if not np.issubdtype(tetrahedra.dtype, np.integer) or not np.issubdtype(
        neighbors.dtype, np.integer
    ):
        raise ValueError("Tetrahedron and neighbor identifiers must be integers")
    if (
        np.any(tetrahedra < 0)
        or np.any(neighbors < -1)
        or np.any(neighbors >= len(tetrahedra))
    ):
        raise ValueError("Invalid atom or neighbor identifier")
    if any(index < 0 or index >= len(tetrahedra) for index in active_tetrahedra):
        raise ValueError("Invalid active tetrahedron identifier")
    canonical = []
    for owner, face in seeds:
        face = tuple(sorted(map(int, face)))
        if (
            owner not in active_tetrahedra
            or len(face) != 3
            or len(set(face)) != 3
            or not set(face).issubset(tetrahedra[owner])
        ):
            raise ValueError("Mouth seed must be local to an active owner tetrahedron")
        face_index = next(i for i, v in enumerate(tetrahedra[owner]) if v not in face)
        if int(neighbors[owner, face_index]) in active_tetrahedra:
            raise ValueError("Mouth seed must be a boundary face")
        canonical.append((int(owner), face))
    if len({face for _owner, face in canonical}) != len(canonical):
        raise ValueError("Mouth seeds contain a duplicate triangle")

    seed_indices_by_edge = defaultdict(lambda: defaultdict(list))
    for index, (owner, face) in enumerate(canonical):
        for edge in combinations(face, 2):
            if edge not in shape_edges:
                seed_indices_by_edge[edge][owner].append(index)
    tets_by_edge = defaultdict(set)
    for index in active_tetrahedra:
        for edge in combinations(sorted(map(int, tetrahedra[index])), 2):
            if edge in seed_indices_by_edge:
                tets_by_edge[edge].add(index)

    adjacency = [set() for _seed in canonical]
    for edge, seeds_by_owner in seed_indices_by_edge.items():
        remaining = set(tets_by_edge[edge])
        while remaining:
            stack = [remaining.pop()]
            indices = []
            while stack:
                current = stack.pop()
                indices.extend(seeds_by_owner.get(current, []))
                # A face containing the edge is opposite either other vertex.
                for position, vertex in enumerate(tetrahedra[current]):
                    if int(vertex) in edge:
                        continue
                    neighbor = int(neighbors[current, position])
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        stack.append(neighbor)
            if indices:
                anchor = indices[0]
                for index in indices[1:]:
                    adjacency[anchor].add(index)
                    adjacency[index].add(anchor)

    remaining_seeds = set(range(len(canonical)))
    result = []
    while remaining_seeds:
        stack = [remaining_seeds.pop()]
        faces = set()
        while stack:
            current = stack.pop()
            faces.add(canonical[current][1])
            for neighbor in adjacency[current] & remaining_seeds:
                remaining_seeds.remove(neighbor)
                stack.append(neighbor)
        result.append(frozenset(faces))
    return sorted(result, key=lambda item: sorted(item))


def compare_single_mouth(target: dict, mouths: list[dict]) -> dict:
    """Use a region-level archive as an individual oracle only for one mouth.

    Triangle sets are never exported by this archive and remain unqualified.
    Multi-mouth totals cannot certify a partition, rim or individual measure.
    """
    report = dict(
        server_id=target["server_id"],
        passed=None,
        server_individual_scalar_reference_available=target["n_mouths"] == 1,
        server_individual_triangle_reference_available=False,
    )
    if target["n_mouths"] != 1:
        report["reason"] = "archive contains only region-level mouth totals"
        return report
    if len(mouths) != 1:
        report.update(passed=False, reason="native mouth count differs")
        return report
    mouth = mouths[0]
    rim_passed = sorted(mouth["atom_indices"]) == target["aggregate_mouth_atoms"]
    rows = []
    for field, attribute, unit in MOUTH_FIELDS:
        printed = target["additional_metrics"][field]
        tolerance = 0.5 * 10 ** (-len(printed.partition(".")[2])) + 1e-8
        value = float(mouth[attribute])
        rows.append(
            dict(
                field=attribute,
                unit=unit,
                actual=value,
                expected=float(printed),
                tolerance=tolerance,
                passed=math.isfinite(value)
                and abs(value - float(printed)) <= tolerance,
            )
        )
    triangle_passed = len(mouth["faces"]) == int(
        target["additional_metrics"]["mouth_triangle_count"]
    )
    report.update(
        rim_membership_passed=rim_passed,
        triangle_count_passed=triangle_passed,
        metrics=rows,
        passed=rim_passed and triangle_passed and all(row["passed"] for row in rows),
    )
    return report


def audit_geometry(archive_path: Path, geometry) -> dict:
    """Compare fixed-domain mouth partitions and available individual scalars."""
    from devtools.compare_castp_servers import read_archive
    from opencastp._core.components import (
        _build_rank_driven_components,
        _component_boundary_faces,
        _geometry_max_rank,
        build_castp_feature_records,
    )
    from opencastp._core.geometry import _edge_is_in_complex_at
    from opencastp._core.mouth_measurements import mouth_measurements

    _pdb, targets = read_archive(archive_path)
    features = build_castp_feature_records(
        geometry, probe_radius=1.4, pocket_definition="castp3"
    )
    components, blocked_nodes, depth = _build_rank_driven_components(
        geometry,
        _geometry_max_rank(geometry),
        rank1=geometry.base_rank,
        pocket_definition="castp3",
    )
    active = {int(index) for group in components.values() for index in group}
    seeds = []
    for group in components.values():
        _boundary, records = _component_boundary_faces(
            geometry,
            group,
            blocked_nodes,
            depth,
            _geometry_max_rank(geometry),
            rank1=geometry.base_rank,
            active_pocket_nodes=active,
        )
        seeds.extend((record.simplex_index, record.face_atoms) for record in records)
    shape_edges = {
        edge
        for _owner, face in seeds
        for edge in combinations(sorted(face), 2)
        if _edge_is_in_complex_at(
            geometry.edge_rho_ranks, geometry.edge_mu1_ranks, edge, geometry.base_rank
        )
    }
    reference = partition_edge_fans(
        geometry.mesh.simplex_atom_indices,
        geometry.mesh.neighbors,
        active,
        seeds,
        shape_edges,
    )
    native = [
        frozenset(tuple(sorted(face)) for face in mouth["faces"])
        for feature in features
        for mouth in feature["mouths"]
    ]
    reference_counts, native_counts = Counter(reference), Counter(native)
    partitions_passed = reference_counts == native_counts
    native_seed_counts = Counter(face for cluster in native for face in cluster)
    seed_counts = Counter(tuple(sorted(face)) for _owner, face in seeds)
    seed_coverage_passed = native_seed_counts == seed_counts

    def key(item):
        return item["feature_type"], tuple(sorted(item["atom_indices"]))

    buckets = defaultdict(list)
    for feature in features:
        buckets[key(feature)].append(feature)
    membership_passed = Counter(map(key, targets)) == Counter(map(key, features))
    rows = []
    for target in targets:
        candidates = buckets[key(target)]
        if len(candidates) != 1:
            rows.append(
                dict(
                    server_id=target["server_id"],
                    error="missing or ambiguous membership",
                    passed=False,
                )
            )
            continue
        feature = candidates.pop()
        mouths = []
        for mouth in feature["mouths"]:
            measures = mouth_measurements(
                geometry, mouth["faces"], 1.4, policy="castp3"
            )
            mouths.append(
                dict(
                    atom_indices=mouth["atom_indices"],
                    faces=mouth["faces"],
                    area_sa=measures.area_sa,
                    area_ms=measures.area_ms,
                    perimeter_sa=measures.perimeter_sa,
                    perimeter_ms=measures.perimeter_ms,
                )
            )
        single = compare_single_mouth(target, mouths)
        aggregate_rows = []
        for field, attribute, unit in MOUTH_FIELDS:
            printed = target["additional_metrics"][field]
            tolerance = 0.5 * 10 ** (-len(printed.partition(".")[2])) + 1e-8
            actual = sum(mouth[attribute] for mouth in mouths)
            aggregate_rows.append(
                dict(
                    field=attribute,
                    unit=unit,
                    actual=actual,
                    expected=float(printed),
                    tolerance=tolerance,
                    passed=math.isfinite(actual)
                    and abs(actual - float(printed)) <= tolerance,
                )
            )
        count_passed = len(mouths) == target["n_mouths"]
        triangle_passed = sum(len(mouth["faces"]) for mouth in mouths) == int(
            target["additional_metrics"]["mouth_triangle_count"]
        )
        rim_passed = (
            sorted({atom for mouth in mouths for atom in mouth["atom_indices"]})
            == target["aggregate_mouth_atoms"]
        )
        rows.append(
            dict(
                server_id=target["server_id"],
                n_mouths=target["n_mouths"],
                single_mouth=single,
                individual_mouths=mouths,
                aggregate_metrics=aggregate_rows,
                aggregate_rim_passed=rim_passed,
                aggregate_triangle_count_passed=triangle_passed,
                passed=count_passed
                and triangle_passed
                and rim_passed
                and all(r["passed"] for r in aggregate_rows),
            )
        )
    return dict(
        case=archive_path.stem,
        completed=True,
        passed=membership_passed
        and partitions_passed
        and seed_coverage_passed
        and all(r["passed"] for r in rows),
        complete_server_equivalence=False,
        individual_multi_mouth_server_equivalence=False,
        shared_inputs=[
            "weighted mesh",
            "filtration",
            "pocket domains",
            "mouth seeds",
            "mouth integration",
        ],
        independent_operation="edge-fan graph partition; no Fnext walk or native clustering call",
        region_membership_passed=membership_passed,
        seed_coverage_passed=seed_coverage_passed,
        partition_passed=partitions_passed,
        reference_mouths=len(reference),
        native_mouths=len(native),
        reference_triangles=sum(map(len, reference)),
        single_mouth_regions=sum(t["n_mouths"] == 1 for t in targets),
        multi_mouth_regions=sum(t["n_mouths"] > 1 for t in targets),
        reference_partition=[sorted(item) for item in reference],
        native_partition=[sorted(item) for item in native],
        archive_sha256=hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        regions=rows,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", type=Path, required=True)
    parser.add_argument(
        "--geometry-cache-dir",
        type=Path,
        required=True,
        help="Trusted developer-only pickle cache; never load untrusted files",
    )
    parser.add_argument("--cases", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = dict(
        completed=False,
        complete_server_equivalence=False,
        cases=[],
        source_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        python=sys.version.split()[0],
        versions={n: metadata.version(n) for n in ("opencastp", "numpy", "scipy")},
        collector_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        core_source_sha256={
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (
                ROOT / "src/opencastp/_core/components.py",
                ROOT / "src/opencastp/_core/mouths.py",
                ROOT / "src/opencastp/_core/mouth_measurements.py",
            )
        },
    )
    for name in args.cases:
        cache = args.geometry_cache_dir / f"opencastp_all_metric_{name}_geometry.pickle"
        case = audit_geometry(
            args.archive_dir / f"{name}.zip", pickle.loads(cache.read_bytes())
        )
        case["geometry_cache_sha256"] = hashlib.sha256(cache.read_bytes()).hexdigest()
        report["cases"].append(case)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        print(
            name,
            {
                k: case[k]
                for k in (
                    "passed",
                    "partition_passed",
                    "native_mouths",
                    "reference_triangles",
                    "single_mouth_regions",
                    "multi_mouth_regions",
                )
            },
            flush=True,
        )
    report["completed"] = True
    report["passed"] = all(case["passed"] for case in report["cases"])
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
