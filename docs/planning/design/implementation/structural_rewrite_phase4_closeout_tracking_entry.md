---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase4_closeout_tracking_entry"
title: "Structural Rewrite Phase 4 Closeout Tracking Entry Package"
summary: "Defines the bounded next Phase 4 checkpoint for reviewing the remaining direct PRD, decision, and design tracking refresh step in InitiativeCloseoutService after the closeout coordination sync-reuse slice passed review."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T09:55:03Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/design/implementation/"
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/closeout/"
  - "core/python/src/watchtower_core/repo_ops/sync/"
aliases:
  - "rewrite phase 4 closeout tracking entry"
  - "phase 4 closeout tracker refresh checkpoint"
  - "phase 4 closeout tracking checkpoint"
---

# Structural Rewrite Phase 4 Closeout Tracking Entry Package

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase4_closeout_tracking_entry`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-15T09:55:03Z`

## Summary
Define the bounded next Phase 4 checkpoint for reviewing whether the remaining direct `prd`, `decision`, and `design` tracking refresh step inside `InitiativeCloseoutService.close` may converge through one later bounded seam after the closeout coordination sync-reuse slice passed review, and keep broader Phase 4 and later-phase implementation blocked in this change set.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)

## Scope Summary
- Reconfirm the public planning parity boundary after the bounded Phase 4 closeout coordination sync-reuse slice passed review.
- Publish the Phase 4 classification and parity addendum for the remaining direct closeout planning-tracker refresh step versus the already-approved shared coordination seam.
- Declare the authored truth, derived outputs, current consumers, parity method, and rollback path for the next closeout-tracking entry question.
- Stop broader implementation at one explicit review task; do not treat this package as standing authorization for further Phase 4 or later-phase work.

## Assumptions and Constraints
- The five current planning-authority answers remain the public machine boundary at this checkpoint.
- `planning_projection_snapshot.py` remains a private runtime detail and does not become a governed public artifact family.
- The approved shared closeout seam remains fixed: `traceability_output_path` stays pre-seam, `CoordinationSyncService.run_closeout_shared_outputs` remains limited to `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking`, and `TaskLifecycleService` plus `PlanningScaffoldService` remain outside this checkpoint.
- This package may define the next Phase 4 entry conditions, but it may not start closeout tracking implementation.
- This package does not authorize changing coordination-sync targets or ordering, changing the shared closeout seam, changing task-lifecycle or scaffold write behavior, broader tracker-family redesign, hotspot decomposition, compatibility retirement, or Phase 5 work.

## Current-State Context
- The bounded closeout coordination sync-reuse slice has now passed its explicit outcome review after proving that `InitiativeCloseoutService.close` can reuse `CoordinationSyncService` for the approved five shared post-traceability outputs without changing the five public planning-authority answers or the current closeout result contract boundary.
- `InitiativeCloseoutService.close` now writes traceability first, then refreshes `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking` through `CoordinationSyncService.run_closeout_shared_outputs(write=True)`, but it still writes `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` directly afterward.
- The closeout command still publishes an explicit result contract with individual output-path fields for the traceability write, the approved shared coordination outputs, and the remaining direct PRD, decision, and design tracking outputs.
- The `.015` review then passed for one bounded successor slice, that slice is now defined by [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md), landed through [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md), and closed through [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md), which recorded one explicit structural-rewrite program closeout decision instead of broader Phase 4 rollout.

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the next Phase 4 checkpoint still needs a bounded package, explicit authored-truth and rollback declarations, and an explicit review outcome before any later implementation begins.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): closeout, tracker, and public planning surfaces touched by the next checkpoint must keep using the controlled four-axis vocabulary.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the next checkpoint may not disturb the public planning-authority boundary while the remaining closeout tracker step is being reviewed.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the next Phase 4 review remains task-backed rather than implied by doc edits alone.

## Proposed Phase 4 Boundary
### In scope for the future phase
- the remaining direct initiative-closeout tracker refresh step for `prd-tracking`, `decision-tracking`, and `design-tracking`
- reuse of one private repo-local helper or one minimal explicit refresh boundary for those three tracker outputs only after the already-approved shared coordination seam completes
- parity and rollback checks for the closeout tracker refresh step only
- any minimal result-contract or direct-test updates required to preserve the current closeout command surface

### Explicitly out of scope for this entry package
- changing the five public planning questions or their canonical machine-readable answers
- changing the approved shared coordination seam or the current `CoordinationSyncService` target ordering
- changing `TaskLifecycleService` or `PlanningScaffoldService` write behavior
- broader tracker-family redesign or broad planning-document refresh redesign
- hotspot decomposition, compatibility retirement, or later-phase rollout

## Current Tracker Refresh Boundary
- `InitiativeCloseoutService.close` still writes `prd-tracking`, `decision-tracking`, and `design-tracking` directly after the approved shared coordination seam completes.
- The three tracker services remain explicit repo-local sync surfaces with deterministic `watchtower-core sync prd-tracking`, `decision-tracking`, and `design-tracking` command families.
- No current checkpoint authorizes pulling those tracker targets into `CoordinationSyncService` or changing their public CLI family names.

