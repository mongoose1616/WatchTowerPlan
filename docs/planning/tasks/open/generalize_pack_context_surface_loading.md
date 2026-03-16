---
id: task.post_rewrite_core_cleanup_and_surface_reduction.generic_pack_surface_loading.003
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Generalize pack context surface loading
summary: Make pack-context startup resolve typed required surfaces from declared paths
  instead of repo-specific loader constants.
type: task
status: active
task_status: in_progress
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T06:40:30Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/loader.py
- core/python/src/watchtower_core/control_plane/pack_context.py
- core/python/tests/unit/test_pack_context.py
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
---

# Generalize pack context surface loading

## Summary
Make pack-context startup resolve typed required surfaces from declared paths instead of repo-specific loader constants.

## Scope
- Allow pack settings to relocate required registry and index surfaces without losing typed model loading.
- Add regression coverage proving alternate declared paths work.

## Done When
- load_pack_context succeeds when a required surface is declared at a non-default repository-relative path.
- The pack-context test suite covers both default and relocated declared surface paths.
