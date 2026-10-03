---
summary: Establish complete measured local CASTp3 and CASTpFold equivalence
issue: uibcdf/opencastp#6
status: active
opened: 2026-10-02
closed:
verification: measured
area: [castp, geometry, validation]
guard:
normative:
blocked_by: []
supersedes: []
---

# CASTp3 and CASTpFold equivalence

## What

The maintainer makes complete server-result equivalence the sole current
scientific priority. Acceleration, extra capabilities and other improvements
are deferred until that gate is demonstrated. Existing compatibility and
provenance records remain truthful; their later development is not part of
this work. TopoMT CASTp code is retained.

## How

Use original pinned server archives as result targets and calculate using
OpenCASTp. Developer-only TopoMT molecular preparation supplies explicit
spheres; its numerical predictions are not the oracle. Retain exact archive,
PDB and prepared-input hashes and actual producer versions. Keep preparation
discrepancies separate from numerical discrepancies.

Compare exact atom-set multisets by class before pairing metrics. Preserve
duplicate multiplicity, missing/extra records, evaluated-empty cases and
calculation failures. Scalar tolerance is half the printed decimal quantum
plus 1e-8 for arithmetic comparison; it never alters geometric decisions.
Ambiguous duplicate lining sets cannot supply metric evidence without an
additional independent identity. No fitted epsilon or molecule-specific rule.

## Why

The inherited TopoMT forty-system result is 39/40 for the compared atom
classes. The OpenCASTp extraction audit demonstrates source parity on two
inputs. Neither result certifies analytical open regions, individual mouths
or complete modern-server equivalence. Historical diagnosis remains linked
through uibcdf/topomt#88 and the scientific extraction checkpoint.

## What was refuted

The initial 1STP molecular regression fails with a missing analytical field
on an open pocket. Applying the retained tetrahedral inclusion/exclusion
calculation to actual open components reproduces all 36 printed SA/MS values
over nine server regions. Open-region closure is not required to define the
tetrahedral integration domain. This does not certify analytical mouth metrics.

## Scope and exclusions

Keep literature and empirical castp3 definitions explicit and radii independent.
Do not migrate consumers, remove TopoMT code, add Rust/GPU, publish a package
or change DFND/Topography during this investigation. Do not redistribute
server archives before the existing provenance review.

## Acceptance criteria

1. Reproduce the original forty-system panel directly in OpenCASTp and expand
   to every applicable archived case without silently dropping failures.
2. Establish independently justified preparation for the remaining 1HIV
   residual; retain original and prepared evidence rather than fitting atom sets.
3. Match region topology, exact atom membership and SA/MS areas and volumes.
4. Validate individual mouth topology and geometry, printed analytical mouth
   areas/perimeters, boundary length and corner counts; audit independent
   contribution/orthosphere evidence where exported.
5. Preserve closed-void evidence and add failing-first durable numerical and
   molecular guards. Commit a completed, versioned result inventory before
   asserting equivalence. General untested chemistry remains explicit.

## Completed checkpoint — 2026-10-02

The fresh forty-case ATOM-prepared comparison passes all 991 exact region
memberships, 3964 region SA/MS values and 6937 additional boundary/aggregate
mouth descriptors. The original 39/40 protein preparation and separate 1HIV
variant remain visible. An 89-archive contributor inventory supports the
observed HETATM omission; it does not establish a universal service contract.

Three further incorporated-HETATM examples (3LCK, 1QPE and 1G1F) and one
free-phosphotyrosine control (1PTY) were calculated under both preparations.
All four ATOM cases match, bringing qualified coverage to 44 distinct cases,
1160 region memberships, 4640 region values and 8120 additional descriptors.
Retaining modified residues changes one lining set in each protein example;
1G1F also produces seven extra lining sets. The ligand control is unchanged.

The signed analytical mouth model initially passes 23/40 extended cases.
An independently declared castp3 convention using unsigned pair projections
reproduces 40/40 without molecule-specific adjustments. 8RAT's negative
SA mouth area remains an explicit compatibility result; signed projections
remain the default numerical choice. Definition/radius/mouth-measurement
choices are independent and recorded. See ../server_equivalence.md for
precise coverage, artifacts, equations and reproduction commands.

Failing-first synthetic open-region and mouth-policy tests, real 1STP/8RAT
archive regressions, comparator guards and artifact inventory guards accompany
the implementation. Molecular tests require an explicit developer reference
and local archives; skips do not establish equivalence. Remaining acceptance
criteria include individual mouth geometry, contribution/orthosphere evidence,
the rest of the archive cohort and broader independently chosen chemistry.
The issue stays active; complete_server_equivalence remains false.

## Maintainer benchmark and format steering

Exclude HETATM before preparation throughout the validation benchmark. Keep
original diagnoses and paired failures; do not fit selections to pocket labels.
Explain the observed archived-server limitation to users using 1HIV and the
new incorporated phosphotyrosine examples. Free modified amino acids are not
automatically polymer residues. The numerical array API retains all spheres
supplied by the caller and is format-neutral. Supported MolSysMT readers can
prepare PDB/CIF/BinaryCIF or molecular objects. Direct file ingestion remains
a separate, unimplemented frontend, not a reason to impose a PDB-only core.

## Local verification

49 source tests pass with pytest-receptor, including the explicitly executed
1STP/8RAT guards. One pre-existing developer Pint cache warning is retained.
Ruff, bounded public-API mypy, generated-index verification and warning-free
Sphinx checks pass. The final numerical wheel passes an isolated non-editable
Python 3.13.14 void/pocket/mouth smoke without TopoMT/MolSysMT imports. Hosted
supported-minor evidence for the changed commit remains independent.

