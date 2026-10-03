# Direct archived-server equivalence checkpoint

Recorded 2026-10-02. Complete measured CASTp3/CASTpFold equivalence is the sole
current scientific priority under uibcdf/opencastp#6. Acceleration, unrelated
capabilities and consumer migration are deferred. TopoMT CASTp remains intact.

The maintained [project rationale](../docs/project_rationale.md) separates
implemented capabilities, bounded comparisons with pyCASTa and future candidates.
Its publication and performance claims must retain the qualification limits here.

## Current measured coverage

The fresh forty-system benchmark excludes HETATM before molecular parsing,
then selects protein/peptide atoms with explicit castp3_protor radii and a
1.4 angstrom probe. OpenCASTp independently rebuilds all numerical geometry;
TopoMT provides developer-only molecular preparation, not expected predictions.
Targets are original archived server outputs, not another local implementation.

| Gate | Fresh ATOM-record forty-system run |
| --- | ---: |
| Completed and passing systems | 40/40 |
| Exact region atom-set multisets | 991/991 |
| Region SA/MS areas and volumes | 3964/3964 |
| Aggregate mouth SA/MS areas/perimeters, open regions | 2412/2412 across 603 regions |
| Intersection lengths, corner counts and mouth-triangle counts | 2973/2973 |

All four analytical mouth measures also match the exported zeros for 388
closed voids. Thus the extended auditor compares 6937 additional descriptors
(7 per region) beyond the 3964 region SA/MS values. This covers aggregate
mouth quantities per region, not independently identified individual mouths.
Mouth count and aggregate rim atom membership match for every region.

`artifacts/server_mouth_castp3_panel_2026_10_02.json` is the completed extended
result. It pins archive/PDB/prepared-input hashes, producer versions and the
executed source hashes. Exact executed API, mouth kernel and runner snapshots
are retained under stage_source_snapshots. The final API subsequently renames
an ndarray probe variable for static typing without changing numerical
operations. Molecular comparison uses Python 3.13; supported-minor installed
checks and CI remain separate evidence.

An earlier fresh forty-input ATOM-record run, comparing region measures only,
is retained in artifacts/server_region_atom_panel_2026_10_02.json with its
runner snapshot. It independently matches the same 991 regions and 3964 values.

## Preparation diagnosis: HETATM within proteins

The original protein/peptide forty-input preparation gives 39/40 passing
cases, 990/991 lining memberships and 3960/3964 region measures. Only 1HIV's
prepared sphere count differs between that preparation and the ATOM variant.
The original residual remains visible in
artifacts/server_region_panel_2026_10_02.json. A separately executed ATOM
variant of 1HIV is retained there; it was not substituted into the original run.

1HIV contains fourteen HETATM atoms in two CSO residues belonging to its
protein chains. None is listed in the server contribution table. Excluding
HETATM before preparation reproduces all 17 regions and 68 region measures.
This is an input-model discrepancy, not evidence of a region-algorithm defect.

The complete 89-archive contributor scan finds no contributing HETATM serials,
including 84 inputs containing 17,945 HETATM records. The pinned scan and its
reproducible collector are retained in the original panel artifact and
artifacts/record_policy_audit_2026_10_02.py.txt. This evidence supports the
corpus convention; it is not a universal claim about all uploaded structures
or other service routes.

Three further polymer examples and a separate-ligand control confirm the
importance of distinguishing file labels from chemistry. MolSysMT selects
PTR A394 in 3LCK and 1QPE, and PTR B1162/B1163 in 1G1F, as protein/peptide
atoms. MODRES and peptide-bond LINK records and the RCSB structure entries
support incorporation. 1PTY's phosphotyrosines are free ligands and are not
selected as protein/peptide atoms.

| Input | Protein/peptide HETATM atoms | Exact server regions with them retained | With HETATM excluded | Native region count, retained/excluded |
| --- | ---: | ---: | ---: | ---: |
| 1HIV | 14 | 16/17 | 17/17 | 17/17 |
| 3LCK | 16 | 41/42 | 42/42 | 42/42 |
| 1QPE | 16 | 45/46 | 46/46 | 46/46 |
| 1G1F | 32 | 41/42 | 42/42 | 48/42 |
| 1PTY control | 0 | 39/39 | 39/39 | 39/39 |

