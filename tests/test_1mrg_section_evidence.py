"""Keep physical reference agreement distinct from failed server equivalence."""

import hashlib
import json
from pathlib import Path

import pytest

ARTIFACTS = Path(__file__).resolve().parents[1] / "devguide/artifacts"


def evidence():
    return json.loads(
        (ARTIFACTS / "1mrg_section_rigid_controls_2026_10_03.json").read_text()
    )


def test_independent_sections_retain_the_volume_rounding_discrepancy():
    report = evidence()
    volume = report["independent_volume"]
    assert report["completed"] and not report["complete_server_equivalence"]
    assert volume["completed"] and not volume["production_source_changed"]
    assert volume["tetrahedra"] == 2 and volume["server_volume_angstrom3"] == 0.004
    assert (
        volume["domains_and_sphere_inputs_shared"]
        and not volume["error_bound_certified"]
    )
    assert len(volume["variants"]) == 5
    for variant in volume["variants"]:
        assert not variant["messages"] and not variant["raw_server_passed"]
        assert variant["below_three_decimal_boundary"]
        assert variant["volume_angstrom3"] == pytest.approx(
            0.003499637802, abs=1e-10, rel=0
        )
        assert abs(variant["difference_from_native_angstrom3"]) < 1e-10
        assert variant["estimated_absolute_error_angstrom3"] < 1e-9
    tight = next(v for v in volume["variants"] if v["variant"] == "z_64_tight")
    assert tight["estimated_absolute_error_angstrom3"] < 1e-12


def test_area_derivative_converges_without_claiming_certified_error():
    area = evidence()["independent_area"]
    assert area["completed"] and not area["error_bound_certified"]
    assert (
        not area["complete_server_equivalence"]
        and not area["production_source_changed"]
    )
    assert [v["step_angstrom"] for v in area["derivatives"]] == [0.001, 0.0005, 0.00025]
    errors = [abs(v["difference_from_native_angstrom2"]) for v in area["derivatives"]]
    assert errors[0] > errors[1] > errors[2]
    assert errors[0] / errors[1] == pytest.approx(4.0, rel=0.001)
    assert abs(area["richardson_difference_from_native_angstrom2"]) < 1e-8
    assert all(v["raw_server_passed"] for v in area["derivatives"])
    assert all(not side["messages"] for v in area["derivatives"] for side in v["sides"])


def test_live_translations_preserve_output_and_all_collectors_are_pinned():
    report = evidence()
    live = report["live_translations"]
    assert live["completed"] and not live["complete_server_equivalence"]
    assert live["server_submission"]["completed"]
    assert live["native_prepared_atoms"] == 1932 and live["original_regions"] == 29
    assert len(live["variants"]) == 3
    for variant in live["variants"]:
        assert variant["exact_archive_memberships"]
        assert not variant["field_differences_from_archive"]
        assert not variant["additional_field_differences_from_archive"]
        assert variant["target_metrics"]["solvent_accessible_volume"] == "0.004"
        assert variant["csv_ids_match_prepared"] and variant["csv_atoms"] == 1932
        assert variant["returned_atom_coordinates_match_upload"]
        assert variant["orthosphere_covariance"]["passed"]
        assert variant["orthosphere_covariance"]["matched_spheres"] == 365
        assert (
            variant["orthosphere_covariance"]["max_coordinate_error_angstrom"] < 1e-10
        )
        assert variant["orthosphere_covariance"]["max_radius_error_angstrom"] == 0
        ordinary = variant["predictions"]["float64"]
        assert (
            ordinary["strict_matches"] == 115
            and ordinary["paired_fields"] == ordinary["required_fields"] == 116
        )
        assert len(ordinary["failed"]) == 1
        assert ordinary["failed"][0]["field"] == "solvent_accessible_volume"
        assert variant["predictions"]["float32_coordinates"]["strict_matches"] < 115
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
