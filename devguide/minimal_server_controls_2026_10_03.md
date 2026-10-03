# Minimal CASTpFold controls and a final-export counterexample — 2026-10-03

Owner: [OpenCASTp #6](https://github.com/uibcdf/opencastp/issues/6), still open.
Six small jobs completed. They do not fix the five original scalar residuals
or change the 89-input corpus verdict: 14911/14916 regional SA/MS values.

## Controlled inputs and executed comparisons

Reduce 1MRG void 22 to its five original ATOM records, retaining atom names,
residues, chain, residue IDs and coordinates. A second copy applies integer
translation (-44, -108, 5) angstroms. Array predictions use explicit original
castp3_protor radii: four carbon atoms at 1.88 and one GLU OE2 oxygen at 1.40
angstroms before probe expansion. These are real original identities in a
partial fragment, not a complete folded protein; no fictitious chemical labels
or additional protein atoms are introduced.

For a symmetric geometric control, reposition the four retained carbon records
at the alternating-sign corners (+/-1.95, +/-1.95, +/-1.95) angstroms of a
regular tetrahedron. This deliberately changes their geometry. Two further
jobs keep that exact PDB and choose probe radii by native root finding, before
server observation, to straddle the predeclared six-decimal volume boundary.
This designs test inputs; it does not fit a radius correction to server results.
The last control separates the same four carbon centers to alternating-sign
corners at +/-10 angstroms, eliminating all sphere overlaps.

Every uploaded file contains only the stated ATOM records plus TER/END.
All six returned PDBs preserve atom IDs, names, residues and coordinates.
All contribution CSVs retain the same IDs and chemical labels. Job ZIP names
and SHA-256 receipts are verified before comparison. Expected radii remain
caller-controlled assumptions, constrained but not independently certified by
printed exported geometry and scalar measurements.

| Control | CASTpFold job | Native SA volume (cubic angstroms) | Server volume | Regional scalar matches |
| --- | --- | ---: | ---: | ---: |
| Five original 1MRG atoms | j_6ac16e68d3f92 | 0.003499637808737438 | 0.004 | 3/4 |
| Five atoms near origin | j_6ac16e692c220 | 0.0034996378020931695 | 0.004 | 3/4 |
| Regular four-carbon tetrahedron, probe 1.4 | j_6ac16e697ef57 | 0.014193987289649046 | 0.014 | 4/4 |
| Regular tetrahedron, probe 1.4355397123768594 | j_6ac171ac8d00f | 0.0034996499999955244 | 0.003 | 4/4 |
| Regular tetrahedron, probe 1.43554144494277 | j_6ac171acd6fff | 0.00349935000003998 | 0.003 | 4/4 |
| Four separated carbons | j_6ac171ad32e7c | 2640.728641037948, open hull region | 2640.729 | 4/4 |

All six exact region memberships, all 42 additional aggregate descriptors and
all eight exported supporting orthospheres match. Regional scalars total
22/24; both failures are the retained 1MRG SA-volume residual. Its SA area,
MS area and MS volume remain identical to the full-protein server output.
There are no pending jobs in this group. No new CASTp3 job was submitted.
These are diagnostic reductions/parameter replicates and constructed point
clouds, not additional distinct proteins or a ligand-site benchmark.

## A useful counterexample to final rounding

The [preceding probe controls](1mrg_probe_assembly_controls_2026_10_03.md) supported
a conditional local six-decimal intermediate format. The symmetric boundary
control is a new counterexample even at similarly tiny cavity volume: native
0.0034996499999955244 would become 0.003500 at six decimals and then print
0.004, whereas the server prints 0.003.

More strongly, the native 1MRG fragment volume is slightly **smaller**, yet its
server value is **larger** (0.004 versus 0.003). No single monotonic final
export function of those native SA volumes can produce both outputs. This
rejects a final-formatter-only explanation conditional on the current model.
It does not exclude different effective server inputs, domains, branch choices,
primitive/partial contribution precision or accumulation followed by export.
No modern server bug or exact internal radius choice is proved.

Predictions for nearest probe-input quantization at four, five and six decimals,
and float32 probe materialization, were retained before submission. Four-decimal
input quantization predicts 0.004 for both symmetric boundary controls and is
rejected in this conditional model. Direct float64, five/six-decimal probe input
and float32 probe input each predict 0.003 for both; these outcomes do not
distinguish those alternatives. The CSV's six-decimal probe annotation is an
output display, not proof of internal probe precision. A joint upstream/export
policy must be evaluated, not inferred from that annotation.

## Independent geometry and the separated-sphere control

The section oracle independently integrates the five closed controls in two
orientations/refinements each. Maximum volume difference from native integration
is below 7e-12 cubic angstroms, with estimated quadrature errors below 1e-12
and no convergence messages. Spheres and domains remain shared inputs; these
are estimated errors, not certified bounds or independent atom preparation.
This supports the native measurements of the explicit test models.

For separated carbon balls the elementary per-atom reference is
SA area 4*pi*(1.88+1.4)^2, SA volume 4*pi*(1.88+1.4)^3/3,
MS area 4*pi*1.88^2 and MS volume 4*pi*1.88^3/3. All 16 exported atom quantities
match both the unchanged printed-precision tolerance and direct formatting.
This checks disjoint spherical contributions without the native CASTp formulas.
It constrains major carbon-radius, unit and SA/MS model differences, not their
exact internal representations or oxygen typing.

The initial assumption that separation would yield zero reported regions was
rejected locally before submission. There is no enclosed void, but both the
native castp3 convention and the server report one open region with one mouth
comprising the four hull faces. Its four regional scalars and seven additional
descriptors match. Do not call it a biological binding pocket or silently
discard it. This is a concrete methodological convention exposed by a simple
case, separate from the five tiny scalar residuals. These SA/MS models are
distinct analytical measures in the [CASTp 3.0 article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6031066/).

## Implications and next gate

Retaining the 1MRG discrepancy with only five atoms makes distant protein atoms,
whole-protein processing and raw absolute coordinate position less plausible
causes. A wholesale region-method disagreement is also unlikely for these six
controls because lining atom sets and exported supporting spheres match at
printed precision.
The independence boundaries above prevent treating that agreement as exact
equality of all hidden server state.

Prioritize decomposition of the tiny volume into initial tetrahedral volumes,
spherical sectors, edge overlaps and triple intersections. Compare one versus
two tetrahedra, equal versus unequal radii, and primitive branch conditions.
Trace cancellation and the precision/storage of **partial** quantities, rather
than changing the final formatter alone. Where possible, vary geometry smoothly
through an intersection transition to separate a changed mathematical branch
from a numeric threshold. Keep passing controls, all five original residuals
and the 89-input gate when testing any joint replacement. All original residuals
are SA quantities; a correction confined to MS toroidal/cusp terms cannot be
their sole cause. Neither a per-case patch nor a tolerance increase is justified.

[Input-free evidence](artifacts/minimal_server_controls_2026_10_03.json) retains
predeclared predictions, source identity, Python 3.14.7, actual package metadata,
input/result/cache hashes, completed job receipts, full compact comparisons,
independent section estimates and six exact own-code collectors. Restore their
documented private paths to replay; existing submission state prevents duplicate
jobs. Original PDBs, server ZIPs and private caches remain outside publication.
Production numerical source, radii, native defaults and tolerances are unchanged.
Existing TopoMT server tooling was reused; no new attribution or optional-engine
integration boundary was introduced. Full server equivalence remains open.


## Accepted economical investigation sequence

The maintainer requests minimal-first hypothesis development. Use these frozen
small jobs as the inner investigation loop, with predeclared predictions and
local numerical experiments. Reuse downloaded server results; submit another
small job only when it discriminates between surviving explanations.

1. **Minimal diagnostic cases:** explain the targeted residual while retaining
   matching equal-radius, translated, boundary and separated-sphere controls.
   Trace individual terms, branches and model choices before changing a public
   numerical implementation. A local hypothesis need not explain all five
   corpus residuals if its declared scope is narrower.
2. **Seven-system molecular panel:** after the minimal gate, evaluate 1STP,
   8RAT, 1MRG, 1PSN, 1YPI, 1FBP and 2FBP. Require the declared improvement and
   no new mismatches; retain untouched residuals as unresolved, not hidden.
3. **Full 89-input corpus:** run only for a candidate that survives the
   preceding panel. This is the final generalization gate, not the inner loop.
   Complete server-equivalence claims still require all applicable open gates.
4. **Counterexample reduction:** if expansion fails, isolate the new molecular
   counterexample into another minimal fixture and return to the first stage.

Scientific corpus calculations are distinct from repository unit/engineering
tests. Do not rerun the full molecular corpus for every diagnostic parameter
trial. Required lint, tests and documentation gates still apply when publishing
code or evidence changes. Reuse prepared inputs and geometry only when the
hypothesis preserves their scientific assumptions; changed coordinates, radii
or geometry/predicate logic require appropriate recomputation. Cache identity
must retain source, inputs, units and effective policies.


## Local validation

All 101 tests pass with Pytest Receptor in `molsyssuite@uibcdf_3.14`, including
enabled 1STP/8RAT molecular guards and four new minimal-evidence guards. The
new guards first failed without the record and passed with the completed
six-job evidence. One pre-existing TopoMT Pint cache warning remains visible.
Ruff lint/format, index verification and Sphinx HTML with warnings treated as
errors pass. TopoMT's catalog-only update passes its two reporting tests and
index check; its numerical engine remains unchanged. Engineering success is
separate from the unclosed scientific equivalence gate.
