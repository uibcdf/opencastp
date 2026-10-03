"""Guard staged precision hypotheses and retained counterexamples."""

import hashlib
import json
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parents[1] / "devguide/artifacts"


def evidence():
    return json.loads(
        (ARTIFACTS / "partial_precision_controls_2026_10_03.json").read_text()
    )


def test_minimal_trace_replays_native_terms_before_precision_changes():
    report = evidence()
    minimal = report["minimal"]
    assert minimal["completed"] and not minimal["production_source_changed"]
    assert len(minimal["cases"]) == 6
    assert len(minimal["plan"]["variant_plan"]) == 41
    assert minimal["plan"]["shared_inputs_and_domains"]
    assert minimal["plan"]["fresh_context_per_variant"]
    case = minimal["cases"][0]
    assert case["kind_counts"] == {"initial": 2, "vertex": 8, "edge": 12, "face": 6}
    assert 24000 < case["cancellation_ratio_sa_volume"] < 25000
    assert case["directed_attachment_branches"]["hidden1_true"] == 2
    rows = {row["name"]: row for row in minimal["summary"]}
    for name in ("accumulator_fsum", "tetrahedron_total_fsum"):
        assert rows[name]["raw_matches"] == 22
        assert rows[name]["repaired"] == rows[name]["introduced"] == 0
    assert {row["name"] for row in rows.values() if row["minimal_gate_passed"]} == {
        "disk_area_float32",
        "cap_volume_decimal6",
        "segment_height_decimal6",
    }


def test_panel_preserves_survivors_and_records_new_counterexample():
    panel = evidence()["molecular_panel"]
    assert panel["completed"] and not panel["full_corpus_executed"]
    assert len(panel["cases"]) == 7
    summaries = {row["name"]: row for row in panel["summary"]}
    assert summaries["baseline"]["raw_matches"] == 1531
    for name in ("disk_area_float32", "cap_volume_decimal6"):
        row = summaries[name]
        assert row["required"] == 1536 and row["raw_matches"] == 1534
        assert row["repaired"] == 3 and row["introduced"] == 0
        assert row["extra_matches"] == row["extra_required"] == 768
        assert row["panel_gate_passed"]
        assert {m["case"] for m in row["repaired_fields"]} == {"1mrg", "1psn", "1ypi"}
        assert {m["case"] for m in row["baseline_failures_remaining"]} == {
            "1fbp",
            "2fbp",
        }
    rejected = summaries["segment_height_decimal6"]
    assert not rejected["panel_gate_passed"] and rejected["introduced"] == 1
    assert rejected["introduced_failures"][0]["case"] == "2fbp"
    assert rejected["introduced_failures"][0]["server_id"] == 33


def test_bounded_expansion_preserves_inputs_and_cannot_certify_full_corpus():
    report = evidence()
    expansion = report["bounded_expansion"]
    assert expansion["completed"] and not expansion["calculation_errors"]
    assert not expansion["complete_89_input_gate"]
    assert expansion["plan"]["corpus_size"] == 89
    assert len(expansion["cases"]) == len(expansion["plan"]["requested_cases"]) == 12
    assert all(
        row["input_hashes_match_original_reference"] for row in expansion["cases"]
    )
    for row in expansion["summary"]:
        assert row["raw_matches"] == row["required"] == 504
        assert row["introduced"] == 0
        assert row["extra_matches"] == row["extra_required"] == 252
    assert not report["complete_server_equivalence"]
    assert report["original_corpus_verdict_unchanged"]


def test_discriminator_predictions_and_collectors_keep_provenance():
    report = evidence()
    scan = report["discriminator_design"]
    assert len(scan["samples"]) == 81 and len(scan["chosen"]) == 2
    assert all(row["printed_divergence"] for row in scan["chosen"])
    assert min(row["minimum_boundary_margin"] for row in scan["chosen"]) > 2e-7
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest


def test_new_minimal_server_jobs_refute_both_uniform_partial_policies():
    report = evidence()
    comparison = report["discriminator_comparison"]
    assert comparison["completed"] and len(comparison["cases"]) == 2
    for case in comparison["cases"]:
        assert case["archive_job_identity_and_receipt_verified"]
        assert case["returned_atom_records_match_upload"]
        assert case["contribution_atom_ids_and_labels_match_upload"]
        assert case["comparison"]["matched_scalars"] == 4
        assert case["comparison"]["matched_additional_descriptors"] == 7
        assert all(sphere["passed"] for sphere in case["orthospheres"])
        assert (
            case["server_regions"][0]["metrics"]["solvent_accessible_volume"] == "0.004"
        )
    verdicts = {row["name"]: row for row in report["discriminator_verdicts"]}
    assert verdicts["baseline"]["raw_matches"] == 8
    for name in ("disk_area_float32", "cap_volume_decimal6"):
        assert verdicts[name]["raw_matches"] == 7
        assert verdicts[name]["refuted_as_uniform_policy"]
    sections = report["discriminator_sections"]
    assert sections["completed"] and sections["shared_spheres_and_domains"]
    assert not sections["error_bound_certified"]
    for case in sections["cases"]:
        for variant in case["variants"]:
            assert not variant["messages"]
            assert abs(variant["difference_from_native_angstrom3"]) < 1e-10
            assert variant["estimated_error_angstrom3"] < 1e-11
