# OpenCASTp architecture checkpoint

OpenCASTp owns local numerical CASTp reconstruction. It is an auxiliary,
incubating MolSysSuite support library governed through uibcdf/molsyssuite#70.
It is not a direct MOLI component and needs no separate MOLI member registration.

## Initial boundary

`analyze(coordinates, radii, length_unit=..., probe_radius=..., atom_indices=...,
pocket_definition=...)` accepts one structure and positive explicit atomic
radii before probe expansion. The default probe is 1.4 angstroms regardless
of the bare-value input unit. Explicit quantities retain their own units.
The boundary converts once to angstroms and does not replace application policy.

`CastpResult` contains region dictionaries, numerical geometry and execution
provenance. Physical region fields carry units. Mesh-local tetrahedral/face IDs
are distinct from original atom IDs. The geometry substrate uses documented
angstrom units; it is inspectable and mutable during incubation. No persisted
format is promised; future persistence must use the shared quantity codec.

## Ownership and coexistence

Coordinates, weighted triangulation, exact filtration events, flow, regions,
mouths and analytical numerical measurements belong here. Molecular conversion,
selection, chemical typing, radius profiles, hydrogen/heterogen policy and
Topography/DFND admission remain with consumers during the initial extraction.
TopoMT will consume OpenCASTp as a soft dependency using its public API.

The maintainer explicitly requested retaining all CASTp code in TopoMT.
Temporary coexistence is tracked in uibcdf/opencastp#1. Extraction does not
authorize removing or replacing either historical or modern TopoMT routes.
A future adapter and any removal require separately demonstrated compatibility
and the maintainer's later instruction.

## Acceleration roadmap

1. Validate and profile the independent Python reference on synthetic and
   molecular inputs, including previously diagnosed numerical boundaries.
2. Separate pure Rust numerical functions from PyO3 bindings. Follow the
   installed-artifact validation and portable CPU packaging pattern in MolSysMT.
3. Port measured hot kernels while preserving arbitrary-precision predicates,
   grid materialization, ordering, atom mapping and region memberships.
4. Introduce controlled Rayon pools and batch processing after serial parity.
   Thread-count changes must preserve topology and declared metric tolerances.
5. Evaluate optional GPU stages using actual workloads and transfer costs.
   Device support, precision, failures and fallback must be explicit.

Rust and GPU are planned. No empty Cargo crate or placeholder backend is counted
as an implemented capability. Dependency and provenance qualification belongs
to uibcdf/opencastp#2; extraction and scientific validation to #1.
