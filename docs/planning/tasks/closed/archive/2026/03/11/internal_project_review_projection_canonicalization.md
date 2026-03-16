---
id: task.internal_project_review_and_hardening.projection_canonicalization.001
trace_id: trace.internal_project_review_and_hardening
title: Canonicalize planning and coordination projection serializers
summary: Reuses shared serializers for initiative and planning payload shaping across
  sync and query surfaces.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T15:36:40Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- core/python/tests/unit/
related_ids:
- prd.internal_project_review_and_hardening
- decision.internal_project_review_and_hardening_direction
- design.features.internal_project_review_and_hardening
- design.implementation.internal_project_review_and_hardening
---

# Canonicalize planning and coordination projection serializers

## Summary
Reuses shared serializers for initiative and planning payload shaping across sync and query surfaces.

## Scope
- Extract shared active-task, initiative, and planning projection serializers.
- Wire the shared serializers into sync and query surfaces without changing public payload fields.
- Add regression tests that keep coordination and planning payload shapes stable.

## Done When
- Initiative and planning payload shaping uses shared serializers instead of parallel dict builders.
- Targeted tests confirm payload stability across sync and query entrypoints.
