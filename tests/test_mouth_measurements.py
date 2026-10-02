"""Analytical mouth units and geometry guards independent of server files."""

from math import pi, sqrt

import numpy as np
import pytest
import pyunitwizard as puw

from opencastp import analyze


def test_open_tetrahedron_exposes_curved_mouth_fields_and_keeps_planar_area():
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [3.2, 0.0, 0.0],
            [1.6, sqrt(3) * 1.6, 0.0],
            [1.6, sqrt(3) * 1.6 / 3, 2.3],
        ]
    )
    result = analyze(
        points, np.full(4, 0.4), length_unit="angstrom", pocket_definition="castp3"
    )
    feature = result.features[0]
    (mouth,) = feature["mouths"]
    assert feature["feature_type"] == "pocket"
    sa = float(puw.get_value(mouth["solvent_accessible_area"], to_unit="angstrom**2"))
    ms = float(puw.get_value(mouth["molecular_surface_area"], to_unit="angstrom**2"))
    planar = float(puw.get_value(mouth["area"], to_unit="angstrom**2"))
    assert 0 < sa < ms < planar
    assert planar == pytest.approx(sqrt(3) * 3.2**2 / 4)
    sa_length = float(
        puw.get_value(mouth["solvent_accessible_perimeter"], to_unit="angstrom")
    )
    ms_length = float(
        puw.get_value(mouth["molecular_surface_perimeter"], to_unit="angstrom")
    )
    assert ms_length - sa_length == pytest.approx(2 * pi * 1.4)
    assert (
        float(
            puw.get_value(
                feature["solvent_accessible_mouth_area"], to_unit="angstrom**2"
            )
        )
        == sa
    )
    assert (
        float(
            puw.get_value(
                feature["molecular_surface_mouth_area"], to_unit="angstrom**2"
            )
        )
        == ms
    )


def test_zero_probe_makes_both_analytical_mouth_models_identical():
    from opencastp._core.mouth_measurements import triangle_mouth_measurements

    triangle = np.array([[0.0, 0.0, 0.0], [3.2, 0.0, 0.0], [1.6, sqrt(3) * 1.6, 0.0]])
    result = triangle_mouth_measurements(
        triangle, np.full(3, 1.8), 0.0, (True, True, True)
    )
    assert result.area_sa == pytest.approx(result.area_ms)
    assert result.perimeter_sa == pytest.approx(result.perimeter_ms)
    assert result.area_sa > 0 and result.perimeter_sa > 0


def test_signed_and_server_mouth_conventions_are_explicit():
    from opencastp._core.mouth_measurements import triangle_mouth_measurements

    # The smaller circle's bisector projection is behind its center. The
    # server's unsigned segment convention differs from oriented geometry.
    triangle = np.array([[0.0, 0.0, 0.0], [1.37, 0.0, 0.0], [0.0, 4.0, 0.0]])
    radii = np.array([3.28, 2.86, 2.9])
    signed = triangle_mouth_measurements(
        triangle, radii, 1.4, (True, False, False), policy="signed"
    )
    server = triangle_mouth_measurements(
        triangle, radii, 1.4, (True, False, False), policy="castp3"
    )
    assert signed.area_sa > server.area_sa
    assert signed.area_ms > server.area_ms
    assert signed.perimeter_sa < server.perimeter_sa
    assert signed.perimeter_ms < server.perimeter_ms
    with pytest.raises(ValueError, match="policy"):
        triangle_mouth_measurements(
            triangle, radii, 1.4, (True, False, False), policy="fitted"
        )


def test_analyze_records_mouth_policy_and_rejects_unknown_choice():
    from opencastp.exceptions import CastpInputError

    points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    result = analyze(
        points,
        np.full(4, 0.25),
        length_unit="angstrom",
        mouth_measurement_policy="castp3",
    )
    assert result.execution["mouth_measurement_policy"] == "castp3"
    with pytest.raises(CastpInputError, match="mouth_measurement_policy"):
        analyze(
            points,
            np.full(4, 0.25),
            length_unit="angstrom",
            mouth_measurement_policy="fitted",
        )


@pytest.mark.parametrize("policy", ["signed", "castp3"])
def test_mouth_measurements_preserve_rigid_motion_and_dimensions(policy):
    from opencastp._core.mouth_measurements import triangle_mouth_measurements

    triangle = np.array([[0.0, 0.0, 0.0], [1.37, 0.0, 0.0], [0.0, 4.0, 0.0]])
    radii = np.array([3.28, 2.86, 2.9])
    reference = triangle_mouth_measurements(
        triangle, radii, 1.4, (True, False, False), policy=policy
    )
    rotation = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    moved = triangle_mouth_measurements(
        triangle @ rotation + np.array([7.0, 5.0, -2.0]),
        radii,
        1.4,
        (True, False, False),
        policy=policy,
    )
    scaled = triangle_mouth_measurements(
        triangle * 0.1, radii * 0.1, 0.14, (True, False, False), policy=policy
    )
    assert moved.area_sa == pytest.approx(reference.area_sa)
    assert moved.area_ms == pytest.approx(reference.area_ms)
    assert moved.perimeter_sa == pytest.approx(reference.perimeter_sa)
    assert moved.perimeter_ms == pytest.approx(reference.perimeter_ms)
    assert scaled.area_sa == pytest.approx(reference.area_sa * 0.01)
    assert scaled.area_ms == pytest.approx(reference.area_ms * 0.01)
    assert scaled.perimeter_sa == pytest.approx(reference.perimeter_sa * 0.1)
    assert scaled.perimeter_ms == pytest.approx(reference.perimeter_ms * 0.1)