## Preliminary Authored Truth and Derived Outputs
### Authored truth to preserve at entry
- `docs/planning/`
- `core/control_plane/registries/authority_map/authority_map.v1.json`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

### Derived outputs to keep aligned
- `docs/planning/prds/prd_tracking.md`
- `docs/planning/design/design_tracking.md`
- `docs/planning/decisions/decision_tracking.md`

### Current consumers to confirm during review
- `watchtower-core closeout initiative`
- `watchtower-core sync prd-tracking`
- `watchtower-core sync decision-tracking`
- `watchtower-core sync design-tracking`
- the write-mode closeout result payload and the tracking docs it refreshes

## Proposed Technical Approach
- Treat this document as the human next Phase 4 entry checkpoint package rather than as implementation authorization.
- Reconfirm the current public planning-authority boundary, the approved shared closeout coordination seam, and the remaining direct tracker refresh step directly from the live authority map, planning indexes, query surfaces, and closeout behavior.
- Publish the write-path classification and parity addendum for the exact closeout, tracker, and public planning surfaces that a bounded later tracker-refresh slice could touch.
- Hand the package to a dedicated review task and stop until that review records an explicit approval or block outcome for one exact remaining tracker seam.

## Review-Resolved Entry Questions
- `Public planning boundary`: reaffirmed. The five current planning-authority answers remain the explicit public machine boundary for the approved closeout-tracking slice.
- `Approved shared closeout seam`: reaffirmed. `traceability_output_path` remains pre-seam, the approved shared coordination outputs remain fixed, and the review does not authorize adding the tracker targets to `CoordinationSyncService`.
- `Closeout result contract boundary`: explicit. `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain individually reported output-path fields in both `InitiativeCloseoutResult` and the closeout CLI payload.
- `Approved first slice`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- `Exact seam`: one private closeout-local refresh boundary for the three remaining tracker outputs after the approved shared closeout seam completes, while `watchtower-core sync prd-tracking`, `decision-tracking`, and `design-tracking` remain the canonical public sync families.

## Work Breakdown
1. Re-verify the public planning-authority boundary and the approved shared closeout seam after the closed closeout coordination sync-reuse outcome review.
2. Record the authored truth, derived outputs, current consumers, remaining direct output-path boundary, parity method, and rollback path for the next closeout-tracking entry question.
3. Publish the write-path classification addendum needed for safe Phase 4 review, including the remaining direct tracker-refresh step and the already-approved shared coordination seam that must stay unchanged.
4. Route the package through the explicit Phase 4 closeout-tracking review task, approve or block one exact next seam, and stop broader implementation at that named checkpoint.

## Entry Questions
- Can `InitiativeCloseoutService.close` normalize the remaining direct `prd`, `decision`, and `design` tracking refresh step without changing the approved shared coordination seam, the public planning-authority answers, or the closeout command result contract?
- Which closeout output-path fields, tracker-refresh guarantees, and explicit directness guarantees must remain stable if a later tracker-refresh seam is approved?
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
  - `core/python/src/watchtower_core/cli/closeout_handlers.py`
  - `core/python/src/watchtower_core/repo_ops/sync/prd_tracking.py`
  - `core/python/src/watchtower_core/repo_ops/sync/decision_tracking.py`
  - `core/python/src/watchtower_core/repo_ops/sync/design_tracking.py`
  - `core/control_plane/indexes/traceability/traceability_index.v1.json`
  - `docs/planning/prds/prd_tracking.md`
  - `docs/planning/design/design_tracking.md`
  - `docs/planning/decisions/decision_tracking.md`
- Accept the entry package only if the five public planning answers remain explicit, the approved shared closeout seam stays unchanged, and any later tracker-refresh slice remains rollback-bounded.

## Rollback Path
1. If review finds the entry package unsound, keep broader rewrite work blocked and do not start further Phase 4 implementation.
2. If an approved later slice drifts beyond the current public planning parity boundary, the approved shared closeout seam, or the explicit closeout result contract, restore the current direct `InitiativeCloseoutService` tracker refresh step after the shared coordination outputs complete.
3. Rebuild derived planning surfaces and re-run validation plus authority queries before proceeding again.

## Risks
- Tracker-refresh convergence can create hidden behavioral drift if initiative closeout stops matching the current closeout result contract or silently widens the already-approved shared coordination seam.
- A tracker-only checkpoint can still widen unsafely if it starts redesigning broader tracker families or planning-document refresh behavior instead of isolating the three remaining direct outputs.
- A clean shared-output seam can create false confidence if the next checkpoint is allowed to act like broader mutation-path or tracker-family approval rather than one bounded remaining outlier question.

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
- Keep broader Phase 4 blocked unless the review task records an explicit approval outcome for one exact remaining closeout tracker seam.

## Stop Condition
- Stop at the bounded Phase 4 closeout-tracking refresh-boundary outcome review and keep broader Phase 4 rollout blocked unless that review records an explicit decision.
- Do not widen this package into broader tracker-family rollout, changes to the approved shared coordination seam, task-lifecycle or scaffold mutation changes, public-planning-boundary changes, or later phases.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)
- [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- [watchtower_core_closeout_initiative.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_closeout_initiative.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)

## Updated At
- `2026-03-15T09:55:03Z`
