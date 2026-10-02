---
summary: Qualify CI lanes and scientific coverage evidence
issue: uibcdf/opencastp#3
status: active
opened: 2026-10-02
closed:
verification: inspected
area: [testing, ci, coverage]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualify CI lanes and scientific coverage evidence

## What

Maintain unfiltered routine Python 3.13 tests and an installed-package gate,
plus full Python 3.11--3.13 Linux coverage for PRs, weekly and manual runs.
Inspect actual hosted job/step evidence before claiming minor qualification.
Assess numerical coverage as applicable; no accepted report or live percentage
is claimed during admission. The central coverage inventory tracks this gap.

## How

Use GH Run Receptor first and native GitHub job/step evidence when its profile
is incomplete. Retain exact source, interpreter and producer versions.
Introduce a meaningful bounded coverage producer, verify its report and upload,
and then add the live percentage with scope/cadence. Do not invent a floor or
expand every internal push into an unrelated scientific benchmark.

## Why

Local source tests and a borrowed-dependency wheel smoke do not establish
clean public installation, every platform or scientific server equivalence.
Linux starts the hosted review; prospective macOS support is Apple Silicon
only and requires separate installed evidence. Distribution is #2 and
scientific extraction/corpus validation is #1.

## Acceptance criteria

- Routine and all supported-minor jobs execute unfiltered tests and the installed gate.
- Exact run/commit identity and limits are retained in this record.
- Coverage applicability is resolved with an accepted measured producer or a justified bounded exception.
- Close only after naming a relevant durable guard and updating the central review.
