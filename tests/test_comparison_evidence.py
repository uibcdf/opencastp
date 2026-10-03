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
