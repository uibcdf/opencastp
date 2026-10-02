# opencastp contributor instructions

Read `MOLSYSSUITE_GUIDE.md` before making changes. It routes suite-wide policy,
compatibility, tooling and cross-component proposals to `uibcdf/molsyssuite` while this
repository remains authoritative for its implementation and product behavior.

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

Run these local gates before committing:

```bash
ruff check .
ruff format --check .
python -m pytest --receptor=llm
python devtools/devguide_index.py --check
```

Follow `devguide/reporting_protocol.md` for every durable bug or proposal record. Open
the owning GitHub issue first, regenerate indexes after lifecycle changes, and archive
resolved records instead of deleting them.

Before adding a required MolSysSuite sibling to `project.dependencies`, consult
`uibcdf/molsyssuite/devguide/ci_dependency_resolution.md` and replace the generated
pip-only CI lane with a verified dependency acquisition route.


## Scientific contracts

Read PYUNITWIZARD_GUIDE.md, PYTEST_RECEPTOR_GUIDE.md and
GH_RUN_RECEPTOR_GUIDE.md at their applicable boundaries. Numerical code lives
in OpenCASTp; molecular preparation and Topography/DFND adaptation belong to
consumers. Do not import TopoMT or MolSysMT into the numerical core.

Keep pocket definitions independent of radius selection. Preserve arbitrary
precision integer predicates until a replacement has equivalent guards.
Distinguish polyhedral measurements from SA/MS quantities. Do not claim a
backend, public package, server equivalence or archival state without evidence.

Consult devguide/architecture.md, devguide/scientific_status.md and
devguide/extraction_manifest.json before changing scientific behavior.
The initial coexistence is deliberate: do not remove CASTp from TopoMT during
this extraction. No deletion is authorized by the OpenCASTp bootstrap.

Source provenance and public distribution qualification remain owned by
uibcdf/opencastp#2. Rust/GPU development requires independent correctness and
performance evidence rather than a language-only speedup claim.
