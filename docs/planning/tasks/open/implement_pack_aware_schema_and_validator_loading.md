---
id: task.plan_domain_pack_core_validation.pack_aware_loading.002
trace_id: trace.plan_domain_pack_core_validation
title: Implement pack-aware schema and validator loading
summary: Adds pack-aware schema catalog merge and pack-declared validator selection
  to reusable core validation.
type: task
status: active
task_status: in_progress
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T20:37:39Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/validation/
related_ids:
- prd.plan_domain_pack_core_validation
- design.features.plan_domain_pack_core_validation
- design.implementation.plan_domain_pack_core_validation
- decision.plan_domain_pack_core_validation_direction
- contract.acceptance.plan_domain_pack_core_validation
depends_on:
- task.plan_domain_pack_core_validation.bootstrap.001
---

# Implement pack-aware schema and validator loading

## Summary
Adds pack-aware schema catalog merge and pack-declared validator selection to reusable core validation.

## Scope
- Extend SchemaStore and ControlPlaneLoader to resolve pack-local schema catalogs alongside the core catalog.
- Add pack-selected validator-registry loading for reusable-core validation services.

## Done When
- Reusable core can build a pack-selected validation context without regressing the repository-default path.
- Unit coverage proves merged-schema and pack-validator loading behavior.
