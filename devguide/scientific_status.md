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
