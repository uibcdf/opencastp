# OpenCASTp

[![MolSysSuite: Support Library](https://img.shields.io/badge/MolSysSuite-support%20library-2563eb?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#support-library)
[![MolSysSuite policy](https://github.com/uibcdf/opencastp/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/opencastp/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/opencastp)](https://github.com/uibcdf/opencastp/blob/main/LICENSE)

OpenCASTp is an incubating auxiliary MolSysSuite library for local analysis of
molecular cavities and openings using an explicit CASTp reconstruction.
It is independent of TopoMT, Topography and DFND. It does not contact a server.

[Why OpenCASTp exists](docs/project_rationale.md) maintains the comparison with
CASTp3/CASTpFold and pyCASTa, implemented capabilities, measured limitations and
future candidates. Offline execution is shared with pyCASTa; current-version
numerical superiority and complete server equivalence are not claims.

## Current implementation

The Python reference engine accepts one coordinate array and explicit atomic
radii, builds weighted geometry and reports pockets, closed voids, channels,
branched channels and their mouths when detected. Caller atom IDs are retained.
The caller owns atom selection, chemistry, radii assignment and hydrogen policy.

```python
import numpy as np
from opencastp import analyze

points = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
result = analyze(points, np.full(4, 0.25), length_unit="angstrom")
assert result.features[0]["feature_type"] == "void"
```

Physical output values are PyUnitWizard quantities. `polyhedral_area` and
`polyhedral_volume` describe triangulation geometry. All detected regions
additionally expose solvent-accessible and molecular-surface areas and volumes.
Analytical SA/MS mouth areas and perimeters use an explicit measurement
convention, separately from planar mouth fields. Mouth faces use local mesh indices;
reported atom IDs use the supplied source mapping.

`pocket_definition='literature'` is the published maximum-depth definition.
`pocket_definition='castp3'` selects an empirical modern-server compatibility
reconstruction; it does not silently replace the caller's radii.
`mouth_measurement_policy='signed'` retains signed segment projections;
`mouth_measurement_policy='castp3'` selects the reconstructed unsigned
archived-server mouth convention, including its observed negative areas.
The effective policy is recorded and does not change region detection.
Complete CASTp3/CASTpFold equivalence is not established. Rust, multithreading
and GPU are planned; the only implemented backend is `python`.

Complete measured server equivalence is the sole current scientific priority
under [issue #6](https://github.com/uibcdf/opencastp/issues/6). All other
improvements are deferred. The fresh forty-system direct-server region audit matches
all 991 regions and 3964 region SA/MS values with the declared benchmark-wide
ATOM-record preparation policy. The original 39/40 diagnosis remains retained. See [the region checkpoint](devguide/server_equivalence.md) for exact
counts, input boundaries and the unqualified individual mouth geometry.
Three further incorporated-phosphotyrosine examples and a free-ligand control
bring the fully matching ATOM-record panel to 44 distinct systems.
The [concrete problem register](docs/problems_and_model_control.md) records
HETATM handling, per-atom radius control and executed pyCASTa index defects.
The later remaining-45 comparison brings cumulative coverage to all 89
archives: all 3729 regions and 26103 aggregate descriptors match, while five
region scalars remain outside the unchanged printed-precision tolerance.
Thus 84/89 systems pass every audited field; complete equivalence remains open.
The archived server route omits HETATM records, including modified protein
residues in 1HIV. The benchmark reproduces that input convention explicitly;
users retain control over their molecular model. See
[molecular inputs and server comparisons](docs/server_comparison.md).

## Development

Use Python 3.13 for routine development. The inherited compatibility target is
Python 3.11, 3.12, 3.13 and 3.14. The four-minor Linux matrix has passed,
including non-editable installed numerical checks. Broader platform and
public-channel dependency qualification remain pending; no public release
or stable API is claimed.

```bash
conda env create -n opencastp-dev -f devtools/conda-envs/development_env.yaml
conda activate opencastp-dev
python -m pip install --no-deps --editable .
python -m pytest --receptor=llm
ruff check .
ruff format --check .
python devtools/devguide_index.py --check
sphinx-build -W -b html docs /tmp/opencastp-docs
```

The official public installation route will be the `uibcdf` Conda channel with
third-party dependencies from `conda-forge`, after candidate verification and
publication. There is no published-package installation claim yet.

Coverage of the numerical library is applicable. A meaningful producer and
accepted uploaded report remain tracked in
[OpenCASTp #3](https://github.com/uibcdf/opencastp/issues/3); no percentage is
claimed before that evidence exists. CI and installed-artifact evidence are
separate from server compatibility.

## Governance and provenance

Read [AGENTS.md](AGENTS.md) and [MOLSYSSUITE_GUIDE.md](MOLSYSSUITE_GUIDE.md).
MOLI governs the platform boundary; MolSysSuite governs this member. Admission
is tracked in [MolSysSuite #70](https://github.com/uibcdf/molsyssuite/issues/70).

The engine was extracted from TopoMT with source hashes retained in
[the extraction manifest](devguide/extraction_manifest.json).
TopoMT's CASTp implementation is retained during this initial coexistence.
[Architecture](devguide/architecture.md) and
[scientific status](devguide/scientific_status.md) define current boundaries.
Consult [source provenance](THIRD_PARTY_NOTICES.md) before public distribution.

The policy workflow currently executes an explicit admission bootstrap pinned to
MolSysSuite commit `2707ef9389e0579ece75138b0b5c5e1fdb2a1a34`.
The published `policy-v1.5.2` caller is visibly disabled because its frozen
membership registry predates OpenCASTp. This bounded source-checker exception
expires on 2026-12-31 and is tracked in
[MolSysSuite #73](https://github.com/uibcdf/molsyssuite/issues/73) and
[OpenCASTp #3](https://github.com/uibcdf/opencastp/issues/3).
A successful bootstrap is separate from published policy adoption.
