---
trace_id: trace.coordination_projection_source_reuse
id: prd.coordination_projection_source_reuse
title: Coordination Projection Source Reuse PRD
summary: Eliminate repeated planning-index and evidence source reloads inside coordination
  sync while preserving deterministic projection outputs, validation boundaries, and
  dry-run fidelity.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T16:16:44Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Coordination Projection Source Reuse PRD

## Record Metadata
- `Trace ID`: `trace.coordination_projection_source_reuse`
- `PRD ID`: `prd.coordination_projection_source_reuse`
- `Status`: `active`
- `Linked Decisions`: `decision.coordination_projection_source_reuse_direction`
- `Linked Designs`: `design.features.coordination_projection_source_reuse`
- `Linked Implementation Plans`: `design.implementation.coordination_projection_source_reuse`
- `Updated At`: `2026-03-12T16:16:44Z`

## Summary
Eliminate repeated planning-index and evidence source reloads inside coordination sync while preserving deterministic projection outputs, validation boundaries, and dry-run fidelity.

## Problem Statement
The comprehensive refactoring and optimization review found a real scale defect in the
coordination projection slice. A single `watchtower-core sync coordination` run reloads the
same planning indexes and evidence inputs from governed source multiple times while
rebuilding the dependent traceability, initiative, planning-catalog, coordination, and
tracker surfaces. Direct instrumentation on the live repo shows one dry-run coordination
sync rereads the same planning index artifact family `18` times from source before counting
acceptance and validation-evidence scans. As the planning corpus grows, that repeated load
and validation work increases runtime cost and keeps dry-run orchestration more dependent on
on-disk intermediate artifacts than it needs to be.

## Goals
- Reuse command-scoped validated planning source artifacts across dependent coordination sync
  targets.
- Preserve deterministic coordination outputs in `sync coordination`, `sync all`, and
  output-directory materialization flows.
- Keep dry-run orchestration faithful to the same dependency chain that write mode uses.
- Close the review finding with explicit regression coverage, full validation, and a clean
  follow-up review pass.

## Non-Goals
- Adding a process-global or cross-command cache for governed control-plane artifacts.
- Changing planning, traceability, initiative, coordination, or tracker document shapes.
- Skipping schema validation or weakening fail-closed behavior to reduce runtime cost.

## Requirements
- `req.coordination_projection_source_reuse.001`: Sync orchestration must be able to publish
  explicit command-scoped validated artifact overrides for already-loaded or newly-built
  governed JSON documents so downstream services can reuse them without rereading source.
- `req.coordination_projection_source_reuse.002`: Coordination sync must preload the stable
  planning projection inputs it reuses repeatedly and expose newly-built task, traceability,
  initiative, planning-catalog, and coordination documents to downstream sync services in
  the same run.
- `req.coordination_projection_source_reuse.003`: The reuse mechanism must preserve current
  write-mode artifact outputs and make dry-run dependency resolution use the same current-run
  projection chain instead of stale on-disk intermediates.
- `req.coordination_projection_source_reuse.004`: Generated document overrides must be schema
  validated before they become current-run coordination sync inputs, so reuse never weakens
  fail-closed artifact guarantees.
- `req.coordination_projection_source_reuse.005`: The initiative must prove the reuse
  behavior with direct instrumentation and keep the repository green on the normal validation
  baseline.

## Acceptance Criteria
- `ac.coordination_projection_source_reuse.001`: The trace publishes a fully-authored PRD,
  accepted direction decision, active feature design, active implementation plan, refreshed
  acceptance contract, refreshed evidence ledger, and bounded closed task set for
  `trace.coordination_projection_source_reuse`.
- `ac.coordination_projection_source_reuse.002`: Direct instrumentation shows coordination
  sync reuses stable planning source artifacts and generated projection documents instead of
  rereading the same governed planning index paths from source for each dependent service.
- `ac.coordination_projection_source_reuse.003`: Coordination sync write and output-directory
  flows preserve deterministic projection outputs, and dry-run orchestration uses generated
  current-run dependencies instead of stale on-disk intermediates while only publishing
  schema-validated generated overrides.
- `ac.coordination_projection_source_reuse.004`: Targeted regressions plus the full
  repository validation baseline pass after the coordination projection reuse change lands.
- `ac.coordination_projection_source_reuse.005`: A follow-up review of adjacent
  control-plane loader and coordination sync surfaces finds no additional actionable issues.

## Risks and Dependencies
- Loader-level reuse must stay explicit and command-scoped so later commands never see stale
  control-plane state.
- Sync orchestration must update overrides in dependency order; otherwise later targets could
  accidentally read stale generated documents.
- Generated document publication must preserve the existing validation boundary; otherwise the
  optimization could hide invalid sync outputs from downstream consumers.
- The change depends on current coordination sync ordering continuing to treat task,
  traceability, initiative, planning-catalog, and coordination artifacts as a deterministic
  projection chain.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): optimization should remove repeated work through explicit composition boundaries rather than hidden mutable state.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): reuse changes must preserve fail-closed behavior and keep human and machine planning surfaces aligned in the same slice.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): as the governed core grows, internal repository orchestration needs to scale without losing operator trust or fidelity.

## References
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/features/coordination_projection_source_reuse.md)
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/coordination_projection_source_reuse.md)
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)

## Updated At
- `2026-03-12T16:16:44Z`
