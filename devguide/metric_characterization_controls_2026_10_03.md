# Cavity and atom characterization controls — 2026-10-03

Owner: uibcdf/opencastp#6. Native numerical production source and the existing
comparison tolerances are unchanged. These controls do not establish complete
CASTp3/CASTpFold equivalence or deliver a public export policy.

## Four-field atom contribution audit

The archived CHECKING CSV describes the space-filling union, not an individual
cavity. Previous bounded controls checked its SA fields. This control also
assembles MS areas and volumes using the native primitives and the inspected
historical CHECKING partition: endpoint torus volume modification terms are
included, and solvent patch contributions are split equally among three atoms.
Those torus modifications cancel globally. The assembled four atom totals
agree with the existing native space-filling totals within 4.24e-9 in their
respective units. The historical full reader/triangulation pipeline was not run.
No modern contribution-export source was recovered.

All three preparations exclude HETATM, select protein/peptide atoms, use the
explicit castp3_protor profile and a 1.4 angstrom probe; the archive states no
cusp correction. OpenCASTp rebuilds geometry from trusted frozen sphere inputs.
Actual calculations run in Python 3.14.7. The preceding preparation identity
remains in its original evidence; it is not relabeled as a fresh molecular parse.

The same candidate used previously formats an intermediate value to four
decimals, then applies NumPy rounding to two decimals for area and three for
volume. Quantum is fixed by field even when CSV trailing zeros are omitted.
Strict raw comparison and candidate-export equality remain separate verdicts.

| Input | Atoms | Strict raw SA matches | Candidate SA matches | Strict raw MS matches | Candidate MS matches |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1STP | 901 | 1755/1802 | 1802/1802 | 1746/1802 | 1802/1802 |
| 8RAT | 950 | 1865/1900 | 1899/1900 | 1857/1900 | 1900/1900 |
| 1MRG | 1932 | 3759/3864 | 3863/3864 | 3765/3864 | 3864/3864 |
| Total | 3783 | 7379/7566 | 7564/7566 | 7368/7566 | 7566/7566 |

All 198 strict MS discrepancies match this candidate in the three-system scope.
This supports the atom-export hypothesis but does not certify arbitrary inputs
or justify rounding cavity totals. The two SA candidate failures are retained:
1MRG atom 588 still fails, and 8RAT atom 429 is a newly introduced export failure
whose raw comparison passes. Across all four fields the candidate matches
15130/15132 quantities; native strict comparisons match 14747/15132.

## The same export rule fails for cavity totals

A separate replay uses all 14916 stored region SA/MS scalar comparisons across
89 inputs and 3729 regions. This is a transformation of pinned earlier evidence,
not a fresh rerun of all molecular calculations. Their source hashes and original
runtime identity remain visible. Every region scalar retains atol=0.00050001,
rtol=0; the production comparator and its five failures remain unchanged.

| Operation on the recorded native value | Matching printed region quantities |
| --- | ---: |
| Existing strict raw comparison | 14911/14916 |
| Direct three-decimal formatted value | 14910/14916 |
| Four-decimal intermediate followed by NumPy three-decimal rounding | 14173/14916 |

The four-decimal intermediate explains four original strict failures but
introduces 742 failures among originally passing quantities. It is rejected
as a uniform cavity-export rule. Its success for most atom contributions must
not be generalized to pocInfo or aggregate mouthInfo fields. No alternative
molecule-specific correction, changed radii or enlarged tolerance is proposed.

The direct formatted-value comparison exposes another public-recipe obligation:
1OKM region 40 MS area is 8.39850000235757 versus printed 8.398. It passes the
existing half-quantum-plus-1e-8 arithmetic comparison, but direct formatting
gives 8.399. This is a printed-output mismatch, not a sixth strict raw failure.
Keep the two criteria explicit; numerical agreement alone does not guarantee
exact server strings. The four-decimal candidate happens to match this value,
which does not remedy its 742 other regressions.

