# Scientific status at extraction

Recorded 2026-10-02. This is an extraction of the Python reference, not a new
validation claim for every OpenCASTp API input.

TopoMT's completed forty-system archived-server investigation matches all
compared feature atom-set multisets in 39/40 inputs: pockets 533/534, closed
voids 388/388, channels 52/52, branched channels 17/17 and aggregated mouths
602/603. The remaining original-input case is 1HIV, with a diagnosed heterogen
preparation discrepancy. See uibcdf/topomt#88. The 1CDO numeric-grid defect was
resolved under uibcdf/topomt#89. Individual mouth triangulation and open-region
SA/MS measures are separate unclosed requirements.

Closed-void scalar validation in TopoMT covered 225 voids and 900 SA/MS values.
These results belong to the recorded TopoMT source/environment and corpus.
They do not automatically certify this extraction, all radii, arbitrary
high-precision inputs, every future version or a public release.

The independent engine retains nearest fixed-point integers at five decimal
places, arbitrary-precision determinant/rank arithmetic, weighted geometry and
separate `literature` / empirical `castp3` definitions. Modern compatibility
was inferred from archived outputs; no server source was recovered and no
server algorithm defect is established.

## Independently executed extraction evidence

On 2026-10-02, the extracted package passed 26 local tests using
`python -m pytest --receptor=llm` in Python 3.13. The tests cover explicit
units and unchanged application policy, input validation, source atom mapping,
caller mutation isolation, completed-empty output, a synthetic closed void,
weighted-center geometry, mouth area/perimeter, definition-specific flow and
arbitrary-precision rank/predicate behavior. A coplanar four-point input first
failed its rejection test and is now rejected on the same fixed-point grid.

The reproducible developer audit was executed as:

```bash
PYTHONPATH=src python devtools/compare_topomt_reference.py \
  --topomt-root /home/diego/repos@uibcdf/topomt \
  --output devguide/artifacts/extraction_parity_2026_10_02.json
```

| Case | Atoms | Pockets | Closed voids | Channels | Branched channels | SA/MS scalars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1STP | 901 | 5 | 3 | 1 | 0 | 12 |
| 1CDO | 5606 | 36 | 43 | 3 | 3 | 172 |

Both cases match the retained TopoMT reference for all 94 region memberships,
aggregated and individual mouth atom sets, mesh vertex IDs and exact filtration
rank arrays. All 184 closed-void SA/MS scalars match at `rtol=1e-10` and
`atol=1e-8`. Each side independently rebuilds geometry from the same prepared
spheres. This verifies extraction parity; it is not a new comparison with a
live server or the entire forty-system archive.

The artifact records source commit, input/archive/prepared-array hashes, timings
and producer versions. Molecular preparation used the current development
MolSysMT `0.22.4+118.g03b318549.dirty`; this state is disclosed rather than
represented as a clean released dependency. Runtime NumPy was 2.4.6, SciPy
1.18.0 and PyUnitWizard 0.25.0+7.g00d756c.

Ruff checks, bounded public-API mypy checks and `sphinx-build -W -b html`
passed. A wheel built with `pip wheel --no-deps --no-build-isolation` was
installed non-editably in a temporary venv. Running its installed-package
validator with `python -I` passed and confirmed that neither TopoMT nor
MolSysMT was imported. The venv borrowed scientific dependencies from the local
development environment: this is installed-artifact evidence, not public
channel or clean dependency-closure qualification. Hosted supported-minor
verification is a separate gate.

## Required follow-up evidence

Verify input validation, units, mapping, completed-empty results, no TopoMT or
MolSysMT runtime imports, known synthetic geometry and exact-integer precision.
Compare prepared molecular arrays and region/mouth membership with the retained
TopoMT reference. Record actual commands and producer versions before claiming
extraction parity. Source hashes are in extraction_manifest.json.

