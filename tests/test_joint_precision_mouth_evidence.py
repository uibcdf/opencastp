"""Retain conditional precision verdicts and bounded mouth-oracle coverage."""

import hashlib
import json
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parents[1] / "devguide/artifacts"


def evidence():
    return json.loads(
        (ARTIFACTS / "joint_precision_mouth_controls_2026_10_03.json").read_text()
    )


def test_precision_ablation_cannot_be_promoted_from_local_repairs():
    report = evidence()
    panel = report["intermediate_precision"]
    assert panel["completed"] and not panel["complete_server_equivalence"]
    assert (
        not panel["production_source_changed"]
        and not panel["modern_server_source_recovered"]
    )
    assert panel["exploratory_not_modern_source_derived"]
    counts = {
        variant: tuple(
            sum(c["variants"][variant][k] for c in panel["cases"])
            for k in (
                "required",
                "raw_matches",
                "candidate_matches",
                "raw_introduced_failures",
                "candidate_introduced_failures",
            )
        )
        for variant in panel["cases"][0]["variants"]
    }
    assert counts == {
        "baseline": (1536, 1531, 1460, 0, 75),
        "center2_float32": (1536, 1509, 1452, 25, 83),
        "center3_float32": (1536, 1478, 1418, 53, 117),
        "triangle_dual_float32": (1536, 1523, 1456, 8, 79),
        "center2_and_triangle_dual_float32": (1536, 1508, 1453, 26, 82),
        "all_three_vectors_float32": (1536, 1464, 1419, 70, 116),
    }
    repaired = {
        case["case"]
        for case in panel["cases"]
        if any(
            r["raw_passed"]
            for r in case["variants"]["center2_float32"]["raw_residuals"]
        )
    }
    assert repaired == {"1mrg", "1ypi", "2fbp"}


def test_individual_mouth_scalar_oracle_is_limited_to_single_mouth_regions():
    report = evidence()
    panel = report["individual_mouths"]
    assert panel["completed"] and panel["passed"]
    assert not panel["complete_server_equivalence"]
    assert sum(c["native_mouths"] for c in panel["cases"]) == 203
    assert sum(c["reference_triangles"] for c in panel["cases"]) == 1059
    assert sum(c["single_mouth_regions"] for c in panel["cases"]) == 158
    assert sum(c["multi_mouth_regions"] for c in panel["cases"]) == 20
    assert sum(len(c["regions"]) for c in panel["cases"]) == 384
    scalars = []
    for case in panel["cases"]:
        assert (
            case["partition_passed"]
            and case["seed_coverage_passed"]
            and case["region_membership_passed"]
        )
        assert not case["individual_multi_mouth_server_equivalence"]
        reference = {
            frozenset(tuple(f) for f in mouth) for mouth in case["reference_partition"]
        }
        native = {
            frozenset(tuple(f) for f in mouth) for mouth in case["native_partition"]
        }
        assert reference == native
        for region in case["regions"]:
            oracle = region["single_mouth"]
            assert not oracle["server_individual_triangle_reference_available"]
            if region["n_mouths"] == 1:
                assert oracle["server_individual_scalar_reference_available"]
                assert (
                    oracle["passed"]
                    and oracle["rim_membership_passed"]
                    and oracle["triangle_count_passed"]
                )
                scalars.extend(oracle["metrics"])
            else:
                assert not oracle["server_individual_scalar_reference_available"]
                assert oracle["passed"] is None
    assert len(scalars) == 632 and all(s["passed"] for s in scalars)


def test_executed_collectors_and_shared_production_sources_are_pinned():
    report = evidence()
    assert report["completed"] and not report["complete_server_equivalence"]
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
    sources = {}
    for key in ("intermediate_precision", "individual_mouths"):
        assert report[key]["python"] == "3.14.7"
        for path, digest in report[key]["core_source_sha256"].items():
            assert len(digest) == 64
            if path in sources:
                assert sources[path] == digest
            sources[path] = digest
