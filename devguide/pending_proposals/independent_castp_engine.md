---
summary: Extract and validate an independent CASTp reference engine
issue: uibcdf/opencastp#1
status: active
opened: 2026-10-02
closed:
verification: measured
area: [architecture, validation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Extract and validate an independent CASTp reference engine

## What

Retain TopoMT CASTp during coexistence. Validate standalone arrays, units, mapping, numerical events and regions before switching any consumer.

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

## Checkpoint — 2026-10-02

The initial standalone Python API, official repository scaffold and numerical
extraction are implemented. The 26-test suite, Ruff, bounded public-API mypy,
warning-free Sphinx build, non-editable installed-wheel smoke and central
repository conformance passed locally. The 1STP/1CDO extraction audit matches
94 regions and 184 closed-void SA/MS scalars; exact membership/rank evidence and
producer hashes are in ../artifacts/extraction_parity_2026_10_02.json.

TopoMT remains unchanged. Broader extracted-engine corpus validation, installed
supported-minor qualification and a future optional TopoMT adapter remain open.
Rust, threads and GPU are future separately measurable stages. Provenance and
public distribution remain tracked by uibcdf/opencastp#2.

## Current priority

The maintainer explicitly defers other improvements until complete measured
CASTp3/CASTpFold equivalence. uibcdf/opencastp#6 owns that investigation and
its direct-server evidence; this extraction issue does not certify equivalence
or authorize consumer migration. Python 3.11--3.14 installation compatibility
is now measured in the separate archived #5 record.
