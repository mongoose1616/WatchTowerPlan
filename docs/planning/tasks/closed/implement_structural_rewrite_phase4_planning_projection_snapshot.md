---
id: task.structural_rewrite_program.phase4_planning_projection_snapshot.010
trace_id: trace.structural_rewrite_program
title: Implement structural rewrite Phase 4 planning projection snapshot
summary: Introduce one private trace-scoped planning projection snapshot behind initiative-index and planning-catalog sync without changing the public planning-authority boundary.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T18:27:09Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md
- docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot.v1.json
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
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

## Outcome
- The slice adds `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py` as the single private trace-scoped planning projection helper and moves the shared coordination derivation behind that runtime-only seam.
- `InitiativeIndexSyncService` and `PlanningCatalogSyncService` now consume the same trace-scoped snapshot and coordination projection while preserving the current initiative-index and planning-catalog public payload contracts.
- Direct parity coverage now asserts that the planning-catalog coordination section matches the initiative projection, the bounded sync and closeout suite passed, and the slice stops at an explicit Phase 4 outcome-review task instead of broader rollout.

## Links
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- [review_structural_rewrite_phase4_shared_projection_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_shared_projection_entry_package.md)
- [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)

## Updated At
- `2026-03-14T18:27:09Z`
