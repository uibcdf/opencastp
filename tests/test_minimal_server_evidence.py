"""Guard minimal server counterexamples and their preparation boundaries."""

import hashlib
import json
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parents[1] / "devguide/artifacts"


def evidence():
    return json.loads(
        (ARTIFACTS / "minimal_server_controls_2026_10_03.json").read_text()
    )


def test_six_completed_jobs_preserve_input_atoms_and_printed_geometry():
    report = evidence()
    assert report["completed"] and not report["complete_server_equivalence"]
    assert not report["production_source_changed"]
    assert report["submission"]["completed"]
    assert len(report["comparison"]["cases"]) == 6
    jobs = report["submission"]["jobs"]
    assert len({job["jobid"] for job in jobs}) == 6
    assert all(job["status"] == "completed_zip" for job in jobs)
    for row in report["comparison"]["cases"]:
        assert row["archive_job_identity_and_receipt_verified"]
        assert row["returned_atom_records_match_upload"]
        assert row["contribution_atom_ids_and_labels_match_upload"]
        assert row["comparison"]["exact_memberships"] == 1
        assert row["comparison"]["matched_additional_descriptors"] == 7
        assert all(sphere["passed"] for sphere in row["orthospheres"])


def test_uniform_final_rounding_is_refuted_by_the_minimal_volume_pair():
    report = evidence()
    comparisons = {row["case"]: row for row in report["comparison"]["cases"]}
    jobs = {row["case"]: row for row in report["submission"]["jobs"]}
    smaller = jobs["1mrg_five_original"]["native_predictions"][0]["metrics"][
        "solvent_accessible_volume"
    ]
    larger = jobs["regular_boundary_above_six_decimal_half"]["native_predictions"][0][
        "metrics"
    ]["solvent_accessible_volume"]
    assert smaller < larger < 0.0035
    assert (
        comparisons["1mrg_five_original"]["server_regions"][0]["metrics"][
            "solvent_accessible_volume"
        ]
        == "0.004"
    )
    assert (
        comparisons["regular_boundary_above_six_decimal_half"]["server_regions"][0][
            "metrics"
        ]["solvent_accessible_volume"]
        == "0.003"
    )
    assert (
        jobs["regular_boundary_above_six_decimal_half"]["native_predictions"][0][
            "six_decimal_then_three"
        ]["solvent_accessible_volume"]
        == "0.004"
    )
    assert report["uniform_monotonic_export_of_native_volume_refuted"]
    assert not report["server_effective_sphere_inputs_independently_certified"]
    assert report["original_corpus_verdict_unchanged"]


def test_separated_spheres_match_elementary_atom_reference_and_open_region():
    report = evidence()
    row = next(
        row
        for row in report["comparison"]["cases"]
        if row["case"] == "separated_four_real_carbons"
    )
    assert len(row["analytical_atom_checks"]) == 16
    assert all(
        check["passed"] and check["direct_format_matches"]
        for check in row["analytical_atom_checks"]
    )
    assert row["server_regions"][0]["feature_type"] == "pocket"
    assert row["server_regions"][0]["n_mouths"] == 1
    assert (
        row["comparison"]["matched_scalars"]
        == row["comparison"]["required_scalars"]
        == 4
    )
    assert row["retained_atoms"] == 4


def test_independent_section_controls_and_own_collectors_keep_provenance():
    report = evidence()
    sections = report["independent_sections"]
    assert sections["completed"] and not sections["error_bound_certified"]
    assert sections["geometry_and_sphere_inputs_shared"]
    assert len(sections["cases"]) == 5
    for case in sections["cases"]:
        assert len(case["variants"]) == 2
        for variant in case["variants"]:
            assert not variant["messages"]
            assert abs(variant["difference_from_native_angstrom3"]) < 1e-10
            assert variant["estimated_absolute_error_angstrom3"] < 1e-11
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