No server archives are redistributed here before the data/provenance review.
Molecular preparation and castp3_protor radius assignment remain caller-owned;
the initial standalone API requires explicit radii and does not resolve 1HIV
preparation or unobserved terminal labels automatically.

## Hosted compatibility checkpoint — 2026-10-02

Source 762db29693f030ac61baa423de0371993ad6a454 passed routine CI
37058866994 and full four-minor Linux matrix 37058887654. Actual Python
3.11.16, 3.12.14, 3.13.15 and 3.14.7 each passed non-editable installation,
the isolated installed numerical validator and 26 unfiltered tests. Native
step/runtime evidence is artifacts/hosted_python_matrix_2026_10_02.json.
These lanes used public Conda dependencies and built OpenCASTp from source;
they do not establish a publicly published OpenCASTp package. The 1STP/1CDO
molecular extraction audit above was executed in the recorded Python 3.13
development environment and is not represented as a new four-minor corpus run.

The official repository starter was re-generated from current MolSysSuite
source 362d440, then extended with the retained numerical extraction and
component-specific scientific instructions. Canonical guides were synchronized
from verified current remote source snapshots. Scoped developer instructions,
report lifecycle and CI/coverage inventory follow the current starter; the
published policy membership defect is tracked separately in central #73.

## Direct server region checkpoint — 2026-10-02

The later [direct-server checkpoint](server_equivalence.md) measures the
independent OpenCASTp engine over the original forty-system panel: 39/40
cases, 990/991 region memberships and 3960/3964 region SA/MS values. A separate
explicit ATOM-record preparation of 1HIV matches its 17 regions and 68 values.
Analytical fields now cover open as well as closed regions; the initial
closed-only description above remains historical extraction evidence.
Individual mouth measures and other exported descriptors remain unqualified.
Complete measured equivalence is the sole current scientific priority under
#6; other improvements are deferred. No complete server equivalence is claimed.

## Extended direct-server checkpoint — 2026-10-02

The fresh benchmark-wide ATOM preparation matches 40/40 systems, 991 region
memberships and 3964 region SA/MS values. Analytical aggregate mouth fields
under the explicit unsigned castp3 convention match 2412 values across 603
open regions; intersection length, corners and mouth-triangle counts also
match. The signed precursor's 23/40 full-descriptor result remains separately
recorded. No epsilon, radius fit or molecule-specific correction is introduced.

Paired 3LCK/1QPE/1G1F phosphotyrosine examples and a 1PTY free-ligand control
add four fully matching ATOM cases. Retained HETATM preparations mismatch the
three incorporated-residue examples; 1G1F produces extra regions. The complete
inventory now covers 44 distinct ATOM systems, 1160 exact region memberships,
4640 region values and 8120 additional descriptors. This does not qualify all
89 archives, individual mouth geometry, contributions or orthospheres.

See server_equivalence.md and its pinned artifacts for executed source hashes,
preparation alternatives, printed precision and open gates. OpenCASTp #6 is
the sole active scientific priority; acceleration and unrelated improvements
remain deferred. The numerical API retains arbitrary explicitly supplied
spheres, and molecular-file ingestion is not yet a public frontend capability.

The final local source gate passes 49 tests with pytest-receptor, including
executed 1STP and 8RAT molecular guards (one pre-existing Pint cache warning
in developer preparation). Ruff, bounded public-API mypy and warning-free
Sphinx checks pass. A non-editable wheel with SHA-256
ad01d66169e14e3a83dedf5455c325e0dfd13a5c7f5506e8152e5b509b4b74e3
passes isolated installed void/pocket and analytical mouth smoke in Python
3.13.14, with neither TopoMT nor MolSysMT imported. Its temporary environment
borrows scientific dependencies and is not a public package qualification.
Hosted verification of the changed source remains a separate gate.

## Hosted verification of the equivalence checkpoint

