---
id: task.structural_rewrite_program.phase4_closeout_coordination_sync_reuse.013
trace_id: trace.structural_rewrite_program
title: Implement structural rewrite Phase 4 closeout coordination sync reuse
summary: Route InitiativeCloseoutService through CoordinationSyncService for the shared planning and coordination outputs after the traceability write while keeping the closeout result contract explicit.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-15T06:18:27Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md
- docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json
- core/python/src/watchtower_core/closeout/initiative.py
- core/python/src/watchtower_core/cli/closeout_handlers.py
- core/python/src/watchtower_core/repo_ops/sync/coordination.py
- core/python/src/watchtower_core/repo_ops/sync/registry.py
- core/python/tests/unit/test_initiative_closeout.py
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py
- core/python/tests/unit/test_coordination_index_sync.py
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase4_closeout_coordination_entry
- design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase4_closeout_coordination_entry_review.012
---

# Implement structural rewrite Phase 4 closeout coordination sync reuse

## Summary
Route InitiativeCloseoutService through CoordinationSyncService for the shared planning and coordination outputs after the traceability write while keeping the closeout result contract explicit.

## Scope
- Reuse `CoordinationSyncService` for `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking` after the traceability write in `InitiativeCloseoutService.close`.
- Preserve the traceability write, the five public planning-authority answers, and the current `planning_projection_snapshot.py` privacy boundary.
- Keep `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` as direct closeout outputs outside the approved seam for this slice.
- Keep `TaskLifecycleService` and `PlanningScaffoldService` write behavior unchanged in this checkpoint.

## Done When
- The shared post-traceability closeout outputs reuse `CoordinationSyncService` or one private equivalent that preserves the same ordering and output contracts.
- `InitiativeCloseoutResult` and the closeout CLI payload still publish the full output-path contract, including the direct PRD, decision, and design tracking outputs.
- The slice stops at an explicit Phase 4 outcome-review task rather than broader Phase 4 rollout.

## Outcome
- `InitiativeCloseoutService.close` now writes traceability first, then reuses `CoordinationSyncService.run_closeout_shared_outputs` for exactly `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking` without widening the seam to `task-index`, `traceability-index`, or `task-tracking`.
- `traceability_output_path` remains the pre-seam canonical write, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain direct post-sync outputs outside the approved seam while the closeout CLI payload keeps the full output-path contract unchanged.
- `core/python/tests/unit/test_initiative_closeout.py` now pins the exact shared coordination target subset plus the preserved direct tracker outputs, the closeout-plus-sync regression suite passed cleanly, and the slice now closes through [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md) instead of broader Phase 4 rollout.

## Links
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)

## Updated At
- `2026-03-15T06:18:27Z`
