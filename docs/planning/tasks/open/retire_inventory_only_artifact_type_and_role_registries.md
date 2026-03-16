---
id: task.post_rewrite_core_cleanup_and_surface_reduction.artifact_registry_retirement.008
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Retire inventory-only artifact type and role registries
summary: Remove the retained artifact type and artifact role registries if no live
  reusable-core or pack consumer still reads them and reconcile their historical
  references.
type: task
status: active
task_status: backlog
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T07:00:01Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/registries/
- core/control_plane/schemas/artifacts/
- core/control_plane/contracts/acceptance/
- docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
depends_on:
- task.post_rewrite_core_cleanup_and_surface_reduction.example_validation_retirement.007
---

# Retire inventory-only artifact type and role registries

## Summary
Remove the retained artifact type and artifact role registries if no live reusable-core or pack consumer still reads them and reconcile their historical references.

## Scope
- Confirm the retained artifact type and artifact role registries are not loaded by current reusable-core or repo-local runtime code.
- Retire the registry, schema, validator, and companion docs surfaces if the consumer audit stays empty.
- Repair or supersede historical rewrite-era acceptance, design, and evidence references that still point at those registries.

## Done When
- The retained artifact type and artifact role registries are either removed cleanly or explicitly justified as still required by a live consumer.
- The cleanup does not leave broken acceptance or traceability references behind.
