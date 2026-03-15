---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase4_closeout_tracking_refresh_boundary"
title: "Structural Rewrite Phase 4 Closeout Tracking Refresh Boundary"
summary: "Implements one bounded Phase 4 slice by routing the remaining PRD, decision, and design tracker refresh step in InitiativeCloseoutService through one private closeout-local refresh boundary after the approved shared closeout seam while preserving the closeout result contract, then closes through one explicit outcome review and program-closeout decision."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T09:55:03Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/python/src/watchtower_core/closeout/"
  - "core/python/src/watchtower_core/cli/"
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/tests/"
  - "docs/planning/tasks/"
aliases:
  - "phase 4 closeout tracking refresh boundary"
  - "closeout tracking refresh slice"
  - "phase 4 closeout tracker boundary"
---

# Structural Rewrite Phase 4 Closeout Tracking Refresh Boundary

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase4_closeout_tracking_refresh_boundary`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-15T09:55:03Z`

## Summary
Implement one bounded Phase 4 slice by routing the remaining `prd-tracking`, `decision-tracking`, and `design-tracking` refresh step in `InitiativeCloseoutService.close` through one private closeout-local refresh boundary after the approved shared closeout seam while preserving the five public planning-authority answers, the stable closeout command result contract, the current tracker sync family names, and the current `TaskLifecycleService` and `PlanningScaffoldService` behavior.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_closeout_tracking_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md)
- [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)

## Scope Summary
- Route the remaining direct closeout tracker refresh step for `prd-tracking`, `decision-tracking`, and `design-tracking` through one private closeout-local boundary after the approved shared coordination outputs complete.
- Preserve the existing traceability write, the approved shared closeout seam, and the explicit output-path fields exposed by `InitiativeCloseoutResult` and the closeout CLI payload.
- Keep `watchtower-core sync prd-tracking`, `decision-tracking`, and `design-tracking` as the canonical public tracker sync families; do not pull those targets into `CoordinationSyncService`.
- Preserve `planning_projection_snapshot.py` as a private runtime helper, keep the five public planning-authority answers unchanged, and stop at an explicit outcome review instead of broader Phase 4 or later-phase rollout.

## Assumptions and Constraints
- The approved shared closeout seam remains fixed: `traceability_output_path` stays pre-seam, `CoordinationSyncService.run_closeout_shared_outputs` remains limited to `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking`, and `TaskLifecycleService` plus `PlanningScaffoldService` remain outside this slice.
- `PrdTrackingSyncService`, `DecisionTrackingSyncService`, and `DesignTrackingSyncService` remain the canonical public sync-family owners for the three tracker outputs touched by this slice.
- The private refresh boundary may live inside `core/python/src/watchtower_core/closeout/initiative.py` or another private closeout-local helper, but it may not become a new public sync group, command family, or broader tracker-family abstraction.
- This slice does not authorize changing tracker-family CLI names, expanding `CoordinationSyncService`, changing task-lifecycle or scaffold write behavior, broader tracker-family redesign, hotspot decomposition, compatibility retirement, or Phase 5 work.
- If the slice does not preserve parity or the stable closeout result contract cleanly, rollback restores the current direct tracker refresh calls after the approved shared closeout seam.

## Current-State Context
- The closed `.015` review approved one exact remaining seam only: the post-shared-seam refresh step for `prd-tracking`, `decision-tracking`, and `design-tracking`.
- `InitiativeCloseoutService.close` currently writes traceability first, then reuses `CoordinationSyncService.run_closeout_shared_outputs` for the approved shared outputs, and then still instantiates `PrdTrackingSyncService`, `DecisionTrackingSyncService`, and `DesignTrackingSyncService` inline to write the remaining tracker documents directly.
- The closeout CLI payload still publishes explicit output-path fields for the traceability write, the approved shared coordination outputs, and the remaining direct PRD, decision, and design tracker outputs.
- The bounded implementation slice landed through [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md), the closed final review [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md) then recorded a pass plus explicit program-closeout decision, and the trace closed instead of opening broader tracker-family convergence or later-phase work.

## Approved Seam and Result-Contract Boundary
### In-seam outputs for this slice
- `prd_tracking_output_path`
- `decision_tracking_output_path`
- `design_tracking_output_path`

