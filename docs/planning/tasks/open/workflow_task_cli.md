---
id: "task.workflow_system_operationalization.task_cli.001"
trace_id: "trace.workflow_system_operationalization"
title: "Add task lifecycle CLI commands"
summary: "Expose task creation, structured task updates, and handoff-style transitions through a first-class CLI family while preserving task-document authority."
type: "task"
status: "active"
task_status: "backlog"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T21:59:21Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/tasks/"
  - "core/python/src/watchtower_core/"
  - "docs/commands/core_python/"
related_ids:
  - "prd.workflow_system_operationalization"
  - "design.features.workflow_routing_and_authoring"
  - "design.implementation.workflow_system_operationalization_execution"
depends_on:
  - "task.workflow_system_operationalization.bootstrap.001"
---

# Add task lifecycle CLI commands

## Summary
Expose task creation, structured task updates, and handoff-style transitions through a first-class CLI family while preserving task-document authority.

## Scope
- Add task create, update, and transition subcommands.
- Reuse existing task-document invariants, placement rules, and derived-surface sync behavior.
- Keep command docs and tests aligned with the new mutation surface.

## Done When
- New governed task docs can be created through the CLI.
- Structured task fields and placement can be updated through the CLI without manual front-matter edits.
- Handoff-style task transitions refresh the dependent planning surfaces correctly.

## Links
- [workflow_routing_and_authoring.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_routing_and_authoring.md)
- [workflow_system_operationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/workflow_system_operationalization_execution.md)

## Updated At
- `2026-03-10T21:59:21Z`
