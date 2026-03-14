---
id: task.structural_rewrite_program.phase3_command_companion_source_surface_normalization_review.008
trace_id: trace.structural_rewrite_program
title: Review structural rewrite Phase 3 command companion source surface normalization outcome
summary: Review the bounded Phase 3 command companion source-surface normalization slice, confirm docs-plus-index parity held, and decide whether broader rewrite work remains blocked or may proceed to a new bounded checkpoint.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T06:44:15Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md
- docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md
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

## Review Outcome
- `Decision`: passed; the bounded Phase 3 slice held cleanly as companion-only normalization and does not need a second broader Phase 3 checkpoint before the next later-phase entry review.
- `Docs-plus-index parity`: passed. The root command page plus the bounded `doctor`, `sync`, and `validate` command docs continue to agree with the command-index implementation paths published from the live parser-backed registry model.
- `Guard result`: passed. `watchtower-core sync command-index --format json` stays green and `python -m pytest tests/unit/test_command_index_sync.py` keeps the new fail-closed drift guard under direct coverage without creating a second command-authority source.
- `Authority result`: unchanged. `core/python/src/watchtower_core/cli/registry.py` plus `core/python/src/watchtower_core/cli/parser.py` remain the only accepted command-authority source, and `watchtower-core query authority --domain planning --format json` still resolves the same five public planning questions to the same canonical machine surfaces.
- `Next-step decision`: do not broaden Phase 3 rollout. Open a dedicated Phase 4 shared-projection entry package and review gate as the next bounded checkpoint, and keep Phase 4 implementation blocked until that entry review closes explicitly.

## Rationale
- The first Phase 3 slice already proved the safety property it was supposed to prove: command companion source-surface drift can be normalized and guarded without changing command presence, hierarchy, or public planning behavior.
- A second broader Phase 3 slice would widen the surface area without answering the next materially different rewrite question.
- The next live rewrite risk sits at the shared projection and internal planning-graph boundary, where public planning parity, private-runtime-only graph assembly, and projection-family rollback boundaries need a dedicated later-phase entry package before implementation.

## Links
- [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [review_structural_rewrite_phase4_shared_projection_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/open/review_structural_rewrite_phase4_shared_projection_entry_package.md)

## Updated At
- `2026-03-14T06:44:15Z`
