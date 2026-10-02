# Molecular inputs and server comparisons

OpenCASTp's numerical API accepts coordinates and explicit atomic radii.
It calculates with the spheres supplied by the caller; it does not remove
modified residues, heterogens or hydrogens based on a file label. Atomic
selection and radii must describe the molecular model you intend to analyze.

## The HETATM limitation: 1HIV

In the archived CASTpFold comparison corpus, HETATM records do not appear
among contributing atoms. This observed limitation can omit atoms that belong to the protein,
including modified amino acids. The PDB record label and membership in the
protein are different concepts.

1HIV illustrates the consequence. It contains two CSO residues, which are
modified cysteines, with fourteen atoms recorded as HETATM. Protein/peptide
preparation includes them, but the archived server calculation omits them.
Including these atoms changes one pocket: sixteen of seventeen region atom
sets match. An explicit ATOM-record preparation reproduces all seventeen
regions and all sixty-eight region SA/MS values. The independent archive
study finds no contributing HETATM serials in eighty-nine inputs. A fresh
forty-case benchmark with the same ATOM-record policy reproduces all 991
region memberships and 3964 region SA/MS values.

For the validation benchmark we exclude HETATM before molecular preparation
to reproduce this observed server convention. For a user's scientific
calculation, keeping those atoms can be the appropriate physical model.
Choose the model explicitly: reproducing the server's omission is not a
requirement of the local numerical method. Evidence is bounded to the archived
corpus; arbitrary uploaded structures or other server routes may differ.

## Further protein and peptide examples

The archived collection also contains these HETATM residues. MolSysMT selects
all of them as part of a protein or peptide, and none of their atom serials
appears in the corresponding server contribution table.

| Structure | Incorporated residue | HETATM atoms in the archived input |
| --- | --- | ---: |
| [1HIV](https://www.rcsb.org/structure/1HIV) | CSO A67 and B67, modified cysteines | 14 |
| [3LCK](https://www.rcsb.org/structure/3LCK) | PTR A394, phosphorylated tyrosine within Lck | 16 |
| [1QPE](https://www.rcsb.org/structure/1QPE) | PTR A394, phosphorylated tyrosine within Lck | 16 |
| [1G1F](https://www.rcsb.org/structure/1G1F) | PTR B1162 and B1163 in the bound insulin-receptor peptide | 32 |

MODRES and peptide-bond LINK records support these incorporations; the RCSB
entries independently identify the modified protein/peptide residues. Paired calculations confirm the consequence on the supplied sphere model:

| Structure | Exact archived region memberships with HETATM retained | With HETATM excluded | Native region count, retained/excluded |
| --- | ---: | ---: | ---: |
| 1HIV | 16/17 | 17/17 | 17/17 |
| 3LCK | 41/42 | 42/42 | 42/42 |
| 1QPE | 45/46 | 46/46 | 46/46 |
| 1G1F | 41/42 | 42/42 | 48/42 |
| 1PTY, separate-ligand control | 39/39 | 39/39 | 39/39 |

All region and aggregate mouth/boundary measures compared in the four new
ATOM-record runs match at the server's printed precision. In 1G1F the effect
includes extra detected regions, not merely a changed lining atom set.
These are explicit preparation alternatives; we do not fit atom membership
to server labels. The data and preparation choices are retained in the
developer checkpoint.
[1PTY](https://www.rcsb.org/structure/1PTY) is a useful control: its two free
phosphotyrosine molecules are separate ligands. A modified amino-acid name
alone does not establish that a residue belongs to the protein.

## Input formats are independent of atom selection

The server route takes PDB files. The local numerical method has no PDB-only
restriction: coordinates and radii can come from supported MolSysMT forms,
including PDB, CIF/BinaryCIF and molecular objects. A molecular frontend can
use MolSysMT for reading, selection and conversion while preserving source
atom identity and physical units.

The current public `analyze` API takes arrays/quantities, not filenames.
Direct molecular-file ingestion is a separate frontend boundary; the
numerical core remains independent of MolSysMT. Changing formats must not
silently remove atoms or change radii to resemble a PDB-only server.

## What agreement currently means

Region comparisons require exact atom-set multisets, mouth count and aggregate
rim membership, followed by solvent-accessible and molecular-surface areas
and volumes at the precision printed by the server. Aggregate analytical
mouth measures and boundary descriptors match in the 44-case ATOM-prepared
panel using the explicit castp3 compatibility convention.
Individual mouth geometry and other exported descriptors remain under validation.
Complete server equivalence is not claimed. It is the sole current scientific
priority in [issue #6](https://github.com/uibcdf/opencastp/issues/6).

## Analytical mouth conventions

`mouth_measurement_policy='signed'` is the default local projection convention.
`mouth_measurement_policy='castp3'` reproduces the unsigned circular-segment
convention inferred from archived server measures. It is independent of
`pocket_definition` and the supplied atomic radii; all three choices are
explicit. The effective policy is retained in `result.execution`.

When the intersection circle projects beyond an atom center, replacing a
signed projection by its absolute value changes the sector angle and triangle
area. In 8RAT, the server reports -0.573 square angstroms for the aggregate
SA mouth area of region 9. The compatibility option deliberately preserves
that reported negative value; it is not silently clamped or presented as a
physical non-negative aperture. The signed option retains the oriented
projection. These reconstructed mouth models remain subject to validation;
this observation alone is not a recovered server implementation or a general
proof of its internals.

Existing `mouth['area']` and `mouth['perimeter']`, and parent `mouth_area` and
`mouth_perimeter`, retain their planar triangulation meanings. Analytical
SA/MS fields are separately named and carry units. The analytical perimeter
is a sum of molecular boundary arcs, not the triangle-edge wire length.
