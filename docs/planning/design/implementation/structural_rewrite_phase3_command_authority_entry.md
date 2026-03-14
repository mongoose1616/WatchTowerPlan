---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase3_command_authority_entry"
title: "Structural Rewrite Phase 3 Command Authority Entry Package"
summary: "Defines the bounded Phase 3 entry checkpoint for command authority normalization and records the approved first command companion normalization slice."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-14T05:41:11Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/design/implementation/"
  - "docs/planning/tasks/"
  - "docs/commands/core_python/"
  - "core/control_plane/indexes/commands/"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "rewrite phase 3 entry"
  - "command authority entry package"
  - "phase 3 command normalization checkpoint"
---

# Structural Rewrite Phase 3 Command Authority Entry Package

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase3_command_authority_entry`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-14T05:41:11Z`

## Summary
Define the bounded Phase 3 entry checkpoint for command authority normalization and record the approved first rollback-safe command companion normalization slice without starting Phase 3 implementation in this change set.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_artifact_role_registry_pilot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_artifact_role_registry_pilot_outcome.md)

## Scope Summary
- Reconfirm the command-authority boundary before any Phase 3 implementation starts.
- Declare the intended authored truth, derived outputs, consumers, parity method, and rollback path for bounded command-authority normalization work.
- Publish any command-adjacent workflow, route, or compatibility classification detail needed for the Phase 3 checkpoint.
- Stop at the review gate for this entry package; do not start Phase 3 implementation in this package.

## Assumptions and Constraints
- The current CLI registry and parser tree remain the only accepted machine authority for command presence and hierarchy at Phase 3 entry.
- The public planning-authority parity boundary is unchanged by this package.
- This package may define Phase 3 entry conditions, but it may not start command-authority normalization implementation.
- Any command-adjacent workflow, route, or compatibility classification published here must stay bounded to the Phase 3 entry question.

## Current-State Context
- The bounded artifact-role registry pilot passed its follow-up review with `watchtower-core validate all`, `watchtower-core query authority --domain planning --format json`, `watchtower-core query coordination --format json`, and `watchtower-core query planning --trace-id trace.structural_rewrite_program --format json` still showing clean parity.
- The artifact-role registry still has no runtime consumers beyond schema-backed validation and review surfaces.
- Command presence and hierarchy remain authored in the live CLI registry and parser tree under `core/python/src/watchtower_core/cli/registry.py` and `core/python/src/watchtower_core/cli/parser.py`.
- The current generated command companion surfaces remain `core/control_plane/indexes/commands/command_index.v1.json` and `docs/commands/core_python/`.
- The next safe step is therefore a bounded Phase 3 entry review, not another broader Phase 2 metadata slice and not direct Phase 3 implementation.

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): Phase 3 still needs a bounded checkpoint package, explicit authored-truth and rollback declarations, and an explicit review outcome before implementation.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): command-adjacent workflow, route, and compatibility surfaces touched by Phase 3 must use the controlled four-axis vocabulary.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): Phase 3 may not disturb the public planning-authority boundary while command authority work is being normalized.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the Phase 3 entry review remains task-backed rather than implied by doc edits alone.

## Proposed Phase 3 Boundary
### In scope for the future phase
- command registry metadata tightening
- parser-backed introspection normalization
- command-index generation alignment
- command-doc structural metadata derivation
- source-surface metadata reconciliation

### Explicitly out of scope for this entry package
- changing command presence or hierarchy authority away from the current CLI registry and parser tree
- Phase 3 implementation work
- public planning-authority changes
- artifact-role metadata expansion into runtime selection behavior

## Preliminary Authored Truth and Derived Outputs
### Authored truth to preserve at entry
- `core/python/src/watchtower_core/cli/registry.py`
- `core/python/src/watchtower_core/cli/parser.py`

### Derived outputs to keep aligned
- `core/control_plane/indexes/commands/command_index.v1.json`
- `docs/commands/core_python/`

### Current consumers to confirm during review
- CLI execution paths under `core/python/src/watchtower_core/cli/`
- command lookup and discovery surfaces under `core/control_plane/indexes/commands/`
- command-reference docs under `docs/commands/core_python/`

## Proposed Technical Approach
- Treat this document as the human Phase 3 entry checkpoint package rather than as implementation authorization.
- Reconfirm the current command-authority boundary directly from the live CLI registry, parser tree, command index, and command-reference docs.
- Publish any command-adjacent workflow, route, or compatibility classification detail that the Phase 3 checkpoint needs before implementation can be reviewed safely.
- Hand the package to a dedicated review task and stop until that review records an explicit approval or block outcome.

## Work Breakdown
1. Re-verify the current command-authority boundary in the live CLI registry, parser tree, command index, and command-reference docs.
2. Record the authored truth, derived outputs, current consumers, parity method, and rollback path for Phase 3 entry.
3. Publish any missing command-adjacent classification detail needed for safe Phase 3 review.
4. Route the package through the explicit Phase 3 entry-review task and stop before implementation.

## Entry Questions
- Is the current CLI registry plus parser tree still the only acceptable command-authority boundary for the next phase?
- Which command-adjacent workflow, route, and compatibility surfaces need explicit Phase 3 classification before implementation starts?
- What is the smallest rollback-safe normalization slice that can improve command companion drift without creating a second durable command-existence authority?

## Review-Resolved Entry Questions
- `Current command-authority boundary`: yes. `core/python/src/watchtower_core/cli/registry.py` plus `core/python/src/watchtower_core/cli/parser.py` remain the only accepted command-authority source for the next phase.
- `First rollback-safe slice`: [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- `Classification sufficiency`: no additional command-adjacent workflow, route, or compatibility classification addendum is required for the first slice because it stays inside the already-classified command index plus command docs companion surfaces and the existing CLI registry plus parser authority boundary.

## Parity Method
- Re-run:
  - `./.venv/bin/watchtower-core validate all`
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
- Inspect the current command-authority boundary directly in:
  - `core/python/src/watchtower_core/cli/registry.py`
  - `core/python/src/watchtower_core/cli/parser.py`
  - `core/control_plane/indexes/commands/command_index.v1.json`
  - `docs/commands/core_python/`
- Accept the Phase 3 entry package only if command authority remains explicit, public planning parity remains unchanged, and the planned slice stays rollback-bounded.

## Rollback Path
1. If review finds the entry package unsound, keep broader rewrite work blocked and do not start Phase 3 implementation.
2. If a later Phase 3 slice drifts beyond the current CLI registry and parser authority boundary, remove the new companion logic and restore command companion generation to the previously approved builder path.
3. Rebuild derived command and planning surfaces and re-run validation plus authority queries before proceeding again.

## Risks
- Command companion cleanup can create dual truth quickly if parser data, registry metadata, command index generation, and docs are normalized without one explicit source-of-truth declaration.
- Route or workflow companion surfaces can be pulled into Phase 3 prematurely if their classification detail is still only implied.
- A command-authority checkpoint can look smaller than it is because the current command model already spans code, generated indexes, and human docs.

## Validation Plan
- Re-run `./.venv/bin/watchtower-core doctor --format json`.
- Re-run `./.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Keep Phase 3 blocked unless the review task records an explicit approval outcome for the entry package.

## Stop Condition
- Stop at the explicit Phase 3 review outcome and hand off to the bounded implementation task.
- Do not widen the approved first slice into broader command-authority, workflow, route, compatibility, or public-planning changes from this package alone.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [review_structural_rewrite_phase3_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_entry_package.md)
- [implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/open/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)

## Updated At
- `2026-03-14T05:41:11Z`