All four new ATOM-record cases match every audited region and aggregate
mouth/boundary descriptor. They add 169 regions, 676 region values and 1183
additional descriptors to the original forty-system cohort: 44 distinct
passing ATOM-prepared systems, 1160 regions, 4640 region values and 8120
additional descriptors. The unfiltered failures and 1G1F's seven extra lining
sets/one missing lining set are preserved, not dropped from a denominator.

Evidence is artifacts/protein_heterogen_inspection_2026_10_02.json and
artifacts/protein_heterogen_panel_2026_10_02.json. The latter retains both
four-case preparations and their separate executed source hashes. The
inspection collector is artifacts/protein_heterogen_inspection_2026_10_02.py.txt;
execute it as Python with --archive-dir and --output in the developer molecular
environment. This is a bounded chemical inventory, not an exhaustive residue
classification of all 89 structures.

The maintainer requests ATOM preparation for validation only. OpenCASTp's
array API never removes HETATM, hydrogens or modified residues: supplied
coordinates and radii define the user's physical model. PDB/CIF/BinaryCIF
and other MolSysMT forms can supply explicit spheres. Direct molecular-file
ingestion remains a separate frontend, not an implemented numerical API.

## Numerical measures and explicit mouth conventions

The inherited integration already calculated atomic sectors and overlaps
inside chosen complement tetrahedra. Public analyze initially exposed SA/MS
only for closed voids. The same integration now measures actual open-region
tetrahedra. Artificial mouth faces delimit volume and do not become molecular
surface. Region ranks, flow, radii, atom mapping and mouth construction are
unchanged by this extension.

Mouth areas and arc perimeters are computed from triangle sectors and pair
terms controlled by base-rank alpha-complex edge membership. Molecular terms
use bare atomic radii and tangent probe circles; when a probe circle crosses
an edge, its out-of-triangle cap is removed from area. Simply clipping planar
triangles by inflated/bare atomic disks failed the 1STP printed measures and
was not promoted.

Two mouth conventions remain explicit and independent of pocket_definition
and radii. For a pair separated by d with expanded radii R_i and R_j, the
intersection projections are x=(R_i^2-R_j^2+d^2)/(2d) and d-x.
The signed policy retains these projections in sector angles and triangles.
The reconstructed castp3 convention uses their absolute values, including
when a projection lies beyond one center. The resulting difference in both
angles and triangular contributions explains the four failing mouth values
of 8RAT region 9: signed SA area 0.886316783 versus archived -0.573, signed
MS area 16.419006725 versus 15.68, and signed perimeters 7.180995858/15.977455288
versus 7.693/16.49. The compatibility option reproduces all printed values.

The complete signed-projection precursor run remains in
artifacts/server_mouth_signed_panel_2026_10_02.json: 23/40 match the full
extended comparator. The unsigned compatibility run passes 40/40 without a
molecule-specific rule, fitted radii, fitted geometric epsilon or scalar
correction. This reconstructs observed behavior; it is not recovered modern
server source or a claim that either model is universally qualified physics.
Do not clamp negative compatibility areas or silently change the user's choice.
The effective mouth_measurement_policy is recorded in result.execution.

Planar mouth area and wire perimeter remain distinct from analytical SA/MS
area and arc perimeter. Per-region aggregates are qualified here; individual
mouth partitions and their independent server identities remain unqualified.

## Comparison and regression contract

Require exact atom-set multisets by feature class before pairing metrics.
Preserve duplicate multiplicity. Ambiguous duplicate lining sets cannot supply
scalar evidence. Require mouth count and aggregate rim membership. Every
requested field must be present and finite; counts are exact and never
truncated. Scalar tolerance is half the printed decimal quantum plus 1e-8,
with zero relative tolerance. This arithmetic allowance never changes geometry.

