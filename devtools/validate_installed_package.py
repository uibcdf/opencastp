"""Verify a non-editable installed package without source-checkout shadowing."""

import sys
from importlib import metadata
from pathlib import Path

import numpy as np
import pyunitwizard as puw

import opencastp


def main() -> None:
    """Check package origin and execute the independent numerical engine."""
    print(f"Runtime Python {sys.version.split()[0]}")
    origin = Path(opencastp.__file__).resolve()
    if not origin.is_relative_to(Path(sys.prefix).resolve()):
        raise RuntimeError(f"Package is not installed in this environment: {origin}")
    distribution = metadata.distribution("opencastp")
    direct_url = distribution.read_text("direct_url.json") or ""
    if '"editable": true' in direct_url:
        raise RuntimeError("Installed-package evidence cannot use an editable install")
    points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    result = opencastp.analyze(points, np.full(4, 0.25), length_unit="angstrom")
    assert result.features[0]["feature_type"] == "void"
    open_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [3.2, 0.0, 0.0],
            [1.6, np.sqrt(3) * 1.6, 0.0],
            [1.6, np.sqrt(3) * 1.6 / 3, 2.3],
        ]
    )
    open_result = opencastp.analyze(
        open_points,
        np.full(4, 0.4),
        length_unit="angstrom",
        pocket_definition="castp3",
        mouth_measurement_policy="castp3",
    )
    assert open_result.features[0]["feature_type"] == "pocket"
    for field, unit in (
        ("solvent_accessible_area", "angstrom**2"),
        ("molecular_surface_area", "angstrom**2"),
        ("solvent_accessible_volume", "angstrom**3"),
        ("molecular_surface_volume", "angstrom**3"),
    ):
        assert puw.get_value(open_result.features[0][field], to_unit=unit) > 0
    mouth = open_result.features[0]["mouths"][0]
    assert puw.get_value(mouth["solvent_accessible_area"], to_unit="angstrom**2") > 0
    assert puw.get_value(mouth["molecular_surface_perimeter"], to_unit="angstrom") > 0
    assert open_result.execution["mouth_measurement_policy"] == "castp3"
    assert "topomt" not in sys.modules
    assert "molsysmt" not in sys.modules
    print(
        f"Installed OpenCASTp {distribution.version}: independent void/pocket numerical smoke passed"
    )


if __name__ == "__main__":
    main()
