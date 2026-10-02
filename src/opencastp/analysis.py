"""Analyze explicit atomic spheres without molecular-system dependencies."""

from importlib import metadata
from typing import Literal

import numpy as np
import pyunitwizard as puw
from scipy.spatial import QhullError

from ._core.components import _validate_pocket_definition, build_castp_feature_records
from ._core.exact import exact_determinant, fixed_point_array
from ._core.geometry import build_castp_geometry
from ._core.volbl import voids_measurements
from .exceptions import CastpGeometryError, CastpInputError
from .result import CastpResult


def _length_values(value, scale: float, name: str) -> np.ndarray:
    try:
        if puw.is_quantity(value):
            result = np.asarray(puw.get_value(value, to_unit="angstrom"), dtype=float)
        else:
            result = np.asarray(value, dtype=float) * scale
    except Exception as error:
        raise CastpInputError(
            f"{name} must contain compatible length values"
        ) from error
    if not np.all(np.isfinite(result)):
        raise CastpInputError(f"{name} must contain finite values")
    return result


def _producer_versions() -> dict[str, str]:
    versions = {}
    for name in ("opencastp", "numpy", "scipy", "pyunitwizard"):
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "uninstalled-source"
    return versions


def _quantity_record(record: dict) -> dict:
    output = dict(record)
    output["source"] = "opencastp"
    output["source_id"] = f"opencastp:{record['feature_type']}:{record['id']}"
    output["center"] = puw.quantity(record["center"], "angstrom")
    output["polyhedral_area"] = puw.quantity(output.pop("area"), "angstrom**2")
    output["polyhedral_volume"] = puw.quantity(output.pop("volume"), "angstrom**3")
    output.pop("score", None)
    output["mouth_area"] = puw.quantity(record["mouth_area"], "angstrom**2")
    output["mouth_perimeter"] = puw.quantity(record["mouth_perimeter"], "angstrom")
    output["mouths"] = [
        dict(
            mouth,
            area=puw.quantity(mouth["area"], "angstrom**2"),
            perimeter=puw.quantity(mouth["perimeter"], "angstrom"),
        )
        for mouth in record["mouths"]
    ]
    return output


