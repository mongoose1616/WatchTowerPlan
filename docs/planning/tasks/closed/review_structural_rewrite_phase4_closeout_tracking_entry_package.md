---
id: task.structural_rewrite_program.phase4_closeout_tracking_entry_review.015
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 4 closeout tracking entry package
summary: Review the bounded Phase 4 closeout-tracking entry package, confirm the public planning parity and closeout result-contract guardrails, and decide whether one bounded closeout tracker-refresh slice may begin.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-15T08:14:01Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_program.md
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md
- docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md
- docs/planning/tasks/open/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json
- core/control_plane/indexes/coordination/coordination_index.v1.json
- core/control_plane/indexes/initiatives/initiative_index.v1.json
- core/control_plane/indexes/planning/planning_catalog.v1.json
- core/control_plane/indexes/traceability/traceability_index.v1.json
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
- task.structural_rewrite_program.phase4_closeout_coordination_sync_reuse_review.014
---

# Review structural rewrite Phase 4 closeout tracking entry package

## Summary
Review the bounded Phase 4 closeout-tracking entry package, confirm the public planning parity and closeout result-contract guardrails, and decide whether one bounded closeout tracker-refresh slice may begin.

## Scope
- Confirm that the five current planning-authority answers remain the explicit public boundary after the closed closeout coordination sync-reuse outcome review.
- Confirm that the approved shared closeout coordination seam remains fixed and that the remaining direct `prd`, `decision`, and `design` tracking refresh step is the only proposed next write-path outlier in `InitiativeCloseoutService.close`.
- Confirm that the Phase 4 classification and parity addendum is explicit for the closeout, tracker, and public planning surfaces touched by the proposed checkpoint.
- Decide whether the rewrite may proceed through one bounded closeout-tracking checkpoint or remains blocked.

## Done When
- The review records an explicit approve or block outcome for the Phase 4 closeout-tracking entry package.
- Any approved later slice remains bounded, parity-backed, and rollback-explicit.
- No further Phase 4 implementation begins before this task reaches an explicit terminal outcome.

## Review Outcome
- `Decision`: approved for exactly one bounded Phase 4 slice.
- `Public planning boundary`: reaffirmed. `watchtower-core query authority --domain planning --format json` still resolves the same five planning-authority answers, and the review does not authorize any public planning-boundary change.
- `Approved shared closeout seam`: unchanged. `traceability_output_path` remains the pre-seam canonical write, and `CoordinationSyncService.run_closeout_shared_outputs` remains fixed to `initiative_index_output_path`, `planning_catalog_output_path`, `coordination_index_output_path`, `initiative_tracking_output_path`, and `coordination_tracking_output_path`.
- `Closeout result contract boundary`: explicit. `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain individually reported output-path fields in `InitiativeCloseoutResult` and the closeout CLI payload even if the implementation stops using three direct inline refresh calls.
- `Approved first slice`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- `Exact seam`: one private closeout-local refresh boundary for `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` after the approved shared closeout seam completes, while `watchtower-core sync prd-tracking`, `decision-tracking`, and `design-tracking` remain the canonical public sync families and `TaskLifecycleService` plus `PlanningScaffoldService` remain unchanged.
- `Next-step decision`: do not broaden Phase 4 rollout. Open one bounded implementation task for the approved closeout-tracking refresh boundary slice and keep broader Phase 4 plus Phase 5, Phase 6, and Phase 7 work blocked until its explicit outcome review closes.

## Rationale
- The remaining direct tracker refresh step is now the only rewrite-specific write-path outlier left inside `InitiativeCloseoutService.close` after the approved shared coordination seam landed cleanly.
- A private closeout-local refresh boundary is smaller than pulling tracker targets into `CoordinationSyncService`, changing tracker-family command ownership, or redesigning the broader tracker refresh model.
- Preserving the stable output-path fields while extracting one private refresh seam keeps rollback straightforward: the three current tracker refresh calls can be restored inline without disturbing the shared coordination seam or public planning-authority answers.

## Links
- [structural_rewrite_phase4_closeout_tracking_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md)
- [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/open/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)

## Updated At
- `2026-03-15T08:14:01Z`
