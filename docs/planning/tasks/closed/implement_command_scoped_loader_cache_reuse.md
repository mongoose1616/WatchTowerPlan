---
id: task.control_plane_loader_cache_reuse.loader_cache.002
trace_id: trace.control_plane_loader_cache_reuse
title: Implement command-scoped loader cache reuse
summary: Add override-aware loader caches and regression coverage for repeated validator
  registry rematerialization and override invalidation.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T19:33:27Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/tests/
related_ids:
- prd.control_plane_loader_cache_reuse
- design.implementation.control_plane_loader_cache_reuse
- decision.control_plane_loader_cache_reuse_direction
- contract.acceptance.control_plane_loader_cache_reuse
depends_on:
- task.control_plane_loader_cache_reuse.bootstrap.001
---

# Implement command-scoped loader cache reuse

## Summary
Add override-aware loader caches and regression coverage for repeated validator registry
rematerialization and override invalidation.

## Scope
- Add command-scoped validated-document and typed-artifact caches to `ControlPlaneLoader`.
- Preserve current-run override semantics by invalidating affected cache entries explicitly.
- Add targeted tests and measurements for validator-registry reuse and override invalidation.

## Done When
- The loader cache implementation lands with targeted regression coverage.
- Direct measurement shows the validator-registry hotspot dropping materially.
- The change is ready for full validation and follow-up review.
