---
id: "task.end_to_end_repo_review_and_rationalization.external_pack_validation.001"
trace_id: "trace.end_to_end_repo_review_and_rationalization"
title: "Expose external pack validation through supplemental schema loading"
summary: "Add file-system supplemental schema loading and CLI-level external artifact validation so future pack-owned artifacts can be validated without patching the canonical schema catalog."
type: "task"
status: "active"
task_status: "ready"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/control_plane/"
  - "core/python/src/watchtower_core/cli/"
  - "core/python/src/watchtower_core/validation/"
  - "core/python/tests/"
  - "docs/commands/core_python/"
  - "core/control_plane/schemas/interfaces/packs/"
related_ids:
  - "prd.end_to_end_repo_review_and_rationalization"
  - "design.features.end_to_end_repo_rationalization"
  - "design.implementation.end_to_end_repo_rationalization_execution"
depends_on:
  - "task.end_to_end_repo_review_and_rationalization.bootstrap.001"
---

# Expose external pack validation through supplemental schema loading

## Summary
Add file-system supplemental schema loading and CLI-level external artifact validation so future pack-owned artifacts can be validated without patching the canonical schema catalog.

## Scope
- Add helpers for loading supplemental schema documents from files or directories.
- Extend `validate artifact` with the bounded supplemental-schema options needed for external pack artifacts.
- Add tests and docs using pack-owned artifact validation scenarios.

## Done When
- External artifacts can be validated against supplemental schemas supplied from files or directories.
- Duplicate or invalid supplemental schemas still fail closed.
- The command docs and workspace README explain the path clearly.

## Links
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- [end_to_end_repo_rationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/end_to_end_repo_rationalization_execution.md)

## Updated At
- `2026-03-10T19:43:34Z`
