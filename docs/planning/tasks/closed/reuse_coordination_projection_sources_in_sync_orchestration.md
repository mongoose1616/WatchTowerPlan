---
id: task.coordination_projection_source_reuse.loader_override_reuse.002
trace_id: trace.coordination_projection_source_reuse
title: Reuse coordination projection sources in sync orchestration
summary: Eliminate repeated planning-index and evidence source rereads by publishing
  command-scoped validated overrides for coordination sync dependencies.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T16:16:44Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
related_ids:
- prd.coordination_projection_source_reuse
- design.features.coordination_projection_source_reuse
- design.implementation.coordination_projection_source_reuse
- decision.coordination_projection_source_reuse_direction
depends_on:
- task.coordination_projection_source_reuse.bootstrap.001
---

# Reuse coordination projection sources in sync orchestration

## Summary
Eliminate repeated planning-index and evidence source rereads by publishing command-scoped
validated overrides for coordination sync dependencies.

## Scope
- Add explicit validated override support to the control-plane loader for current-run
  artifacts that sync orchestration wants to reuse.
- Prime stable coordination projection inputs once and publish newly-built task,
  traceability, initiative, planning-catalog, and coordination documents for downstream
  reuse.
- Preserve schema-validation boundaries before generated documents become reusable overrides.
- Add targeted regressions proving reduced source reads, validated override publication, and
  current-run dependency reuse.

## Done When
- Coordination sync rereads stable planning projection inputs from source only once per run
  and reuses generated downstream documents without falling back to stale intermediates.
- Generated coordination projection documents are schema-validated before orchestration
  publishes them as current-run overrides.
- Write-mode and dry-run coordination sync preserve deterministic artifact behavior.
- Targeted regression coverage proves the optimization boundary.
