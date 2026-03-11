---
trace_id: trace.internal_project_code_review_and_hardening
id: design.features.internal_project_code_review_and_hardening
title: Internal Project Code Review and Hardening Feature Design
summary: Defines the code-review-backed design for lifecycle sync completeness across
  traced scaffold writes and initiative closeout.
type: feature_design
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

# Internal Project Code Review and Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_and_hardening`
- `Design ID`: `design.features.internal_project_code_review_and_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.internal_project_code_review_and_hardening`
- `Linked Decisions`: `decision.internal_project_code_review_and_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.internal_project_code_review_and_hardening`
- `Updated At`: `2026-03-11T16:10:47Z`

## Summary
Defines the code-review-backed design for lifecycle sync completeness across traced scaffold writes and initiative closeout.

## Source Request
- User request to perform an ultra-deep internal project code review, fix every validated issue through the normal task cycle, and commit the final closeout.
- Code-review reproductions showing stale planning state after traced scaffold writes and after initiative closeout.

## Scope and Feature Boundary
- Covers `watchtower-core plan scaffold --write` for traced documents that belong to an existing coordination-participating trace.
- Covers `watchtower-core closeout initiative --write` and its derived output set.
- Covers the docs, handler payloads, and regression tests needed to keep those lifecycle behaviors explicit.
- Does not change bootstrap semantics for creating new traced initiatives; full bootstrap remains the path that creates a bounded task set and enters coordination cleanly.
- Does not relax traceability or planning-catalog schema requirements.

## Current-State Context
- `watchtower-core plan scaffold --write` currently writes the planning document plus family-specific indexes and trackers, but it does not rebuild `traceability`, `initiative-index`, `planning-catalog`, or `coordination-index`.
- When the target trace already exists in coordination, the missing sync leaves `query planning`, `query initiatives`, and `query coordination` stale until a manual `sync coordination` or `sync all`.
- An unconditional coordination rebuild after every scaffold write is not valid because active traceability entries require `task_ids`, and standalone single-document scaffolds can exist before a new trace has a bounded task.
- `watchtower-core closeout initiative --write` currently updates traceability, initiative index, coordination index, initiative tracking, coordination tracking, and the PRD/decision/design trackers, but it omits `planning-catalog`.
- The user-facing repro shows `query planning` still reporting `initiative_status: active` and `current_phase: closeout` after closeout while coordination already reports the trace as `completed` and `closed`.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): deterministic write paths should leave derived machine surfaces truthful without extra operator repair steps.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): companion machine-readable views must remain aligned with authoritative planning mutations.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traced planning changes need explicit traceability outcomes instead of silent drift.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): the planning catalog is a canonical machine-readable planning join and must stay current after closeout.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): lifecycle changes that alter current phase, ownership, or next action must refresh the initiative-family coordination view.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): new traces should not be treated as active coordination work until they have bounded task state.

## Design Goals and Constraints
- Refresh stale coordination-derived surfaces immediately after traced scaffold mutations that belong to an existing coordination-valid trace.
- Keep standalone single-document scaffolds valid and side-effect bounded instead of forcing them into an invalid active trace state.
- Refresh `planning-catalog` in the initiative closeout write path without changing command arguments or closeout semantics.
- Preserve existing query payload fields; additive fields are acceptable only where the command already reports output paths.
- Keep the implementation small and local to the current lifecycle services rather than redesigning sync orchestration broadly.

## Options Considered
### Option 1
- Keep the current partial refresh behavior and rely on manual `sync coordination` or `sync all` after scaffold and closeout operations.
- Strength: no code change to lifecycle services.
- Tradeoff: stale derived state remains a live defect and the repo continues to require manual repair for normal write paths.

### Option 2
- Refresh coordination surfaces conditionally for scaffold writes when the trace already participates in coordination or has traced tasks, and explicitly rebuild `planning-catalog` during initiative closeout.
- Strength: fixes the reproduced stale-state bugs while respecting the schema requirement that active traces publish `task_ids`.
- Tradeoff: the write-path behavior becomes slightly more conditional and requires sharper regression coverage.

### Option 3
- Refresh coordination unconditionally after every scaffold write and relax traceability expectations for single-document scaffolds.
- Strength: simplest mental model for scaffold writes.
- Tradeoff: changes the repository's task-handling threshold and risks treating unbounded planning drafts as active initiatives.

## Recommended Design
### Scaffold Write Refresh
- Keep the existing family-specific sync for PRD, design, or decision indexes and trackers.
- Add a coordination refresh only when the target trace already exists in traceability or already has traced tasks in the task index.
- Treat standalone scaffold writes for new traces as planning-authoring work only; they stay out of coordination until bootstrap or task creation establishes bounded work state.

### Initiative Closeout Refresh
- Preserve the existing closeout flow that writes traceability first and then rebuilds initiative and coordination outputs.
- Add an explicit `planning-catalog` rebuild between initiative-index and coordination-index so the canonical planning query surface reflects the new terminal state immediately.
- Surface the additional planning-catalog output path in the closeout result payload because the command already reports individual write outputs.

### Docs and Runtime Contract
- Update `watchtower_core_plan_scaffold` command guidance to explain that write mode refreshes family planning surfaces and also refreshes traced coordination surfaces for traces already participating in coordination.
- Update `watchtower_core_closeout_initiative` docs and handler payloads to include the planning-catalog refresh.
- Add targeted tests for both service behaviors and for the additive closeout JSON payload field.

### Invariants and Failure Cases
- Standalone scaffold writes for brand-new traces must remain valid without forcing an active traceability entry that lacks `task_ids`.
- Traced scaffold writes for existing coordination-participating traces must not leave traceability, initiative, planning-catalog, or coordination results stale.
- Initiative closeout must not report success while leaving `query planning` on the old initiative state.

## Affected Surfaces
- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`
- `core/python/src/watchtower_core/closeout/initiative.py`
- `core/python/src/watchtower_core/cli/closeout_handlers.py`
- `core/python/tests/unit/test_planning_scaffolds.py`
- `core/python/tests/unit/test_initiative_closeout.py`
- `core/python/tests/unit/test_closeout_handlers.py`
- `docs/commands/core_python/watchtower_core_plan_scaffold.md`
- `docs/commands/core_python/watchtower_core_closeout_initiative.md`
- `core/python/README.md`

## Design Guardrails
- Do not widen scaffold behavior into implicit initiative bootstrap.
- Do not add a second source of truth for planning closeout state outside the planning catalog and existing coordination surfaces.
- Do not rely on manual sync commands to make normal write paths truthful.

## Risks
- Conditional scaffold refresh logic could become too implicit if the trace-participation rule is not tested clearly.
- The closeout payload change is additive but still user-facing, so docs and handler tests must land in the same slice.
- Because these flows rebuild derived artifacts, the final sync and validation pass will produce legitimate tracker and index churn.

## References
- docs/planning/prds/internal_project_code_review_and_hardening.md
- docs/commands/core_python/watchtower_core_plan_scaffold.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
