---
id: task.validated_core_pack_data_shape_convergence.data_shape_alignment.004
trace_id: trace.validated_core_pack_data_shape_convergence
title: Align current repo data families with pack artifact and index surfaces
summary: Maps current repository-local machine surfaces onto the future pack artifact-family
  and derived-index model.
type: task
status: active
task_status: backlog
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T04:42:59Z'
audience: shared
authority: authoritative
related_ids:
- prd.validated_core_pack_data_shape_convergence
- design.features.validated_core_pack_data_shape_convergence
depends_on:
- task.validated_core_pack_data_shape_convergence.pack_models.003
---

# Align current repo data families with pack artifact and index surfaces

## Summary
Maps current repository-local machine surfaces onto the future pack artifact-family and derived-index model.

## Scope
- Define how current planning and control-plane artifacts map to future pack-owned families and derived index surfaces.
- Retire or demote repo-shape assumptions that conflict with the pack model.
- Preserve current query and validation behavior while the data shape converges.

## Done When
- Current machine-readable surfaces have an explicit mapping to the target pack artifact and index families.
- Repo-specific authority assumptions no longer block the future pack model.
