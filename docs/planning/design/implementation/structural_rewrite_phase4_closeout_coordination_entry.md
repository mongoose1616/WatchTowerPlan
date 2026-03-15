---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase4_closeout_coordination_entry"
title: "Structural Rewrite Phase 4 Closeout Coordination Entry Package"
summary: "Defines the bounded Phase 4 checkpoint for aligning the initiative-closeout write path with the existing coordination-sync orchestration after the first private planning projection snapshot slice passed review."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T07:14:50Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/design/implementation/"
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/repo_ops/"
  - "core/python/src/watchtower_core/closeout/"
aliases:
  - "rewrite phase 4 closeout entry"
  - "phase 4 closeout coordination checkpoint"
  - "phase 4 write-path convergence entry"
---

# Structural Rewrite Phase 4 Closeout Coordination Entry Package

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase4_closeout_coordination_entry`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-15T07:14:50Z`

## Summary
Define the bounded next Phase 4 checkpoint for aligning the `InitiativeCloseoutService` write path with the existing coordination-sync orchestration after the first bounded private planning projection snapshot slice passed review, and keep broader Phase 4 and later-phase implementation blocked in this change set.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)

## Scope Summary
- Reconfirm the public planning parity boundary after the first bounded Phase 4 shared private snapshot slice passed review.
- Publish the Phase 4 classification and parity addendum for the direct initiative-closeout rebuild path versus the existing coordination-sync orchestration boundary.
- Declare the authored truth, derived outputs, current consumers, parity method, and rollback path for the next closeout-coordination entry question.
- Stop broader implementation at one explicit review task; do not treat this package as standing authorization for further Phase 4 or later-phase work.

## Assumptions and Constraints
- The five current planning-authority answers remain the public machine boundary at this checkpoint.
- `planning_projection_snapshot.py` remains a private runtime detail and does not become a governed public artifact family.
- `TaskLifecycleService` and `PlanningScaffoldService` already rebuild through `CoordinationSyncService.run(write=True)` and remain outside the exact future implementation seam for this checkpoint.
- This package may define the next Phase 4 entry conditions, but it may not start closeout-orchestration implementation.
- This package does not authorize broader coordination-sync reordering, hotspot decomposition, compatibility retirement, or Phase 5 work.

## Current-State Context
- The first bounded Phase 4 slice has now passed its explicit outcome review after proving that `InitiativeIndexSyncService` and `PlanningCatalogSyncService` can share one private trace-scoped planning projection snapshot without changing the five public planning-authority answers.
- `TaskLifecycleService.create`, `update`, and `transition` plus `PlanningScaffoldService.scaffold` and `bootstrap` already rebuild the planning and coordination slice through `CoordinationSyncService.run(write=True)` when they mutate traced planning state.
- `InitiativeCloseoutService.close` still writes traceability and then rebuilds the adjacent `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking` surfaces directly instead of flowing through the existing coordination-sync orchestration.
- The closeout command also publishes a result contract with individual output-path fields for the traceability, initiative, planning-catalog, coordination, and tracker surfaces it rebuilds.
- The `.012` review passed for one bounded successor slice, that slice landed through [implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md), its outcome review then passed through [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md), and the next active checkpoint is [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/open/review_structural_rewrite_phase4_closeout_tracking_entry_package.md), not broader Phase 4 rollout.

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the next Phase 4 checkpoint still needs a bounded package, explicit authored-truth and rollback declarations, and an explicit review outcome before any later implementation begins.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): closeout, orchestration, tracker, and public planning surfaces touched by the next checkpoint must keep using the controlled four-axis vocabulary.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the next checkpoint may not disturb the public planning-authority boundary while write-path convergence is being reviewed.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the next Phase 4 review remains task-backed rather than implied by doc edits alone.

