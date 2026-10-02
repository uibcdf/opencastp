"""Scientific and boundary contracts for the independent array API."""

import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw

from opencastp import analyze


@pytest.fixture
def closed_tetrahedron():
    # Face circumradius < expanded radius < tetrahedron circumradius.
    return np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    )


def test_closed_void_has_original_atom_ids_and_distinct_measures(closed_tetrahedron):
    result = analyze(
        closed_tetrahedron,
        np.full(4, 0.25),
        length_unit="angstrom",
        probe_radius=1.4,
        atom_indices=np.array([100, 200, 300, 400]),
    )
    assert len(result.features) == 1
    feature = result.features[0]
    assert feature["feature_type"] == "void"
    assert sorted(feature["atom_indices"]) == [100, 200, 300, 400]
    assert feature["n_mouths"] == 0
    assert puw.get_value(
        feature["polyhedral_volume"], to_unit="angstrom**3"
    ) == pytest.approx(8 / 3)
    assert (
        puw.get_value(feature["solvent_accessible_volume"], to_unit="angstrom**3") > 0
    )
    assert puw.get_value(feature["molecular_surface_volume"], to_unit="angstrom**3") > 0
    assert result.execution["pocket_definition"] == "literature"
    assert result.execution["backend"] == "python"


def test_units_do_not_depend_on_application_defaults(closed_tetrahedron):
    aa = analyze(
        closed_tetrahedron, np.full(4, 0.25), length_unit="angstrom", probe_radius=1.4
    )
    nm = analyze(
        closed_tetrahedron / 10, np.full(4, 0.025), length_unit="nm", probe_radius=0.14
    )
    np.testing.assert_allclose(
        aa.geometry.atom_coordinates, nm.geometry.atom_coordinates, atol=1e-14
    )
    np.testing.assert_allclose(
        aa.geometry.atom_radii, nm.geometry.atom_radii, atol=1e-14
    )
    for key in (
        "solvent_accessible_area",
        "molecular_surface_area",
        "solvent_accessible_volume",
        "molecular_surface_volume",
    ):
        assert puw.get_value(aa.features[0][key]) == pytest.approx(
            puw.get_value(nm.features[0][key])
        )


def test_no_pocket_is_a_completed_result():
    points = np.array(
        [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 10.0, 0.0], [0.0, 0.0, 10.0]]
    )
    result = analyze(points, np.full(4, 0.1), length_unit="angstrom", probe_radius=0.0)
    assert result.features == []
    assert result.execution["status"] == "completed"


@pytest.mark.parametrize("definition", ["literature", "castp3"])
def test_both_definitions_are_explicit(closed_tetrahedron, definition):
    result = analyze(
        closed_tetrahedron,
        np.full(4, 0.25),
        length_unit="angstrom",
        pocket_definition=definition,
    )
    assert result.execution["pocket_definition"] == definition
    assert result.features[0]["feature_type"] == "void"


@pytest.mark.parametrize(
    "changes,match",
    [
        ({"radii": np.array([1.0, 1.0])}, "radii"),
        ({"radii": np.array([1.0, 1.0, -1.0, 1.0])}, "radii"),
        ({"coordinates": np.full((4, 3), np.nan)}, "coordinates"),
        ({"length_unit": "picosecond"}, "length_unit"),
        ({"pocket_definition": "unknown"}, "pocket_definition"),
        ({"probe_radius": -1.0}, "probe_radius"),
        ({"probe_radius": float("nan")}, "probe_radius"),
        ({"atom_indices": np.array([1, 1, 2, 3])}, "atom_indices"),
        ({"atom_indices": np.array([1.5, 2.0, 3.0, 4.0])}, "atom_indices"),
    ],
)
def test_invalid_input_is_rejected(closed_tetrahedron, changes, match):
    arguments = dict(
        coordinates=closed_tetrahedron, radii=np.full(4, 0.25), length_unit="angstrom"
    )
    arguments.update(changes)
    with pytest.raises(ValueError, match=match):
        analyze(**arguments)


def test_unknown_backend_cannot_claim_acceleration(closed_tetrahedron):
    with pytest.raises(ValueError, match="backend"):
        analyze(
            closed_tetrahedron, np.full(4, 0.25), length_unit="angstrom", backend="rust"
        )


def test_package_has_no_topomt_or_molsysmt_import_dependency():
    source = Path(__file__).resolve().parents[1] / "src"
    script = f"""import sys
sys.path.insert(0, {str(source)!r})
import opencastp
assert 'topomt' not in sys.modules
assert 'molsysmt' not in sys.modules
opencastp.analyze([[1,1,1], [1,-1,-1], [-1,1,-1], [-1,-1,1]],
                 [0.25]*4, length_unit='angstrom')
assert 'topomt' not in sys.modules
assert 'molsysmt' not in sys.modules
"""
    completed = subprocess.run(
        [sys.executable, "-I", "-c", script], capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def test_exact_predicates_keep_python_integer_precision():
    # A determinant which does not fit i128 guards a future Rust port.
    from opencastp._core.exact import exact_determinant

    matrix = np.array([[10**50, 0], [0, 10**50]], dtype=object)
    assert exact_determinant(matrix) == 10**100


def test_four_coplanar_points_cannot_be_reported_as_a_valid_triangulation():
    from opencastp import CastpGeometryError

    points = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
    )
    with pytest.raises(CastpGeometryError, match="coplanar"):
        analyze(points, np.full(4, 0.1), length_unit="angstrom", probe_radius=0.0)


def test_application_unit_policy_survives_import_and_execution():
    source = Path(__file__).resolve().parents[1] / "src"
    script = f"""import sys
sys.path.insert(0, {str(source)!r})
import pyunitwizard as puw
puw.configure.set_standard_units(['nm'], provenance='application')
before = puw.configure.get_standard_units()
import opencastp
result = opencastp.analyze([[1,1,1], [1,-1,-1], [-1,1,-1], [-1,-1,1]],
                          [0.25]*4, length_unit='angstrom')
assert puw.configure.get_standard_units() == before
assert puw.get_value(result.features[0]['polyhedral_volume'], to_unit='angstrom**3') > 2.6
"""
    completed = subprocess.run(
        [sys.executable, "-I", "-c", script], capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr
