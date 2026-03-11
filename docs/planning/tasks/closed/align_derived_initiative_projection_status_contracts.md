---
id: task.derived_projection_status_semantics.projection_contracts.001
trace_id: trace.derived_projection_status_semantics
title: Align derived initiative projection status contracts
summary: Rename the ambiguous per-entry initiative-family status field to artifact_status
  across schemas, sync, query, docs, and tests.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T03:36:57Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/indexes/initiatives/
- core/control_plane/indexes/coordination/
- core/control_plane/schemas/artifacts/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/
related_ids:
- prd.derived_projection_status_semantics
- design.features.derived_projection_status_semantics
- design.implementation.derived_projection_status_semantics
- decision.derived_projection_status_semantics_direction
---

# Align derived initiative projection status contracts

## Summary
Rename the ambiguous per-entry initiative-family status field to artifact_status across schemas, sync, query, docs, and tests.

## Scope
- Update initiative and coordination entry contracts to use artifact_status.
- Align typed models, query handlers, and sync services with the renamed field.
- Refresh command docs, standards, and tests for the contract change.

## Done When
- Closed initiatives returned by watchtower-core query initiatives use artifact_status plus initiative_status without an entry-level status field.
- The initiative and coordination schemas, docs, and tests all validate after sync and full repository checks.
