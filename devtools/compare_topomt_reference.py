"""Compare the extraction with the retained TopoMT reference on prepared arrays.

TopoMT is a developer-only reference for this tool, not an OpenCASTp dependency.
No molecular inputs or server archives are redistributed by this runner.
"""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
import zipfile
from collections import Counter
from importlib import metadata
from pathlib import Path

import numpy as np
import pyunitwizard as puw

from opencastp import analyze


def _memberships(records: list[dict]) -> Counter:
    return Counter(
        (
            item["feature_type"],
            tuple(sorted(item["atom_indices"])),
            tuple(
                sorted(tuple(sorted(mouth["atom_indices"])) for mouth in item["mouths"])
            ),
        )
        for item in records
    )


def audit(root: Path, cases: list[str], output: Path) -> None:
    """Execute independent geometry and compare memberships and measurements."""
    from topomt.third_party.castp3.core.castp_core.components import (
        build_castp_feature_records,
    )
    from topomt.third_party.castp3.core.castp_core.geometry import build_castp_geometry
    from topomt.third_party.castp3.core.castp_core.volbl import voids_measurements

    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    report = dict(
        topomt_commit=commit,
        pocket_definition="castp3",
        radii_preparation="castp3_protor",
        comparison="same prepared spheres; independent geometry and analytical void calculations",
        cases=[],
    )
    for case in cases:
        started = time.monotonic()
        archive = root / f"topomt/data/CASTpFold_server/{case}.zip"
        with tempfile.TemporaryDirectory(prefix=f"opencastp-{case}-") as folder:
            with zipfile.ZipFile(archive) as handle:
                name = next(
                    name for name in handle.namelist() if name.lower().endswith(".pdb")
                )
                pdb_bytes = handle.read(name)
            pdb = Path(folder) / f"{case}.pdb"
            pdb.write_bytes(pdb_bytes)
            original = build_castp_geometry(
                str(pdb),
                selection='molecule_type in ["protein", "peptide"]',
                radii_model="castp3_protor",
                solvent_radius=1.4,
            )
            expected = build_castp_feature_records(
                original, probe_radius=1.4, pocket_definition="castp3"
            )
            result = analyze(
                original.atom_coordinates,
                original.atom_radii - 1.4,
                length_unit="angstrom",
                probe_radius=1.4,
                atom_indices=original.atom_indices_map,
                pocket_definition="castp3",
            )
            assert _memberships(expected) == _memberships(result.features), (
                f"{case}: region/mouth membership mismatch"
            )
            for field in (
                "simplex_rho_ranks",
                "face_rho_ranks",
                "face_mu1_ranks",
                "face_mu2_ranks",
                "vertex_rho_ranks",
                "vertex_mu1_ranks",
                "vertex_mu2_ranks",
            ):
                np.testing.assert_array_equal(
                    getattr(original, field), getattr(result.geometry, field)
                )
            np.testing.assert_array_equal(
                original.mesh.simplex_atom_indices,
                result.geometry.mesh.simplex_atom_indices,
            )
            expected_voids = {
                item.simplex_indices: item
                for item in voids_measurements(original, original.base_rank).voids
            }
            scalars = 0
            for feature in result.features:
                if feature["feature_type"] != "void":
                    continue
                measurement = expected_voids[
                    tuple(sorted(feature["tetrahedron_indices"]))
                ]
                for key, field, unit in (
                    ("solvent_accessible_area", "area_sa", "angstrom**2"),
                    ("molecular_surface_area", "area_ms", "angstrom**2"),
                    ("solvent_accessible_volume", "volume_sa", "angstrom**3"),
                    ("molecular_surface_volume", "volume_ms", "angstrom**3"),
                ):
                    np.testing.assert_allclose(
                        puw.get_value(feature[key], to_unit=unit),
                        getattr(measurement, field),
                        rtol=1e-10,
                        atol=1e-8,
                    )
                    scalars += 1
            item = dict(
                case=case,
                passed=True,
                archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                pdb_sha256=hashlib.sha256(pdb_bytes).hexdigest(),
                prepared_coordinates_sha256=hashlib.sha256(
                    original.atom_coordinates.tobytes()
                ).hexdigest(),
                prepared_expanded_radii_sha256=hashlib.sha256(
                    original.atom_radii.tobytes()
                ).hexdigest(),
                counts=dict(Counter(feature["feature_type"] for feature in expected)),
                analytical_void_scalars=scalars,
                atom_count=len(original.atom_indices_map),
                seconds=round(time.monotonic() - started, 3),
                versions={
                    name: metadata.version(name)
                    for name in ("molsysmt", "numpy", "scipy", "pyunitwizard")
                },
            )
            report["cases"].append(item)
            print(
                f"{case}: memberships, ranks and {scalars} SA/MS scalars match; {item['counts']}",
                flush=True,
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topomt-root", type=Path, required=True)
    parser.add_argument("--cases", nargs="+", default=["1stp", "1cdo"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit(args.topomt_root.resolve(), args.cases, args.output)
