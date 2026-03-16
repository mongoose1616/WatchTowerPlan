---
id: task.planning_projection_pipeline_modularity_hardening.sync_surface_alignment.003
trace_id: trace.planning_projection_pipeline_modularity_hardening
title: Tighten planning projection sync composition seams
summary: Move planning-catalog-only aggregation and sync composition into smaller
  private helpers while preserving initiative-versus-planning parity.
type: task
status: active
task_status: in_progress
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T00:46:51Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py
- core/python/src/watchtower_core/repo_ops/planning_projection_policy.py
- core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py
related_ids:
- prd.planning_projection_pipeline_modularity_hardening
- design.features.planning_projection_pipeline_modularity_hardening
- design.implementation.planning_projection_pipeline_modularity_hardening
- decision.planning_projection_pipeline_modularity_hardening_direction
- contract.acceptance.planning_projection_pipeline_modularity_hardening
depends_on:
- task.planning_projection_pipeline_modularity_hardening.serialization_boundary.002
---

# Tighten planning projection sync composition seams

## Summary
Move planning-catalog-only aggregation and sync composition into smaller private helpers while preserving initiative-versus-planning parity.

## Scope
- Extract catalog-only aggregation for validator IDs, related paths, tags, and updated-at state out of PlanningCatalogSyncService.
- Keep InitiativeIndexSyncService on shared coordination and initiative-entry projection only.
- Align repo_ops runtime docs and targeted sync parity coverage with the new helper boundary.

## Done When
- planning_catalog.py and initiative_index.py are slimmer orchestration entrypoints over shared private helpers.
- coordination parity and catalog aggregation semantics remain stable under targeted tests.
- repo_ops runtime docs and derived planning surfaces remain aligned after the refactor.
