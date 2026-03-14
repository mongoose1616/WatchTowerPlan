---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase4_shared_projection_entry"
title: "Structural Rewrite Phase 4 Shared Projection Entry Package"
summary: "Defines the bounded Phase 4 entry checkpoint for shared projection mechanics and a private internal planning graph after the first bounded Phase 3 slice passed outcome review."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-14T06:44:15Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/design/implementation/"
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/repo_ops/"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "rewrite phase 4 entry"
  - "shared projection entry package"
  - "phase 4 projection checkpoint"
---

# Structural Rewrite Phase 4 Shared Projection Entry Package

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase4_shared_projection_entry`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-14T06:44:15Z`

## Summary
Define the bounded Phase 4 entry checkpoint for shared projection mechanics and a private internal planning graph after the first bounded Phase 3 command companion normalization slice passed review, without starting Phase 4 implementation in this change set.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)

## Scope Summary
- Reconfirm the public planning parity boundary before any Phase 4 implementation starts.
- Publish the Phase 4 classification and parity addendum for the projection, sync, and validator-adjacent families that a shared-projection checkpoint could touch.
- Declare the authored truth, derived outputs, current consumers, parity method, and rollback path for the bounded Phase 4 entry question.
- Stop at the review gate for this entry package; do not start shared projection or internal planning-graph implementation in this package.

## Assumptions and Constraints
- The five current planning-authority answers remain the public machine boundary at Phase 4 entry.
- Any internal planning graph introduced in a future Phase 4 slice remains a private runtime detail unless a separate accepted decision creates a new public artifact family.
- This package may define Phase 4 entry conditions, but it may not start shared projection or graph implementation.
- This package does not authorize history cleanup, compatibility retirement, or hotspot-decomposition work.

## Current-State Context
- The first bounded Phase 3 slice has already reconciled the root command page plus the bounded `doctor`, `sync`, and `validate` command docs to the existing command-index implementation paths.
- `watchtower-core sync command-index --format json` remains green and `python -m pytest tests/unit/test_command_index_sync.py` keeps the new fail-closed command-companion drift guard under direct coverage.
- `core/python/src/watchtower_core/cli/registry.py` plus `core/python/src/watchtower_core/cli/parser.py` remain the only accepted command-authority source, and public planning parity remains unchanged after the closed Phase 3 outcome review.
- The next materially different rewrite risk now sits at shared planning projection duplication and the boundary between a possible private internal planning graph and the existing public planning-authority surfaces.

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): Phase 4 still needs a bounded checkpoint package, explicit authored-truth and rollback declarations, and an explicit review outcome before implementation.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): projection, sync, validator, and public planning surfaces touched by Phase 4 must use the controlled four-axis vocabulary.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): Phase 4 may not disturb the public planning-authority boundary while shared projection work is being normalized.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the Phase 4 entry review remains task-backed rather than implied by doc edits alone.

## Proposed Phase 4 Boundary
### In scope for the future phase
- graph assembly from existing governed planning inputs
- shared projection mechanics for `coordination_index`, `planning_catalog`, `initiative_index`, `task_index`, `traceability_index`, and selected human tracker byproducts
- projection dependency ordering, parity or shadow checks, and rollback-bounded sync-path normalization
- any minimal validator or loader-adjacent support required to keep the projection family fail-closed and reviewable

### Explicitly out of scope for this entry package
- changing the five public planning questions or their canonical machine-readable answers
- publishing a new public planning graph artifact family
- history relocation or compatibility retirement
- hotspot-decomposition implementation work

## Phase 4 Classification Addendum
| Surface Family | Current Role | Phase 4 Entry Treatment |
|---|---|---|
| `docs/planning/**` trace records and family trackers | authored authority plus human companion surfaces | Preserve as authored inputs or human byproducts; do not collapse them into hidden runtime-only truth. |
| `core/control_plane/indexes/coordination/coordination_index.v1.json`; `planning_catalog.v1.json`; `initiative_index.v1.json`; `task_index.v1.json`; `traceability_index.v1.json` | canonical machine answers to the five planning questions | Preserve as the public planning contract; any new shared projection logic remains behind these same surfaces. |
| `core/python/src/watchtower_core/repo_ops/sync/coordination_index.py`; `planning_catalog.py`; `initiative_index.py`; `task_index.py`; `traceability.py`; `coordination_tracking.py` | generated-projection builders and tracker emitters | Eligible for bounded normalization only through explicit parity proof and rollback-bounded slices. |
| `core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py`; adjacent shared projection helpers | private runtime support for projection composition | Eligible for refactoring in a later Phase 4 slice, but must remain a private implementation detail rather than a public authority surface. |
| validator or loader-adjacent support that only exists to keep projection assembly fail-closed | supporting infrastructure | Must stay bounded, explicit, and subordinate to the existing authored truth and public planning parity contract. |