The real 1STP guard initially failed missing open-region fields. The synthetic
four-sphere one-mouth pocket independently reproduced that defect on published
OpenCASTp 6303af5. It guards analytical fields and non-default unit conversion.
Real 1STP now checks all region and aggregate descriptors. Real 8RAT guards
the negative unsigned-compatible mouth result. Synthetic guards check explicit
conventions, invalid choices, rigid-motion/dimensional behavior and zero probe.
Audit guards reject count-only agreement, absent/nonfinite fields, wrong
precision, ambiguous duplicates, incomplete rim sets and fractional counts.
Artifact guards preserve all forty original cases, the separate 1HIV variant,
the global ATOM run, signed failures, unsigned successes and the paired new
heterogen cases/control. Molecular tests skip visibly without the explicitly
configured local archive/reference; such a skip is not equivalence evidence.

## Reproduce the current extended benchmark

Set PYTHONPATH to OpenCASTp src and the developer TopoMT root:

```bash
python devtools/compare_castp_servers.py \
  --topomt-root /path/to/topomt \
  --archive-dir /path/to/topomt/topomt/data/CASTpFold_server \
  --cases 1crn 1rop 2pk4 3phv 8rat 1stp 1rob 2lyz 1ifb 2ifb \
    1hew 1stn 1hel 1snc 5dfr 1hfc 1brq 1rbp 1hsi 1hiv \
    1ida 3ptb 3ptn 4phv 2tga 1cge 1a6u 1srf 1mtw 2ctv \
    1esa 1a6w 1inc 1bmq 1ahc 4ca2 3tms 1djb 1a4j 1cdo \
  --atom-record-policy atom --workers 4 --output /tmp/server-extended.json

python devtools/compare_castp_servers.py \
  --topomt-root /path/to/topomt \
  --archive-dir /path/to/topomt/topomt/data/CASTpFold_server \
  --cases 3lck 1qpe 1g1f 1pty --atom-record-policy protein \
  --workers 2 --output /tmp/heterogen-protein.json
```

Repeat the second command with --atom-record-policy atom for the declared
benchmark alternative. The current CLI and audit function default to atom;
they explicitly select castp3 mouth measurements. The current full comparator
is broader than the preserved region-only runner snapshots. Exit 1 means a
calculation or comparison failure. All discrepancies and completion states
remain in the report. Server archives remain external and are not redistributed.

## Gates still open

Individual mouth identity/boundary geometry, per-atom contributions and
exported orthospheres require independent audit. The remaining 45 archives
have now been calculated as recorded below; five scalar discrepancies remain.
New independently selected inputs have not been fully predicted here.
All reports retain complete_server_equivalence=false. Extend measured
coverage while preserving the present closed-void/open-region controls;
no finite panel alone establishes equivalence for arbitrary chemistry.

## Expanded corpus checkpoint — 2026-10-03

The complete remaining-45 run independently calculates the disjoint archive
cohort with the same declared ATOM preparation and compatibility conventions.
It completes all cases and preserves five strict scalar failures. Results are
2569/2569 exact regions, 10271/10276 region SA/MS values and 17983/17983
aggregate mouth/boundary descriptors; 40/45 systems pass every audited field.
The run exits 1. Evidence is artifacts/server_remaining_panel_2026_10_03.json
with pinned runner/launch snapshots, hashes, source commit 51bed38 and versions.

Together with the earlier 44 distinct cases, cumulative coverage is all 89
archives, 3729/3729 exact regions, 14911/14916 region values and 26103/26103
additional descriptors; 84/89 systems pass the full comparator. This combines
separately pinned stages rather than claiming a new single 89-input run.

| Input / region | Field | Expected | Actual | Fixed tolerance |
| --- | --- | ---: | ---: | ---: |
| 1MRG / 22 | SA volume | 0.004 | 0.0034996378073546275 | 0.00050001 |
| 1PSN / 13 | SA volume | 0.686 | 0.6854994934777379 | 0.00050001 |
| 1YPI / 6 | SA volume | 18.094 | 18.094500169312916 | 0.00050001 |
| 1FBP / 3 | SA area | 299.277 | 299.2764954437975 | 0.00050001 |
| 2FBP / 11 | SA volume | 36.266 | 36.26650173333687 | 0.00050001 |

Areas use square angstroms and volumes cubic angstroms. These lie near printed
rounding boundaries, but the cause remains unestablished. Do not loosen the
comparator, fit radii or promote an unexplained scalar correction. Fixed-
topology rigid-translation diagnostics on the first three cases retain each
failure; a simple coordinate-frame remedy is refuted. No numerical source
changed during this expanded audit. Individual mouth geometry, contributions
and orthospheres remain unqualified; complete_server_equivalence stays false.

