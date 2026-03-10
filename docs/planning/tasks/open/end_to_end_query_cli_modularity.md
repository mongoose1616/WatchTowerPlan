---
id: "task.end_to_end_repo_review_and_rationalization.query_cli_modularity.001"
trace_id: "trace.end_to_end_repo_review_and_rationalization"
title: "Split query CLI registration and handlers into smaller family modules"
summary: "Reduce maintenance risk in the largest remaining CLI modules by splitting query parser registration and query runtime handlers into smaller family-focused modules without changing the durable command contract."
type: "task"
status: "active"
task_status: "ready"
task_kind: "chore"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/cli/"
  - "core/python/tests/"
  - "docs/commands/core_python/"
  - "core/control_plane/indexes/commands/"
related_ids:
  - "prd.end_to_end_repo_review_and_rationalization"
  - "design.features.end_to_end_repo_rationalization"
  - "design.implementation.end_to_end_repo_rationalization_execution"
depends_on:
  - "task.end_to_end_repo_review_and_rationalization.bootstrap.001"
---

# Split query CLI registration and handlers into smaller family modules

## Summary
Reduce maintenance risk in the largest remaining CLI modules by splitting query parser registration and query runtime handlers into smaller family-focused modules without changing the durable command contract.

## Scope
- Split query parser registration into smaller family modules.
- Split runtime query handlers into smaller family modules.
- Keep command docs, command index metadata, and tests aligned with the refactor.

## Done When
- The largest query CLI modules are materially smaller.
- Query command behavior and output contracts stay stable.
- Docs and tests stay green after the refactor.

## Links
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- [end_to_end_repo_rationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/end_to_end_repo_rationalization_execution.md)

## Updated At
- `2026-03-10T19:43:34Z`
