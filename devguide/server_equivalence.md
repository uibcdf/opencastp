# Direct archived-server equivalence checkpoint

Recorded 2026-10-02. Complete measured CASTp3/CASTpFold equivalence is the sole
current scientific priority under uibcdf/opencastp#6. Acceleration, unrelated
capabilities and consumer migration are deferred. TopoMT CASTp remains intact.

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
and new independently selected inputs have not been fully predicted here.
All reports retain complete_server_equivalence=false. Extend measured
coverage while preserving the present closed-void/open-region controls;
no finite panel alone establishes equivalence for arbitrary chemistry.
