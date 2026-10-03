# Concrete problems and model control

Evidence checkpoint: 2026-10-03. This is the problem-specific companion to the
[project rationale](project_rationale.md). It separates input restrictions,
measurement conventions, executed upstream defects and still-open OpenCASTp
comparisons. A different molecular model is not automatically a more accurate
prediction; agreement with the archived service is a separate question.

## Comparison register

| Problem or restriction | CASTp3/CASTpFold | pyCASTa checkout f3418f3 | OpenCASTp response and evidence |
| --- | --- | --- | --- |
| Incorporated protein/peptide residues labeled HETATM | The audited CASTpFold archive route omits them. Current public forms expose no inclusion control | Executed preparation puts all HETATM into the ligand table and takes only ATOM as protein | Supplied spheres are retained regardless of file labels. Paired 1HIV, 3LCK, 1QPE and 1G1F calculations include modified residues and produce changed regions |
| Choosing a ProtOr variant or changing selected atoms' radii | The forms accept a probe radius, but no per-atom radius array or editable type-radius table | The inspected loader assigns elemental radii from a mutable dictionary; changing O changes every O, not just ASP/GLU carboxylates | The caller supplies one positive radius per atom. It can use a published ProtOr assignment, a compatibility assignment or individual overrides without changing the pocket definition |
| Undeclared radius/measurement differences affecting reproducibility | Archived ASP/GLU oxygen behavior and negative mouth areas require explicit diagnosis | Elemental radii and tetrahedral-volume outputs are different modeling/measurement contracts | Radius assignment, pocket definition and signed/unsigned mouth policy are independent choices; polyhedral and SA/MS quantities are separately named |
| Valid tetrahedron groups rejected using the number of atoms as an index limit | Not observed in the server comparison | Reproduced in geometric routines for 1STP and 1HEW | Atom IDs and mesh IDs are separate. Both inputs match the archived regions and every currently audited aggregate descriptor |
| Main analysis module cannot compile | Not applicable | The pinned checkout has an IndentationError at run_analysis.py:457 | The numerical API is independently executable and tested; this is a version-specific upstream maintenance observation, not scientific novelty |

