"""Guard explicit models and the retained competitor/corpus evidence."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw

from opencastp import analyze

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "devguide/artifacts"


@pytest.mark.parametrize("definition", ["literature", "castp3"])
def test_changing_one_caller_radius_changes_the_void_without_retyping(definition):
    points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    initial = np.full(4, 0.25)
    custom = initial.copy()
    custom[0] = 0.30
    baseline = analyze(
        points, initial, length_unit="angstrom", pocket_definition=definition
    )
    changed = analyze(
        points, custom, length_unit="angstrom", pocket_definition=definition
    )
    assert len(baseline.features) == len(changed.features) == 1
    assert changed.features[0]["feature_type"] == "void"
    assert float(
        puw.get_value(changed.features[0]["solvent_accessible_volume"])
    ) < float(puw.get_value(baseline.features[0]["solvent_accessible_volume"]))
    np.testing.assert_allclose(changed.geometry.atom_radii - 1.4, custom, atol=1e-14)
    np.testing.assert_array_equal(custom, [0.30, 0.25, 0.25, 0.25])


def test_remaining_archive_panel_retains_every_case_and_strict_scalar_failure():
    report = json.loads(
        (ARTIFACTS / "server_remaining_panel_2026_10_03.json").read_text()
    )
    previous = json.loads(
        (ARTIFACTS / "server_mouth_castp3_panel_2026_10_02.json").read_text()
    )
    heterogens = json.loads(
        (ARTIFACTS / "protein_heterogen_panel_2026_10_02.json").read_text()
    )
    earlier = {row["case"] for row in previous["cases"]} | {
        row["case"] for row in heterogens["benchmarks"]["atom"]["cases"]
    }
    cases = report["cases"]
    names = {row["case"] for row in cases}
    assert len(cases) == len(names) == 45
    assert not names & earlier
    assert len(names | earlier) == 89
    assert report["completed"] and not report["passed"]
    assert not report["complete_server_equivalence"]
    assert {row["case"] for row in cases if not row["passed"]} == {
        "1mrg",
        "1psn",
        "1ypi",
        "1fbp",
        "2fbp",
    }
    assert sum(row["server_regions"] for row in cases) == 2569
    assert sum(row["exact_memberships"] for row in cases) == 2569
    assert sum(row["required_scalars"] for row in cases) == 10276
    assert sum(row["matched_scalars"] for row in cases) == 10271
    assert sum(row["matched_additional_descriptors"] for row in cases) == 17983
    failures = []
    for case in cases:
        assert case["completed"] and not case["missing"] and not case["extra"]
        assert case["preparation"]["atom_record_policy"] == "atom"
        assert case["preparation"]["mouth_measurement_policy"] == "castp3"
        for region in case["regions"]:
            assert region["mouths_passed"]
            for metric in region["metrics"]:
                if not metric["passed"]:
                    failures.append(metric)
                    assert metric["tolerance"] == pytest.approx(
                        0.00050001, rel=0, abs=1e-15
                    )
                    assert (
                        abs(metric["actual"] - metric["expected"]) > metric["tolerance"]
                    )
            assert all(metric["passed"] for metric in region["additional_metrics"])
    assert len(failures) == 5
    runner = ARTIFACTS / "server_remaining_panel_2026_10_03_runner.py.txt"
    assert (
        hashlib.sha256(runner.read_bytes()).hexdigest()
        == report["source_sha256"]["devtools/compare_castp_servers.py"]
    )


def test_executed_pycasta_preparation_excludes_incorporated_heterogens():
    artifact = json.loads(
        (ARTIFACTS / "pycasta_preparation_2026_10_03.json").read_text()
    )
    assert artifact["upstream_commit"] == "f3418f38cd3d3c11e6cdd8c13b11431cc5b91894"
    expected = {"1hiv": 14, "1qpe": 16, "3lck": 16, "1g1f": 32, "1pty": 0}
    assert {
        row["case"]: row["incorporated_heterogen_atoms"] for row in artifact["cases"]
    } == expected
    for row in artifact["cases"]:
        assert not row["included_in_protein"]
        assert len(row["classified_as_ligand"]) == expected[row["case"]]
        assert row["water_option_preserves_protein_exclusion"]
        assert row["oxygen_radius_values"] == [1.52]
        assert row["elemental_oxygen_override_affects_all_oxygen"]
        assert row["other_element_radii_unchanged"]


def test_pycasta_index_audit_separates_flow_groups_from_final_pockets():
    artifact = json.loads(
        (ARTIFACTS / "pycasta_core_indices_2026_10_03.json").read_text()
    )
    assert artifact["upstream_commit"] == "f3418f38cd3d3c11e6cdd8c13b11431cc5b91894"
    assert not artifact["entry_module_compiles"]
    assert artifact["entry_module_error"]["type"] == "IndentationError"
    for row in artifact["cases"]:
        assert row["completed"]
        (flow,) = row["flow_observations"]
        assert flow["tetrahedra"] > flow["atoms"]
        assert flow["groups_rejected_by_atom_count_check"] > 0
        assert (
            flow["rejected_valid_tetrahedron_groups"]
            == flow["groups_rejected_by_atom_count_check"]
        )
        assert all(
            0 <= index < flow["tetrahedra"] for index in flow["sample_rejected_group"]
        )
        assert any(index >= flow["atoms"] for index in flow["sample_rejected_group"])
        assert flow["flow_groups"] > row["reported_pockets"]


def test_historical_metric_controls_preserve_all_five_strict_failures():
    """A precision diagnostic must not become a false server-equivalence claim."""
    from decimal import Decimal, localcontext

    report = json.loads(
        (ARTIFACTS / "historical_metric_controls_2026_10_03.json").read_text()
    )
    assert report["completed"] and not report["passed"]
    assert not report["complete_server_equivalence"]
    assert report["historical_pipeline_executed"] is False
    assert report["scope"] == "SA primitives on frozen modern integration domains"
    assert report["historical_coordinate_input"] == "modern float64 arrays"
    assert report["high_precision_input"] == "decimal strings of modern float64 arrays"
    assert report["source_commit"] == "63d9693c666185bc33d7202ad68d0862c54f37d2"
    assert {row["case"] for row in report["cases"]} == {
        "1mrg",
        "1psn",
        "1ypi",
        "1fbp",
        "2fbp",
    }
    assert len(report["cases"]) == 5
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
    assert report["historical_source_sha256"]["alpha-4.1-src/volbl/metric.c"]
    with localcontext() as context:
        context.prec = 90
        tolerance = Decimal(str(report["scalar_tolerance"]))
        assert tolerance == Decimal("0.00050001")
        for row in report["cases"]:
            expected = Decimal(str(row["expected"]))
            assert row["corrections"] == row["warnings"] == 0
            assert [value["digits"] for value in row["precision"]] == [40, 80]
            low = Decimal(row["precision"][0][row["field"]])
            high = Decimal(row["precision"][1][row["field"]])
            assert abs(low - high) < Decimal("1e-30")
            values = [
                Decimal(str(row["actual"])),
                Decimal(str(row["fsum"])),
                Decimal(str(row["c_" + row["field"]])),
                high,
            ]
            assert all(abs(value - expected) > tolerance for value in values)
            required_correction = abs(values[0] - expected) - tolerance
            assert max(abs(value - values[0]) for value in values) < (
                required_correction / 100
            )
            assert row["tetrahedra"] > 0


def test_residual_orthosphere_control_is_complete_only_for_its_five_regions():
    report = json.loads(
        (ARTIFACTS / "historical_metric_controls_2026_10_03.json").read_text()
    )["orthosphere_control"]
    assert report["scope"] == "five residual regions only"
    assert not report["complete_server_equivalence"]
    assert sum(row["exported_bulbs"] for row in report["cases"]) == 247
    for row in report["cases"]:
        assert row["passed"]
        assert (
            len(row["checks"])
            == row["exported_bulbs"]
            == row["tetrahedra"]
            == row["matched_distinct_tetrahedra"]
        )
        assert len({check["simplex"] for check in row["checks"]}) == row["tetrahedra"]
        for check in row["checks"]:
            assert check["compatible"] and check["support_matches"]
            assert check["status"] == "compatible" and check["interior_atoms"] == 0
            assert check["center_max_absolute_error_angstrom"] <= 0.00005001
            assert check["radius_absolute_error_angstrom"] <= 0.00005001


def test_input_materialization_controls_do_not_establish_server_equivalence():
    report = json.loads(
        (ARTIFACTS / "input_export_controls_2026_10_03.json").read_text()
    )
    assert report["completed"] and not report["complete_server_equivalence"]
    assert report["python"] == "3.14.7"
    assert report["source_commit"] == "4ffb6cbf3273a0cf22c42f700137ee96e2eead8a"
    assert report["region_comparator_changed"] is False
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
    for control in report["region_input_controls"]:
        assert control["fixed_modern_domains_and_predicates"]
        assert len(control["cases"]) == 5
        variants = {row["variant"] for row in control["cases"][0]["variants"]}
        assert len(variants) == 7
        for variant in variants:
            checks = [
                next(row for row in case["variants"] if row["variant"] == variant)
                for case in control["cases"]
            ]
            assert not all(row["passed"] for row in checks)
            for case, row in zip(control["cases"], checks):
                assert row["passed"] == (
                    abs(row["actual"] - case["expected"]) <= 0.00050001
                )
        assert control["metric_unchanged"] == (control["vol_real"] == "double")


def test_atom_export_candidate_preserves_strict_failures_and_unconfirmed_scope():
    report = json.loads(
        (ARTIFACTS / "input_export_controls_2026_10_03.json").read_text()
    )
    atoms = report["atom_contributions"]
    assert (
        atoms["scope"]
        == "SA space-filling per-atom CHECKING values; not pocket contributions"
    )
    assert atoms["units"] == {"SA_Area": "angstrom**2", "SA_Volume": "angstrom**3"}
    (case,) = atoms["cases"]
    assert case["case"] == "1mrg" and case["atoms"] == 1932
    assert case["tested"] == 3864 and case["passed"] == 3759
    assert len(case["failed"]) == 105
    for row in case["failed"]:
        assert abs(row["actual"] - row["expected"]) > row["tolerance"]
    export = case["quantization_diagnostic"]
    assert export["matched"] == 3863 and export["required"] == 3864
    assert export["explained_original_failures"] == 104
    assert export["introduced_failures"] == 0
    (remaining,) = export["failed"]
    assert remaining["atom_id"] == 588 and remaining["field"] == "SA_Volume"
    assert remaining["expected"] == 25.886 and remaining["diagnostic_export"] == 25.887
    assert report["modern_export_source_recovered"] is False
    c_control = report["atom588_metric_control"]
    assert c_control["primitive_count"] == 66
    assert c_control["corrections"] == c_control["warnings"] == 0
    assert abs(c_control["c_volume_sa"] - c_control["native_volume_sa"]) < 1e-8
    assert abs(c_control["c_volume_sa"] - 25.886) > 0.00050001
    inputs = report["atom588_input_control"]
    assert len(inputs["variants"]) == 7
    assert not any(row["strict_passed"] for row in inputs["variants"])
    assert {row["variant"] for row in inputs["variants"] if row["export_matches"]} == {
        "coordinates_direct_float32",
        "both_direct_float32",
    }
    panel = report["atom_materialization_panel"]
    assert panel["completed"] and panel["atoms"] == 1932
    assert panel["required_scalars"] == 3864
    assert len(panel["variants"]) == 3
    for row in panel["variants"]:
        assert row["strict_matched"] < panel["required_scalars"]
        assert (
            row["export_matched"] + len(row["export_failures"])
            == panel["required_scalars"]
        )


def test_live_output_inspection_rejects_html_even_with_http_200():
    report = json.loads(
        (ARTIFACTS / "input_export_controls_2026_10_03.json").read_text()
    )
    outputs = report["live_output_inspection"]
    assert len(outputs) == 9
    assert {row["case"] for row in outputs} == {"1mrg", "1psn", "1ypi"}
    for row in outputs:
        assert row["status"] == 200
        if row["suffix"] == ".4.contrib":
            assert row["html"] and not row["valid_data"]
            assert row["bytes"] == 713
        else:
            assert not row["html"] and row["valid_data"]
            assert row["same_bytes_as_archive"]
            assert row["sha256"] == row["archive_sha256"]


def test_independent_atom_export_controls_preserve_a_new_formatting_failure():
    report = json.loads(
        (ARTIFACTS / "independent_atom_export_controls_2026_10_03.json").read_text()
    )
    assert report["completed"] and not report["complete_server_equivalence"]
    assert report["python"] == "3.14.7"
    assert not report["public_export_policy_delivered"]
    assert {row["case"] for row in report["cases"]} == {"1stp", "8rat"}
    assert sum(row["tested"] for row in report["cases"]) == 3702
    assert sum(row["passed"] for row in report["cases"]) == 3620
    assert sum(len(row["failed"]) for row in report["cases"]) == 82
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
    cases = {row["case"]: row for row in report["cases"]}
    first = cases["1stp"]["quantization_diagnostic"]
    assert first["matched"] == first["required"] == 1802
    assert first["explained_original_failures"] == 47
    assert first["introduced_failures"] == 0
    other = cases["8rat"]["quantization_diagnostic"]
    assert other["matched"] == 1899 and other["required"] == 1900
    assert other["explained_original_failures"] == 35
    assert other["introduced_failures"] == 1
    (introduced,) = other["failed"]
    assert introduced["atom_id"] == 429 and introduced["field"] == "SA_Volume"
    assert introduced["passed"] and not introduced["export_matches"]
    assert abs(introduced["actual"] - introduced["expected"]) <= introduced["tolerance"]
    assert float(np.round(float(f"{introduced['actual']:.4f}"), 3)) == 11.040
    assert introduced["expected"] == 11.039
    for case in report["cases"]:
        for row in case["failed"]:
            assert abs(row["actual"] - row["expected"]) > row["tolerance"]
        assert case["preparation"]["atom_record_policy"] == "atom"
        assert case["preparation"]["radii_model"] == "castp3_protor"
