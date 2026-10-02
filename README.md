# OpenCASTp

[![MolSysSuite: Support Library](https://img.shields.io/badge/MolSysSuite-support%20library-2563eb?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#support-library)
[![MolSysSuite policy](https://github.com/uibcdf/opencastp/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/opencastp/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/opencastp)](https://github.com/uibcdf/opencastp/blob/main/LICENSE)

OpenCASTp is an incubating auxiliary MolSysSuite library for local analysis of
molecular cavities and openings using an explicit CASTp reconstruction.
It is independent of TopoMT, Topography and DFND. It does not contact a server.

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
`polyhedral_volume` describe triangulation geometry. Closed voids additionally
expose solvent-accessible and molecular-surface areas and volumes. Open-region
analytical SA/MS measures remain pending. Mouth faces use local mesh indices;
reported atom IDs use the supplied source mapping.

`pocket_definition='literature'` is the published maximum-depth definition.
`pocket_definition='castp3'` selects an empirical modern-server compatibility
reconstruction; it does not silently replace the caller's radii.
Complete CASTp3/CASTpFold equivalence is not established. Rust, multithreading
and GPU are planned; the only implemented backend is `python`.

## Development

Use Python 3.13 for routine development. The inherited compatibility target is
Python 3.11, 3.12 and 3.13. Initial platform and installed-package qualification
remain pending; no public release or stable API is claimed.

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
