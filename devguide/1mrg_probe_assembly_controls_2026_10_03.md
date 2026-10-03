# 1MRG probe boundaries and historical regional assembly — 2026-10-03

Owner: [OpenCASTp #6](https://github.com/uibcdf/opencastp/issues/6), still open.
The original 89-input corpus remains at 3729 exact regions, 14911/14916
regional SA/MS scalars and 26103/26103 additional aggregate descriptors.
These diagnostics do not establish complete equivalence or a server defect.

## Five completed live probe controls

Five new CASTpFold jobs use the exact same ATOM/TER/END-only 1MRG PDB as the
[previous translation controls](1mrg_geometric_server_controls_2026_10_03.md).
Its SHA-256 is retained. Probe values and conditional predictions were recorded
before submission. Final comparisons rebuild geometry and filtration through
public `analyze`, using frozen prepared coordinates, explicit unexpanded radii,
original atom IDs, angstrom units and the castp3 region/mouth conventions.
Preparation remains shared; exported geometry is compared at display precision.

| Probe (angstroms) | CASTpFold job | Native void-22 SA volume (cubic angstroms) | Server volume | Raw scalar matches |
| --- | --- | ---: | ---: | ---: |
| 1.3999 | j_6ac15ba892fe8 | 0.0035196183333613407 | 0.004 | 116/116 |
| 1.4001 | j_6ac15ba94bafa | 0.0034797282494416493 | 0.003 | 116/116 |
| 1.4003 | j_6ac15ba9eb729 | 0.003440121565229881 | 0.003 | 116/116 |
| 1.399999 | j_6ac15fdfe6f5b | 0.0034998372609419404 | 0.004 | 115/116 |
| 1.400001 | j_6ac15fe08c966 | 0.003499438358244511 | 0.003 | 116/116 |

Every job matches all 29 region atom memberships, all 203 additional descriptors
and all 365 exported orthospheres. Totals across these five parameter controls
are 145 region comparisons, 579/580 regional scalars, 1015/1015 additional
descriptors and 1825/1825 orthospheres. These are five parameter replicates of
one existing molecular system, not five new benchmark systems. No new CASTp3
job was submitted. Three earlier nominal-probe jobs continue to print 0.004.

### Archive identity correction

The initial private runner used a four-decimal probe value in ZIP filenames.
Both fine probes therefore mapped to `probe_1.4000.zip`; the second overwrote
the first. The initial fine comparison was invalid, including its apparent
geometry discrepancies and the conclusion that both server volumes were 0.003.
It is superseded, not scientific evidence of server nonmonotonicity.

Recovery fetched each already completed job without submitting another job.
Both recovered SHA-256 values exactly match their separately recorded original
download receipts. They are now saved by unique job IDs. The final collector
rejects any receipt mismatch or numerical payload whose filename belongs to
another job, allowing the shared README. Both cohorts were recalculated with
those checks. The historical submission-runner snapshot retains the executed
code, including this known filename defect; do not reuse its `poll` for fine
probes. Use job-ID filenames and receipt verification for further collection.

## What the probe sequence says about rounding

The coarser 1.4001 control rejects the previous four-decimal intermediate rule
for this volume: that rule predicts 0.004, while the server returns 0.003.
The finer pair brackets a different transition. Five-decimal intermediate
formatting predicts 0.004 for both fine probes and fails the upper one.
Six-decimal intermediate formatting followed by three-decimal formatting
reproduces all 580 printed scalar fields in the five new controls.

This supports a **conditional local six-decimal hypothesis**. It does not locate
the precision loss, prove that server inputs equal our inputs exactly, or show
that the server simply rounds its final cavity total twice. Input materialization,
intermediate geometry and metric assembly remain possible coupled explanations.

Uniform replay on all 14916 retained original regional values gives:

| Python formatting rule | Printed matches | Original raw failures explained | Failures introduced on originally passing values |
| --- | ---: | ---: | ---: |
| Direct nearest, three decimals | 14910/14916 | 0 | 1 |
| Five decimals, then three | 14835/14916 | 1 | 77 |
| Six decimals, then three | 14903/14916 | 1 | 9 |
| Seven decimals, then three | 14910/14916 | 0 | 1 |
| Historical `%e` with seven significant digits, then three | 14806/14916 | 0 | 105 |

This is formatting replay, not a fresh 89-system calculation. Intermediate
strings are parsed as floats before the final Python nearest formatting; this
differs from the previously retained NumPy four-decimal replay. The direct
formatting failure on 1OKM is already documented and remains distinct from
the five original raw comparison failures. Fixed `atol=0.00050001`, `rtol=0`
is unchanged. The six-decimal candidate fixes the nominal 1MRG void but leaves
four original residuals and creates nine failures. It is unqualified as a
uniform public export policy. No field-specific or molecule-specific remedy
has been introduced.

## Original C regional assembly and reader materialization

The earlier historical control executed unchanged metric primitives. This
slice additionally compiles unchanged `do_tetra_vertex`, `do_tetra_edge` and
`do_tetra_triangle` bodies from original `volbl.c`, together with original
`metric.c`. Own glue supplies inputs, initializes region totals, dispatches
native complex membership and provides shared native visibility/orientation
callbacks. This executes original regional corrections on frozen native domains;
it does **not** execute the full historical reader, triangulation or traversal.
The 1996 code remains an algorithmic reference, not recovered modern source.

Across 1STP, 8RAT and the five residual systems, 384 regions retain exactly the
same five SA/MS failures: 1531/1536 scalars. All 768 intersection-length/corner
values pass. The maximum scalar difference from native Python is below 8e-9;
historical runtime correction and warning counts are zero. Original C source
and private compiled binaries are not redistributed. The own build script,
compiler command, source hashes and binary fingerprint are recorded.

A separate source-derived control composes the old `lia_ffpload` floor-to-five-
decimal conversion with optional `Alf_coord` float32 materialization. It reuses
OpenCASTp's existing `castp1_fixed_point_array` helper with source preformatting
disabled. It is distinct from prior nearest-integer materialization controls.
Five declared variants share modern domains and predicates. None fixes all five
targets. Coordinate flooring repairs 1YPI and 2FBP in isolation; adding the
old float materialization retains only the 2FBP repair. These targeted results
do not qualify a whole reader or exclude a coupled upstream adjustment.

## Web output, evidence and next experiment

Read-only retrieval of the current frontend's `measure.json` for the three
previous translation jobs returns byte-identical 29-region data with keys
`area`, `atoms`, `id`, `vol`. Its void-22 volume is still 0.004; this schema
provides neither higher precision nor individual-mouth measurements.
Old bundled frontend examples use a different schema and are not an oracle for
the current jobs. No additional individual multi-mouth reference was obtained.

[Input-free evidence](artifacts/1mrg_probe_assembly_controls_2026_10_03.json)
retains Python 3.14.7, actual editable-package metadata, source commits, units,
private input/output hashes, completed jobs, summarized comparisons and ten
exact own-code collector snapshots. Full private comparison hashes are recorded;
large failure lists retain bounded examples explicitly marked incomplete.
To replay, restore the private paths named by the collectors; build original C
first, execute its comparison and reader controls, execute fresh comparisons
only after archive receipt verification, then run formatting replay and assembly.
No molecular coordinates, PDBs, server ZIPs, original C bodies or binaries are
published. Existing submission state prevents duplicate submissions.

Next, predeclare probes that straddle the predicted six-decimal transition and
distinguish it from probe-input quantization. Check the full exported geometry
and all fields, rather than just void 22. Then test source-motivated intermediate
precision or accumulation conventions jointly with export on the seven-system
panel, expanding any improvement to all 89 inputs before public adoption.
Use 1FBP's SA-area residual as a separate field control. Final formatting alone
is already insufficient; no adjustment should be accepted by selecting a
different rule for each failed molecule. Individual multi-mouth, full-corpus
geometry/contributions and the public native/compatibility recipe remain open.

Production numerical code, radii, native defaults and comparator tolerances
are unchanged. Attribution integration and optional-engine contracts have no
new boundary in this diagnostic slice; the existing TopoMT server client is
reused unchanged. Engineering tests do not certify scientific equivalence.


## Local engineering gates

All 97 tests pass with Pytest Receptor in `molsyssuite@uibcdf_3.14`
(Python 3.14.7), including the enabled local 1STP/8RAT molecular guards and
four new evidence guards. The new guards first failed because the evidence
record was absent, then passed with the completed verified record. One
pre-existing TopoMT Pint-registry-cache warning remains visible. Ruff lint and
format check, generated-index verification and Sphinx HTML with warnings
treated as errors pass. TopoMT's catalog-only change passes its two reporting
tests and index check; its numerical engine is unchanged. The existing hosted
push lane is a separate engineering gate and does not certify a new full
Python matrix or a four-minor molecular corpus calculation.


## Subsequent minimal counterexample

The [six completed minimal controls](minimal_server_controls_2026_10_03.md)
retain the discrepancy after reducing 1MRG to five atoms. A regular one-cell
void at nearly the same, slightly larger native volume prints 0.003, refuting
the six-decimal final-format candidate outside the preceding fixed-1MRG probe
controls. This rules out a common monotonic final exporter of current native
volumes; shared effective inputs and upstream-plus-export alternatives remain
unqualified. The original five corpus residuals stay open.