### Explicitly out of seam for this slice
- `traceability_output_path`
- `initiative_index_output_path`
- `planning_catalog_output_path`
- `coordination_index_output_path`
- `initiative_tracking_output_path`
- `coordination_tracking_output_path`

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the slice must name one exact refresh seam, preserve the explicit result-contract boundary, and stop at an explicit outcome review.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): closeout, tracker, sync, and command-payload surfaces remain explicitly classified rather than widened implicitly.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the five public planning-authority answers remain unchanged while the remaining closeout tracker step is normalized.
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): closeout continues to record terminal initiative state explicitly and cannot silently weaken acceptance or open-task guardrails.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the runtime change remains inside the canonical Python workspace with targeted unit coverage.

## Proposed Technical Approach
- Keep the traceability write and the approved shared coordination step in `InitiativeCloseoutService.close` unchanged before the new tracker-refresh boundary runs.
- Introduce one private closeout-local boundary that refreshes `prd-tracking`, `decision-tracking`, and `design-tracking` using the existing tracker sync services and returns their explicit output paths.
- Preserve the `InitiativeCloseoutResult` fields and closeout CLI payload fields so the stable closeout command result contract still reports all shared and tracker outputs individually.
- Extend direct closeout coverage so the approved shared coordination seam, the preserved tracker output fields, and the still-private tracker refresh boundary all remain pinned explicitly.

## Work Breakdown
1. Refactor `InitiativeCloseoutService.close` so the remaining tracker refresh step runs through one private closeout-local boundary after `CoordinationSyncService.run_closeout_shared_outputs`.
2. Preserve the direct `prd-tracking`, `decision-tracking`, and `design-tracking` result fields and their CLI payload exposure without widening the approved shared seam.
3. Keep the tracker sync service implementations and public sync command family names unchanged while adjusting only the internal closeout orchestration for the remaining tracker step.
4. Extend direct closeout coverage to assert the preserved explicit tracker output fields and the unchanged shared closeout seam.
5. Rebuild the affected planning surfaces, validate the repo, and stop with one explicit Phase 4 outcome-review task instead of broader rollout.

## Implementation Outcome
- `InitiativeCloseoutService.close` now routes the remaining `prd-tracking`, `decision-tracking`, and `design-tracking` refresh step through `_run_closeout_tracking_refresh_boundary()` after `CoordinationSyncService.run_closeout_shared_outputs(write=True)` completes, so the last direct tracker outlier is isolated behind one private closeout-local helper without widening the approved shared seam.
- `_CloseoutTrackingOutputs` groups the three tracker output paths privately inside `core/python/src/watchtower_core/closeout/initiative.py`, while `InitiativeCloseoutResult` and the closeout CLI payload still expose `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` individually with no contract drift.
- `core/python/tests/unit/test_initiative_closeout.py` still pins the exact shared coordination target subset plus the preserved explicit tracker outputs, and the landed slice closed through [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md), which then recorded the explicit structural-rewrite program closeout decision instead of broader Phase 4 rollout.

## Risks
- The private boundary can still create hidden behavioral drift if the closeout path stops matching the current tracker document outputs or silently weakens the explicit result-contract fields.
- The slice can widen unsafely if it starts pulling tracker targets into `CoordinationSyncService` or a new public tracker-family abstraction instead of isolating the remaining closeout-local step.
- A clean final closeout seam can create false confidence if it is misread as broader tracker-family approval rather than one bounded proof around the last direct outlier.

## Validation Plan
- Re-run `./core/python/.venv/bin/watchtower-core doctor --format json`.
- Re-run `./core/python/.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./core/python/.venv/bin/watchtower-core query coordination --format json`
  - `./core/python/.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Re-run targeted closeout and tracker coverage:
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_initiative_closeout.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_initiative_index_sync.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_planning_catalog_sync.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_coordination_index_sync.py`

## Rollback Path
1. Restore the current direct `PrdTrackingSyncService`, `DecisionTrackingSyncService`, and `DesignTrackingSyncService` calls inline inside `InitiativeCloseoutService.close` after the approved shared closeout seam completes.
2. Keep the closeout result payload fields, tracker sync family names, and the approved shared coordination seam unchanged.
3. Rebuild the derived planning surfaces and re-run validation plus planning-authority queries before proceeding again.

## Stop Condition
- Stop at the explicit Phase 4 closeout-tracking outcome review and do not widen this slice into broader tracker-family convergence, coordination-group redesign, public-planning-boundary changes, or later phases.

## References
- [structural_rewrite_phase4_closeout_tracking_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md)
- [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [watchtower_core_closeout_initiative.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_closeout_initiative.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)

## Updated At
- `2026-03-15T09:55:03Z`
