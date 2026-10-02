# OpenCASTp architecture checkpoint

OpenCASTp owns local numerical CASTp reconstruction. It is an auxiliary,
incubating MolSysSuite support library governed through uibcdf/molsyssuite#70.
It is not a direct MOLI component and needs no separate MOLI member registration.

## Initial boundary

`analyze(coordinates, radii, length_unit=..., probe_radius=..., atom_indices=...,
pocket_definition=..., mouth_measurement_policy=...)` accepts one structure and positive explicit atomic
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

The maintainer's current decision is to defer this entire roadmap until
complete measured CASTp3/CASTpFold equivalence is established under
uibcdf/opencastp#6. It describes later possibilities, not active work.

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

## Coexistence review boundary

Retained duplication is deliberate under the maintainer's instruction and
uibcdf/opencastp#1 / uibcdf/molsyssuite#70. The maintainer owns the future
migration decision. Review by 2026-12-31; this is a review checkpoint, not
permission to remove TopoMT code. Removal requires a later explicit instruction
and a validated optional consumer adapter. Until then, TopoMT retains both
historical and modern implementations and its molecular preparation contracts.

## Format boundary and server-compatible benchmark preparation

The numerical sphere contract is format-neutral. Molecular readers and
preparation can use supported MolSysMT forms, including CIF/BinaryCIF; format
conversion does not imply filtering modified residues. During equivalence
work the maintainer requests explicit HETATM exclusion for the benchmark,
with 1HIV documenting the archived server route's omission. This is not
a default atom filter in analyze and not a physical modeling recommendation.
The current public API takes arrays. Direct molecular ingestion remains a
separate frontend boundary; no direct file-reader support is claimed here.

## Independent measurement conventions

Region detection (`pocket_definition`), explicit radii and analytical mouth
measurement (`mouth_measurement_policy`) are independent scientific choices.
The signed projection model is the default; the reconstructed `castp3` model
uses unsigned circular segments observed in the pinned modern-server output.
Both use the same alpha-complex faces/edges and leave topology, filtration and
region SA/MS integration unchanged. The execution record retains the selected
policy. Preserve negative server-compatible mouth measures rather than
silently clamping them. Planar triangulation area/wire length stays separately
named from analytical SA/MS measures. See server_equivalence.md for executed
coverage and unclosed gates; API availability does not certify every input.
