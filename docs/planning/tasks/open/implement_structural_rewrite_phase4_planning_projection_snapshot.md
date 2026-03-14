---
id: task.structural_rewrite_program.phase4_planning_projection_snapshot.010
trace_id: trace.structural_rewrite_program
title: Implement structural rewrite Phase 4 planning projection snapshot
summary: Introduce one private trace-scoped planning projection snapshot behind initiative-index and planning-catalog sync without changing the public planning-authority boundary.
type: task
status: active
task_status: ready
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T17:49:25Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/closeout/initiative.py
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py
- core/python/tests/unit/test_coordination_index_sync.py
- core/python/tests/unit/test_initiative_closeout.py
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase4_shared_projection_entry
- design.implementation.structural_rewrite_phase4_planning_projection_snapshot
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase4_entry_review.009
---

# Implement structural rewrite Phase 4 planning projection snapshot

## Summary
Introduce one private trace-scoped planning projection snapshot behind initiative-index and planning-catalog sync without changing the public planning-authority boundary.

## Scope
- Add one private trace-scoped projection snapshot helper for the governed planning inputs shared by `initiative_index` and `planning_catalog`.
- Refactor `InitiativeIndexSyncService` and `PlanningCatalogSyncService` to consume that snapshot while preserving their current public output contracts.
- Keep coordination-sync ordering, mutation callers, tracker emitters, and initiative-closeout behavior stable at the public contract level.

## Done When
- The private snapshot exists only as a runtime implementation detail behind `initiative_index` and `planning_catalog`.
- The five public planning-authority answers and downstream coordination behavior remain unchanged.
- The slice stops with an explicit Phase 4 outcome-review task rather than broader Phase 4 rollout.

## Links
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- [review_structural_rewrite_phase4_shared_projection_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_shared_projection_entry_package.md)

## Updated At
- `2026-03-14T17:49:25Z`
