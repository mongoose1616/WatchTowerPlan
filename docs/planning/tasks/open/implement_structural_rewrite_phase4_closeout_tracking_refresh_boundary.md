---
id: task.structural_rewrite_program.phase4_closeout_tracking_refresh_boundary.016
trace_id: trace.structural_rewrite_program
title: Implement structural rewrite Phase 4 closeout tracking refresh boundary
summary: Route the remaining PRD, decision, and design tracking refresh step in InitiativeCloseoutService through one private closeout-local boundary after the approved shared closeout seam while keeping the closeout result contract explicit.
type: task
status: active
task_status: ready
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-15T08:14:01Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md
- docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json
- core/python/src/watchtower_core/closeout/initiative.py
- core/python/src/watchtower_core/cli/closeout_handlers.py
- core/python/src/watchtower_core/repo_ops/sync/prd_tracking.py
- core/python/src/watchtower_core/repo_ops/sync/decision_tracking.py
- core/python/src/watchtower_core/repo_ops/sync/design_tracking.py
- core/python/tests/unit/test_initiative_closeout.py
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase4_closeout_tracking_entry
- design.implementation.structural_rewrite_phase4_closeout_tracking_refresh_boundary
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase4_closeout_tracking_entry_review.015
---

# Implement structural rewrite Phase 4 closeout tracking refresh boundary

## Summary
Route the remaining PRD, decision, and design tracking refresh step in InitiativeCloseoutService through one private closeout-local boundary after the approved shared closeout seam while keeping the closeout result contract explicit.

## Scope
- Add one private refresh boundary for `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` after `CoordinationSyncService.run_closeout_shared_outputs` completes.
- Preserve `traceability_output_path`, the approved shared closeout seam, and the explicit output-path fields exposed by `InitiativeCloseoutResult` and the closeout CLI payload.
- Keep `watchtower-core sync prd-tracking`, `decision-tracking`, and `design-tracking` as the canonical public tracker sync families.
- Keep `TaskLifecycleService`, `PlanningScaffoldService`, and broader tracker-family behavior unchanged in this slice.

## Done When
- `InitiativeCloseoutService.close` routes the remaining tracker refresh step through one private closeout-local boundary without widening the approved shared seam.
- `InitiativeCloseoutResult` and the closeout CLI payload still publish `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` explicitly.
- The slice stops at an explicit Phase 4 outcome-review task rather than broader Phase 4 or later-phase rollout.

## Links
- [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)
- [structural_rewrite_phase4_closeout_tracking_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)

## Updated At
- `2026-03-15T08:14:01Z`
