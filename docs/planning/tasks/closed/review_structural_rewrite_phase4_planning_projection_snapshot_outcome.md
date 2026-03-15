---
id: task.structural_rewrite_program.phase4_planning_projection_snapshot_review.011
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 4 planning projection snapshot outcome
summary: Review the bounded Phase 4 planning projection snapshot slice, confirm the shared private snapshot held public planning parity, and decide whether broader rewrite work remains blocked or may proceed to a new bounded checkpoint.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-15T03:11:32Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md
- docs/planning/design/implementation/structural_rewrite_program.md
- docs/planning/tasks/closed/implement_structural_rewrite_phase4_planning_projection_snapshot.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot.v1.json
- core/control_plane/indexes/coordination/coordination_index.v1.json
- core/control_plane/indexes/initiatives/initiative_index.v1.json
- core/control_plane/indexes/planning/planning_catalog.v1.json
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
- design.implementation.structural_rewrite_phase4_planning_projection_snapshot
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase4_planning_projection_snapshot.010
---

# Review structural rewrite Phase 4 planning projection snapshot outcome

## Summary
Review the bounded Phase 4 planning projection snapshot slice, confirm the shared private snapshot held public planning parity, and decide whether broader rewrite work remains blocked or may proceed to a new bounded checkpoint.

## Scope
- Confirm the new private trace-scoped planning projection snapshot remains a runtime-only helper behind `initiative_index` and `planning_catalog`.
- Confirm `InitiativeIndexSyncService` and `PlanningCatalogSyncService` now share one coordination projection path while preserving the same public planning-authority answers and downstream coordination behavior.
- Confirm the coordination-sync ordering, mutation-path callers, and initiative-closeout rebuild path remain stable at the public contract boundary.
- Decide whether the rewrite stays blocked at this review or may proceed to a new explicit bounded checkpoint.

## Done When
- The review records an explicit pass or block outcome for the bounded Phase 4 slice.
- Any proposed next step is framed as a new explicit checkpoint rather than implied broader rollout.
- No broader Phase 4 or later-phase rewrite work is implied by this slice alone.

## Review Outcome
- `Decision`: passed; the bounded Phase 4 slice proved one private trace-scoped planning projection snapshot can be shared by `initiative_index` and `planning_catalog` without public planning drift.
- `Parity result`: passed. `watchtower-core doctor --format json`, `watchtower-core validate all`, `watchtower-core query authority --domain planning --format json`, `watchtower-core query coordination --format json`, and `watchtower-core query planning --trace-id trace.structural_rewrite_program --format json` all remained green after the slice landed.
- `Boundary result`: unchanged. `planning_projection_snapshot.py` remains a private runtime helper behind `initiative_index` and `planning_catalog`, and the coordination-sync ordering, tracker emitters, mutation callers, and initiative-closeout public behavior remain stable at the current public contract boundary.
- `Next-step decision`: do not broaden Phase 4 rollout. Open one bounded Phase 4 closeout-coordination entry package and review gate for the single remaining direct write-path outlier in the reviewed consumer boundary, and keep broader Phase 4 plus Phase 5, Phase 6, and Phase 7 work blocked.

## Rationale
- The first Phase 4 slice already proved the safety property it was supposed to prove: two read-side planning projections can share one private trace-scoped snapshot without changing the five public planning-authority answers.
- The next materially different rewrite risk now sits at the write-path boundary, where `TaskLifecycleService` and `PlanningScaffoldService` already rebuild through `CoordinationSyncService` but `InitiativeCloseoutService` still performs its own adjacent planning and coordination rebuild chain directly.
- Opening a bounded entry package for that exact outlier advances the rewrite without implying broader shared-projection rollout or later-phase work.

## Links
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- [implement_structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_planning_projection_snapshot.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)
- [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)

## Updated At
- `2026-03-15T03:11:32Z`
