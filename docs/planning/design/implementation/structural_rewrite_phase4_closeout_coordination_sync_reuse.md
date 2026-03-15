---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse"
title: "Structural Rewrite Phase 4 Closeout Coordination Sync Reuse"
summary: "Implements one bounded Phase 4 slice by routing InitiativeCloseoutService through CoordinationSyncService for the shared planning and coordination outputs after the traceability write while keeping the closeout result contract explicit, then closes through an explicit outcome review that hands the trace to the next bounded entry checkpoint."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T09:55:03Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/python/src/watchtower_core/closeout/"
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/src/watchtower_core/cli/"
  - "core/python/tests/"
  - "docs/planning/tasks/"
aliases:
  - "phase 4 closeout sync reuse slice"
  - "closeout coordination sync reuse"
  - "phase 4 closeout orchestration slice"
---

# Structural Rewrite Phase 4 Closeout Coordination Sync Reuse

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-15T09:55:03Z`

## Summary
Implement one bounded Phase 4 slice by routing `InitiativeCloseoutService.close` through `CoordinationSyncService` for the shared planning and coordination outputs after the traceability write while preserving the five public planning-authority answers, the current closeout command result contract, and the current `TaskLifecycleService` and `PlanningScaffoldService` write behavior, then close through an explicit outcome review that names the next bounded checkpoint.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)
- [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)

## Scope Summary
- Reuse `CoordinationSyncService` for the shared post-traceability closeout outputs: `initiative_index`, `planning_catalog`, `coordination_index`, `initiative_tracking`, and `coordination_tracking`.
- Preserve the existing traceability write as the pre-seam authored-truth update and preserve the current output-path fields exposed by `InitiativeCloseoutResult` and the CLI handler payload.
- Keep `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` as direct closeout outputs outside the approved seam for this slice.
- Preserve `planning_projection_snapshot.py` as a private runtime helper, keep the five public planning-authority answers unchanged, and stop at an explicit outcome review instead of broader Phase 4 rollout.

## Assumptions and Constraints
- `CoordinationSyncService.run(write=True)` remains the canonical ordering for the shared coordination slice: `task-index` -> `traceability-index` -> `initiative-index` -> `planning-catalog` -> `coordination-index` -> `task-tracking` -> `initiative-tracking` -> `coordination-tracking`.
- `InitiativeCloseoutService.close` continues to write traceability first and then refreshes the remaining mirrored planning surfaces.
- `TaskLifecycleService` and `PlanningScaffoldService` already rely on `CoordinationSyncService.run(write=True)` and remain outside the exact refactor seam for this slice.
- This slice does not authorize broader coordination-group redesign, tracker-family redesign, compatibility retirement, hotspot decomposition, or Phase 5 work.
- If the slice does not preserve parity or the current closeout result contract cleanly, rollback restores the current direct closeout rebuild chain after the traceability write.

## Current-State Context
- The closed `.012` review approved one exact write-path convergence seam and kept broader Phase 4 plus later-phase work blocked.
- `InitiativeCloseoutService.close` now writes traceability first, then reuses `CoordinationSyncService.run_closeout_shared_outputs` for exactly `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking` before refreshing the direct PRD, decision, and design tracking outputs.
- The closeout CLI payload still publishes explicit output-path fields for all shared and direct outputs, so the stable closeout result contract remains broader than the shared coordination seam alone.
- `TaskLifecycleService` and `PlanningScaffoldService` still converge on `CoordinationSyncService.run(write=True)` for the full coordination slice, and the bounded closeout helper leaves those callers unchanged while isolating the closeout path as the only touched outlier.
- The implementation slice landed and closed through [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md), which kept broader Phase 4 rollout blocked while handing the trace to the closeout-tracking entry review; that review then closed, the approved successor slice landed through [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md), and the trace then closed through [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md) instead of opening another bounded checkpoint.

## Approved Seam and Result-Contract Boundary
### In-seam outputs for this slice
- `initiative_index_output_path`
- `planning_catalog_output_path`
- `coordination_index_output_path`
- `initiative_tracking_output_path`
- `coordination_tracking_output_path`

### Explicitly out of seam for this slice
- `traceability_output_path`: remains the pre-seam canonical write and validated authored-truth update.
- `prd_tracking_output_path`
- `decision_tracking_output_path`
- `design_tracking_output_path`

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the slice must name one exact orchestration seam, preserve the explicit result-contract boundary, and stop at an explicit outcome review.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): closeout, sync, tracker, and command-payload surfaces remain explicitly classified rather than widened implicitly.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the five public planning-authority answers remain unchanged while the closeout path reuses the existing shared coordination ordering.
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): closeout continues to record terminal initiative state explicitly and cannot silently bypass acceptance or open-task guardrails.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the runtime change remains inside the canonical Python workspace with targeted unit coverage.

## Proposed Technical Approach
- Keep the traceability write and validation flow in `InitiativeCloseoutService.close` unchanged before the new shared-output reuse step.
- Reuse `CoordinationSyncService` for the five shared planning and coordination outputs after the traceability write, either directly or through one minimal private adapter that preserves identical ordering and output capture.
- Continue to refresh `prd-tracking`, `decision-tracking`, and `design-tracking` directly after the shared coordination slice so the closeout command result contract remains explicit and rollback-safe.
- Keep the CLI payload fields and command-doc contract stable while adjusting only the internal closeout orchestration for the approved shared outputs.
- Extend direct closeout coverage so the shared-output convergence and the preserved out-of-seam tracking outputs are both pinned explicitly.

## Work Breakdown
1. Refactor `InitiativeCloseoutService.close` so the shared post-traceability outputs reuse `CoordinationSyncService` while preserving existing write ordering and output-path reporting.
2. Preserve the direct `prd-tracking`, `decision-tracking`, and `design-tracking` rebuilds and their CLI payload fields outside the approved seam.
3. Keep `closeout_handlers.py` and the closeout command docs aligned with the unchanged result contract.
4. Extend direct closeout coverage to assert both the converged shared outputs and the preserved out-of-seam tracking outputs.
5. Rebuild the affected planning surfaces, validate the repo, and stop with one explicit Phase 4 outcome-review task instead of broader rollout.

## Implementation Outcome
- `InitiativeCloseoutService.close` now records the traceability write as the authored-truth step, then delegates the approved five shared outputs to `CoordinationSyncService.run_closeout_shared_outputs` so the closeout path reuses the same coordination rebuild machinery without widening into `task-index`, `traceability-index`, or `task-tracking`.
- `InitiativeCloseoutResult` and the closeout CLI payload still expose `traceability_output_path`, the five shared coordination output paths, and the direct `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` fields without contract drift.
- `core/python/tests/unit/test_initiative_closeout.py` now asserts the exact shared coordination target subset and the preserved direct tracker outputs, and the closeout-plus-sync regression suite passed `17` tests before the repo-wide reruns.
- The slice closes through [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md), keeping broader mutation-path convergence, tracker-family convergence, and later-phase rewrite work blocked pending explicit review of the new closeout-tracking entry package.

## Risks
- Reusing `CoordinationSyncService` can create hidden behavior drift if the closeout path stops matching the current coordination ordering or output-path contract.
- The slice can widen unsafely if it starts pulling `prd`, `decision`, or `design` tracking into the coordination group without a separate approved checkpoint.
- A clean closeout convergence slice can create false confidence if it is misread as broader write-path approval rather than one bounded proof around the remaining direct outlier.

## Validation Plan
- Re-run `./core/python/.venv/bin/watchtower-core doctor --format json`.
- Re-run `./core/python/.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./core/python/.venv/bin/watchtower-core query coordination --format json`
  - `./core/python/.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Re-run targeted closeout and coordination coverage:
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_initiative_closeout.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_initiative_index_sync.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_planning_catalog_sync.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_coordination_index_sync.py`

## Rollback Path
1. Restore the current direct `InitiativeCloseoutService` rebuild chain for the five shared outputs after the traceability write.
2. Keep the direct `prd`, `decision`, and `design` tracking writes and the closeout result payload unchanged.
3. Rebuild the derived planning surfaces and re-run validation plus planning-authority queries before proceeding again.

## References
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)
- [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)
- [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md)
- [watchtower_core_closeout_initiative.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_closeout_initiative.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)

## Updated At
- `2026-03-15T09:55:03Z`
