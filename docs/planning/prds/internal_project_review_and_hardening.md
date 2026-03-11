---
trace_id: trace.internal_project_review_and_hardening
id: prd.internal_project_review_and_hardening
title: Internal Project Review and Hardening PRD
summary: Defines the ultra-deep internal review remediation needed to keep planning
  bootstrap flows validation-compatible and to remove coordination payload drift
  risk from shared query and sync surfaces.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T15:11:22Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/
- workflows/
---

# Internal Project Review and Hardening PRD

## Record Metadata
- `Trace ID`: `trace.internal_project_review_and_hardening`
- `PRD ID`: `prd.internal_project_review_and_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.internal_project_review_and_hardening_direction`
- `Linked Designs`: `design.features.internal_project_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.internal_project_review_and_hardening`
- `Updated At`: `2026-03-11T15:11:22Z`

## Summary
Defines the ultra-deep internal review remediation needed to keep planning bootstrap flows validation-compatible and to remove coordination payload drift risk from shared query and sync surfaces.

## Problem Statement
The internal review validated two repo-level hardening gaps. First, `watchtower-core plan bootstrap --write` can leave the repository in a failing state immediately after a normal traced bootstrap because it writes feature and implementation documents that do not satisfy the repository's governed design-document expectations and it does not publish the acceptance contract and baseline evidence required by `validate all`. Second, the initiative, coordination, and planning query paths each shape the same planning data into JSON independently, which increases drift risk between machine-readable indexes and query payloads.

## Goals
- Keep traced planning bootstrap write mode validation-compatible by default.
- Ensure bootstrap-generated design documents satisfy the repository's executable documentation rules without manual follow-up edits.
- Publish a full machine-readable bootstrap baseline for this trace and future traces, including acceptance contract and evidence coverage.
- Remove duplicated initiative and planning JSON shaping logic so coordination-facing payloads come from canonical serializers.
- Close the review with the repository back on the green baseline.

## Non-Goals
- Loosening acceptance or documentation validation to permit incomplete bootstrap traces.
- Reworking the overall planning-family model or adding a new planning artifact family.
- Changing query command names or user-facing filter semantics.
- Reopening already closed traces unless the review proves a live regression.

## Requirements
- `req.internal_project_review_and_hardening.001`: The initiative must publish a traced remediation chain with an active PRD, accepted decision record, feature design, implementation plan, acceptance contract, planning-baseline evidence, closed bootstrap task, and bounded execution tasks.
- `req.internal_project_review_and_hardening.002`: `watchtower-core plan bootstrap --write` must leave the repository validation-compatible by generating governed design documents with repository-compliant applied-reference sections and by publishing the minimum acceptance and evidence artifacts needed for traced bootstrap state.
- `req.internal_project_review_and_hardening.003`: The bootstrap command docs, runtime result payloads, generated artifacts, and regression tests must stay aligned when bootstrap output changes.
- `req.internal_project_review_and_hardening.004`: Initiative and planning query payload shaping must reuse canonical serializer helpers instead of maintaining parallel dict-building logic across sync and CLI surfaces.
- `req.internal_project_review_and_hardening.005`: The repository must remain green on the current `validate all`, `pytest`, `mypy`, and `ruff` baseline after the hardening work lands.

## Acceptance Criteria
- `ac.internal_project_review_and_hardening.001`: This trace publishes the PRD, accepted decision, feature design, implementation plan, acceptance contract, planning-baseline evidence, closed bootstrap task, and bounded execution tasks required for closeout-ready review remediation.
- `ac.internal_project_review_and_hardening.002`: A bootstrap write in tests creates design documents with the required applied-reference sections and keeps the repository on a passing non-acceptance and acceptance validation baseline.
- `ac.internal_project_review_and_hardening.003`: The bootstrap command surface, runtime payloads, docs, and integration tests all reflect the additional acceptance-contract and evidence outputs.
- `ac.internal_project_review_and_hardening.004`: Coordination and planning JSON projections are emitted through shared serializers, and regression tests confirm payload stability for query and sync surfaces.
- `ac.internal_project_review_and_hardening.005`: The repository passes `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check`.

## Risks and Dependencies
- Bootstrap hardening touches planning docs, control-plane artifacts, task creation, traceability, and evidence recording in one flow, so sequencing errors could create partial state unless the write path stays fail closed.
- Serializer consolidation touches stable JSON contracts, so targeted regression tests must prove that the public payload shape is preserved.
- This initiative depends on keeping generated trackers and indexes synchronized in the same change sets as the authored planning and contract artifacts.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the fix should remove known failure paths and duplicated shaping logic instead of adding more manual repair steps.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-authored planning, machine-readable contracts, and derived mirrors must remain aligned in the same traced change set.

## References
- docs/planning/coordination_tracking.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/control_plane/contracts/acceptance/README.md