[Concrete comparison evidence](comparison_evidence_2026_10_03.md) records the
executed pyCASTa preparation/index discrepancies and current public form
inspection. The public [problem register](../docs/problems_and_model_control.md)
keeps implemented model control separate from physical correctness claims.

## Historical metric controls — 2026-10-03

Compiled unchanged 1996 metric.c primitives, accurate summation and 40/80-digit
re-evaluation all retain the five strict scalar failures on frozen modern
integration domains. The selected compiled C quantities differ from current
Python quantities by less than 7e-11, with zero runtime metric corrections.
The 247 exported orthospheres in these five regions match distinct supporting
tetrahedra at printed precision. This constrains those domains; it does not
qualify every exported orthosphere or execute the whole historical pipeline.
Source geometry, radius choices and comparison tolerances remain unchanged.
See [diagnostic evidence and replay](metric_controls_2026_10_03.md). Modern
input, measurement and export conventions remain open; no modern-server bug
or complete equivalence is established. The 84/89 corpus verdict is unchanged.

Local diagnostic verification passes 56 tests with pytest-receptor, including
the explicitly configured 1STP/8RAT molecular guards and two new evidence
guards. Ruff lint/format, generated-index and warning-free Sphinx checks pass.
One pre-existing developer Pint cache warning remains visible. These passing
engineering checks do not change the five strict scalar failures.


## Input and contribution export controls — 2026-10-03

The new [bounded diagnostic](input_export_controls_2026_10_03.md) separately audits 1MRG's 3,864 SA
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

See [the accepted contract](native_model_and_server_compatibility.md) for boundaries, public-API requirements,
effective-choice provenance and recipe acceptance gates. Array analyze already
accepts explicit radii and independent region/mouth policies; public molecular
preparation controls and a certified server export recipe remain to implement
and validate. No new API, rounding rule or full equivalence claim is introduced
by this documentation decision. Current scientific failures remain open under #6.


## Independent export-hypothesis controls — 2026-10-03

The [1STP/8RAT atom controls](independent_atom_export_controls_2026_10_03.md) test the same four-decimal intermediate
export candidate on 3,702 additional SA space-filling quantities. All 82
strict raw discrepancies match that candidate, but it introduces a new
8RAT atom-429 export failure where the raw value passed. Across the three
independent systems including 1MRG, the candidate matches 7,564/7,566 values,
explains 186/187 native discrepancies and introduces one other mismatch.
It remains unqualified as a public server-export policy. Native precision
and original failures are retained; the region gate is unchanged.

## Cavity and atom characterization controls — 2026-10-03

The [four-field controls](metric_characterization_controls_2026_10_03.md) newly audit 7566 MS space-filling atom
quantities in 1STP, 8RAT and 1MRG: 7368 strict raw matches and 7566 candidate
export matches. Two SA candidate failures remain. Atom contributions are not
cavity totals. Applying the same intermediate-rounding candidate to all 14916
recorded region quantities introduces 742 failures; it is rejected as a uniform
cavity-export rule. Direct formatting also exposes a 1OKM MS-area printed-output
mismatch within the existing arithmetic tolerance; this is not a sixth raw failure.

Complete orthosphere-set comparison now matches 5668/5668 spheres across all
384 regions in seven systems, including the five residual systems. It checks
a geometric bijection at exported precision, not independent atom contacts or
individual mouth partitions. Native numerical source, preparation profiles and
comparison tolerances are unchanged. The five strict regional scalar failures,
84/89 region-gate verdict and incomplete whole-corpus/individual-mouth gates
remain visible under #6. No public compatibility export recipe is delivered.


## Joint precision and individual-mouth checkpoint — 2026-10-03

The [joint controls](joint_precision_mouth_controls_2026_10_03.md) clarify that the rejected uniform export transform
is conditional on the current kernel; it does not establish all upstream
assumptions. None of five exploratory intermediate-vector precision variants
improves the seven-system 1536-scalar panel, raw or jointly with export.
An independent edge-fan graph agrees on 203 mouths / 1059 triangles in the
same seven systems. All 632 individual area/perimeter values, rim atoms and
triangle counts match for 158 one-mouth regions. The 20 multi-mouth regions
have matching aggregates but lack an individual server oracle. Shared mesh,
filtration, domains and seeds limit this independence claim. The five strict
regional failures and complete-equivalence gate remain open; production
numerical source, radii and tolerances are unchanged.


