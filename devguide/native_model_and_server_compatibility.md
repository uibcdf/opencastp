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