## Hosted verification

Commit a050289 passes full matrix 37075626305 on actual Python 3.11.16,
3.12.14, 3.13.15 and 3.14.7, with non-editable installation, isolated
void/pocket/mouth smoke and 47 source tests plus two explicit molecular skips
per minor. The locally executed molecular guards and 44-case benchmark remain
separate evidence. Routine CI 37075626152 and admission bootstrap 37075626661
also pass. See ../scientific_status.md and the pinned native runtime artifact.

## Comparative rationale checkpoint — 2026-10-03

The maintained [comparison register](../../docs/project_rationale.md) pins the
inspected pyCASTa source to f3418f38cd3d3c11e6cdd8c13b11431cc5b91894
(metadata version 1.0.8). Its analytic tetrahedral-volume routine and alpha/flow
processing differ from the CASTp quantities and reconstruction audited here.
These source observations do not certify current-version output differences
or superiority. An executed comparison must control inputs, radii, backend,
probe/alpha semantics and postprocessing, comparing lining sets before scalars
and distinguishing polyhedral from SA/MS measures. Preserve missing quantities
as missing. The server archive remains the oracle; pyCASTa is a comparison
provider. This evidence may support publication rationale but does not replace
the remaining individual-mouth, contribution, orthosphere and corpus gates.

## Expanded corpus and concrete comparisons — 2026-10-03

All remaining 45 archives were independently predicted; 40/45 pass every
audited field. Cumulative disjoint coverage is all 89 archives, 3729 exact
regions, 14911/14916 region scalars and 26103 additional aggregate descriptors.
Five strict scalar discrepancies in 1MRG/1PSN/1YPI/1FBP/2FBP remain explicit.
Rigid translations retain the first three failures; no production correction
or tolerance change is justified by that diagnosis. Source numerical code is
unchanged. See ../server_equivalence.md for exact targets and values.

The executed pyCASTa preparation excludes incorporated HETATM atoms in four
protein/peptide examples and allows elemental, rather than per-atom, radius
overrides through its inspected table. Its current main module cannot compile;
separate unchanged geometric-routine calls on 1STP/1HEW demonstrate rejection
of valid tetrahedron groups using an atom-count limit. These observations are
pinned to f3418f3 and do not certify a separately distributed package or full
competitor metric parity. Current public server forms expose no HETATM toggle
or per-atom radii. The observed restrictions, possible unqualified workarounds,
negative-mouth convention and independently tested OpenCASTp radius control
are recorded in ../../docs/problems_and_model_control.md and
../comparison_evidence_2026_10_03.md. All remaining scientific gates stay open.

## Historical metric controls — 2026-10-03

Compiled unchanged 1996 metric.c primitives, accurate summation and 40/80-digit
re-evaluation all retain the five strict scalar failures on frozen modern
integration domains. The selected compiled C quantities differ from current
Python quantities by less than 7e-11, with zero runtime metric corrections.
The 247 exported orthospheres in these five regions match distinct supporting
tetrahedra at printed precision. This constrains those domains; it does not
qualify every exported orthosphere or execute the whole historical pipeline.
Source geometry, radius choices and comparison tolerances remain unchanged.
See [diagnostic evidence and replay](../metric_controls_2026_10_03.md). Modern
input, measurement and export conventions remain open; no modern-server bug
or complete equivalence is established. The 84/89 corpus verdict is unchanged.

Local diagnostic verification passes 56 tests with pytest-receptor, including
the explicitly configured 1STP/8RAT molecular guards and two new evidence
guards. Ruff lint/format, generated-index and warning-free Sphinx checks pass.
One pre-existing developer Pint cache warning remains visible. These passing
engineering checks do not change the five strict scalar failures.


## Input and contribution export controls — 2026-10-03

The new [bounded diagnostic](../input_export_controls_2026_10_03.md) separately audits 1MRG's 3,864 SA
space-filling atom contributions: 3,759 strict matches. A four-decimal
intermediate export candidate reproduces 3,863 values, explaining 104/105
strict discrepancies, but the modern export source remains unknown. Historical
C primitives reproduce the unresolved atom 588. Uniform float32 coordinates
can fix its candidate export while worsening the full-atom comparison; none
of seven declared input conventions fixes all five region residuals.

The same-job live PDB/pocInfo files for three residual inputs match the archived
bytes; inspected raw contribution URLs return HTTP 200 HTML, not numerical
data. No new calculations or production numerical changes were made. Existing
region coverage remains 84/89 passing systems; per-atom and individual-mouth
qualification remains incomplete. Controls run in Python 3.14.7 with installed
editable OpenCASTp and TopoMT; previous 3.13 evidence keeps its original identity.


## Accepted native model and server recipe — 2026-10-03

The maintainer requests an explicit native OpenCASTp model, independently
selectable server-compatibility controls and a documented public recipe that
guarantees equivalence within its validated scope. Native calculations retain
selected incorporated HETATM atoms and full calculated precision; server
reproduction may explicitly choose its record filtering, castp3_protor radii,
region/mouth conventions and qualified export precision. These decisions must
remain separate and observable. Native here does not mean TopoMT's DFND engine.

See [the accepted contract](../native_model_and_server_compatibility.md) for boundaries, public-API requirements,
effective-choice provenance and recipe acceptance gates. Array analyze already
accepts explicit radii and independent region/mouth policies; public molecular
preparation controls and a certified server export recipe remain to implement
and validate. No new API, rounding rule or full equivalence claim is introduced
by this documentation decision. Current scientific failures remain open under #6.
