"""Preserve bounded metric coverage and rejected export hypotheses."""

import hashlib
import json
from pathlib import Path

import pytest

ARTIFACTS = Path(__file__).resolve().parents[1] / "devguide/artifacts"


def evidence():
    return json.loads(
        (ARTIFACTS / "metric_characterization_controls_2026_10_03.json").read_text()
    )


def test_ms_atom_controls_preserve_native_and_candidate_verdicts():
    report = evidence()
    atoms = report["atom_contributions"]
    assert atoms["completed"] and not atoms["passed"]
    assert not atoms["export_candidate_qualified"]
    assert not report["complete_server_equivalence"]
    assert not atoms["production_source_changed"]
    assert not atoms["modern_export_source_recovered"]
    assert {c["case"] for c in atoms["cases"]} == {"1stp", "8rat", "1mrg"}
    counts = {
        f: tuple(
            sum(c["fields"][f][key] for c in atoms["cases"])
            for key in ("raw_matches", "candidate_export_matches", "required")
        )
        for f in atoms["units"]
    }
    assert counts == {
        "SA_Area": (3767, 3783, 3783),
        "SA_Volume": (3612, 3781, 3783),
        "MS_Area": (3768, 3783, 3783),
        "MS_Volume": (3600, 3783, 3783),
    }
    failures = []
    for case in atoms["cases"]:
        assert case["total_conservation_max_error"] < 2e-7
        assert set(case["fields"]) == set(atoms["units"])
        for field, values in case["fields"].items():
            quantum = 0.01 if field.endswith("Area") else 0.001
            assert values["tolerance"] == pytest.approx(
                quantum / 2 + 1e-8, rel=0, abs=1e-15
            )
            failures.extend(
                (case["case"], field, r["atom_id"], r["raw_passed"])
                for r in values["failures"]
                if not r["export_passed"]
            )
    assert set(failures) == {
        ("8rat", "SA_Volume", 429, True),
        ("1mrg", "SA_Volume", 588, False),
    }


def test_region_export_candidate_cannot_be_promoted_from_atom_success():
    replay = evidence()["region_export_replay"]
    assert replay["completed"] and replay["source_verdict_unchanged"]
    assert not replay["complete_server_equivalence"]
    assert (replay["cases"], replay["regions"], replay["fields"]) == (89, 3729, 14916)
    assert replay["raw_matches"] == 14911
    assert replay["native_printed_matches"] == 14910
    assert replay["candidate_matches"] == 14173
    assert replay["candidate_introduced_failures"] == 742
    assert replay["candidate_explained_raw_failures"] == 4
    assert len(replay["raw_failed"]) == 5
    assert len(replay["candidate_failed"]) == 743
    tolerated = [r for r in replay["native_printed_failed"] if r["raw_passed"]]
    assert len(tolerated) == 1
    assert (tolerated[0]["case"], tolerated[0]["server_id"], tolerated[0]["field"]) == (
        "1okm",
        40,
        "molecular_surface_area",
    )
    for name, digest in replay["source_artifact_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest


def test_complete_domain_controls_remain_bounded_and_collectors_pinned():
    report = evidence()
    geometry = report["orthospheres"]
    assert geometry["completed"] and geometry["passed"]
    assert not geometry["complete_server_equivalence"]
    assert {c["case"] for c in geometry["cases"]} == {
        "1stp",
        "8rat",
        "1mrg",
        "1psn",
        "1ypi",
        "1fbp",
        "2fbp",
    }
    for case in geometry["cases"]:
        assert case["completed"] and case["passed"]
        assert (
            case["native_regions"]
            == case["server_regions"]
            == case["exact_memberships"]
        )
        assert (
            case["native_spheres"] == case["server_spheres"] == case["matched_spheres"]
        )
        for region in case["regions"]:
            assert not region["missing"] and not region["extra"]
            assert region["max_center_error_angstrom"] <= 0.00005001
            assert region["max_radius_error_angstrom"] <= 0.00005001
    for name, digest in report["collector_sha256"].items():
        assert hashlib.sha256((ARTIFACTS / name).read_bytes()).hexdigest() == digest
