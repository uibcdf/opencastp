"""Executed molecular guards use original local archives, never fitted targets."""

import os
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pytest
import pyunitwizard as puw

from opencastp import analyze


def test_1stp_all_regions_have_server_analytical_measures(tmp_path):
    # This developer-only guard requires the retained molecular preparation
    # reference and local archives. Neither becomes a runtime dependency.
    root_value = os.environ.get("OPENCASTP_TOPOMT_ROOT")
    if root_value is None:
        pytest.skip("Explicit local molecular archive/preparation reference required")
    root = Path(root_value)
    from topomt.third_party.castp3.core.castp_core.geometry import build_castp_geometry

    archive = root / "topomt/data/CASTpFold_server/1stp.zip"
    with ZipFile(archive) as handle:
        pdb_bytes = handle.read("1stp.pdb")
        labels = handle.read("1stp.poc").decode()
        info = handle.read("1stp.pocInfo").decode()
        mouth_info = handle.read("1stp.mouthInfo").decode()
    pdb = tmp_path / "1stp.pdb"
    pdb.write_bytes(pdb_bytes)
    prepared = build_castp_geometry(
        str(pdb),
        selection='molecule_type in ["protein", "peptide"]',
        radii_model="castp3_protor",
        solvent_radius=1.4,
    )
    # 1STP has no discarded altlocs: verify source serials explicitly.
    rows = [
        line
        for line in pdb_bytes.decode().splitlines()
        if line.startswith(("ATOM", "HETATM"))
    ]
    serials = np.array([int(rows[int(i)][6:11]) for i in prepared.atom_indices_map])
    coordinates = np.array(
        [
            [float(rows[int(i)][a:b]) for a, b in ((30, 38), (38, 46), (46, 54))]
            for i in prepared.atom_indices_map
        ]
    )
    np.testing.assert_allclose(
        prepared.atom_coordinates, coordinates, rtol=0, atol=1e-10
    )
    result = analyze(
        prepared.atom_coordinates,
        prepared.atom_radii - 1.4,
        length_unit="angstrom",
        atom_indices=serials,
        pocket_definition="castp3",
        mouth_measurement_policy="castp3",
    )
    atom_sets = {}
    for line in labels.splitlines():
        atom_sets.setdefault(int(line.split()[-2]), set()).add(int(line[6:11]))
    expected = {
        frozenset(atom_sets[int(row[2])]): row
        for row in (line.split() for line in info.splitlines()[1:])
    }
    assert len(result.features) == len(expected) == 9
    for feature in result.features:
        row = expected[frozenset(feature["atom_indices"])]
        assert feature["n_mouths"] == int(row[3])
        for field, position, unit in (
            ("solvent_accessible_area", 4, "angstrom**2"),
            ("molecular_surface_area", 5, "angstrom**2"),
            ("solvent_accessible_volume", 6, "angstrom**3"),
            ("molecular_surface_volume", 7, "angstrom**3"),
        ):
            actual = float(puw.get_value(feature[field], to_unit=unit))
            assert abs(actual - float(row[position])) <= 0.00050001, (
                row[2],
                field,
                actual,
            )

    mouth_targets = {
        int(row[2]): row
        for row in (line.split() for line in mouth_info.splitlines()[1:])
    }
    for feature in result.features:
        row = expected[frozenset(feature["atom_indices"])]
        mouth_row = mouth_targets[int(row[2])]
        assert feature["corner_count"] == int(row[9])
        assert (
            abs(
                float(puw.get_value(feature["intersection_length"], to_unit="angstrom"))
                - float(row[8])
            )
            <= 0.00050001
        )
        assert sum(len(mouth["faces"]) for mouth in feature["mouths"]) == int(
            mouth_row[8]
        )
        for field, position, unit in (
            ("solvent_accessible_mouth_area", 4, "angstrom**2"),
            ("molecular_surface_mouth_area", 5, "angstrom**2"),
            ("solvent_accessible_mouth_perimeter", 6, "angstrom"),
            ("molecular_surface_mouth_perimeter", 7, "angstrom"),
        ):
            actual = float(puw.get_value(feature[field], to_unit=unit))
            printed = mouth_row[position]
            tolerance = 0.5 * 10 ** (-len(printed.partition(".")[2])) + 1e-8
            assert abs(actual - float(printed)) <= tolerance, (row[2], field, actual)


def test_8rat_server_mouth_policy_preserves_unsigned_segment_result(tmp_path):
    import importlib.util

    root_value = os.environ.get("OPENCASTP_TOPOMT_ROOT")
    if root_value is None:
        pytest.skip("Explicit local molecular archive/preparation reference required")
    path = Path(__file__).resolve().parents[1] / "devtools/compare_castp_servers.py"
    spec = importlib.util.spec_from_file_location("server_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = Path(root_value)
    report = module.audit_archive(
        root / "topomt/data/CASTpFold_server/8rat.zip", root, "atom"
    )
    assert report["passed"]
    assert report["exact_memberships"] == 12
    assert report["matched_scalars"] == 48
    assert report["matched_additional_descriptors"] == 84
    row = next(item for item in report["regions"] if item["server_id"] == 9)
    sa = next(
        item
        for item in row["additional_metrics"]
        if item["field"] == "solvent_accessible_mouth_area"
    )
    assert sa["expected"] == -0.573
    assert sa["actual"] < 0
    assert report["preparation"]["mouth_measurement_policy"] == "castp3"