## Proposed Phase 4 Boundary
### In scope for the future phase
- initiative-closeout write-path orchestration for the planning and coordination outputs it already rebuilds
- reuse of the existing coordination-sync ordering or one private shared helper after the traceability write completes
- parity and rollback checks for the closeout write path only
- any minimal result-contract or test updates required to preserve the current closeout command surface

### Explicitly out of scope for this entry package
- changing the five public planning questions or their canonical machine-readable answers
- changing `TaskLifecycleService` or `PlanningScaffoldService` write behavior
- broader coordination-sync target reordering or tracker-family redesign
- hotspot decomposition, compatibility retirement, or later-phase rollout

## Phase 4 Classification Addendum
| Surface Family | Current Role | Phase 4 Entry Treatment |
|---|---|---|
| `core/python/src/watchtower_core/closeout/initiative.py`; closeout command docs | traced initiative terminal-state mutation and write-mode output reporting | Eligible for bounded orchestration normalization only if the acceptance gate, output-path contract, and public planning parity stay intact. |
| `core/python/src/watchtower_core/repo_ops/sync/coordination.py`; `registry.py` | canonical coordination-sync ordering and orchestration boundary | Preserve as the current write-path contract; later reuse must stay rollback-bounded and explicit. |
| `core/control_plane/indexes/coordination/coordination_index.v1.json`; `planning_catalog.v1.json`; `initiative_index.v1.json`; selected human trackers | canonical public planning answers and human byproducts | Preserve unchanged while the next checkpoint evaluates one closeout write-path convergence seam. |
| `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py`; adjacent sync services | private runtime projection helpers | May support a later closeout seam but remain private implementation detail rather than new public authority. |

## Current Write-Side Caller Comparison
- `TaskLifecycleService.create`, `update`, and `transition` rebuild the coordination slice through `CoordinationSyncService.run(write=True)`.
- `PlanningScaffoldService.scaffold` and `bootstrap` rebuild the coordination slice through `CoordinationSyncService.run(write=True)` when the trace already participates in coordination.
- `InitiativeCloseoutService.close` currently writes traceability first and then rebuilds `InitiativeIndexSyncService`, `PlanningCatalogSyncService`, `CoordinationIndexSyncService`, `InitiativeTrackingSyncService`, and `CoordinationTrackingSyncService` directly.

## Preliminary Authored Truth and Derived Outputs
### Authored truth to preserve at entry
- `docs/planning/`
- `core/control_plane/registries/authority_map/authority_map.v1.json`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

