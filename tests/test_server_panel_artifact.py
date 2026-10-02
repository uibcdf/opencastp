"""Retain every original input and distinguish a preparation variant from a rerun."""

import hashlib
import json
from pathlib import Path


def test_original_forty_inputs_and_1hiv_variant_remain_separate():
    root = Path(__file__).resolve().parents[1]
    artifact = json.loads(
        (root / "devguide/artifacts/server_region_panel_2026_10_02.json").read_text()
    )
    cases = artifact["cases"]
    expected = set(
        "1crn 1rop 2pk4 3phv 8rat 1stp 1rob 2lyz 1ifb 2ifb 1hew 1stn 1hel 1snc 5dfr 1hfc 1brq 1rbp 1hsi 1hiv 1ida 3ptb 3ptn 4phv 2tga 1cge 1a6u 1srf 1mtw 2ctv 1esa 1a6w 1inc 1bmq 1ahc 4ca2 3tms 1djb 1a4j 1cdo".split()
    )
    assert len(cases) == len(expected) == 40
    assert {case["case"] for case in cases} == expected
    assert all(case["completed"] for case in cases)
    assert {case["case"] for case in cases if not case["passed"]} == {"1hiv"}
    assert sum(case["server_regions"] for case in cases) == 991
    assert sum(case["exact_memberships"] for case in cases) == 990
    assert sum(case["required_scalars"] for case in cases) == 3964
    assert sum(case["matched_scalars"] for case in cases) == 3960
    assert all(case["preparation"]["atom_record_policy"] == "protein" for case in cases)
    for case in cases:
        assert case["required_scalars"] == 4 * case["server_regions"]
        metrics = [metric for region in case["regions"] for metric in region["metrics"]]
        assert case["matched_scalars"] == sum(metric["passed"] for metric in metrics)
        assert not case["complete_server_equivalence"]
        for field in (
            "archive_sha256",
            "pdb_sha256",
            "prepared_coordinates_sha256",
            "prepared_expanded_radii_sha256",
        ):
            assert len(case[field]) == 64
    (variant,) = artifact["preparation_variants"]
    original = next(case for case in cases if case["case"] == "1hiv")
    assert variant["case"] == "1hiv"
    assert variant["completed"] and variant["passed"]
    assert variant["matched_scalars"] == variant["required_scalars"] == 68
    assert variant["exact_memberships"] == variant["server_regions"] == 17
    assert variant["archive_sha256"] == original["archive_sha256"]
    assert variant["pdb_sha256"] == original["pdb_sha256"]
    assert variant["prepared_pdb_sha256"] != original["pdb_sha256"]
    assert variant["preparation"]["atom_record_policy"] == "atom"
    assert not artifact["complete_server_equivalence"]
    runner = root / "devguide/artifacts/server_region_panel_2026_10_02_runner.py.txt"
    assert (
        hashlib.sha256(runner.read_bytes()).hexdigest()
        == artifact["source_sha256"]["devtools/compare_castp_servers.py"]
    )
    heterogens = artifact["heterogen_diagnostic"]
    assert len(heterogens) == len({case["case"] for case in heterogens}) == 89
    assert not any(case["contribution_heterogens"] for case in heterogens)


def test_global_atom_policy_panel_is_a_fresh_complete_forty_case_run():
    root = Path(__file__).resolve().parents[1]
    artifact = json.loads(
        (
            root / "devguide/artifacts/server_region_atom_panel_2026_10_02.json"
        ).read_text()
    )
    original = json.loads(
        (root / "devguide/artifacts/server_region_panel_2026_10_02.json").read_text()
    )
    cases = artifact["cases"]
    assert artifact["completed"] and artifact["passed"]
    assert len(cases) == len({case["case"] for case in cases}) == 40
    assert {case["case"] for case in cases} == {
        case["case"] for case in original["cases"]
    }
    assert all(case["completed"] and case["passed"] for case in cases)
    assert all(case["preparation"]["atom_record_policy"] == "atom" for case in cases)
    assert sum(case["exact_memberships"] for case in cases) == 991
    assert sum(case["matched_scalars"] for case in cases) == 3964
    assert not artifact["complete_server_equivalence"]
    runner = (
        root / "devguide/artifacts/server_region_atom_panel_2026_10_02_runner.py.txt"
    )
    assert (
        hashlib.sha256(runner.read_bytes()).hexdigest()
        == artifact["source_sha256"]["devtools/compare_castp_servers.py"]
    )