Scientific source a0502899e61b4a6d5cc2232f951bea45ccf43d98 passes routine CI
37075626152, the bounded admission source-policy check 37075626661 and full
four-minor Linux matrix 37075626305. GH Run Receptor reports GitHub success.
Native logs verify Python 3.11.16, 3.12.14, 3.13.15 and 3.14.7. Each minor
passes non-editable installation, isolated installed void/pocket/mouth
validation and 47 source tests; two explicit local-archive molecular guards
skip visibly in hosted environments. Both guards passed in the 49-test local
run. This is not a four-minor rerun of the 44-system molecular benchmark.
The sanitized native job/step and runtime facts are retained in
artifacts/hosted_equivalence_python_matrix_2026_10_02.json. The published-policy
caller remains separately disabled under the existing central #73 bootstrap
exception; source-check success is not published policy adoption.

## Expanded archived-server checkpoint — 2026-10-03

The remaining 45 archived inputs were independently calculated with the declared
ATOM preparation: all 2569 region memberships and 17983 aggregate descriptors
match; 10271/10276 region scalars pass. Five fields in 1MRG, 1PSN, 1YPI, 1FBP
and 2FBP lie just outside the fixed printed-precision comparison. Their cause
is open, and the completed run exits 1. Together with the earlier disjoint
44 cases, cumulative coverage is 89 inputs, 3729 exact regions, 14911/14916
region scalars and 26103/26103 additional descriptors; 84/89 systems pass every
audited field. These are separately pinned runs, not new four-minor corpus
evidence. Source geometry and comparator tolerances were not changed.

See server_equivalence.md and comparison_evidence_2026_10_03.md for full
artifacts, strict failures, refuted frame-remedy diagnostics, competitor source
observations and implemented model-control boundaries. Individual mouth
geometry, per-atom contributions and exported orthospheres remain open under
#6. No complete equivalence or publicly qualified distribution is claimed.

## Historical metric controls — 2026-10-03

Compiled unchanged 1996 metric.c primitives, accurate summation and 40/80-digit
re-evaluation all retain the five strict scalar failures on frozen modern
integration domains. The selected compiled C quantities differ from current
Python quantities by less than 7e-11, with zero runtime metric corrections.
The 247 exported orthospheres in these five regions match distinct supporting
tetrahedra at printed precision. This constrains those domains; it does not
qualify every exported orthosphere or execute the whole historical pipeline.
Source geometry, radius choices and comparison tolerances remain unchanged.
See [diagnostic evidence and replay](metric_controls_2026_10_03.md). Modern
input, measurement and export conventions remain open; no modern-server bug
or complete equivalence is established. The 84/89 corpus verdict is unchanged.

Local diagnostic verification passes 56 tests with pytest-receptor, including
the explicitly configured 1STP/8RAT molecular guards and two new evidence
guards. Ruff lint/format, generated-index and warning-free Sphinx checks pass.
One pre-existing developer Pint cache warning remains visible. These passing
engineering checks do not change the five strict scalar failures.


## Input and contribution export controls — 2026-10-03

The new [bounded diagnostic](input_export_controls_2026_10_03.md) separately audits 1MRG's 3,864 SA
space-filling atom contributions: 3,759 strict matches. A four-decimal
intermediate export candidate reproduces 3,863 values, explaining 104/105
strict discrepancies, but the modern export source remains unknown. Historical
C primitives reproduce the unresolved atom 588. Uniform float32 coordinates
can fix its candidate export while worsening the full-atom comparison; none
of seven declared input conventions fixes all five region residuals.

The same-job live PDB/pocInfo files for three residual inputs match the archived
bytes; inspected raw contribution URLs return HTTP 200 HTML, not numerical
data. No new calculations or production numerical changes were made. Existing
region coverage remains 84/89 passing systems; per-atom and individual-mouth
qualification remains incomplete. Controls run in Python 3.14.7 with installed
editable OpenCASTp and TopoMT; previous 3.13 evidence keeps its original identity.
