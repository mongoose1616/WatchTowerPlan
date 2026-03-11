---
trace_id: trace.internal_project_code_review_and_hardening
id: prd.internal_project_code_review_and_hardening
title: Internal Project Code Review and Hardening PRD
summary: Captures the ultra-deep internal code-review findings around stale derived
  planning surfaces after scaffold writes and initiative closeout operations.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T16:10:47Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/
---

# Internal Project Code Review and Hardening PRD

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_and_hardening`
- `PRD ID`: `prd.internal_project_code_review_and_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.internal_project_code_review_and_hardening_direction`
- `Linked Designs`: `design.features.internal_project_code_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.internal_project_code_review_and_hardening`
- `Updated At`: `2026-03-11T16:10:47Z`

## Summary
Captures the ultra-deep internal code-review findings around stale derived planning surfaces after scaffold writes and initiative closeout operations.

## Problem Statement
The internal code review confirmed two still-live lifecycle defects in the repo-local orchestration layer. First, `watchtower-core plan scaffold --write` refreshes only family-specific planning indexes and trackers, so traced scaffold writes can leave `traceability`, `initiative`, `planning-catalog`, and `coordination` surfaces stale until a separate manual sync is run. Second, `watchtower-core closeout initiative --write` refreshes traceability, initiative, coordination, and family tracking surfaces but omits `planning-catalog`, so `watchtower-core query planning` can continue to report an initiative as active after terminal closeout.

The review also confirmed an adjacent constraint that shapes the scaffold fix: standalone single-document scaffolds should not be forced into the coordination slice before they have a bounded task set, because the traceability schema requires active traces to publish `task_ids`. The remediation therefore needs to refresh coordination surfaces for traces that already participate in coordination, while preserving valid standalone planning-document authoring for new, not-yet-bootstrapped traces.

## Goals
- Make traced scaffold writes update the derived coordination slice immediately when the target trace already participates in coordination.
- Keep standalone one-document scaffold writes valid without forcing them into an invalid active trace state.
- Make initiative closeout refresh `planning-catalog` so planning queries reflect terminal initiative status immediately.
- Keep command docs, runtime payloads, and regression tests aligned with the lifecycle write-path changes.
- Close the trace with the repository back on a green validation baseline.

## Non-Goals
- Redesigning the overall planning-family or coordination model.
- Relaxing traceability, planning-catalog, or initiative-closeout validation rules to hide stale-state bugs.
- Making `plan scaffold` a substitute for full traced bootstrap when a new initiative still needs a bounded task set.
- Changing user-facing command names, argument syntax, or query filters.

## Requirements
- `req.internal_project_code_review_and_hardening.001`: This trace must publish a real PRD, accepted direction decision, feature design, implementation plan, acceptance contract, updated planning-baseline evidence, closed bootstrap task, and bounded execution tasks for the code-review findings.
- `req.internal_project_code_review_and_hardening.002`: `watchtower-core plan scaffold --write` must refresh traceability, initiative, planning-catalog, and coordination surfaces when the target trace already participates in the coordination slice, and it must not force standalone scaffolded traces into invalid active traceability state.
- `req.internal_project_code_review_and_hardening.003`: `watchtower-core closeout initiative --write` must rebuild `planning-catalog` outputs in the same closeout write path as the initiative and coordination surfaces, and the closeout result payload must report that output.
- `req.internal_project_code_review_and_hardening.004`: The scaffold and closeout command docs, runtime outputs, and regression tests must stay aligned with the additional derived-surface refresh behavior.
- `req.internal_project_code_review_and_hardening.005`: The repository must return to a green baseline on `watchtower-core validate all`, `pytest`, `mypy`, and `ruff` after the fixes land.

## Acceptance Criteria
- `ac.internal_project_code_review_and_hardening.001`: This trace publishes the full planning chain, the accepted decision, the acceptance contract, updated planning-baseline evidence, and three bounded task records covering bootstrap, scaffold coordination refresh, and closeout planning-catalog refresh.
- `ac.internal_project_code_review_and_hardening.002`: Regression coverage proves that scaffold writes refresh traceability, initiative, and planning-catalog state for existing traced initiatives while leaving standalone scaffold writes valid.
- `ac.internal_project_code_review_and_hardening.003`: Regression coverage proves that initiative closeout refreshes planning-catalog state so planning queries reflect terminal initiative status and closed phase immediately after closeout.
- `ac.internal_project_code_review_and_hardening.004`: The `plan scaffold` and `closeout initiative` command docs and runtime payloads match the implemented lifecycle refresh behavior.
- `ac.internal_project_code_review_and_hardening.005`: The repository passes `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check` after the trace closes.

## Risks and Dependencies
- The scaffold fix touches a high-fan-out write path that already drives multiple authoritative and derived surfaces, so the refresh condition must stay explicit and deterministic.
- The closeout fix changes a user-facing JSON payload, so handler tests and command docs must be updated in the same change set.
- The trace depends on keeping PRD, decision, design, contract, evidence, task, index, and tracker surfaces aligned through the final sync and closeout cycle.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): write paths should be deterministic and valid by construction rather than relying on manual reconciliation after mutation.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): authoritative planning and machine-readable companion surfaces must remain synchronized in the same bounded change.

## References
- docs/planning/coordination_tracking.md
- docs/commands/core_python/watchtower_core_plan_scaffold.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