## Preliminary Authored Truth and Derived Outputs
### Authored truth to preserve at entry
- `docs/planning/`
- `core/control_plane/registries/authority_map/authority_map.v1.json`

### Derived outputs to keep aligned
- `core/control_plane/indexes/coordination/coordination_index.v1.json`
- `core/control_plane/indexes/planning/planning_catalog.v1.json`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`
- `core/control_plane/indexes/tasks/task_index.v1.json`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`
- selected human planning trackers under `docs/planning/`

### Current consumers to confirm during review
- `watchtower-core query coordination`
- `watchtower-core query planning`
- `watchtower-core query initiatives`
- `watchtower-core query tasks`
- `watchtower-core query trace`
- the sync paths that publish the planning indexes and trackers

## Proposed Technical Approach
- Treat this document as the human Phase 4 entry checkpoint package rather than as implementation authorization.
- Reconfirm the current public planning-authority boundary directly from the live authority map, planning indexes, query surfaces, and human tracking projections.
- Publish the Phase 4 classification addendum for the exact projection, sync, and validator-adjacent families that a shared-projection checkpoint could touch.
- Hand the package to a dedicated review task and stop until that review records an explicit approval or block outcome.

## Work Breakdown
1. Re-verify the current public planning-authority boundary in the live authority map, planning indexes, query surfaces, and trackers.
2. Record the authored truth, derived outputs, current consumers, parity method, and rollback path for Phase 4 entry.
3. Publish the projection-family classification and parity addendum needed for safe Phase 4 review.
4. Route the package through the explicit Phase 4 entry-review task and stop before implementation.

## Entry Questions
- Can shared projection mechanics be introduced without changing the five public planning questions or creating a new public planning graph artifact family?
- Which projection, sync, and validator-adjacent surfaces need explicit Phase 4 classification before implementation starts?
- What is the smallest rollback-safe Phase 4 slice if the entry review approves later work?

## Parity Method
- Re-run:
  - `./.venv/bin/watchtower-core doctor --format json`
  - `./.venv/bin/watchtower-core validate all`
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Inspect the current projection boundary directly in:
  - `core/control_plane/registries/authority_map/authority_map.v1.json`
  - `core/control_plane/indexes/coordination/coordination_index.v1.json`
  - `core/control_plane/indexes/planning/planning_catalog.v1.json`
  - `core/control_plane/indexes/initiatives/initiative_index.v1.json`
  - `core/control_plane/indexes/tasks/task_index.v1.json`
  - `core/control_plane/indexes/traceability/traceability_index.v1.json`
  - `core/python/src/watchtower_core/repo_ops/sync/coordination_index.py`
  - `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py`
  - `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
  - `core/python/src/watchtower_core/repo_ops/sync/task_index.py`
  - `core/python/src/watchtower_core/repo_ops/sync/traceability.py`
- Accept the Phase 4 entry package only if the five public planning answers remain explicit, the internal graph stays private by default, and any future projection slice remains rollback-bounded.

## Rollback Path
1. If review finds the entry package unsound, keep broader rewrite work blocked and do not start Phase 4 implementation.
2. If a later Phase 4 slice drifts beyond the current public planning parity boundary, remove the new shared projection logic and restore the current per-family builders.
3. Rebuild derived planning surfaces and re-run validation plus authority queries before proceeding again.

## Risks
- Shared projection work can create hidden public-boundary drift if an internal graph starts behaving like a new public authority surface.
- Projection-family normalization can widen too quickly if validator, loader, or sync changes are treated as incidental rather than as bounded same-checkpoint work.
- A clean Phase 3 outcome can create false confidence if Phase 4 is treated as implementation-ready before the entry package records its own explicit approval or block outcome.

## Validation Plan
- Re-run `./.venv/bin/watchtower-core doctor --format json`.
- Re-run `./.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Keep Phase 4 blocked unless the review task records an explicit approval outcome for the entry package.

## Stop Condition
- Stop at the explicit Phase 4 review outcome and do not start shared projection or internal planning-graph implementation from this package alone.
- Do not widen this package into compatibility, history, hotspot-decomposition, or public-planning-boundary changes.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)

## Updated At
- `2026-03-14T06:44:15Z`
