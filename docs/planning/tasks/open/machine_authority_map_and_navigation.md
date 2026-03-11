---
id: task.planning_authority_unification.authority_map.001
trace_id: trace.planning_authority_unification
title: Publish machine authority map and canonical navigation updates
summary: Add the machine authority-map registry, authority query surface, and the documentation and standards updates that explain canonical planning precedence.
type: task
status: active
task_status: backlog
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T01:48:43Z'
audience: shared
authority: authoritative
related_ids:
  - prd.planning_authority_unification
  - design.features.planning_authority_unification
  - design.implementation.planning_authority_unification
  - decision.planning_authority_unification_direction
  - task.planning_authority_unification.planning_catalog.001
depends_on:
  - task.planning_authority_unification.planning_catalog.001
applies_to:
  - core/control_plane/
  - core/python/
  - docs/planning/
  - docs/commands/core_python/
  - README.md
---

# Publish machine authority map and canonical navigation updates

## Summary
Add the machine authority-map registry, authority query surface, and the documentation and standards updates that explain canonical planning precedence.

## Scope
- Add the authority-map schema, canonical registry artifact, schema-catalog entry, artifact-type entry, validator entry, typed model, and loader support.
- Add `watchtower-core query authority` for canonical planning and governance surface lookup.
- Update standards, root and planning entrypoints, and command docs to explain the canonical-versus-projection relationship across planning surfaces.
- Keep the authority map narrow and policy-oriented rather than encyclopedic.

## Done When
- The repo publishes a machine-readable authority-map registry with planning and governance question coverage.
- `watchtower-core query authority` resolves canonical surfaces and preferred commands for supported questions.
- Root, planning, and command docs explain the new canonical machine path clearly.

## Links
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authority_unification.md)
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_authority_unification.md)
