"""Guard matching of printed orthospheres without changing metric tolerances."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture
def compare_spheres():
    path = Path(__file__).resolve().parents[1] / "devtools/audit_castp_orthospheres.py"
    spec = importlib.util.spec_from_file_location("orthosphere_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_spheres


def test_orthosphere_centers_and_radii_require_printed_precision(compare_spheres):
    target = np.array([[1.0, 2.0, 3.0, 0.4]])
    actual = target + 0.00004999
    report = compare_spheres(target, actual)
    assert report["passed"] and report["matched_spheres"] == 1
    assert not report["complete_server_equivalence"]
    for position in range(4):
        actual = target.copy()
        actual[0, position] += 0.00005002
        assert not compare_spheres(target, actual)["passed"]


def test_orthosphere_multiplicity_and_missing_or_extra_rows(compare_spheres):
    sphere = np.array([[0.0, 0.0, 0.0, 1.0]])
    empty = np.empty((0, 4))
    assert compare_spheres(empty, empty)["passed"]
    assert not compare_spheres(sphere, empty)["passed"]
    assert not compare_spheres(empty, sphere)["passed"]
    duplicated = np.repeat(sphere, 2, axis=0)
    assert compare_spheres(duplicated, duplicated)["passed"]
    assert not compare_spheres(duplicated, sphere)["passed"]


def test_orthosphere_pairing_is_bijective_in_a_rounding_overlap(compare_spheres):
    # Nearest-neighbor pairing reuses the first native sphere. A full matching
    # uses its second candidate for row 0, reserving the first for row 1.
    target = np.array([[0.00004, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 1.0]])
    actual = np.array([[0.00004, 0.0, 0.0, 1.0], [0.00008, 0.0, 0.0, 1.0]])
    report = compare_spheres(target, actual)
    assert report["passed"] and report["matched_spheres"] == 2
    assert len({row["native_index"] for row in report["pairs"]}) == 2


def test_orthosphere_nearest_center_cannot_hide_wrong_radius(compare_spheres):
    target = np.array([[0.0, 0.0, 0.0, 1.0]])
    actual = np.array([[0.0, 0.0, 0.0, 2.0]])
    assert compare_spheres(target, actual)["matched_spheres"] == 0


@pytest.mark.parametrize("row", [[np.nan, 0, 0, 1], [0, 0, 0, np.inf], [0, 0, 0, -1]])
def test_orthosphere_invalid_numbers_are_rejected(compare_spheres, row):
    with pytest.raises(ValueError):
        compare_spheres(np.array([row]), np.array([[0.0, 0.0, 0.0, 1.0]]))
    with pytest.raises(ValueError):
        compare_spheres(np.array([[0.0, 0.0, 0.0, 1.0]]), np.array([row]))


def test_orthosphere_wrong_shapes_are_rejected(compare_spheres):
    with pytest.raises(ValueError):
        compare_spheres(np.zeros((1, 3)), np.zeros((1, 4)))
