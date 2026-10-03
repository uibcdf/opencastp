# Why OpenCASTp exists

Evidence checkpoint: 2026-10-03. This is the maintained rationale and comparison
register for OpenCASTp. The current scientific priority is complete measured
server equivalence under [issue #6](https://github.com/uibcdf/opencastp/issues/6).
The register records demonstrated capabilities, bounded source observations and
future candidates separately. It does not certify a public release.

## Purpose and alternatives

OpenCASTp aims to provide an inspectable local Python reconstruction of CASTp
geometry with explicit molecular inputs and measured compatibility with modern
server results. It is an auxiliary MolSysSuite library, independent of TopoMT,
Topography and DFND. TopoMT consumption is intended and remains deferred.

CASTp3 and CASTpFold provide valuable online analyses and downloadable results.
A command-line client is a different execution boundary: for example,
[castpfoldpy](https://pypi.org/project/castpfoldpy/) explicitly submits calculations
to CASTpFold. Local visualization of downloaded results also does not provide a
local numerical engine. These observations do not prove that no other offline
implementation exists.

[pyCASTa](https://github.com/giorgioluciano/pycasta) already offers local,
open-source pocket analysis. Offline execution is shared with pyCASTa and cannot
justify OpenCASTp's distinction from it. Its ranking, ligand validation and
configurable pocket processing are useful capabilities; OpenCASTp does not
claim to replace that application workflow.

## Implemented capabilities and their comparative scope

| Capability | Relative to CASTp3/CASTpFold services | Relative to pyCASTa | Evidence and qualification |
| --- | --- | --- | --- |
| Local numerical Python API without submitting structures | Removes dependence on remote execution, queues and uploads for an OpenCASTp calculation | Shared capability, not a distinguishing advantage | `analyze` operates on supplied coordinate/radius arrays; isolated installed numerical checks pass |
| Caller-controlled atoms, radii, units and source atom IDs | Makes the calculation's physical model explicit; can retain incorporated HETATM atoms omitted in the audited archive route | Our contract is explicit; no claim that pyCASTa cannot retain those atoms | Array API and paired 1HIV, 3LCK, 1QPE, 1G1F and 1PTY controls; changing retained atoms intentionally changes results |
| Region SA/MS areas and volumes, separate from polyhedral measures | Provides these CASTp quantities locally; their availability itself is shared with the services | Inspected pyCASTa analytic-volume routine sums tetrahedral volumes, a different quantity; current-version matched numerical comparison remains pending | 4640 region SA/MS values match archived targets on 44 declared prepared cases |
| Explicit empirical CASTp3 definition and mouth convention alongside alternative definitions | Exposes choices and the observed compatibility behavior, including negative archived mouth areas | Distinct reconstruction objective; source differences do not prove numerical superiority | `pocket_definition`, independent radii and `mouth_measurement_policy`; retained signed/unsigned comparisons and 8RAT regression |
| Traceable modern-server validation | Enables local reproducibility of an explicitly bounded archive comparison | We have this validation evidence for OpenCASTp; no claim that pyCASTa's entire validation is absent or inferior | 1160 exact region memberships and 8120 additional aggregate descriptors match; complete equivalence remains false |
| Unit-bearing results and an independent numerical core | Supports in-process scientific consumers without a server interchange | Concrete integration contract; no claim of exclusive interoperability | NumPy, SciPy and PyUnitWizard runtime; no TopoMT/MolSysMT imports in the numerical core |
| Executed Python 3.11 through 3.14 compatibility | Qualifies the local implementation on the four supported Linux interpreters | Evidence for OpenCASTp, not evidence that pyCASTa fails on any interpreter | Four-minor non-editable installation/numerical checks; 47 tests pass and two explicit molecular guards skip per hosted minor |

Numerical evidence and exact artifact paths are in the developer
[server-equivalence checkpoint](https://github.com/uibcdf/opencastp/blob/main/devguide/server_equivalence.md).
Molecular-model boundaries and examples are explained in
[server comparisons](server_comparison.md). Hosted compatibility evidence is
separate from the molecular benchmark and from public package qualification.

## What the pyCASTa source inspection establishes

The inspected upstream checkout is commit
[`f3418f38cd3d3c11e6cdd8c13b11431cc5b91894`](https://github.com/giorgioluciano/pycasta/tree/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894),
with package metadata version 1.0.8. The observations below concern these
specific routines and configured paths, not every possible pyCASTa workflow.

- [The analytic pocket-volume routine](https://github.com/giorgioluciano/pycasta/blob/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894/src/pycasta/pocket_detection.py)
  sums absolute tetrahedral determinants divided by six. It does not perform
  the atomic-sector/overlap subtraction defining the compared CASTp SA/MS volumes.
- [Alpha filtering and discrete flow](https://github.com/giorgioluciano/pycasta/blob/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894/src/pycasta/alpha_shape.py)
  use ordinary circumsphere radii and configurable descent tolerances.
- [Defaults](https://github.com/giorgioluciano/pycasta/blob/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894/src/pycasta/config.py)
  include minimum-volume filtering, merging and ranking. These are additional
  processing choices that a controlled comparison must record.

The optional CGAL path supports weighted triangulation, with an ordinary
SciPy fallback. Therefore this inspection does not support a claim that
pyCASTa never uses weights. Nor does it establish that its current outputs
cannot match any CASTp pocket. A fair executed comparison must pin the version,
input atom set, radii, probe/alpha semantics, backend and postprocessing;
compare lining sets before scalars; and distinguish tetrahedral from SA/MS
quantities. Missing quantities are reported as missing rather than zero.
This comparison belongs to the validation work in issue #6.

## Future candidates, with no implementation or performance claim

| Candidate | Intended benefit | Current status |
| --- | --- | --- |
| Rust numerical backend | Potential runtime improvement with the Python reference as a correctness oracle | Not implemented; requires equivalence and measured performance |
| Multithreading and GPU acceleration | Potential throughput improvement on suitable workloads | Not implemented; requires workload-specific correctness, speed and memory evidence |
| Molecular-format frontend through MolSysMT | Convenient preparation from supported PDB/CIF/BinaryCIF and molecular objects | Core accepts explicit spheres today; direct file ingestion is not implemented |
| TopoMT consumer adapter | Make OpenCASTp results available through the existing external-provider contracts | Deferred; TopoMT's retained CASTp code has not been replaced |
| Public Conda package and benchmark publication | Accessible installation and reproducible community evaluation | Source provenance, dependency/channel qualification and publication remain pending |
| Scientific paper | Describe the reconstruction, controlled comparisons and explicit model discrepancies | Candidate after scientific and distribution qualification; no novel CASTp algorithm or universal equivalence claim |

## Remaining gates and publication rationale

The implemented local interface and the traceable reconstruction justify
continuing OpenCASTp development. A defensible publication argument would be a
reproducible local implementation of the targeted modern CASTp behavior,
transparent molecular/measurement policies, and independent comparison data.
A new package name or an unmeasured acceleration plan is insufficient.

The current 44-system comparison qualifies exact region memberships, region
SA/MS values and the audited aggregate mouth/boundary descriptors under the
declared ATOM-record preparation. Targets are original archived CASTpFold
outputs. This is not a fresh live comparison of every CASTp3/server route.
Individual mouth identity and geometry, per-atom contributions, exported
orthospheres, the remaining 45 archives and independent new inputs still need
audit. No finite panel establishes equivalence for arbitrary chemistry.

After the sole scientific priority is satisfied, readiness work includes source
and license provenance/public distribution ([issue #2](https://github.com/uibcdf/opencastp/issues/2)),
scientific coverage and broader CI/platform qualification
([issue #3](https://github.com/uibcdf/opencastp/issues/3)), and incoming PR-validation
and skipped-CI recovery work ([issue #7](https://github.com/uibcdf/opencastp/issues/7)).
These remain separate from numerical equivalence; the scientific work does not
implicitly complete them.

## Maintaining this register

Change a capability's status only with linked implementation and independently
executed evidence. Pin competitor versions when making source or numerical
comparisons. Retain refuted paths, skipped dimensions and limitations in the
owning validation record. Update this page and the corresponding issue-backed
checkpoint together when the measured scope changes. Future performance claims
must state their workload, baseline, hardware and numerical agreement.
