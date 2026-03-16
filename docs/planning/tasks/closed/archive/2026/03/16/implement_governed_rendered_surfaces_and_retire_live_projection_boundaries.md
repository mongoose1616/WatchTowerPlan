---
id: task.rendered_surface_contract_enforcement.rendered_registry_and_runtime_alignment.002
trace_id: trace.rendered_surface_contract_enforcement
title: Implement governed rendered surfaces and retire live projection boundaries
summary: Adds the rendered-surface contract, refactors rendered trackers onto it,
  and retires live projection terminology in active runtime and authority surfaces.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T17:34:52Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/
- docs/planning/
related_ids:
- prd.rendered_surface_contract_enforcement
- design.features.rendered_surface_contract_enforcement
- design.implementation.rendered_surface_contract_enforcement
- decision.rendered_surface_contract_enforcement_direction
- contract.acceptance.rendered_surface_contract_enforcement
---

# Implement governed rendered surfaces and retire live projection boundaries

## Summary
Adds the rendered-surface contract, refactors rendered trackers onto it, and retires live projection terminology in active runtime and authority surfaces.

## Scope
- Author the schema-backed rendered-surface registry and align schema catalog, validator, and pack settings surfaces.
- Add the generic rendered Markdown adapter and refactor the tracker sync services to emit rendered Markdown from governed definitions.
- Rename active projection-named runtime helpers and current authority docs to rendered terminology without compatibility wrappers.

## Done When
- The rendered-surface registry is loadable and schema-validated through current control-plane paths.
- The tracker family renders through the generic rendered Markdown path rather than handwritten per-service layout assembly.
- No active projection compatibility boundary remains in the scoped runtime, command, and standards surfaces.

## Outcome
- Added the governed rendered-surface registry, schema, validator-registry entry, schema-catalog entry, pack-settings registration, typed models, and loader support needed to load the contract deterministically.
- Refactored the PRD, decision, design, task, initiative, and coordination tracking services onto the generic rendered Markdown adapter and retired the handwritten tracker layout helpers they replaced.
- Renamed the active planning and coordination-query runtime boundaries from `projection` to `rendered` and updated the current command, standards, and planning guidance surfaces in the same slice.
