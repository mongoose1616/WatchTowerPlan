---
id: task.structural_rewrite_program.phase3_command_companion_source_surface_normalization_review.008
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 3 command companion source surface normalization outcome
summary: Review the bounded Phase 3 command companion source-surface normalization slice, confirm docs-plus-index parity held, and decide whether broader rewrite work remains blocked or may proceed to a new bounded checkpoint.
type: task
status: active
task_status: ready
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T05:41:11Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md
- docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md
- docs/commands/core_python/
- core/control_plane/indexes/commands/command_index.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json
- core/python/src/watchtower_core/repo_ops/sync/command_index.py
- core/python/tests/unit/test_command_index_sync.py
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase3_command_companion_source_surface_normalization.007
---

# Review structural rewrite Phase 3 command companion source surface normalization outcome

## Summary
Review the bounded Phase 3 command companion source-surface normalization slice, confirm docs-plus-index parity held, and decide whether broader rewrite work remains blocked or may proceed to a new bounded checkpoint.

## Scope
- Confirm the root command page plus the affected `doctor`, `sync`, and `validate` command docs now agree with the command index implementation paths.
- Confirm the new command-index sync guard and direct unit coverage fail closed on future source-surface drift without creating a second command-authority source.
- Confirm `registry.py` plus `parser.py` remain the only accepted command-authority source and that public planning parity remains unchanged.
- Decide whether the rewrite stays blocked at this review or may proceed to a new explicit bounded checkpoint.

## Done When
- The review records an explicit pass or block outcome for the bounded Phase 3 slice.
- Any proposed next step is framed as a new explicit checkpoint rather than implied broader rollout.
- No broader Phase 3 or later-phase rewrite work is implied by this slice alone.

## Links
- [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md)

## Updated At
- `2026-03-14T05:41:11Z`
