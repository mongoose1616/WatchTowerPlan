---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase4_planning_projection_snapshot"
title: "Structural Rewrite Phase 4 Planning Projection Snapshot"
summary: "Implements the first bounded Phase 4 slice by introducing a private trace-scoped planning projection snapshot behind initiative-index and planning-catalog sync, then closes cleanly through an explicit outcome review."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T09:55:03Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/src/watchtower_core/repo_ops/"
  - "core/python/src/watchtower_core/closeout/"
  - "core/python/tests/"
  - "docs/planning/tasks/"
aliases:
  - "phase 4 projection snapshot slice"
  - "planning projection snapshot"
  - "phase 4 private planning graph slice"
---

# Structural Rewrite Phase 4 Planning Projection Snapshot

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase4_planning_projection_snapshot`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-15T09:55:03Z`

## Summary
Implement the first bounded Phase 4 slice by introducing one private trace-scoped planning projection snapshot behind `InitiativeIndexSyncService` and `PlanningCatalogSyncService` without changing the five public planning-authority answers, the coordination-sync ordering, or the current mutation-path callers, then close that slice through an explicit outcome review.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [review_structural_rewrite_phase4_shared_projection_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_shared_projection_entry_package.md)

## Scope Summary
- Introduce one private trace-scoped planning projection snapshot over the current governed planning inputs needed by `initiative_index` and `planning_catalog`.
- Refactor `InitiativeIndexSyncService` and `PlanningCatalogSyncService` to consume that shared private snapshot instead of open-coding their overlapping trace-scoped source assembly.
- Preserve the existing coordination-sync ordering, public planning query answers, task and planning mutation callers, and downstream tracker behavior.
- Stop after the bounded slice is synced, validated, and handed to an explicit outcome-review task.

## Assumptions and Constraints
- The private planning projection snapshot remains an implementation detail; it does not become a new governed public artifact family.
- `coordination_index`, `task_index`, and `traceability_index` remain the public machine answers to their current questions.
- `TaskLifecycleService`, `PlanningScaffoldService`, and `InitiativeCloseoutService` keep their current public rebuild behavior for this slice; they are consumers of the changed outputs, not the exact seam under direct refactor.
- The first Phase 4 slice may not widen into hotspot decomposition, compatibility retirement, history cleanup, or broad coordination-orchestration rewrites.
- If the private snapshot does not preserve parity cleanly, rollback restores the current per-family builders in `initiative_index.py` and `planning_catalog.py`.

## Current-State Context
- `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py` now owns the shared trace-scoped planning source assembly and coordination projection needed by `initiative_index` and `planning_catalog`.
- `InitiativeIndexSyncService` and `PlanningCatalogSyncService` now consume the same private snapshot and coordination derivation path, and direct unit coverage asserts that the planning-catalog coordination section matches the initiative projection.
- `CoordinationSyncService` still rebuilds the coordination slice in this order: `task-index`, `traceability-index`, `initiative-index`, `planning-catalog`, `coordination-index`, `task-tracking`, `initiative-tracking`, and `coordination-tracking`.
- `TaskLifecycleService`, `PlanningScaffoldService`, and `InitiativeCloseoutService` still consume that same public projection boundary, and the bounded sync plus closeout suite, `watchtower-core doctor --format json`, `watchtower-core validate all`, and the planning authority or coordination queries all pass after the slice lands.
- The bounded slice outcome review passed, the closeout-coordination entry review approved one bounded successor slice, that successor slice landed through [implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md), that slice then passed its own explicit outcome review through [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md), the closeout-tracking entry review then passed through [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md), the approved closeout-tracking refresh-boundary slice landed through [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md), and the trace then closed through [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md) instead of broader Phase 4 rollout.

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the slice must name one exact builder seam, publish authored truth and rollback notes, and stop at an explicit successor review.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): the slice keeps public planning surfaces classified as canonical machine answers and the private snapshot classified as a runtime implementation detail only.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the five public planning-authority answers remain unchanged while the private snapshot normalizes internal projection mechanics.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): downstream initiative and coordination projections must keep their phase, owner, and next-step semantics stable through the refactor.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the runtime change remains inside `core/python/src/watchtower_core/repo_ops/` with targeted tests under `core/python/tests/`.

## Proposed Technical Approach
- Add one private helper-backed trace-scoped planning projection snapshot under `watchtower_core.repo_ops` that assembles the governed per-trace source set required by `initiative_index` and `planning_catalog`.
- Keep the helper private to repo-local orchestration code; do not add a new public CLI command, control-plane artifact family, or export-safe API boundary.
- Refactor `InitiativeIndexSyncService` to derive its active-task summaries, coordination section, and initiative projection from that snapshot rather than from open-coded grouped source collections alone.
- Refactor `PlanningCatalogSyncService` to consume the same snapshot for its trace-scoped planning inputs while preserving the existing planning-catalog payload shape and ordering.
- Leave `CoordinationIndexSyncService`, tracker emitters, mutation callers, and initiative-closeout orchestration behavior unchanged except for the downstream outputs they already consume.

## Work Breakdown
1. Introduce a private trace-scoped planning projection snapshot helper and supporting data shape under `watchtower_core.repo_ops`.
2. Refactor `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py` to consume the snapshot and preserve its current public payload semantics.
3. Refactor `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py` to consume the same snapshot and preserve its current public payload semantics.
4. Extend direct sync coverage for `initiative_index`, `planning_catalog`, and coordination or closeout-adjacent parity expectations touched by the new private snapshot.
5. Rebuild the affected planning surfaces, validate the repo, and stop with one explicit Phase 4 outcome-review task instead of broadening the rewrite.

## Implementation Outcome
- The slice now publishes `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py` as the single private trace-scoped planning projection helper and keeps the shared graph behind the existing public planning answers.
- `PlanningCatalogSyncService` no longer depends on a separately loaded initiative index to build its coordination section; both sync services now derive that shared coordination view from the same trace snapshot.
- `core/python/tests/unit/test_planning_catalog_sync.py` now includes direct parity coverage for the initiative-versus-planning coordination projection, and the bounded sync plus closeout suite passed `18` tests before the repo-wide sync and validation reruns.
- The slice closed cleanly through [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md), the successor closeout-coordination entry review passed through [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md), and the trace now points to one bounded closeout coordination sync-reuse slice rather than broader rollout.

## Risks
- The private snapshot can become an accidental shadow authority if the slice starts treating it as public truth instead of a runtime composition helper.
- `initiative_index` and `planning_catalog` can drift apart if the shared snapshot does not preserve the same phase, owner, task, and related-path semantics the current per-family builders emit.
- A slice that only checks query parity can miss regressions in downstream tracker emission or initiative-closeout rebuild behavior.

## Validation Plan
- Re-run `./.venv/bin/watchtower-core doctor --format json`.
- Re-run `./.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Re-run targeted sync coverage:
  - `./.venv/bin/python -m pytest tests/unit/test_initiative_index_sync.py`
  - `./.venv/bin/python -m pytest tests/unit/test_planning_catalog_sync.py`
  - `./.venv/bin/python -m pytest tests/unit/test_coordination_index_sync.py`
  - `./.venv/bin/python -m pytest tests/unit/test_initiative_closeout.py`

## References
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)
- [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)
- [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)
- [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)

## Updated At
- `2026-03-15T09:55:03Z`
