"""Independent disk-boundary and volume quadrature reference guards."""

import importlib.util
from math import acos, pi, sqrt
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture
def oracle():
    path = Path(__file__).resolve().parents[1] / "devtools/section_volume_oracle.py"
    spec = importlib.util.spec_from_file_location("section_volume_oracle", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def square():
    return np.array([[-2.0, -2.0], [2.0, -2.0], [2.0, 2.0], [-2.0, 2.0]])


def test_empty_and_fully_covering_disks(oracle):
    polygon = square()
    assert oracle.uncovered_polygon_area(
        polygon, np.empty((0, 2)), np.empty(0)
    ) == pytest.approx(16.0)
    assert oracle.uncovered_polygon_area(
        polygon, np.array([[0.0, 0.0]]), np.array([4.0])
    ) == pytest.approx(0.0, abs=1e-12)


def test_internal_half_and_quarter_disks(oracle):
    assert oracle.uncovered_polygon_area(
        square(), np.array([[0.0, 0.0]]), np.ones(1)
    ) == pytest.approx(16 - pi, abs=1e-12)
    half = np.array([[0.0, -2.0], [2.0, -2.0], [2.0, 2.0], [0.0, 2.0]])
    assert oracle.uncovered_polygon_area(
        half, np.array([[0.0, 0.0]]), np.ones(1)
    ) == pytest.approx(8 - pi / 2, abs=1e-12)
    quarter = np.array([[0.0, 0.0], [3.0, 0.0], [0.0, 3.0]])
    assert oracle.uncovered_polygon_area(
        quarter, np.array([[0.0, 0.0]]), np.ones(1)
    ) == pytest.approx(4.5 - pi / 4, abs=1e-12)


def test_overlapping_disks_and_duplicates(oracle):
    overlap = 2 * acos(0.5) - sqrt(3) / 2
    area = oracle.uncovered_polygon_area(
        square(), np.array([[-0.5, 0.0], [0.5, 0.0]]), np.ones(2)
    )
    assert area == pytest.approx(16 - (2 * pi - overlap), abs=1e-12)
    assert oracle.uncovered_polygon_area(
        square(), np.zeros((2, 2)), np.ones(2)
    ) == pytest.approx(16 - pi, abs=1e-12)


def test_nested_and_tangent_disks(oracle):
    assert oracle.uncovered_polygon_area(
        square(), np.zeros((2, 2)), np.array([1.0, 0.5])
    ) == pytest.approx(16 - pi, abs=1e-12)
    assert oracle.uncovered_polygon_area(
        square(), np.array([[-1.0, 0.0], [1.0, 0.0]]), np.ones(2)
    ) == pytest.approx(16 - 2 * pi, abs=1e-12)


def test_area_preserves_motion_orientation_and_dimensions(oracle):
    polygon = square()
    centers = np.array([[-0.5, 0.0], [0.5, 0.0]])
    radii = np.ones(2)
    expected = oracle.uncovered_polygon_area(polygon, centers, radii)
    rotation = np.array([[0.6, -0.8], [0.8, 0.6]])
    shift = np.array([50.0, -100.0])
    assert oracle.uncovered_polygon_area(
        polygon @ rotation + shift, centers @ rotation + shift, radii
    ) == pytest.approx(expected, abs=1e-11)
    assert oracle.uncovered_polygon_area(
        polygon[::-1], centers, radii
    ) == pytest.approx(expected, abs=1e-12)
    assert oracle.uncovered_polygon_area(
        polygon * 0.1, centers * 0.1, radii * 0.1
    ) == pytest.approx(expected * 0.01, abs=1e-13)


def test_tetrahedral_volume_and_corner_sphere(oracle):
    tet = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    empty = oracle.integrate_tetrahedron(
        tet, np.empty((0, 3)), np.empty(0), epsabs=1e-10
    )
    assert empty["volume"] == pytest.approx(1 / 6, abs=1e-11)
    corner = oracle.integrate_tetrahedron(
        tet, np.zeros((1, 3)), np.array([0.2]), epsabs=1e-10
    )
    assert corner["volume"] == pytest.approx(1 / 6 - pi * 0.2**3 / 6, abs=1e-10)
    assert not corner["messages"]
    assert not corner["error_bound_certified"]


def test_bad_inputs_are_rejected(oracle):
    with pytest.raises(ValueError):
        oracle.uncovered_polygon_area(square(), np.zeros((1, 2)), np.array([-1.0]))
    with pytest.raises(ValueError):
        oracle.integrate_tetrahedron(
            np.zeros((4, 3)), np.empty((0, 3)), np.empty(0), epsabs=1e-10
        )


def test_disks_can_cover_polygon_collectively(oracle):
    assert oracle.uncovered_polygon_area(
        square(), np.array([[-1.5, 0.0], [1.5, 0.0]]), np.full(2, 3.0)
    ) == pytest.approx(0.0, abs=1e-12)


def test_three_disks_leave_an_internal_hole(oracle):
    # The disk union covers every polygon edge but leaves a central component.
    # An outer-boundary-only algorithm would incorrectly return zero.
    side = 1.8
    triangle = np.array([[0.0, 0.0], [side, 0.0], [side / 2, sqrt(3) * side / 2]])
    half_lens = acos(side / 2) - side * sqrt(4 - side**2) / 4
    expected = sqrt(3) * side**2 / 4 - pi / 2 + 3 * half_lens
    assert expected > 0
    assert oracle.uncovered_polygon_area(
        triangle, triangle, np.ones(3)
    ) == pytest.approx(expected, abs=1e-12)
