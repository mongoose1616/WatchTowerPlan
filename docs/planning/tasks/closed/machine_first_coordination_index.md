---
id: "task.machine_first_coordination_surface.coordination_index.001"
trace_id: "trace.machine_first_coordination_surface"
title: "Publish the derived coordination index"
summary: "Add the coordination-index artifact family, sync logic, loader support, and query integration so one machine-readable surface becomes the default planning current-state entrypoint."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:20:47Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/schemas/artifacts/"
  - "core/control_plane/indexes/coordination/"
  - "core/python/src/watchtower_core/control_plane/"
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/src/watchtower_core/cli/"
  - "core/python/tests/"
related_ids:
  - "prd.machine_first_coordination_surface"
  - "design.features.machine_first_coordination_surface"
  - "design.implementation.machine_first_coordination_execution"
depends_on:
  - "task.machine_first_coordination_surface.bootstrap.001"
---

# Publish the derived coordination index

## Summary
Add the coordination-index artifact family, sync logic, loader support, and query integration so one machine-readable surface becomes the default planning current-state entrypoint.

## Scope
- Add the coordination index schema, examples, model, loader entry, validator coverage, and sync service.
- Include the coordination index in `sync coordination` and `sync all`.
- Change `query coordination` to read from the derived coordination index.

## Done When
- A coordination index exists and validates.
- `query coordination` is always useful, even when no initiative is active.
- The repo stays green after the new derived surface lands.

## Outcome
- Added the governed coordination-index artifact family with schema, examples, registry coverage, validator coverage, and a machine-readable start-here surface under `core/control_plane/indexes/coordination/`.
- Switched `watchtower-core query coordination` to the derived coordination index so the command now returns repo-level coordination state, actionable-task context, and bootstrap-ready guidance.
- Extended `sync coordination` and `sync all` to rebuild the coordination index in dependency order, with loader support, typed models, and targeted validation coverage.

## Links
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/design/features/machine_first_coordination_surface.md)
- [machine_first_coordination_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/machine_first_coordination_execution.md)

## Updated At
- `2026-03-10T19:20:47Z`
