---
summary: Qualify source provenance, ecosystem boundaries and public distribution
issue: uibcdf/opencastp#2
status: active
opened: 2026-10-02
closed:
verification: inspected
area: [architecture, validation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualify source provenance, ecosystem boundaries and public distribution

## What

PyUnitWizard is used for quantities. ArgDigest applies to the evolving public normalization boundary; adoption remains pending. DepDigest/SMonitor apply when optional/heavy backend loading or recoverable diagnostics are introduced. Do not add unused dependencies. Receptors are developer tools. Validate license provenance, Python/platform support, installed artifacts and Conda publication before release.

## How

Follow architecture.md, scientific_status.md and the extraction manifest.
Separate observed source/runtime evidence from intended capabilities.

## Why

The maintainer created an auxiliary library for local CASTp execution and
future TopoMT consumption. Admission is uibcdf/molsyssuite#70.

## Acceptance criteria

Record independently executed evidence for this theme and name a durable guard
before closing. Bootstrap alone does not complete future acceleration,
consumer migration, provenance review or public release qualification.

## Rationale checkpoint — 2026-10-03

[The maintained comparison register](../../docs/project_rationale.md) records why
OpenCASTp is being developed, which capabilities are implemented and which are
future candidates. Local execution is already provided by pyCASTa; it is not
an exclusive advantage. The distinction being qualified is transparent local
reconstruction and measured compatibility with modern archived CASTp results.
Complete server equivalence, current-version pyCASTa numerical superiority,
Rust/GPU speedups and public distribution are not certified. File-by-file
provenance and publication qualification remain open under this issue.
