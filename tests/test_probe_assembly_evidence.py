"""Preserve job identity and the limits of probe/assembly diagnostic evidence."""

import hashlib
import json
from pathlib import Path

import pytest

ARTIFACTS = Path(__file__).resolve().parents[1] / "devguide/artifacts"


def evidence():
    return json.loads(
        (ARTIFACTS / "1mrg_probe_assembly_controls_2026_10_03.json").read_text()
    )


def test_completed_probe_jobs_have_verified_distinct_archive_receipts():
    report = evidence()
    probes = report["probe_controls"]
    assert report["completed"] and not report["complete_server_equivalence"]
    assert not report["production_source_changed"]
    assert len(probes) == len({row["jobid"] for row in probes}) == 5
    assert len({row["archive_sha256"] for row in probes}) == 5
    for row in probes:
        assert row["archive_receipt_and_job_identity_verified"]
        assert row["geometry_and_filtration_rebuilt"]
        assert row["exact_regions"] == row["required_regions"] == 29
        assert row["additional_matches"] == row["required_additional"] == 203
        assert row["orthospheres_passed"] and row["orthospheres"] == 365
    fine = {row["probe_angstrom"]: row for row in probes}
    assert fine[1.399999]["target_server_volume_angstrom3"] == 0.004
    assert fine[1.400001]["target_server_volume_angstrom3"] == 0.003
    assert fine[1.399999]["scalar_matches"] == 115
    assert fine[1.400001]["scalar_matches"] == 116
    assert all(
        row["scalar_matches"] == 116
        for row in probes
        if row["probe_angstrom"] not in (1.399999, 1.400001)
    )
    correction = report["archive_recovery"]
    assert correction["collision_corrected"]
    assert correction["original_download_sha256_recovered"]
    assert correction["superseded_fine_comparison_invalid"]
    assert not correction["new_jobs_submitted_during_recovery"]


def test_six_decimal_candidate_is_locally_supported_but_globally_unqualified():
    replay = evidence()["formatting_replay"]
    assert replay["original_cases"] == 89 and replay["original_fields"] == 14916
    six = replay["original_corpus"]["6_decimal_then_three"]
    assert six["matches"] == 14903 and six["required"] == 14916
    assert six["explained_raw_failures"] == 1
    assert six["introduced_raw_pass_failures"] == 9
    assert len(replay["probe_controls"]) == 5
    for probe in replay["probe_controls"]:
        six = probe["rules"]["6_decimal_then_three"]
        assert six["matches"] == six["required"] == 116
    assert all(
        rule["matches"] < rule["required"]
        for rule in replay["original_corpus"].values()
    )


def test_original_c_assembly_keeps_all_five_residuals_on_shared_domains():
    historical = evidence()["historical_assembly"]
    assert (
        historical["completed"] and not historical["full_historical_pipeline_executed"]
    )
    assert historical["domains_predicates_and_inputs_shared"]
    assert historical["build"]["original_assembly_functions_unchanged"]
    assert historical["regions"] == 384
    assert historical["strict_scalar_matches"] == 1531
    assert historical["required_scalars"] == 1536
    assert historical["additional_matches"] == historical["required_additional"] == 768
    assert len(historical["failed_fields"]) == 5
    assert {row["case"] for row in historical["failed_fields"]} == {
        "1mrg",
        "1psn",
        "1ypi",
        "1fbp",
        "2fbp",
    }
    assert all(
        case["corrections"] == case["warnings"] == 0 for case in historical["cases"]
    )
    assert (
        max(case["max_scalar_difference_from_native"] for case in historical["cases"])
        < 1e-8
    )
    mrg = next(row for row in historical["failed_fields"] if row["case"] == "1mrg")
    assert mrg["historical"] == pytest.approx(0.003499637802, abs=1e-11, rel=0)


def test_floor_reader_controls_are_conditional_and_collectors_are_pinned():
    report = evidence()
    reader = report["historical_reader_materialization"]
    assert reader["completed"] and not reader["full_historical_pipeline_executed"]
    assert reader["python"] == "3.14.7"
    assert len(reader["cases"]) == 5
    variants = {row["variant"] for row in reader["cases"][0]["variants"]}
    assert len(variants) == 5
    for variant in variants:
        assert not all(
            next(row for row in case["variants"] if row["variant"] == variant)[
                "raw_passed"
            ]
            for case in reader["cases"]
        )
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