## Complete orthosphere sets in seven systems

The new developer auditor pairs regions by exact feature class and atom-set
membership before comparing the complete exported bulb set with the supporting
native tetrahedra's orthospheres. Every x/y/z coordinate and radius uses the
fixed four-decimal tolerance 0.00005001 angstrom. A maximum bipartite matching
requires a bijection, preserving duplicate multiplicity and refusing to reuse
one native sphere. Nearest-center matching alone is insufficient when rounding
windows overlap. Negative powers/radii, nonfinite values, missing/extra spheres
and ambiguous region memberships cannot provide passing evidence.

| Input | Regions | Matched/exported orthospheres |
| --- | ---: | ---: |
| 1STP | 9 | 119/119 |
| 8RAT | 12 | 198/198 |
| 1MRG | 29 | 365/365 |
| 1PSN | 41 | 733/733 |
| 1YPI | 75 | 1026/1026 |
| 1FBP | 98 | 1606/1606 |
| 2FBP | 120 | 1621/1621 |
| Total | 384 | 5668/5668 |

This extends the earlier 247-sphere five-residual-region check to every region
in seven systems, including all five residual systems. It supports the geometric
domains at exported precision; it does not recover exact unrounded server
geometry, prove tetrahedron connectivity in degenerate configurations or identify
individual mouths. This new control does not independently repeat the earlier
atom-contact/no-interior-atom check. Whole-corpus orthosphere, atom-contribution
and individual-mouth qualification remain incomplete.

## Evidence and replay

Evidence is artifacts/metric_characterization_controls_2026_10_03.json. It retains
every failed scalar verdict, source/input hashes, actual installed versions,
native-total conservation, original producer identities and own collector hashes.
No historical C/header/binary, molecular coordinate cache, PDB or server archive
is redistributed. Trusted developer pickle caches are never a public input format.

Recreate the private frozen sphere inputs with the preceding retained collectors
in metric_controls_2026_10_03.md and independent_atom_export_controls_2026_10_03.md.
Copy this checkpoint's own .py.txt collectors to their recorded /tmp paths; adjust
developer paths to local checkouts. Then run in the configured Python 3.14 environment:

```bash
python /tmp/opencastp_all_atom_metric_controls.py 1stp 8rat 1mrg
python /tmp/opencastp_prepare_residual_geometry_controls.py 1psn 1ypi 1fbp 2fbp
python /tmp/opencastp_region_export_inventory.py
python -m devtools.audit_castp_orthospheres \
  --archive-dir /path/to/topomt/topomt/data/CASTpFold_server \
  --geometry-cache-dir /tmp \
  --cases 1stp 8rat 1mrg 1psn 1ypi 1fbp 2fbp \
  --output /tmp/opencastp_orthosphere_seven_panel.json
python /tmp/opencastp_assemble_characterization.py
```

For exact historical replay use the pinned auditor snapshot, not an unexamined
later tool revision. Collection completion is separate from equivalence: the
atom collector exits normally with failed comparisons preserved; the geometry
auditor's passing exit qualifies only its declared geometric scope. Tests in
test_orthosphere_audit.py first failed for the absent auditor and now guard
precision, multiplicity, overlapping match windows and invalid data. The three
artifact guards first failed for absent evidence and preserve these bounded
verdicts and rejected hypotheses. Complete server equivalence remains false.

## Local engineering verification

The configured Python 3.14.7 environment passes 71 tests with pytest-receptor,
including the explicitly enabled 1STP/8RAT molecular guards. One pre-existing
TopoMT Pint-registry cache warning remains visible. Ruff lint/format, generated
report-index verification and Sphinx's warning-as-error HTML build pass.
Sphinx 9.1.0 and MyST Parser 5.1.0 were installed from the repository's declared
optional documentation requirements into the same Python 3.14 environment.
The passing engineering suite does not change the scientific failure verdicts.
Hosted evidence remains a separate source/commit-qualified gate.
