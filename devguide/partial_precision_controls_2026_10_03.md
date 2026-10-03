# Partial precision, staged gates and two minimal counterexamples — 2026-10-03

Owner: [OpenCASTp #6](https://github.com/uibcdf/opencastp/issues/6), still open.
No numerical policy was adopted. The original 89-input verdict remains
3729/3729 regions, 14911/14916 regional SA/MS scalars, 26103/26103 additional
aggregate descriptors and 84/89 complete cases for those comparisons.

## Decomposition and predeclared hypotheses

Replay the six [minimal controls](minimal_server_controls_2026_10_03.md) using
the existing metric primitives, prepared spheres, complex membership and
tetrahedral domains. Fresh contexts prevent cached primitive values leaking
between hypotheses. The baseline trace exactly reproduces the native sequential
accumulation before any change. Python's built-in floating-point sum is not
the sequential += operation on this Python version; the collector explicitly
uses += for baseline replay and labels math.fsum experiments separately.

For the five-atom original 1MRG fragment, SA volume contributions in cubic
angstroms are:

| Contribution | Count | Sum |
| --- | ---: | ---: |
| Initial tetrahedral volumes | 2 | 24.47905909316667 |
| Vertex spherical sectors | 8 | -40.85832197980033 |
| Edge overlaps | 12 | 17.856788664339486 |
| Triple intersections | 6 | -1.4740261398970853 |

Their final sequential volume is 0.003499637808737438. The sum of absolute
individual terms divided by the final volume is about 24193; the tiny void
results from cancellation of much larger contributions. Both math.fsum
controls retain the two 1MRG scalar failures. This does not explain the
server discrepancy through ordinary summation order or float64 cancellation.

The plan declares 41 variants before execution: the baseline; float32 or
six-decimal scalar returns for sixteen individual methods; and term,
tetrahedron-total or accumulator materialization/aggregation controls.
Underlying geometry, branch predicates and primitive formulas remain shared.
This is an ablation of explicit candidate storage policies, not evidence of
the modern server's internal numeric types. The fragment has two directed
hidden1 attachment outcomes; the regular controls have none. Branch counts,
unequal radii, asymmetry and one versus two tetrahedra remain confounded.

## Economical promotion and bounded expansion

Three hypotheses repair both fragment volumes and retain all 24 minimal
regional scalars: float32 disk_area, six-decimal cap_volume and six-decimal
segment_height. Only these enter the seven-system molecular panel.

| Hypothesis | Seven-system regional scalars | Repaired / newly broken | Length and corners |
| --- | ---: | ---: | ---: |
| Native baseline | 1531/1536 | 0 / 0 | 768/768 |
| float32 disk_area | 1534/1536 | 3 / 0 | 768/768 |
| Six-decimal cap_volume | 1534/1536 | 3 / 0 | 768/768 |
| Six-decimal segment_height | 1532/1536 | 2 / 1 | 768/768 |

The last hypothesis introduces a 2FBP region 33 SA-volume failure and is
rejected at this gate. The other two provisionally repair 1MRG, 1PSN and 1YPI;
1FBP SA area and 2FBP region 11 SA volume remain unresolved. Neither candidate
changes SA area, so it cannot alone repair the 1FBP area residual.

Next evaluate only the two survivors on the twelve smallest atom-count inputs
outside that panel, with lexical tie-breaking fixed before evaluation:
1CRN, 1ROP, 2PK4, 3PHV, 1ROB, 1HEL, 1HEW, 2LYZ, 1IFB, 2IFB, 1SNC and 1STN.
All three calculations, including baseline, match 504/504 regional scalars
and 252/252 recalculated length/corner fields. Every archive and prepared PDB,
coordinate array and expanded-radius array hash matches the original reference.
This is a 19-protein diagnostic stage, not a completed fresh 89-input gate.
Original molecular archives were reused; no molecular server job was resubmitted.
The existing developer reference auditor supplies preparation and public
OpenCASTp analysis; a consumer-local callback retains results in private caches.
No numerical core function is patched or replaced.

## Two deliberately discriminatory server controls

Before POST, scan 81 evenly spaced probes over the same previously submitted
four-carbon regular tetrahedron, spanning native SA volumes 0.003497–0.003503.
For each ordering of the surviving predictions, choose the largest minimum
distance from the 0.0035 display boundary. This designs informative inputs
without consulting new server outcomes or fitting a compatibility correction.
All jobs retain the same four original carbon ATOM identities/coordinates;
these are geometric point clouds, not folded proteins or ligand-site benchmarks.

| Control / CASTpFold job | Probe (angstroms) | Native SA volume | float32 disk_area | Six-decimal cap_volume | Server |
| --- | ---: | ---: | ---: | ---: | ---: |
| Disk above cap / j_6ac17eb2896b9 | 1.4355324990521443 | 0.00350089920185348 → 0.004 | 0.003501834644461743 → 0.004 | 0.0034997734326898122 → 0.003 | 0.004 |
| Cap above disk / j_6ac17eb2eaa87 | 1.4355363969456285 | 0.003500224127831686 → 0.004 | 0.003499399107702139 → 0.003 | 0.0035007544017466863 → 0.004 | 0.004 |

Both jobs completed. SHA-256 archive receipts/job prefixes, returned PDB atom
records and contribution-table identities agree with the exact uploads.
Native matches both regions, all eight regional scalars, fourteen additional
descriptors and two exported supporting spheres at printed precision.
Each candidate fails a different SA volume, giving 7/8 scalars each.
Thus **both uniform partial-precision policies are refuted**, despite their
success on nineteen proteins. Repeating the complete corpus for these now
refuted policies would not justify adopting either.

Independent planar-section integration in two orientations/refinements per
new closed control differs from native by less than 5e-14 cubic angstroms,
with estimated errors below 1e-12 and no convergence messages. Spheres and
domains remain shared inputs; estimates are not certified error bounds.
Printed geometry and retained chemistry do not independently certify the
server's exact hidden sphere representation.

## Current inference and next investigation

The experiments exclude these two **common** storage policies; they do not
exclude a branch-dependent upstream representation, effective atom inputs,
another partial-contribution convention or a combined implementation/export
path. No recovered modern implementation or server algorithm defect is proved.
A chance boundary crossing can repair several residuals without identifying
their cause. Keep all five original discrepancies visible.

Return to minimal experiments that disentangle unequal radii, local triple-
intersection attachment branches and one versus two tetrahedra. Predict their
outcomes before additional POSTs. Prefer a small counterexample over a broad
rerun, and promote only a surviving, justified hypothesis to molecular gates.
Do not implement a molecule-specific, branch-specific or numeric-type patch
solely because it moves one number across a printed boundary.

[Input-free evidence](artifacts/partial_precision_controls_2026_10_03.json)
retains plans, actual Python 3.14.7/package metadata, source/input/cache/result
hashes, all comparisons, successful receipts, section estimates and exact own
collectors with their reused submission dependency. Private PDBs/ZIPs/caches
remain outside publication. The five artifact guards were failing first.
No public API, native precision, radius table, default, tolerance, optional
dependency or attribution boundary changed; no new suite admission or full
equivalence claim is made. Source/distribution qualification remains #2.