def test_modified_polymer_residues_are_distinct_from_free_phosphotyrosines():
    root = Path(__file__).resolve().parents[1]
    artifact = json.loads(
        (
            root / "devguide/artifacts/protein_heterogen_inspection_2026_10_02.json"
        ).read_text()
    )
    cases = {case["case"]: case for case in artifact["cases"]}
    assert {
        name: len(case["protein_heterogen_atom_ids"]) for name, case in cases.items()
    } == {"1hiv": 14, "3lck": 16, "1qpe": 16, "1g1f": 32, "1pty": 0}
    assert all(not case["contributing_protein_heterogens"] for case in cases.values())
    assert cases["1qpe"]["MODRES"] and cases["1qpe"]["LINK"]
    assert cases["3lck"]["MODRES"] and cases["3lck"]["LINK"]
    assert cases["1g1f"]["MODRES"] and cases["1g1f"]["LINK"]
    for case in cases.values():
        for field in ("archive_sha256", "pdb_sha256", "contribution_sha256"):
            assert len(case[field]) == 64


def test_paired_heterogen_panel_retains_failures_and_ligand_control():
    root = Path(__file__).resolve().parents[1]
    artifact = json.loads(
        (
            root / "devguide/artifacts/protein_heterogen_panel_2026_10_02.json"
        ).read_text()
    )
    runs = artifact["benchmarks"]
    atom = {case["case"]: case for case in runs["atom"]["cases"]}
    protein = {case["case"]: case for case in runs["protein"]["cases"]}
    assert atom.keys() == protein.keys() == {"3lck", "1qpe", "1g1f", "1pty"}
    assert runs["atom"]["completed"] and runs["atom"]["passed"]
    assert runs["protein"]["completed"] and not runs["protein"]["passed"]
    assert all(case["passed"] for case in atom.values())
    assert protein["1pty"]["passed"]
    for case, extra_atoms in [("3lck", 16), ("1qpe", 16), ("1g1f", 32)]:
        assert not protein[case]["passed"]
        assert protein[case]["exact_memberships"] == atom[case]["server_regions"] - 1
        assert protein[case]["atom_count"] - atom[case]["atom_count"] == extra_atoms
        assert atom[case]["archive_sha256"] == protein[case]["archive_sha256"]
        assert atom[case]["pdb_sha256"] == protein[case]["pdb_sha256"]
        assert atom[case]["preparation"]["atom_record_policy"] == "atom"
        assert protein[case]["preparation"]["atom_record_policy"] == "protein"
    assert protein["1g1f"]["native_regions"] == 48
    assert atom["1g1f"]["native_regions"] == 42
    assert protein["1pty"]["atom_count"] == atom["1pty"]["atom_count"]
    assert not artifact["complete_server_equivalence"]


def test_unsigned_mouth_panel_matches_all_forty_cases_without_dropping_signed_failures():
    root = Path(__file__).resolve().parents[1]
    folder = root / "devguide/artifacts"
    report = json.loads(
        (folder / "server_mouth_castp3_panel_2026_10_02.json").read_text()
    )
    signed = json.loads(
        (folder / "server_mouth_signed_panel_2026_10_02.json").read_text()
    )
    cases = report["cases"]
    assert len(cases) == len({case["case"] for case in cases}) == 40
    assert {case["case"] for case in cases} == {
        case["case"] for case in signed["cases"]
    }
    assert report["completed"] and report["passed"]
    assert signed["completed"] and not signed["passed"]
    assert sum(case["passed"] for case in signed["cases"]) == 23
    assert all(case["preparation"]["atom_record_policy"] == "atom" for case in cases)
    assert all(
        case["preparation"]["mouth_measurement_policy"] == "castp3" for case in cases
    )
    assert sum(case["exact_memberships"] for case in cases) == 991
    assert sum(case["matched_scalars"] for case in cases) == 3964
    assert sum(case["matched_additional_descriptors"] for case in cases) == 6937
    assert all(
        case["matched_additional_descriptors"]
        == case["required_additional_descriptors"]
        for case in cases
    )
    assert not report["complete_server_equivalence"]
    for source, snapshot in report["stage_source_snapshots"].items():
        assert (
            hashlib.sha256((folder / snapshot).read_bytes()).hexdigest()
            == report["source_sha256"][source]
        )
