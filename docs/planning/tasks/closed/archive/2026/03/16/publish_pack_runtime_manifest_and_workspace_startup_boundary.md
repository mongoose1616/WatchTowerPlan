---
id: task.validated_core_pack_data_shape_convergence.runtime_manifest.002
trace_id: trace.validated_core_pack_data_shape_convergence
title: Publish pack runtime manifest and workspace startup boundary
summary: Adds the validated pack-runtime manifest and manifest-driven workspace startup
  boundary for shared core.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T04:46:03Z'
audience: shared
authority: authoritative
related_ids:
- prd.validated_core_pack_data_shape_convergence
- design.features.validated_core_pack_data_shape_convergence
- design.implementation.validated_core_pack_data_shape_convergence
- decision.validated_core_pack_data_shape_convergence_direction
---

# Publish pack runtime manifest and workspace startup boundary

## Summary
Adds the validated pack-runtime manifest and manifest-driven workspace startup boundary for shared core.

## Scope
- Publish the pack-runtime manifest schema, manifest artifact, and schema catalog entry.
- Expose the runtime manifest through typed control-plane models and loader access.
- Allow WorkspaceConfig to consume manifest-declared logical prefixes without breaking current defaults.

## Done When
- The runtime manifest validates and is discoverable through the schema catalog.
- Loader and workspace tests cover manifest-driven startup behavior.
- The repository remains green after sync and validation.
