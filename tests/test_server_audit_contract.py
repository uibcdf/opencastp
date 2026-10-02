"""Guard direct oracle comparison against false-positive equivalence claims."""

import importlib.util
from pathlib import Path

import pytest
import pyunitwizard as puw


@pytest.fixture
def compare():
    path = Path(__file__).resolve().parents[1] / "devtools/compare_castp_servers.py"
    spec = importlib.util.spec_from_file_location("server_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_regions


@pytest.fixture
def records():
    fields = (
        ("solvent_accessible_area", "angstrom**2"),
        ("molecular_surface_area", "angstrom**2"),
        ("solvent_accessible_volume", "angstrom**3"),
        ("molecular_surface_volume", "angstrom**3"),
    )
    expected = dict(
        server_id=7,
        feature_type="pocket",
        atom_indices=[10, 20],
        n_mouths=1,
        aggregate_mouth_atoms=[10, 20],
        metrics={field: "1.000" for field, _unit in fields},
    )
    actual = dict(
        feature_type="pocket",
        atom_indices=[20, 10],
        n_mouths=1,
        mouths=[dict(atom_indices=[20, 10])],
        **{field: puw.quantity(1.0, unit) for field, unit in fields},
    )
    return expected, actual


def test_region_agreement_cannot_certify_unmeasured_mouths(compare, records):
    expected, actual = records
    result = compare([expected], [actual])
    assert result["passed"]
    assert result["matched_scalars"] == 4
    assert not result["complete_server_equivalence"]
    assert "individual mouth geometry" in result["untested"]


def test_same_count_and_different_atoms_fail(compare, records):
    expected, actual = records
    actual["atom_indices"] = [10, 30]
    result = compare([expected], [actual])
    assert not result["passed"]
    assert result["exact_memberships"] == result["matched_scalars"] == 0
    assert len(result["missing"]) == len(result["extra"]) == 1


def test_missing_scalar_cannot_be_counted_as_zero(compare, records):
    expected, actual = records
    del actual["solvent_accessible_volume"]
    result = compare([expected], [actual])
    assert not result["passed"]
    assert result["matched_scalars"] == 3


def test_printed_precision_is_used_without_relative_tolerance(compare, records):
    expected, actual = records
    actual["solvent_accessible_area"] = puw.quantity(0.01000499, "nm**2")
    assert compare([expected], [actual])["passed"]
    actual["solvent_accessible_area"] = puw.quantity(0.01000502, "nm**2")
    assert not compare([expected], [actual])["passed"]


def test_duplicate_multiplicity_and_ambiguous_pairing_are_preserved(compare, records):
    expected, actual = records
    assert not compare([expected, expected], [actual])["passed"]
    report = compare([expected, expected], [actual, actual])
    assert report["exact_memberships"] == 2
    assert not report["passed"]
    assert report["matched_scalars"] == 0


def test_mouth_count_and_parent_rim_are_required(compare, records):
    expected, actual = records
    actual["mouths"][0]["atom_indices"] = [10]
    assert not compare([expected], [actual])["passed"]


def test_atom_record_policy_does_not_use_oracle_membership():
    path = Path(__file__).resolve().parents[1] / "devtools/compare_castp_servers.py"
    spec = importlib.util.spec_from_file_location("server_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pdb = b"HEADER example\nATOM      1  CA  ALA A   1\nHETATM    2  CA  CSO A   2\nTER\nEND\n"
    expected = b"HEADER example\nATOM      1  CA  ALA A   1\nTER\nEND\n"
    assert module.prepare_pdb_records(pdb, "atom") == expected
    assert module.prepare_pdb_records(pdb, "protein") == pdb
    with pytest.raises(ValueError, match="record policy"):
        module.prepare_pdb_records(pdb, "oracle")


def test_additional_counts_are_exact_and_never_truncated(compare, records):
    expected, actual = records
    expected["additional_metrics"] = {"mouth_triangle_count": "1"}
    actual["mouth_triangle_count"] = 1.9
    result = compare([expected], [actual])
    assert not result["passed"]
    assert result["matched_additional_descriptors"] == 0
    actual["mouth_triangle_count"] = 1
    assert compare([expected], [actual])["passed"]
    del actual["mouth_triangle_count"]
    assert not compare([expected], [actual])["passed"]


def test_unknown_requested_descriptor_cannot_be_silently_ignored(compare, records):
    expected, actual = records
    expected["additional_metrics"] = {"future_descriptor": "1.000"}
    actual["future_descriptor"] = 1.0
    result = compare([expected], [actual])
    assert not result["passed"]
    assert result["required_additional_descriptors"] == 1
    assert result["matched_additional_descriptors"] == 0
