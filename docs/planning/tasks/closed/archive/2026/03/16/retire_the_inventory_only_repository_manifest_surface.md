---
id: task.post_rewrite_core_cleanup_and_surface_reduction.inventory_manifest_retirement.004
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Retire the inventory-only repository manifest surface
summary: Remove the retained repository_manifest family if it has no runtime consumer
  and repair the remaining schema, validator, and docs references.
type: task
status: active
task_status: done
task_kind: chore
priority: medium
owner: repository_maintainer
updated_at: '2026-03-16T06:53:48Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/manifests/
- core/control_plane/registries/validator_registry.json
- core/control_plane/schemas/artifacts/
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
---

# Retire the inventory-only repository manifest surface

## Summary
Remove the retained repository_manifest family if it has no runtime consumer and repair the remaining schema, validator, and docs references.

## Scope
- Confirm the repository_manifest family is inventory-only and remove it from active governed maintenance if safe.
- Repair schemas, registries, docs, and validation surfaces that still reference the retired family.

## Done When
- The repository manifest family is either retired cleanly or explicitly justified as still required by a live consumer.
- validate all no longer carries an inventory-only manifest surface without a runtime use case.
