---
id: task.typed_query_surface_modularity_hardening.model_modularity.002
trace_id: trace.typed_query_surface_modularity_hardening
title: Split typed retrieval models into focused modules
summary: Refactor the typed planning and documentation retrieval models into focused
  modules with explicit shared helpers while preserving stable public imports and
  loader or query behavior.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T18:21:56Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/models/
- core/python/src/watchtower_core/control_plane/loader.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/validation/acceptance.py
related_ids:
- prd.typed_query_surface_modularity_hardening
- design.features.typed_query_surface_modularity_hardening
- design.implementation.typed_query_surface_modularity_hardening
- decision.typed_query_surface_modularity_hardening_direction
- contract.acceptance.typed_query_surface_modularity_hardening
---

# Split typed retrieval models into focused modules

## Summary
Refactor the typed planning and documentation retrieval models into focused modules with explicit shared helpers while preserving stable public imports and loader or query behavior.

## Scope
- Split the mixed-domain typed model hotspot into smaller domain-focused modules.
- Preserve the watchtower_core.control_plane.models re-export surface and ControlPlaneLoader contracts.

## Done When
- Typed retrieval models live in focused modules with explicit helper-backed materialization or lookup seams.
- Direct loader, query, sync, and validation consumers stay aligned and targeted regressions pass.
