---
id: task.planning_projection_pipeline_modularity_hardening.serialization_boundary.002
trace_id: trace.planning_projection_pipeline_modularity_hardening
title: Split planning projection serialization boundaries
summary: Extract family-focused planning projection serializers and preserve compact
  payload semantics for initiative and planning outputs.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T00:46:51Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py
related_ids:
- prd.planning_projection_pipeline_modularity_hardening
- design.features.planning_projection_pipeline_modularity_hardening
- design.implementation.planning_projection_pipeline_modularity_hardening
- decision.planning_projection_pipeline_modularity_hardening_direction
- contract.acceptance.planning_projection_pipeline_modularity_hardening
---

# Split planning projection serialization boundaries

## Summary
Extract family-focused planning projection serializers and preserve compact payload semantics for initiative and planning outputs.

## Scope
- Split shared planning projection serialization into smaller family-focused seams without changing payload fields.
- Keep compact-mode omissions and shared helper semantics stable for initiative and planning projections.
- Add focused regression coverage for serializer-level parity where the new boundary needs it.

## Done When
- planning_projection_serialization.py is materially smaller and delegates the heavy payload shaping through focused helpers or seams.
- initiative and planning payloads remain stable under targeted regression coverage.
- the sync services compile against the slimmer serialization boundary without reabsorbing catalog-specific logic.
