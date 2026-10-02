"""Results from one local CASTp calculation."""

from dataclasses import dataclass

from ._core.geometry import CastpGeometry


@dataclass(slots=True)
class CastpResult:
    """Store regions, numerical geometry and execution provenance.

    Parameters
    ----------
    features : list[dict]
        Physical values are PyUnitWizard quantities. Atom IDs use the supplied
        mapping; tetrahedra and mouth faces use local mesh indices. These
        records do not define Topography or DFND features.
    geometry : CastpGeometry
        Numerical substrate exposed for inspection during incubation. Arrays
        use angstroms for coordinates/radii, angstroms squared for weights and
        angstroms cubed for simplex volumes.
    execution : dict
        Applied definition, probe, backend, precision and producer versions.

    Notes
    -----
    Input geometry is copied. Result objects themselves are mutable.
    Persistence is not implemented; future formats must retain units and
    producer provenance through the shared quantity codec.
    """

    features: list[dict]
    geometry: CastpGeometry
    execution: dict
