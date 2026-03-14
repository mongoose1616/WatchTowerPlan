---
id: task.structural_rewrite_program.phase4_entry_review.009
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 4 shared projection entry package
summary: Review the bounded Phase 4 shared-projection entry package, confirm the public planning parity and private-graph guardrails, and decide whether bounded Phase 4 work may begin.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T17:49:25Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_program.md
- docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md
- docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/indexes/coordination/coordination_index.v1.json
- core/control_plane/indexes/planning/planning_catalog.v1.json
- core/control_plane/indexes/initiatives/initiative_index.v1.json
- core/control_plane/indexes/tasks/task_index.v1.json
- core/control_plane/indexes/traceability/traceability_index.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase4_shared_projection_entry
- design.implementation.structural_rewrite_phase4_planning_projection_snapshot
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase3_command_companion_source_surface_normalization_review.008
---

# Review structural rewrite Phase 4 shared projection entry package

## Summary
Review the bounded Phase 4 shared-projection entry package, confirm the public planning parity and private-graph guardrails, and decide whether bounded Phase 4 work may begin.

## Scope
- Confirm that the five current planning-authority answers remain the explicit public boundary at Phase 4 entry.
- Confirm that any internal planning graph remains a private runtime detail unless a separate accepted decision changes that boundary.
- Confirm that the Phase 4 classification and parity addendum is explicit for the projection, sync, and validator-adjacent families touched by the proposed checkpoint.
- Decide whether Phase 4 may proceed through one bounded checkpoint or remains blocked.

## Done When
- The review records an explicit approve or block outcome for the Phase 4 entry package.
- Any approved Phase 4 slice remains bounded, parity-backed, and rollback-explicit.
- No Phase 4 implementation work begins before this task reaches an explicit terminal outcome.

## Review Outcome
- `Decision`: approved for exactly one bounded Phase 4 slice.
- `Public planning boundary`: reaffirmed. `watchtower-core query authority --domain planning --format json` still resolves the same five planning-authority answers, and the review does not authorize any public planning-boundary change.
- `Private internal-graph boundary`: reaffirmed. Any internal planning graph introduced by the first Phase 4 slice remains a private runtime detail rather than a new public artifact family.
- `Consumer boundary`: explicit. The reviewed boundary now carries the coordination-sync group ordering (`task-index` -> `traceability-index` -> `initiative-index` -> `planning-catalog` -> `coordination-index` -> `task-tracking` -> `initiative-tracking` -> `coordination-tracking`), the task lifecycle and planning scaffold write paths that already call `CoordinationSyncService`, the direct initiative-closeout rebuild path, and the downstream tracker emitters the first slice can affect.
- `Approved first slice`: [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- `Exact seam`: one private trace-scoped planning projection snapshot consumed by `InitiativeIndexSyncService` and `PlanningCatalogSyncService`. `task_index`, `traceability_index`, `coordination_index`, tracker emitters, and mutation callers remain on their current public outputs for this first slice.
- `Next-step decision`: open one bounded implementation task for the approved first slice and keep broader Phase 4, Phase 5, Phase 6, and Phase 7 work blocked.

## Rationale
- The current entry package is sound once the live coordination-sync ordering, mutation-path callers, and touched tracker emitters are named explicitly instead of left implied.
- The private trace-scoped snapshot seam is smaller than broader coordination or closeout orchestration normalization and therefore better matches the first Phase 4 proof obligation.
- Refactoring `initiative_index` and `planning_catalog` behind one private snapshot is enough to prove shared-projection reuse and private-graph discipline without reopening the five public planning answers.

## Links
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- [implement_structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/tasks/open/implement_structural_rewrite_phase4_planning_projection_snapshot.md)
- [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)

## Updated At
- `2026-03-14T17:49:25Z`
