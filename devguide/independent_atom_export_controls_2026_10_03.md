# Independent atom export controls — 2026-10-03

Owner: uibcdf/opencastp#6. This extends the 1MRG diagnostic without changing
native calculations, public policies or comparison tolerances.

Two independently chosen, previously region-qualified systems test the same
export hypothesis: format a calculated SA space-filling atom contribution to
four decimals, then NumPy-round to two area or three volume decimals. These
are CHECKING contribution fields, not individual pocket contributions. PDB
HETATM records are excluded before protein/peptide preparation with the
castp3_protor model and a 1.4 angstrom probe; source serials and prepared
coordinates map uniquely to every archived contributor. OpenCASTp independently
rebuilds numerical geometry from prepared arrays.

| System | Atoms | SA values | Strict raw matches | Candidate export matches | Strict failures explained | New export failures among raw passing values |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1STP | 901 | 1,802 | 1,755 | 1,802 | 47 | 0 |
| 8RAT | 950 | 1,900 | 1,865 | 1,899 | 35 | 1 |

All 47 native discrepancies in 1STP and all 35 in 8RAT match the hypothesis.
However, 8RAT atom 429 introduces a new export mismatch: calculated SA volume
11.039450149385319 angstrom cubed passes the raw comparison with archived
11.039 at tolerance 0.00050001. Intermediate four-decimal formatting gives
11.0395 and the candidate final export gives 11.040. The new mismatch cannot
be removed from the report because the original raw value passed.

Together with the [previous 1MRG control](input_export_controls_2026_10_03.md),
the same candidate matches 7,564/7,566 SA atom values over three systems.
It explains 186/187 strict raw failures and introduces one different failure;
1MRG atom 588 remains unresolved. These counts are separate from the region
gate and do not qualify MS contributions, every corpus input or individual
mouth geometry. Complete server equivalence remains false.

The evidence supports investigating an intermediate export boundary, but
does not establish the server's exact rounding/input process or justify a
public castp3 export policy. This independently reproduces why the accepted
[native model and compatibility contract](native_model_and_server_compatibility.md)
keeps full calculated values and a distinct, validated export representation.
Continue seeking one independently justified convention rather than selecting
rounding or input rules separately for each failing atom or molecule.

[Retained evidence](artifacts/independent_atom_export_controls_2026_10_03.json)
includes all 82 strict raw failures in the new two-system panel, the new export
failure, archive/PDB/CSV/prepared-array hashes, numerical source hashes,
producer versions and the own collector snapshots. Inputs and molecular
archives remain external; no PDB, coordinate pickle or upstream source is
redistributed. tests/test_comparison_evidence.py guards both raw and exported
verdicts, introduced failure identity and collector integrity.

Replay copies the retained .py.txt collectors to their /tmp names, adjusts
developer paths, runs prepare_contribution_controls with the explicit
molsyssuite@uibcdf_3.14 prefix, then atom_export_independent with arguments
1stp 8rat and independent_export_assemble. The preparation helper generates
trusted local coordinate/radius snapshots; the numerical collector uses the
installed editable OpenCASTp. Actual producer Python is 3.14.7. Collection
success is not a server-equivalence verdict, and a full four-minor molecular
rerun is not claimed.
