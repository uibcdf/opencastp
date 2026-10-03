# Concrete comparison evidence — 2026-10-03

Owner: uibcdf/opencastp#6 for validation, and #2 for publication rationale.
The maintained user-facing [problem register](../docs/problems_and_model_control.md)
separates demonstrated input control, executed defects and pending science.
No third-party numerical source or original server ZIP is redistributed here.

## Current public form inspection

artifacts/server_form_inspection_2026_10_03.json pins the retrieved CASTp3 HTML
and deployed CASTpFold bundle by SHA-256, URL and byte count. Both submissions
contain file, probe and email; the probe bounds are 0–10 angstroms. Neither
exposes a per-atom radius input or active HETATM control. CASTpFold's hetatm
mentions only display the server reply. The pinned frontend source has the
historical checkbox and appended field commented out.

These were read-only inspections, not submitted jobs or backend probes.
No result demonstrates that undocumented parameters or HETATM-to-ATOM
rewriting produce a chemically equivalent model. CASTp3 was read from its
published HTTP URL; HTTPS did not connect. Availability is not an algorithm
comparison. Raw third-party HTML/bundles remain local rather than being copied
into this repository.

## Executed pyCASTa preparation

artifacts/pycasta_preparation_2026_10_03.json and its .py.txt collector pin
upstream f3418f38cd3d3c11e6cdd8c13b11431cc5b91894 and the executed loader,
elemental table and configuration hashes. The original archived PDB is passed
to the unchanged upstream load_and_separate_pdb and calculate_atomic_radii.
Incorporated heterogen IDs come from the independently retained molecular
inventory, not from inferred pocket overlap.

The 14/16/16/32 incorporated atoms of 1HIV/1QPE/3LCK/1G1F all enter the ligand
rather than protein table; the 1PTY negative control contains none. Including
water changes no protein membership. All oxygen radii are initially 1.52
angstroms. A temporary process-local elemental O dictionary override changes
all O and leaves every other element unchanged; the original value is restored.
No upstream file is edited. This is a preparation audit, not a full prediction.

## Executed pyCASTa index-space discrepancy

artifacts/pycasta_core_indices_2026_10_03.json and its collector retain source
hashes and completed 1STP/1HEW geometric-routine runs. The main run_analysis.py
cannot compile (IndentationError at line 457, following line 456). This is the
pinned source checkout, not a claim about separately distributed wheels.

The collector invokes unchanged upstream loading, triangulation, alpha and
pocket-detection functions. Only the temporary output location and debug/
write_steps settings change. A flow wrapper records the original return and
passes it through unchanged. The optional pocketlab dependency is absent, so
the upstream triangulator uses its implemented SciPy fallback.

| Input | Atoms | Tetrahedra | Flow groups | Valid groups rejected by atom-count bound | Tetrahedra in rejected groups | Returned final pockets |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1STP | 901 | 5718 | 574 | 478 | 1389 | 2 |
| 1HEW | 1001 | 6416 | 640 | 548 | 1523 | 1 |

The incorrect bound is len(protein_coords)-1 in detect_pockets, applied to
indices returned for tetrahedra. Every rejected group satisfies the actual
0 <= tetrahedron_id < len(simplices) bound. Their deletion precedes merging,
volume filtering and ranking. These intermediate groups are not proven pockets;
the table does not equate their number to missing CASTp features.

OpenCASTp's pinned direct-server panel matches all 9 1STP regions, 36 region
scalars and 63 additional descriptors, and all 7 1HEW regions, 28 scalars and
49 additional descriptors. Its distinct prediction objective is explicit.
This evidence does not certify pyCASTa field-by-field CASTp equivalence or a
universally better ligand-binding prediction.

## Expanded OpenCASTp corpus and refuted numerical diagnosis

The completed remaining-45 artifact is
artifacts/server_remaining_panel_2026_10_03.json. It preserves all 45 requested
cases, its runner and launch collector, input/prepared-array hashes, versions,
commit 51bed38, the unchanged numerical source hashes and every strict mismatch.
It matches 2569/2569 regions, 10271/10276 region scalars and 17983/17983
additional descriptors. Exactly 40/45 systems pass every audited field.
Together with the earlier disjoint 44 cases, cumulative coverage is 89 inputs,
3729 exact regions, 14911/14916 region scalars and 26103/26103 additional
aggregate descriptors. These are separately pinned runs, not a fresh single
89-input run or a four-interpreter molecular benchmark.

The five failing fields in 1MRG/1PSN/1YPI/1FBP/2FBP are listed in the public
register and retained in full precision. Their error exceeds the fixed
half-printed-quantum plus 1e-8 tolerance. No geometric epsilon, radius choice,
scalar correction or comparator tolerance was fitted to them.

artifacts/volume_rounding_diagnostic_2026_10_03.json and its collector test
original, +10/+100 angstrom and centered coordinate frames for the first three
failing regions, holding topology/radii fixed. All translations retain the
strict discrepancy. Observed variation is much smaller than the difference
needed to cross the print boundary. This refutes a simple coordinate-frame
remedy for these cases; it does not establish the underlying cause.

## Reproduction and durable evidence guards

Run the retained collectors as Python scripts in the recorded developer
environment. Their explicit local repository/archive paths must be adjusted
when reproducing elsewhere. They write to temporary folders, do not submit
server jobs and do not modify the upstream checkout. Full pocketlab/PyMOL
workflow qualification is not provided by these limited audits.

The remaining panel uses the committed comparison CLI with the exact requested
case list and arguments retained in its artifact. Its exit is 1 because five
fields fail; completed=true is not numerical success. Raw server archives stay
external. tests/test_comparison_evidence.py preserves denominators, disjoint
cohorts, every strict failure, the executed preparation/index evidence and
caller-controlled per-atom radii under both pocket definitions. Artifact guards
preserve historical executed states; they do not replace rerunning changed
numerical source or a new competitor revision.

## Local verification

54 tests pass with pytest-receptor, including the explicitly configured local
1STP/8RAT molecular guards and the new radius/evidence guards. One existing
developer Pint registry-cache warning is retained. Ruff lint/format, generated
indexes, diff whitespace and Sphinx with warnings-as-errors pass. A successful
source test suite does not change the remaining corpus comparator exit 1 or
its five recorded scalar failures. Hosted checks are separate evidence.

The optional type-check probe without external-import exclusions reports missing
PyUnitWizard and SciPy stubs in this environment. The bounded public-API check
uses mypy --ignore-missing-imports --follow-imports=silent on analysis.py,
result.py and exceptions.py; it does not qualify those external libraries.
The launch collector expects /tmp/opencastp_remaining_cases.json; reconstruct
that file from the retained remaining-panel requested_cases array before
replaying it. The comparison CLI and full argument list are also retained.
