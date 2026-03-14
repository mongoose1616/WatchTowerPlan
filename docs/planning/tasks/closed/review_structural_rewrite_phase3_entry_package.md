---
id: task.structural_rewrite_program.phase3_entry_review.006
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 3 entry package
summary: Review the command-authority normalization entry package, confirm the current command-authority boundary and rollback model, and decide whether bounded Phase 3 work may begin.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T05:41:11Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_program.md
- docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md
- docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/indexes/commands/command_index.v1.json
- core/python/src/watchtower_core/cli/registry.py
- core/python/src/watchtower_core/cli/parser.py
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase3_command_authority_entry
- design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.artifact_role_registry_pilot_review.005
---

# Review structural rewrite Phase 3 entry package

## Summary
Review the command-authority normalization entry package, confirm the current command-authority boundary and rollback model, and decide whether bounded Phase 3 work may begin.

## Scope
- Confirm that the current CLI registry and parser tree remain the only accepted command-authority source at Phase 3 entry.
- Confirm that the proposed Phase 3 boundary stays compatible with the public planning-authority parity contract.
- Confirm that any missing command-adjacent workflow, route, or compatibility classification detail is explicitly called out before implementation starts.
- Decide whether Phase 3 may proceed through one bounded checkpoint or remains blocked.

## Done When
- The review records an explicit approve or block outcome for the Phase 3 entry package.
- Any approved Phase 3 slice remains bounded and rollback-explicit.
- No command-authority implementation work begins before this task reaches an explicit terminal outcome.

## Review Outcome
- `Decision`: approved for exactly one bounded Phase 3 slice.
- `Current command-authority boundary`: reaffirmed. `core/python/src/watchtower_core/cli/registry.py` and `core/python/src/watchtower_core/cli/parser.py` remain the only accepted machine authority for command presence and hierarchy.
- `Approved first slice`: [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- `Slice rationale`: the command index already routes family-owned `doctor`, `sync`, and `validate` leaf commands to their owning family files, but `23` command docs still point to `core/python/src/watchtower_core/cli/main.py`. The first Phase 3 slice therefore stays inside companion-surface normalization rather than broader authority replacement.
- `Classification sufficiency`: no additional command-adjacent workflow, route, or compatibility classification addendum is required for this first slice because it stays inside the already-classified CLI registry plus parser authority surfaces and the existing command index plus command docs companion surfaces.
- `Public planning parity`: unchanged. The review does not authorize any change to the five planning-authority answers or their current machine-readable surfaces.
- `Next-step decision`: open one bounded implementation task for the approved first slice and stop before implementation begins in this review change.

## Links
- [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)
- [structural_rewrite_phase3_command_authority_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md)
- [review_structural_rewrite_artifact_role_registry_pilot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_artifact_role_registry_pilot_outcome.md)

## Updated At
- `2026-03-14T05:41:11Z`
