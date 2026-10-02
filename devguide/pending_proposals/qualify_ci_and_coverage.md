---
summary: Qualify CI lanes and scientific coverage evidence
issue: uibcdf/opencastp#3
status: active
opened: 2026-10-02
closed:
verification: measured
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

## Hosted checkpoint — 2026-10-02

At `c9a6f65ea6a7b76924f21df17c88830e745ca561`, routine CI
37055144977 passed and full matrix 37055176911 passed. GH Run Receptor 1.1.1
preserved the native success. Native job/step evidence separately confirms
successful non-editable installation, the `python -I` installed numerical
validator and unfiltered pytest for all three supported Linux minors.
No macOS/Windows or public-channel claim follows from these runs.

The published policy caller failed at run 37055145913 with `[UNREGISTERED]`:
its immutable policy-v1.5.2 registry predates this member. The provider defect is
uibcdf/molsyssuite#73. Interim conformance uses the explicit immutable central
admission checker `a801b4ae09aa3085228013dbfdead8b3b905868b`, the same inherited
Ruff version and a deadline gate. The old caller remains visibly disabled; no
published policy adoption is claimed. The central policy-caller exception
expires on 2026-12-31. The maintainer owns review; removal requires a published
admission-aware gate that recognizes OpenCASTp and passes actual hosted checks.

Coverage reporting remains pending. Do not close this theme based solely on
bootstrap success or use a static badge to replace missing coverage evidence.
