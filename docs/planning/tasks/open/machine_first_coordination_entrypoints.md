---
id: "task.machine_first_coordination_surface.entrypoints.001"
trace_id: "trace.machine_first_coordination_surface"
title: "Align human and agent coordination entrypoints"
summary: "Generate a compact human coordination tracker and reroute planning and agent entrypoint guidance so humans and agents start from the same derived coordination state."
type: "task"
status: "active"
task_status: "ready"
task_kind: "feature"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-10T18:54:43Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/"
  - "README.md"
  - "AGENTS.md"
  - "docs/commands/core_python/"
  - "core/python/tests/"
related_ids:
  - "prd.machine_first_coordination_surface"
  - "design.features.machine_first_coordination_surface"
  - "design.implementation.machine_first_coordination_execution"
depends_on:
  - "task.machine_first_coordination_surface.coordination_index.001"
---

# Align human and agent coordination entrypoints

## Summary
Generate a compact human coordination tracker and reroute planning and agent entrypoint guidance so humans and agents start from the same derived coordination state.

## Scope
- Generate `docs/planning/coordination_tracking.md`.
- Update planning README, nearby entrypoint docs, and root agent guidance to point to the coordination surfaces first.
- Keep command docs aligned with the coordination-surface behavior.

## Done When
- Humans can start from one compact coordination tracker.
- Agents are routed to `query coordination` as the default planning current-state surface.
- Family trackers remain available but stop acting as the first default entrypoint.

## Links
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/design/features/machine_first_coordination_surface.md)
- [machine_first_coordination_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/machine_first_coordination_execution.md)

## Updated At
- `2026-03-10T18:54:43Z`
