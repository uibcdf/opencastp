---
summary: Adopt the MolSysSuite repository governance baseline during bootstrap
issue: uibcdf/opencastp#4
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: measured
area: [governance, packaging, documentation]
guard: tests/test_reporting_protocol.py
normative: AGENTS.md
blocked_by: []
supersedes: []
---

# Adopt the repository governance baseline

## Outcome

The incoming central handoff described the empty published snapshot at 163b27d.
Bootstrap at cd07d43 and current-starter reconciliation at c9a6f65 deliver the
independent package, canonical guide, root/scoped instructions, local report
queues/template/archive/validator, license/provenance notice, versioning,
Ruff, Conda profiles, documentation and installed gates. Existing scientific
source was preserved by extraction and manifest rather than arbitrary re-templating.
The current official starter source was central 362d440, with explicit admission
under uibcdf/molsyssuite#70. Python 3.14 was subsequently qualified under #5.

Current-source common conformance, generated indexes and local reporting tests
passed. The report guard protects the lifecycle/template/index contract; root
instructions define contributor routing, while the executed central checker
protects broader metadata, badge, guide and workflow conformance. No single
reporting test is claimed to validate every scientific or packaging boundary.

## Limits and owning work

Central #73 owns the frozen published-checker defect; the bounded pinned source
route is explicit. Source rights/public distribution remain #2; CI/coverage #3;
scientific extraction and future consumer migration #1. TopoMT remains intact.
The dated central audit/handoff is uibcdf/molsyssuite#72. Repository baseline
adoption does not close these independently owned qualifications.