def analyze(
    coordinates: np.ndarray,
    radii: np.ndarray,
    *,
    length_unit: str,
    probe_radius: float | None = None,
    atom_indices: np.ndarray | None = None,
    pocket_definition: Literal["literature", "castp3"] = "literature",
    backend: Literal["python"] = "python",
) -> CastpResult:
    """Analyze local regions using explicit atomic radii and a solvent probe.

    Parameters
    ----------
    coordinates : array-like or quantity, shape (n_atoms, 3)
        Finite atom coordinates for one structure.
    radii : array-like or quantity, shape (n_atoms,)
        Positive atomic radii before adding the solvent probe. Chemical typing,
        hydrogen handling and heterogen selection belong to the caller.
    length_unit : str
        Explicit length unit for bare coordinates, radii and probe values.
        Quantities retain their own units. Application unit policy is preserved.
    probe_radius : float or quantity, optional
        Non-negative probe. The default is explicitly 1.4 angstroms, independent
        of ``length_unit``. Explicit bare values use ``length_unit``.
    atom_indices : array-like of int, optional
        Unique non-negative source atom IDs. Defaults to input positions.
    pocket_definition : {'literature', 'castp3'}, default 'literature'
        Published maximum-depth definition or empirically reconstructed modern
        minimum-terminal compatibility. This choice does not change radii.
    backend : {'python'}, default 'python'
        Initial reference implementation. Rust and GPU are not implemented.

    Returns
    -------
    CastpResult
        Regions with explicit quantities and retained numerical geometry.
        Closed voids also carry SA/MS areas and volumes. Open-region analytical
        SA/MS fields are absent. An evaluated-empty input returns an empty list.

    Raises
    ------
    CastpInputError
        If shapes, values, units, IDs or requested policies are invalid.
    CastpGeometryError
        If fewer than four effective spheres remain or triangulation fails.

    Examples
    --------
    >>> import numpy as np
    >>> points = np.array([[1,1,1], [1,-1,-1], [-1,1,-1], [-1,-1,1]])
    >>> result = analyze(points, np.full(4, 0.25), length_unit='angstrom')
    >>> result.features[0]['feature_type']
    'void'
    """
    try:
        _validate_pocket_definition(pocket_definition, False)
    except ValueError as error:
        raise CastpInputError(str(error)) from error
    if backend != "python":
        raise CastpInputError("backend must be python; Rust/GPU are not implemented")
    try:
        scale = float(puw.get_value(puw.quantity(1.0, length_unit), to_unit="angstrom"))
    except Exception as error:
        raise CastpInputError("length_unit must be a compatible length unit") from error
    points = _length_values(coordinates, scale, "coordinates")
    atomic_radii = _length_values(radii, scale, "radii")
    if points.ndim != 2 or points.shape[1] != 3:
        raise CastpInputError("coordinates must have shape (n_atoms, 3)")
    if atomic_radii.shape != (len(points),) or np.any(atomic_radii <= 0):
        raise CastpInputError("radii must have shape (n_atoms,) and be positive")
    if len(points) == 4:
        # The inherited four-point shortcut bypasses Qhull. Guard it on the
        # same fixed grid as the filtration, without a fitted float tolerance.
        grid_points = fixed_point_array(points, 5)
        if exact_determinant(grid_points[1:] - grid_points[0]) == 0:
            raise CastpGeometryError(
                "Four points are coplanar on the five-decimal grid"
            )
    probe = (
        np.asarray(1.4)
        if probe_radius is None
        else _length_values(probe_radius, scale, "probe_radius")
    )
    if probe.ndim != 0 or not np.isfinite(probe) or probe < 0:
        raise CastpInputError("probe_radius must be one finite non-negative length")
    probe = float(probe)
    ids: np.ndarray
    if atom_indices is None:
        ids = np.arange(len(points), dtype=int)
    else:
        ids = np.asarray(atom_indices)
        if ids.shape != (len(points),) or ids.dtype.kind not in "iu":
            raise CastpInputError("atom_indices must contain one integer per atom")
        if np.any(ids < 0) or len(np.unique(ids)) != len(ids):
            raise CastpInputError("atom_indices must be unique and non-negative")
        if np.any(ids > np.iinfo(np.int64).max):
            raise CastpInputError("atom_indices exceed the supported integer range")
    try:
        geometry = build_castp_geometry(
            points, atomic_radii + probe, atom_indices=ids, solvent_radius=probe
        )
    except (QhullError, ValueError) as error:
        raise CastpGeometryError(f"Cannot build CASTp geometry: {error}") from error
    records = build_castp_feature_records(
        geometry, probe_radius=probe, pocket_definition=pocket_definition
    )
    measurements = {}
    if any(record["feature_type"] == "void" for record in records):
        measurements = {
            item.simplex_indices: item
            for item in voids_measurements(geometry, geometry.base_rank).voids
        }
    features = []
    for record in records:
        feature = _quantity_record(record)
        if record["feature_type"] == "void":
            key = tuple(sorted(record["tetrahedron_indices"]))
            item = measurements[key]
            for field, value, unit in (
                ("solvent_accessible_area", item.area_sa, "angstrom**2"),
                ("molecular_surface_area", item.area_ms, "angstrom**2"),
                ("solvent_accessible_volume", item.volume_sa, "angstrom**3"),
                ("molecular_surface_volume", item.volume_ms, "angstrom**3"),
            ):
                feature[field] = puw.quantity(value, unit)
        features.append(feature)
    execution = dict(
        status="completed",
        backend="python",
        pocket_definition=pocket_definition,
        radii_model="explicit",
        probe_radius=puw.quantity(probe, "angstrom"),
        input_length_unit=length_unit,
        geometry_length_unit="angstrom",
        fixed_point_decimals=geometry.spectrum_decimals,
        producer_versions=_producer_versions(),
    )
    return CastpResult(features=features, geometry=geometry, execution=execution)
