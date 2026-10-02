---
summary: Support Python 3.14 with installed scientific validation
issue: uibcdf/opencastp#5
status: active
opened: 2026-10-02
closed:
verification: inspected
area: [compatibility, testing, distribution]
guard:
normative:
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
