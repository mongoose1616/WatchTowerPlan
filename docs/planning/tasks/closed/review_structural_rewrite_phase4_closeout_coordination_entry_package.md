---
id: task.structural_rewrite_program.phase4_closeout_coordination_entry_review.012
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 4 closeout coordination entry package
summary: Review the bounded Phase 4 closeout-coordination entry package, confirm the public planning parity and write-path guardrails, and decide whether one bounded closeout orchestration slice may begin.
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
- docs/planning/design/implementation/structural_rewrite_program.md
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md
- docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md
- docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json
- core/control_plane/indexes/coordination/coordination_index.v1.json
- core/control_plane/indexes/initiatives/initiative_index.v1.json
- core/control_plane/indexes/planning/planning_catalog.v1.json
- core/control_plane/indexes/traceability/traceability_index.v1.json
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
- task.structural_rewrite_program.phase4_planning_projection_snapshot_review.011
---

# Review structural rewrite Phase 4 closeout coordination entry package

## Summary
Review the bounded Phase 4 closeout-coordination entry package, confirm the public planning parity and write-path guardrails, and decide whether one bounded closeout orchestration slice may begin.

## Scope
- Confirm that the five current planning-authority answers remain the explicit public boundary after the closed first Phase 4 outcome review.
- Confirm that `InitiativeCloseoutService` is still the only named direct write-path outlier inside the reviewed Phase 4 consumer boundary and that broader mutation-path convergence remains blocked.
- Confirm that the Phase 4 classification and parity addendum is explicit for the closeout, orchestration, tracker, and public planning surfaces touched by the proposed checkpoint.
- Decide whether the rewrite may proceed through one bounded closeout-coordination checkpoint or remains blocked.

## Done When
- The review records an explicit approve or block outcome for the Phase 4 closeout-coordination entry package.
- Any approved later slice remains bounded, parity-backed, and rollback-explicit.
- No further Phase 4 implementation begins before this task reaches an explicit terminal outcome.

## Review Outcome
- `Decision`: approved for exactly one bounded Phase 4 slice.
- `Public planning boundary`: reaffirmed. `watchtower-core query authority --domain planning --format json` still resolves the same five planning-authority answers, and the review does not authorize any public planning-boundary change.
- `Private planning boundary`: reaffirmed. `planning_projection_snapshot.py` remains a private runtime helper, and the review does not authorize any new public planning graph or helper family.
- `Closeout result contract boundary`: explicit. `traceability_output_path` remains the pre-seam canonical write, the approved shared-output seam is limited to `initiative_index_output_path`, `planning_catalog_output_path`, `coordination_index_output_path`, `initiative_tracking_output_path`, and `coordination_tracking_output_path`, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain direct post-sync outputs outside the approved seam for this slice.
- `Approved first slice`: [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- `Exact seam`: one post-traceability closeout step in which `InitiativeCloseoutService.close` reuses `CoordinationSyncService` for the shared planning and coordination outputs only, while `TaskLifecycleService` and `PlanningScaffoldService` remain unchanged and the PRD, decision, and design tracking outputs stay direct.
- `Next-step decision`: open one bounded implementation task for the approved first slice and keep broader Phase 4, Phase 5, Phase 6, and Phase 7 work blocked.

## Rationale
- The entry package is now specific enough to review because it names the exact remaining write-path outlier, the preserved public planning boundary, and the rollback-safe convergence seam.
- Reusing the existing coordination-sync orchestration for the five shared outputs is smaller than broader write-path normalization because it does not require changing task lifecycle, planning scaffold, or tracker-family authority rules in the same slice.
- Keeping `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` direct for this slice preserves the current closeout command result contract while isolating one exact duplication seam for proof.

## Links
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)

## Updated At
- `2026-03-15T06:18:27Z`