### Derived outputs to keep aligned
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`
- `core/control_plane/indexes/planning/planning_catalog.v1.json`
- `core/control_plane/indexes/coordination/coordination_index.v1.json`
- `docs/planning/initiatives/initiative_tracking.md`
- `docs/planning/coordination_tracking.md`

### Current consumers to confirm during review
- `watchtower-core closeout initiative`
- `watchtower-core query coordination`
- `watchtower-core query planning`
- the write-mode closeout result payload and the tracker surfaces it refreshes

## Proposed Technical Approach
- Treat this document as the human next Phase 4 entry checkpoint package rather than as implementation authorization.
- Reconfirm the current public planning-authority boundary directly from the live authority map, planning indexes, query surfaces, and closeout behavior.
- Publish the write-path classification and parity addendum for the exact closeout and orchestration surfaces that a bounded convergence slice could touch.
- Hand the package to a dedicated review task and stop until that review records an explicit approval or block outcome for one exact seam.

## Review-Resolved Entry Questions
- `Public planning boundary`: reaffirmed. The five current planning-authority answers remain the explicit public machine boundary for the approved closeout slice.
- `Remaining direct outlier`: reaffirmed. `InitiativeCloseoutService.close` remains the only approved write-path convergence target in the reviewed consumer boundary.
- `Closeout result contract boundary`: explicit. `traceability_output_path` remains the pre-seam write, the approved shared-output seam is limited to `initiative_index_output_path`, `planning_catalog_output_path`, `coordination_index_output_path`, `initiative_tracking_output_path`, and `coordination_tracking_output_path`, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain direct outputs outside the approved seam.
- `Approved first slice`: [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- `Exact seam`: one post-traceability closeout step that reuses `CoordinationSyncService` for the shared planning and coordination outputs only while leaving `TaskLifecycleService`, `PlanningScaffoldService`, and the direct PRD, decision, and design tracking outputs unchanged.

## Work Breakdown
1. Re-verify the public planning-authority boundary after the closed Phase 4 planning projection snapshot outcome review.
2. Record the authored truth, derived outputs, current consumers, closeout result contract, parity method, and rollback path for this next entry question.
3. Publish the write-path classification addendum needed for safe Phase 4 review, including the existing coordination-sync ordering and the direct closeout rebuild outlier.
4. Route the package through the explicit Phase 4 closeout-coordination review task, approve or block one exact slice, and stop broader implementation at that named successor task.

## Entry Questions
- Can `InitiativeCloseoutService.close` reuse the existing coordination-sync orchestration after its traceability write without changing public planning outputs or the closeout command's result contract?
- Which closeout output-path fields, acceptance-gating semantics, and tracker refresh guarantees must remain stable?
- What is the smallest rollback-safe future slice if the review approves later work?

## Parity Method
- Re-run:
  - `./core/python/.venv/bin/watchtower-core doctor --format json`
  - `./core/python/.venv/bin/watchtower-core validate all`
  - `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./core/python/.venv/bin/watchtower-core query coordination --format json`
  - `./core/python/.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Inspect the current write-path boundary directly in:
  - `core/python/src/watchtower_core/closeout/initiative.py`
  - `core/python/src/watchtower_core/repo_ops/sync/coordination.py`
  - `core/python/src/watchtower_core/repo_ops/sync/registry.py`
  - `core/control_plane/indexes/traceability/traceability_index.v1.json`
  - `core/control_plane/indexes/initiatives/initiative_index.v1.json`
  - `core/control_plane/indexes/planning/planning_catalog.v1.json`
  - `core/control_plane/indexes/coordination/coordination_index.v1.json`
- Accept the entry package only if the five public planning answers remain explicit, the private planning graph stays private, and the next write-path slice remains rollback-bounded.

## Rollback Path
1. If review finds the entry package unsound, keep broader rewrite work blocked and do not start further Phase 4 implementation.
2. If an approved later slice drifts beyond the current public planning parity boundary or the closeout result contract, restore the current direct `InitiativeCloseoutService` rebuild chain after the traceability write.
3. Rebuild derived planning surfaces and re-run validation plus authority queries before proceeding again.

## Risks
- Write-path convergence can create hidden behavioral drift if initiative closeout stops matching the existing coordination-sync ordering or the current closeout result contract.
- A closeout-only checkpoint can still widen unsafely if it starts changing all mutation callers or public planning outputs instead of isolating the remaining direct outlier.
- A clean first Phase 4 slice can create false confidence if the next checkpoint is allowed to act like broader shared-projection approval rather than one bounded write-path question.

## Validation Plan
- Re-run `./core/python/.venv/bin/watchtower-core doctor --format json`.
- Re-run `./core/python/.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./core/python/.venv/bin/watchtower-core query coordination --format json`
  - `./core/python/.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_initiative_closeout.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_initiative_index_sync.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_planning_catalog_sync.py`
  - `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_coordination_index_sync.py`
- Keep broader Phase 4 blocked unless the review task records an explicit approval outcome for one exact closeout-coordination seam.

## Stop Condition
- Stop at the explicit Phase 4 closeout-coordination review outcome and hand off only to the approved first slice task if the review passes.
- Do not widen this package into broader shared-projection rollout, task-lifecycle or scaffold mutation changes, public-planning-boundary changes, or later phases.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)
- [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)

## Updated At
- `2026-03-15T07:14:50Z`