The pyCASTa observations concern the inspected and executed upstream source
commit [f3418f38cd3d3c11e6cdd8c13b11431cc5b91894](https://github.com/giorgioluciano/pycasta/tree/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894),
whose metadata reports 1.0.8. They do not establish that a separately built
PyPI/Conda artifact has identical source. Repairing these upstream defects would
not erase OpenCASTp's independent reconstruction and validation objective.

## HETATM: chemical membership and possible workarounds

The exact modified residues and paired calculations are retained in
[server comparisons](server_comparison.md). The executed upstream
[preparation routine](https://github.com/giorgioluciano/pycasta/blob/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894/src/pycasta/utils/preprocessing_utils.py)
excludes all 14 incorporated atoms of 1HIV, 16 each in 3LCK and 1QPE, and 32
in 1G1F from its protein geometry. They enter the non-water ligand table instead.
The include_water option does not change protein membership. Free PTR ligands
in 1PTY remain a separate control, rather than being automatically promoted to
protein because of their residue name.

The public [CASTp3 form](http://sts.bioe.uic.edu/castp/calculation.html) and
[CASTpFold form](https://cfold.bme.uic.edu/castpfold/compute) inspected on this date
submit file, probe and email. Neither exposes an HETATM-inclusion control or
per-atom radii. The CASTpFold bundle's mentions of hetatm display a reply field;
they are not an active submission option. This says nothing about undocumented
backend acceptance of manually invented fields.

Relabeling selected HETATM records as ATOM might bypass a record filter in a
server or in pyCASTa. It has not been qualified here as a correct workaround.
Chemical typing, atom identity and assigned radii must also be checked; renaming
modified residues to standard ones can change the model. Uploading a rewritten
file does not give the user control over the server's internal radius assignment.
There is no verified supported server remedy in this checkpoint.

OpenCASTp avoids that loader restriction because its array API uses exactly the
supplied sphere model. MolSysMT-based preparation can identify incorporated
residues chemically before supplying arrays. Their radius assignment remains
caller-owned; no built-in molecular reader or automatic typing is claimed.
Retained-HETATM calculations demonstrate inclusion and changed results, not an
independent physical ground truth for every modified residue or ligand.

## Editable radii and the meaning of ProtOr

The numerical engine does not hardcode ProtOr. The caller may provide any
supported positive per-atom radius assignment, including selected overrides:

```python
import numpy as np
from opencastp import analyze

radii = np.array(prepared_protor_radii, dtype=float, copy=True)
radii[carboxylate_oxygen_positions] = 1.42  # positions in the coordinate array
result = analyze(
    coordinates,
    radii,
    length_unit="angstrom",
    atom_indices=source_atom_ids,
    pocket_definition="castp3",
    mouth_measurement_policy="castp3",
)
```

This example assumes already prepared, aligned coordinate/radius/ID arrays;
it is not a direct molecular-file loader. Compatibility choices never silently
replace these radii. A numerical regression changes one sphere and observes the
expected decrease in its synthetic void volume under both pocket definitions.

The observed archived compatibility assignment uses 1.40 angstroms for the
named ASP/GLU carboxylate oxygens. The [published CASTpFold parameter page](https://cfold.bme.uic.edu/castpfold/infos/allabout/computation_settings.html)
lists O1H0 as 1.42 angstroms. This discrepancy does not prove that all oxygen
types use the same server radius or that the entire server table is recovered.
Neither profile is silently declared universal physical truth. Choose and record
the intended assignment; changing it can intentionally break server equivalence.

In pyCASTa's inspected [elemental table](https://github.com/giorgioluciano/pycasta/blob/f3418f38cd3d3c11e6cdd8c13b11431cc5b91894/src/pycasta/atomic_radii.py),
O has radius 1.52 angstroms. The executed dictionary override changes all oxygen
radii while leaving other elements unchanged. Programmers can replace the loader
or call lower-level routines with their own radii, but this is not an exposed
per-atom ProtOr option in the audited process_pdb workflow. Its optional weighted
triangulation path also does not by itself establish CASTp SA/MS equivalence.

## Which concrete molecular cases establish a difference?

- **1HIV, 3LCK, 1QPE and 1G1F:** OpenCASTp can calculate the explicitly retained
  modified-residue model. The archived service route and the executed pyCASTa
  loader omit those atoms from protein geometry. See the paired region counts
  and negative control in server_comparison.md.
- **1STP and 1HEW:** the executed pyCASTa geometric routines respectively reject
  478 of 574 and 548 of 640 flow groups because valid tetrahedron IDs exceed the
  atom-count bound. These are intermediate flow groups, not that many proven
  pockets. OpenCASTp matches all 9 and 7 archived regions, respectively, and all
  audited region/aggregate metrics. This does not mean that their different
  final pocket counts should otherwise be identical by definition.
- **8RAT, region 9:** the archived SA mouth area is negative (-0.573 square
  angstroms). The explicit compatibility convention reproduces it; the signed
  convention gives 0.886316783. OpenCASTp makes the choice available. This is
  not a proof that the signed model is universally correct or that the server's
  internals have been recovered.

The pyCASTa main module fails compilation before any molecular input is
processed. The geometric-routine audit was therefore separate from process_pdb;
no temporary repair of the upstream source was used. The environment lacked
pocketlab and used the module's existing SciPy fallback. Mathematical defaults
were retained; output location and diagnostic verbosity were changed explicitly.

## OpenCASTp's remaining discrepancies

The expanded comparison now covers all 89 archived inputs in separately pinned
cohorts. All 3729 region memberships and 26103 additional aggregate descriptors
match. Of 14916 region SA/MS scalars, 14911 pass the strict printed-precision
comparator. Five fields remain outside its unchanged tolerance, so only 84/89
systems pass every audited field:

| Input and region | Field | Archived value | OpenCASTp value |
| --- | --- | ---: | ---: |
| 1MRG 22 | SA volume, cubic angstroms | 0.004 | 0.003499637807 |
| 1PSN 13 | SA volume, cubic angstroms | 0.686 | 0.685499493478 |
| 1YPI 6 | SA volume, cubic angstroms | 18.094 | 18.094500169313 |
| 1FBP 3 | SA area, square angstroms | 299.277 | 299.276495443797 |
| 2FBP 11 | SA volume, cubic angstroms | 36.266 | 36.266501733337 |

They lie close to rounding boundaries; their cause is not established. They are
not evidence of corrected server bugs. Translation diagnostics for the first
three retain the discrepancy and do not justify a frame-dependent correction.
Individual mouth geometry, per-atom contributions and exported orthospheres
also remain open. Complete equivalence remains false under
[issue #6](https://github.com/uibcdf/opencastp/issues/6).

Executed source hashes, full case inventories, original failures and collector
snapshots are retained in the developer
[server-equivalence checkpoint](https://github.com/uibcdf/opencastp/blob/main/devguide/server_equivalence.md).
