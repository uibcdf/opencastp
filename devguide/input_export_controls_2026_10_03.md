# Input materialization and export controls — 2026-10-03

Owner: uibcdf/opencastp#6. Complete server equivalence remains false.

## Result and scope

The five strict region discrepancies remain unresolved. Seven uniformly applied
input conventions, tested with both historical double metric primitives and a
deliberate float metric ablation, do not make all five regions pass. The float
ablation changes only Vol_real in a temporary header; it is not the unchanged
historical implementation or a recovered modern CASTp pipeline. Its wrapper
still assembles double-valued terms with math.fsum. All controls keep modern
integration domains and native visibility/orientation predicates fixed. No
production coordinate, radius, numerical method or comparator changed.

The declared input controls separately materialize coordinates, expanded radii
or both using a direct float32 conversion or the source-derived alf_get_coords
conversion: float32 scale 1e-5 times float32 fixed-point coordinates; the same
scale times the float32 square root of squared fixed-point radii. The unchanged
float64 input supplies a seventh baseline. The original reader was not run.

The additional per-atom audit is separate from the existing region gate. In
1MRG, all 1,932 prepared atoms map uniquely to original ATOM coordinates and
their serials exactly match the archived CHECKING contributor set. Its SA
columns describe space-filling contributions (Ac.sf/Vc.sf in historical
save_contributions), not an atom's contribution to one pocket. Native
inclusion/exclusion over alpha-complex simplices compares 3,864 quantities:
3,759 pass, with 7 area and 98 volume discrepancies. Area tolerance remains
0.00500001 angstrom squared and volume tolerance 0.00050001 angstrom cubed,
based on the exported two/three decimal columns, regardless of dropped zeros.

## Candidate export boundary, not a production correction

The original 1996 CHECKING export prints each quantity to four decimals. A
diagnostic first formats our value to four decimals and then applies NumPy
rounding to two area or three volume decimals. This reproduces 3,863/3,864
archived 1MRG quantities, explaining 104 of the 105 strict failures without
introducing another mismatch. The modern export source has not been recovered;
these observations do not establish that its rounding sequence is identical.

Atom serial 588 remains: native SA volume is 25.886550350920732 angstrom cubed,
the archived value is 25.886, and the candidate export gives 25.887. Applying
unchanged compiled historical C primitives to its same 66 terms gives
25.886550350999595, with zero runtime corrections/warnings. A transcription
error in these primitives does not account for this residual.

Direct float32 coordinates move that one value across the intermediate export
threshold, while its strict raw comparison still fails. Applying that same
convention to every 1MRG atom demonstrates why this isolated match is not a fix:

| Uniform input for unchanged compiled C primitives | Strict raw matches / 3,864 | Candidate export matches / 3,864 | Export mismatches introduced among raw passing values |
| --- | ---: | ---: | ---: |
| Original float64 arrays | 3,759 | 3,863 | 0 |
| Direct float32 coordinates; original expanded radii | 3,759 | 3,823 | 19 |
| Source-derived alf_get_coords coordinates and radii | 3,752 | 3,834 | 16 |

The seven atom-588 input variants and this three-convention full-atom panel
remain diagnostic evidence. No molecule-specific convention is selected.

## Same-job live export inspection

Read-only retrieval from the three original public job routes for 1MRG, 1PSN
and 1YPI returns PDB and pocInfo files byte-identical to the frozen archives.
pocInfo still supplies three-decimal region quantities. The inspected raw
.4.contrib routes return HTTP 200 with the same 713-byte HTML application
fallback, not usable contribution data. HTTP success alone is not evidence
that a numerical output exists. No new job was submitted, and no higher
precision metric source was recovered through these routes.

## Evidence and replay

[The retained report](artifacts/input_export_controls_2026_10_03.json) contains
all 105 native atom failures, the remaining candidate-export failure, all
three full-atom convention results, the five-region controls, live retrieval
hashes/timestamps and original/modified source hashes. Own collectors and the
own C bridge are retained as .py.txt/.c.txt snapshots; their hashes are guarded
in tests/test_comparison_evidence.py. Original C, headers, molecular archives,
coordinate snapshots and compiled libraries remain external.

These controls and local tests run in molsyssuite@uibcdf_3.14, actual Python
3.14.7. Both OpenCASTp and TopoMT are installed with pip --no-deps --editable
from their checkouts. Input snapshots were originally frozen in the preceding
Python 3.13 experiment; its 40/80-digit result was not rerun or relabeled.
The region input collectors explicitly import the recorded OpenCASTp source
checkout; the atom collectors use the installed editable package.

Replay first follows metric_controls_2026_10_03.md to regenerate the trusted
local snapshots and compile the external unchanged metric.c. Copy the new
retained collectors to their recorded /tmp names, adjusting developer paths
as necessary. Compile the own historical_sf bridge against that unchanged
metric object. Run the atom588_metric collector once to rebuild its private
geometry cache, then atom588_materialization and sf_materialization_panel.
Run atom_contribution_probe with argument 1mrg. The region input controls use
the preceding historical bridge; the float variant needs a temporary external
header changing only typedef double Vol_real to float and a separately rebuilt
metric/bridge shared object. fetch_raw_job_outputs performs only read-only GETs.
input_export_assemble validates the modified header and assembles the report.
Use the explicit 3.14 Conda prefix for every Python command. Collector exit zero
means collection completed, not equivalence passed.

Next: compare the contribution export pattern on independently chosen systems;
keep raw and candidate-export verdicts separate, and investigate modern input
or export conventions with independent evidence. Individual mouth geometry,
whole-corpus contributions and orthospheres remain open. The existing region
gate stays 84/89 passing systems and 14,911/14,916 passing region scalars.


## Local engineering verification

Python 3.14.7 passes all 59 tests with pytest-receptor, including the explicitly
configured 1STP/8RAT molecular guards and three failing-first evidence guards.
Ruff lint, format and generated-index checks pass. One pre-existing TopoMT
Pint cache warning remains visible. The 54 selected TopoMT CASTp/import/radius
and optional-dependency tests previously passed in this same environment after
updating its required DepDigest installation from 0.11 to 0.12.
Neither these local checks nor a routine hosted CI pass establishes a new
four-minor corpus run or changes the strict scientific failure verdicts.
