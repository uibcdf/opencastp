# Native model and server-equivalence recipe

Accepted maintainer direction, 2026-10-03. Scientific ownership:
uibcdf/opencastp#6. This checkpoint defines the target contract; implemented
API and measured coverage are identified separately below.

## Decision

OpenCASTp provides an explicit native model and independently selectable
server-compatibility conventions. Achieving server equivalence does not make
every observed server convention an appropriate native default. Native results
preserve the declared molecular model and numerical precision; a documented,
validated recipe lets a caller request the corresponding CASTp3/CASTpFold
model and exported results instead.

Here, native means OpenCASTp's own model defaults. TopoMT's native engine
remains DFND; this decision changes neither Topography nor provider admission.
Differences in radius assignment, atom selection and exported precision are
not automatically proven server bugs or proof that our model is universally
more physically correct. Both choices must be inspectable and justified.

## Independent choices

| Boundary | Native direction | Server-compatible direction | Current implementation |
| --- | --- | --- | --- |
| Molecular selection | Use chemical membership and the caller's selection; retain selected incorporated HETATM residues | Apply the explicitly validated server record filter before parsing/typing | Caller-owned preparation; analyze receives explicit spheres |
| Atomic radii | Explicit named radius profile or per-atom values; use the independently documented ProtOr assignment when that molecular profile is requested | The separately identified castp3_protor assignment, including empirically audited typing/masking differences | Public analyze accepts per-atom radii; molecular profiles currently live in the TopoMT developer preparation |
| Hydrogen handling | Consistent with the radius model; united-atom ProtOr does not add separate hydrogen spheres | Reproduce the validated server preparation for that profile | Caller-owned preparation |
| Region definition | The published literature definition | The reconstructed modern castp3 definition | pocket_definition, default literature |
| Analytical mouth measures | Signed projections | Explicit reconstructed castp3 projections, including observed negative compatibility values | mouth_measurement_policy, default signed |
| Output precision | Preserve the calculated values and units | A validated field-specific export convention reproducing printed server values | Native results are unrounded; a server export policy is not implemented or qualified |

Retaining HETATM means retaining atoms selected by chemistry, even when their
PDB record uses that label. It does not automatically include all waters,
free ligands, ions or unrelated molecules. Conversely, record-based server
exclusion is an intentional compatibility choice, not a chemical judgment.
The effect of atom selection, radius typing and terminal-atom masks must each
be visible in the prepared atom IDs and effective sphere model.

The geometry API cannot infer record types, residue chemistry or a ProtOr
profile from coordinate/radius arrays. Molecular controls belong at a distinct
public preparation/frontend boundary; its future implementation must use
MolSysMT's reusable conversion, selection and typing capabilities without
importing molecular dependencies into the numerical core. Molecular readers
may support PDB, CIF, BinaryCIF or other MolSysMT forms. File-format conversion
alone is not a HETATM inclusion/exclusion policy.

No direct molecular frontend or new argument names are delivered by this
decision. Its public radius-profile and atom-policy arguments must be exposed
when implemented, with optional-dependency handling and separate tests.
The existing analyze signature and defaults remain unchanged at this checkpoint.

## Native results and compatibility exports

Retain full calculated SA/MS quantities, units, original atom IDs and numerical
geometry in the native result. Compatibility formatting operates on a distinct
export representation. It must not round coordinates, alter predicates, change
filtration or overwrite the raw metrics to force a printed agreement. Raw
and exported values have separate validation verdicts.

Public compatibility choices must remain independently selectable. A future
named server preset may compose them only when explicitly requested, record
all effective choices and preserve supported caller overrides. Overriding a
certified recipe produces a custom model, not an automatic equivalence claim.
A single implicit castp mode must not silently select radii, omit atoms and
change measurement/export conventions together.

Provenance must record the effective selection/record policy, retained atom
IDs, radius profile and overrides, probe, region/mouth conventions, export
rule/version and actual producer identity. Preserve source input/model hashes
and raw values so a saved compatibility view can be traced to its calculation.
Missing molecular context must stay unknown rather than being reconstructed
from an analyze result that only received arrays.

## Required equivalence recipe

The public documentation will publish a runnable recipe containing:

1. Pinned reference server outputs, supported input scope, preparation rules
   and source atom-ID mapping. Specify the server route being reproduced.
2. Explicit selection and HETATM policy, hydrogen treatment, radius assignment
   and any validated atom-typing/masking conventions. Do not use pocket labels
   to choose atoms or fit radii.
3. Probe and region/mouth conventions, supplied through supported public
   functions and arguments rather than private developer preparation helpers.
4. Field-specific compatibility export choices and units, with the unrounded
   native result available alongside the exported view.
5. Independent benchmark evidence, reproducible comparison commands, expected
   outcomes and the precisely scoped equivalence guarantee.

The recipe promises equivalence only after every declared validation gate
passes for its stated scope. Exact region/mouth identities and multiplicities
must be established before comparing quantities. Printed-output equality and
raw numerical agreement are separate obligations; neither implies identical
hidden server floating-point intermediates or byte-identical ZIP archives.
Incomplete/missing outputs and original failures remain in the denominator.
Do not enlarge tolerances, fit geometric epsilons or introduce molecule-specific
rounding/input rules to label a recipe successful.

The current numerical part of a candidate recipe already uses explicit radii,
pocket_definition='castp3' and mouth_measurement_policy='castp3'. Its developer
benchmark excludes HETATM before parsing, uses castp3_protor and a 1.4 angstrom
probe. This is a reproducible partial validation route, not the delivered
public molecular recipe or a complete guarantee.

## Present evidence and next work

The [server-equivalence checkpoint](server_equivalence.md) retains all 89
archived inputs, 3,729 exact region memberships, 14,911/14,916 passing region
quantities and 26,103 matching aggregate descriptors. Five region scalar
discrepancies remain; complete_server_equivalence stays false. Individual
mouth geometry and whole-corpus contribution/orthosphere qualification are
also incomplete.

The [input/export controls](input_export_controls_2026_10_03.md) support an
intermediate rounding hypothesis for 104/105 strict atom discrepancies in
1MRG, but do not recover or fully reproduce the modern export process.
That hypothesis is not yet a public castp3 export policy. Independently chosen
systems must test it before implementation or certification.

Continue scientific diagnosis with native and compatibility verdicts side by
side. Then implement only independently justified controls at their owning
public boundaries, with failing-first tests, effective-choice provenance and
an end-to-end recipe regression. Preserve both preparation/model outcomes
for 1HIV and the other incorporated-HETATM cases. Native modeling improvements
do not close a compatibility failure; compatibility success does not establish
native physical superiority. Rust/GPU and unrelated improvements remain
deferred, and TopoMT CASTp code remains retained.


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
