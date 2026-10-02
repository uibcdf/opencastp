"""A synthetic opening guards the public fields on every supported interpreter."""

import numpy as np
import pytest
import pyunitwizard as puw

from opencastp import analyze


def test_one_open_face_has_analytical_region_measures_with_explicit_units():
    # Base circumradius is ~1.848, the other face circumradii ~1.754,
    # and the tetrahedron circumradius ~1.892. At radius 1.8, exactly
    # the base is open and the interior orthocenter is a finite sink.
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [3.2, 0.0, 0.0],
            [1.6, np.sqrt(3) * 1.6, 0.0],
            [1.6, np.sqrt(3) * 1.6 / 3, 2.3],
        ]
    )
    aa = analyze(
        points, np.full(4, 0.4), length_unit="angstrom", pocket_definition="castp3"
    )
    nm = analyze(
        points / 10, np.full(4, 0.04), length_unit="nm", pocket_definition="castp3"
    )
    assert len(aa.features) == len(nm.features) == 1
    feature = aa.features[0]
    assert feature["feature_type"] == "pocket"
    assert feature["n_mouths"] == 1
    assert len(feature["mouths"][0]["faces"]) == 1
    for field, unit in (
        ("solvent_accessible_area", "angstrom**2"),
        ("molecular_surface_area", "angstrom**2"),
        ("solvent_accessible_volume", "angstrom**3"),
        ("molecular_surface_volume", "angstrom**3"),
    ):
        value = float(puw.get_value(feature[field], to_unit=unit))
        assert np.isfinite(value) and value > 0
        assert value == pytest.approx(
            float(puw.get_value(nm.features[0][field], to_unit=unit))
        )
    assert float(
        puw.get_value(feature["solvent_accessible_volume"], to_unit="angstrom**3")
    ) < float(puw.get_value(feature["polyhedral_volume"], to_unit="angstrom**3"))