## Independent 1MRG geometry and fresh server jobs — 2026-10-03

The [geometric and live-server checkpoint](1mrg_geometric_server_controls_2026_10_03.md) independently integrates
the two tetrahedra of 1MRG void 22 using planar disk boundaries. Its volume
agrees with native integration within 7e-12 cubic angstroms, and an independent
volume derivative supports native SA area. These checks share the prepared
spheres and fixed native domain; they do not independently certify server radii
or preceding geometry. Quadrature errors are estimates, not certified bounds.

Three fresh CASTpFold jobs (baseline and two translations) preserve all 29
regions, printed metrics, additional descriptors and 365 exported orthospheres.
They reproduce the unresolved 0.004 volume. Simple float32 coordinate
materialization does not fix it. The original five residuals remain open,
with no production change, proven server bug or qualified equivalence recipe.


## Probe boundaries and original C regional assembly — 2026-10-03

The [probe/assembly checkpoint](1mrg_probe_assembly_controls_2026_10_03.md) adds five completed CASTpFold probe
controls on the same 1MRG input: all 145 region memberships, 1015 additional
descriptors and 1825 exported orthospheres match; 579/580 regional scalars pass.
Distinct job receipts were verified after correcting a private collector ZIP
filename collision; the superseded fine comparison is invalid. A six-decimal
intermediate formatting candidate matches every printed scalar in these five
controls, but explains only one original corpus residual and introduces nine
failures on originally passing values. It is a local hypothesis, not a public
compatibility policy or proof of the server's internal rounding.

Unchanged original C regional correction bodies plus metric primitives retain
the same five failures on 384 frozen native regions (1531/1536 scalars), with
all 768 intersection-length/corner values matching. Reader-floor controls fix
at most two isolated targets; no variant fixes all five. Domains, inputs and
visibility remain shared, and the full historical pipeline was not executed.
The original 89-system gate is unchanged at 14911/14916 scalars, with #6 open.
No numerical source, native defaults, radii or tolerances changed. The next gate
is discriminating probe quantization from intermediate measurement/export
precision, followed by full-panel validation of any joint explanation.


## Minimal completed server controls — 2026-10-03

The [six minimal controls](minimal_server_controls_2026_10_03.md) retain the 1MRG SA-volume discrepancy with
only its five original atoms, in two coordinate frames. A regular single-
tetrahedron control with a slightly larger native volume prints 0.003 while
the smaller 1MRG fragment prints 0.004. This refutes a common monotonic final
formatter applied to the current native values, including uniform six-decimal
intermediate formatting. Effective sphere inputs, local intersection branches,
partial contribution precision and accumulation remain possible upstream causes.
Independent sections support all five explicit closed-void measurements.

All six lining sets, 42 additional descriptors and eight supporting spheres
match; 22/24 regional scalars pass. Sixteen separated-sphere atom quantities
match elementary formulas. Both implementations report one open hull region
for the separated balls; it is not an enclosed void or biological binding-site
claim. All six jobs completed and atom retention/labels/coordinates were verified.
The original five residuals and 89-input gate are unchanged, with no numerical
source, default, radius or tolerance modification. See the evidence for the
predeclared alternatives and boundaries; a public exact-equivalence recipe is
still unavailable.

## Partial-precision policies refuted by minimal controls — 2026-10-03

The [partial-precision checkpoint](partial_precision_controls_2026_10_03.md)
traces cancellation on six minimal controls and predeclares 41 ablations.
Two policies repair three scalar residuals without new failures on seven
proteins, then pass another twelve systems. Two subsequently designed
four-atom CASTpFold controls each refute one policy; native matches all eight
new scalars. Both uniform policies are rejected, and no numerical change is
adopted. The original five residuals/89-input verdict remain unchanged.
Independent sections support the explicit new geometries. This was a bounded
19-protein diagnostic expansion, not a fresh complete corpus qualification.
Keep issue #6 open and return to minimal branch/input/domain discrimination.
