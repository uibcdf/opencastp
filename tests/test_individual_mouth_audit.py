"""Independent edge-fan reference guards; archives never supply partitions."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture
def audit_module():
    path = Path(__file__).resolve().parents[1] / "devtools/audit_castp_mouths.py"
    spec = importlib.util.spec_from_file_location("individual_mouth_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chain():
    # Rotation about edge (0, 1) passes through a tetrahedron with no mouth
    # seed. The terminal mouth triangles share no third vertex.
    tetrahedra = np.array([[0, 1, 2, 3], [0, 1, 3, 4], [0, 1, 4, 5]])
    neighbors = np.array([[-1, -1, 1, -1], [-1, -1, 2, 0], [-1, -1, -1, 1]])
    seeds = [(0, (0, 1, 2)), (2, (0, 1, 5))]
    return tetrahedra, neighbors, seeds


def test_fan_connects_through_tetrahedron_without_seed(audit_module):
    tetrahedra, neighbors, seeds = chain()
    assert audit_module.partition_edge_fans(
        tetrahedra, neighbors, {0, 1, 2}, seeds, set()
    ) == [frozenset({(0, 1, 2), (0, 1, 5)})]


def test_inactive_tetrahedron_splits_fan(audit_module):
    tetrahedra, neighbors, seeds = chain()
    assert set(
        audit_module.partition_edge_fans(tetrahedra, neighbors, {0, 2}, seeds, set())
    ) == {frozenset({(0, 1, 2)}), frozenset({(0, 1, 5)})}


def test_shape_edge_must_not_merge_mouths(audit_module):
    tetrahedra, neighbors, seeds = chain()
    assert (
        len(
            audit_module.partition_edge_fans(
                tetrahedra, neighbors, {0, 1, 2}, seeds, {(0, 1)}
            )
        )
        == 2
    )


def test_fan_reference_ignores_seed_order_and_face_orientation(audit_module):
    tetrahedra, neighbors, seeds = chain()
    reversed_seeds = [(owner, tuple(reversed(face))) for owner, face in reversed(seeds)]
    assert audit_module.partition_edge_fans(
        tetrahedra, neighbors, {0, 1, 2}, seeds, set()
    ) == audit_module.partition_edge_fans(
        tetrahedra, neighbors, {0, 1, 2}, reversed_seeds, set()
    )


def test_duplicate_or_nonlocal_seeds_are_rejected(audit_module):
    tetrahedra, neighbors, seeds = chain()
    with pytest.raises(ValueError, match="duplicate"):
        audit_module.partition_edge_fans(
            tetrahedra, neighbors, {0, 1, 2}, seeds + seeds[:1], set()
        )
    with pytest.raises(ValueError, match="local"):
        audit_module.partition_edge_fans(
            tetrahedra, neighbors, {0, 1, 2}, [(0, (0, 1, 5))], set()
        )


def test_one_mouth_audit_checks_individual_fields(audit_module):
    target = {
        "server_id": 7,
        "n_mouths": 1,
        "aggregate_mouth_atoms": [10, 20, 30],
        "additional_metrics": {
            "solvent_accessible_mouth_area": "2.000",
            "molecular_surface_mouth_area": "3.000",
            "solvent_accessible_mouth_perimeter": "4.000",
            "molecular_surface_mouth_perimeter": "5.000",
            "mouth_triangle_count": "1",
        },
    }
    mouth = {
        "atom_indices": [30, 10, 20],
        "faces": [(0, 1, 2)],
        "area_sa": 2.0,
        "area_ms": 3.0,
        "perimeter_sa": 4.0,
        "perimeter_ms": 5.0,
    }
    report = audit_module.compare_single_mouth(target, [mouth])
    assert report["passed"] and report["server_individual_scalar_reference_available"]
    assert not report["server_individual_triangle_reference_available"]
    mouth["perimeter_ms"] += 0.00050002
    assert not audit_module.compare_single_mouth(target, [mouth])["passed"]
    mouth["atom_indices"] = [10, 20]
    assert not audit_module.compare_single_mouth(target, [mouth])[
        "rim_membership_passed"
    ]


def test_multi_mouth_totals_cannot_certify_individuals(audit_module):
    target = {
        "server_id": 7,
        "n_mouths": 2,
        "aggregate_mouth_atoms": [],
        "additional_metrics": {},
    }
    report = audit_module.compare_single_mouth(target, [{}, {}])
    assert report["passed"] is None
    assert not report["server_individual_scalar_reference_available"]
    assert report["reason"] == "archive contains only region-level mouth totals"
