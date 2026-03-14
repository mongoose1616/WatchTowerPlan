---
id: task.structural_rewrite_program.phase3_command_companion_source_surface_normalization.007
trace_id: trace.structural_rewrite_program
title: Implement structural rewrite Phase 3 command companion source surface normalization
summary: Normalize command-doc source-surface metadata for the first bounded Phase 3 slice so the human command companions agree with the registry-backed command index without changing command authority.
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
- docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md
- docs/commands/core_python/
- core/control_plane/indexes/commands/command_index.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json
- core/python/src/watchtower_core/cli/registry.py
- core/python/src/watchtower_core/cli/parser.py
- core/python/src/watchtower_core/cli/introspection.py
- core/python/src/watchtower_core/repo_ops/sync/command_index.py
- core/python/tests/
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_phase3_command_authority_entry
- design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase3_entry_review.006
---

# Implement structural rewrite Phase 3 command companion source surface normalization

## Summary
Normalize command-doc source-surface metadata for the first bounded Phase 3 slice so the human command companions agree with the registry-backed command index without changing command authority.

## Scope
- Reconcile the root command page's primary `Source Surface` section plus the affected `doctor`, `sync`, and `validate` command docs to the parser-owned or family-owned implementation paths already published in the command index.
- Keep `registry.py` plus `parser.py` as the only accepted command-authority source.
- Add only the narrowest targeted guard needed to keep the affected command docs aligned with the command index.

## Done When
- The bounded mismatch set is reconciled and validated.
- Command authority remains unchanged and explicit.
- The slice stops with an explicit follow-up review task rather than broader Phase 3 rollout.

## Outcome
- The slice reconciles the root command page's primary `Source Surface` section and the `23` affected `doctor`, `sync`, and `validate` command docs to the parser-owned or family-owned implementation paths already published in the command index.
- The command-index sync path now fails closed if a companion command doc's `Command` table or primary `## Source Surface` entry drifts from the registry-backed implementation path, and `test_command_index_sync.py` covers that guard directly.
- The slice remains companion-only. `registry.py` plus `parser.py` still own command presence and hierarchy, and the next controlling surface is an explicit outcome review task rather than broader rewrite rollout.

## Links
- [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [review_structural_rewrite_phase3_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_entry_package.md)
- [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)

## Updated At
- `2026-03-14T05:41:11Z`
