---
trace_id: trace.planning_projection_pipeline_modularity_hardening
id: design.features.planning_projection_pipeline_modularity_hardening
title: Planning Projection Pipeline Modularity Hardening Feature Design
summary: Defines the technical design boundary for Planning Projection Pipeline Modularity
  Hardening.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-15T23:55:21Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py
- core/python/src/watchtower_core/repo_ops/planning_projection_policy.py
- core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py
---

# Planning Projection Pipeline Modularity Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.planning_projection_pipeline_modularity_hardening`
- `Design ID`: `design.features.planning_projection_pipeline_modularity_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.planning_projection_pipeline_modularity_hardening`
- `Linked Decisions`: `decision.planning_projection_pipeline_modularity_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.planning_projection_pipeline_modularity_hardening`
- `Updated At`: `2026-03-15T23:55:21Z`

## Summary
Defines the technical design boundary for Planning Projection Pipeline Modularity Hardening.

## Source Request
- Turn the current WatchTowerPlan planning-projection hotspot review into a concrete bounded planning slice.

## Scope and Feature Boundary
- Covers the private planning-projection helpers under `watchtower_core.repo_ops`, the initiative and planning sync consumers, targeted sync regression suites, and the runtime-boundary README for this seam.
- Covers splitting serializer families, catalog-only aggregation, and shared coordination composition behind the existing snapshot, source-assembly, policy, and task-selection boundary.
- Does not change public planning authority artifacts, CLI contracts, query payload fields, or sync ordering.
- Does not reopen unrelated hotspots or broaden the earlier Phase 4 rewrite work into another public-boundary change.

## Current-State Context
- The March 15, 2026 live repo counts now show `planning_projection_snapshot.py` at `134` lines, `planning_projection_source_assembly.py` at `89`, `planning_projection_task_selection.py` at `169`, `planning_projection_policy.py` at `291`, `planning_projection_serialization.py` at `378`, `planning_catalog.py` at `359`, and `initiative_index.py` at `121`.
- The earlier Phase 4 rewrite work already extracted the trace-scoped snapshot, source-assembly, and coordination-policy seams, so the remaining hotspot is no longer raw trace-source assembly; it is payload shaping and catalog-specific aggregation around the private snapshot.
- Current unit coverage proves initiative-versus-planning coordination parity at whole-document level, but the serializer boundary and catalog-only aggregation still lack narrower direct contracts, so small private payload changes can ripple across two sync services.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keep helper seams explicit and repo-local rather than introducing a new framework or reusable-core abstraction.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): same-change updates must keep code, docs, trackers, and machine-readable planning surfaces aligned.

## Internal Standards and Canonical References Applied
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the public planning authority boundary must not change while the private projection pipeline is being tightened.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative phase, owner, and next-step semantics must remain stable across initiative and planning projections.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the bounded execution queue, trackers, and coordination surfaces must remain aligned with task state changes in the same change set.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): helper extraction should stay inside the repo-local Python workspace and land with direct unit coverage.

## Design Goals and Constraints
- Reduce blast radius by separating serializer families and catalog-only aggregation from sync-service orchestration.
- Preserve compact payload semantics, existing query results, and initiative-versus-planning coordination parity.
- Keep the snapshot, source-assembly, policy, and task-selection boundary private and readable; do not create a new public artifact or compatibility layer.

## Options Considered
### Option 1
- Leave the current private projection boundary in place because the earlier Phase 4 snapshot extraction already improved the larger hotspot.
- Strength: avoids another internal refactor pass now.
- Tradeoff: leaves the remaining serializer and planning-catalog concentration intact and keeps small payload changes expensive to review.

### Option 2
- Expand the seam into a broader internal planning-graph or shared-projection rewrite.
- Strength: could normalize more of the projection family at once.
- Tradeoff: too broad for this bounded slice and risks public-boundary drift while solving a narrower live hotspot.

### Option 3
- Keep the current private snapshot boundary and extract bounded helper seams around serialization and planning-catalog composition.
- Strength: addresses the current hotspot with the smallest behavior-preserving change.
- Tradeoff: requires careful parity coverage and same-change alignment across docs, trackers, and derived planning surfaces.

## Recommended Design
### Architecture
- Keep `planning_projection_snapshot.py`, `planning_projection_source_assembly.py`, `planning_projection_policy.py`, and `planning_projection_task_selection.py` as the private upstream graph boundary.
- Narrow `planning_projection_serialization.py` to shared coordination plus thin family dispatch, and move per-family payload shaping into focused helper-backed seams or adjacent private modules.
- Move catalog-only summary assembly, validator or related-path or tag aggregation, and updated-at calculation out of `PlanningCatalogSyncService` into dedicated helpers so `planning_catalog.py` becomes orchestration over one snapshot and a smaller catalog projection collaborator.
- Keep `InitiativeIndexSyncService` consuming the same coordination and shared serializers, but avoid pulling catalog-only rules into the initiative path.

### Data and Interface Impacts
- No control-plane schema, CLI, or public planning payload changes are intended.
- The planning catalog and initiative index stay in the same artifact paths and keep the same payload fields.
- Direct tests should expand to cover serializer outputs or catalog aggregation semantics explicitly instead of relying only on full-document parity.

### Execution Flow
1. Lock current initiative and planning outputs with focused serializer and parity expectations.
2. Extract family-focused serialization and catalog-only aggregation helpers behind the existing sync services.
3. Rebuild planning surfaces, rerun targeted sync or query tests plus full validation, then refresh evidence and close out.

### Invariants and Failure Cases
- Initiative coordination fields and the planning catalog coordination section must remain semantically identical for the same trace.
- Compact mode must continue omitting empty optional fields consistently across all projection families.
- Related-path, validator, or tag aggregation must not silently drop acceptance, evidence, or task-derived values during helper extraction.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py
- core/python/src/watchtower_core/repo_ops/planning_projection_policy.py
- core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py

## Design Guardrails
- Do not introduce a new public planning artifact, export-safe API, or compatibility wrapper as part of this slice.
- Do not widen the work into `coordination_index`, `task_index`, `traceability`, or initiative-closeout orchestration unless parity testing proves a same-change dependency.

## Risks
- Serializer splits can create subtle compact-mode drift that only shows up in query payloads or derived indexes.
- Catalog-only helper extraction can hide data provenance if the new helper boundary becomes too abstract.
- Tests that only assert document existence may miss payload-level regressions unless the slice adds more direct expectations.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
