---
id: task.validated_core_pack_data_shape_convergence.pack_models.003
trace_id: trace.validated_core_pack_data_shape_convergence
title: Introduce pack-facing typed models and generic loader surfaces
summary: Moves shared core closer to pack-facing artifact families by adding typed
  pack models and reducing planning-specific loader bias.
type: task
status: active
task_status: ready
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T04:46:03Z'
audience: shared
authority: authoritative
related_ids:
- prd.validated_core_pack_data_shape_convergence
- design.features.validated_core_pack_data_shape_convergence
depends_on:
- task.validated_core_pack_data_shape_convergence.runtime_manifest.002
---

# Introduce pack-facing typed models and generic loader surfaces

## Summary
Moves shared core closer to pack-facing artifact families by adding typed pack models and reducing planning-specific loader bias.

## Scope
- Add typed models for the generic pack-facing artifact families already published in core/control_plane.
- Expose generic loader entrypoints that do not require named WatchTowerPlan planning-family methods.
- Keep repo-local planning semantics behind repo_ops during the transition.

## Done When
- Generic pack-facing artifact families have typed models in shared core.
- At least one generic loader path exists for pack-facing artifacts without new repo-specific assumptions.
