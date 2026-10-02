---
summary: Support Python 3.14 with installed scientific validation
issue: uibcdf/opencastp#5
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: measured
area: [compatibility, testing, distribution]
guard: tests/test_analysis.py
normative: devguide/python_support.md
blocked_by: []
supersedes: []
---

# Support Python 3.14

## What

The maintainer explicitly requested Python 3.14 alongside 3.11--3.13.
Widen metadata and both Conda environments to >=3.11,<3.15 and execute the
full supported-minor matrix with actual interpreter assertions, a non-editable
installed numerical smoke and unfiltered tests. Routine development stays 3.13.

## How

Register component-specific transition authorization in MolSysSuite, linked to
this issue. Do not claim admission in the public badge until the 3.14 lane has
executed and passed. Record native job/step/runtime identity in the CI evidence.
The current frozen published-policy limitation is central #73; the bounded
source bootstrap must use the exact central authorization commit.

## Why

OpenCASTp should run in the MolSysSuite Python 3.14 environments without
widening TopoMT's existing contract or removing either of its CASTp routes.

## Acceptance criteria

- All four supported minors execute installed numerical and full test gates.
- Record source/artifact/interpreter evidence and limits.
- Admit the wider component contract and generate its canonical Python badge only after success.
- Retain the scientific suite as the durable runtime guard; public Conda publication stays in #2.

## Resolution — 2026-10-02

Full matrix 37058887654 at 762db29693f030ac61baa423de0371993ad6a454
executed and passed on Python 3.11.16, 3.12.14, 3.13.15 and 3.14.7.
Each cell passed non-editable installation, the isolated installed numerical
validator and 26 unfiltered tests. Actual interpreter assertions passed.
Native evidence is ../artifacts/hosted_python_matrix_2026_10_02.json;
GH Run Receptor 1.1.1 preserved native success. Routine 37058866994 and the
bounded source-policy gate 37058867837 also passed.

The public analysis tests protect numerical execution, quantities, validation
and atom mapping in the real interpreter. Installation and interpreter gates
separately protect acquisition and matrix identity; the test module alone is
not represented as complete packaging evidence. The normative support document
records the accepted range and these limits. Metadata/Conda constraints and
routine/full CI remain aligned. Central transition admission and its generated
badge now reflect this measured outcome.

This qualifies Linux interpreter/runtime compatibility; no macOS/Windows,
public OpenCASTp channel or complete server-equivalence claim follows.
