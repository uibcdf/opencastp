"""Independent geometry and policy checks on the retained reference engine."""

from types import SimpleNamespace

import numpy as np
import pytest

from opencastp import analyze
from opencastp._core import components
from opencastp._core.metrics import mouth_area, mouth_perimeter
from opencastp._core.weighted_mesh import WeightedDelaunayMesh


def test_exact_weighted_center_has_equal_power_distance():
    points = np.array(
        [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 5.0]]
    )
    weights = np.array([1.0, 2.0, 3.0, 4.0])
    mesh = WeightedDelaunayMesh(points=points, weights=weights)
    expected = np.array([8 / 6, 14 / 8, 22 / 10])
    np.testing.assert_allclose(mesh.centers[0], expected, rtol=0, atol=1e-14)
    powers = np.sum((points - mesh.centers[0]) ** 2, axis=1) - weights
    np.testing.assert_allclose(powers, np.full(4, powers[0]), atol=1e-14)
    assert mesh.simplex_volumes[0] == pytest.approx(10.0)


def test_mouth_perimeter_counts_only_boundary_edges():
    points = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    )
    faces = [(0, 1, 2), (0, 2, 3)]
    assert mouth_area(points, faces) == pytest.approx(1.0)
    assert mouth_perimeter(points, faces) == pytest.approx(4.0)


def test_finite_and_exterior_reachability_distinguish_policies(monkeypatch):
    geometry = SimpleNamespace(
        mesh=SimpleNamespace(
            n_simplices=2, neighbors=np.asarray([[1, -1, -1, -1], [-1, -1, -1, -1]])
        ),
        simplex_rho_ranks=np.asarray([1, 2]),
        face_is_on_hull=np.asarray([[False, True, False, False], [False] * 4]),
    )
    monkeypatch.setattr(components, "_hidden_triangle", lambda *args: True)
    monkeypatch.setattr(components, "_triangle_is_attached", lambda *args: True)
    monkeypatch.setattr(
        components, "_iter_master_tetra_rho_indices", lambda *args, **kwargs: [1, 0]
    )
    np.testing.assert_array_equal(components._compute_pocket_depths(geometry), [2, 1])
    np.testing.assert_array_equal(
        components._compute_castp3_pocket_depths(geometry), [1, 1]
    )


def test_minimum_terminal_flow_rejects_cycles():
    with pytest.raises(ValueError, match="cycl"):
        components._minimum_reachable_sinks([[1], [0], []], [1, 2], 2)


def test_caller_mutation_does_not_change_existing_geometry():
    points = np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    )
    radii = np.full(4, 0.25)
    result = analyze(points, radii, length_unit="angstrom")
    original = result.geometry.atom_coordinates.copy()
    points[:] = 999
    radii[:] = 999
    np.testing.assert_array_equal(result.geometry.atom_coordinates, original)
    np.testing.assert_allclose(result.geometry.atom_radii, 1.65)
