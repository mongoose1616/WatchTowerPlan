---
trace_id: trace.coordination_projection_source_reuse
id: decision.coordination_projection_source_reuse_direction
title: Coordination Projection Source Reuse Direction Decision
summary: Prefer explicit command-scoped validated artifact overrides in sync orchestration
  over broad passive loader caching.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T15:55:07Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Coordination Projection Source Reuse Direction Decision

## Record Metadata
- `Trace ID`: `trace.coordination_projection_source_reuse`
- `Decision ID`: `decision.coordination_projection_source_reuse_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.coordination_projection_source_reuse`
- `Linked Designs`: `design.features.coordination_projection_source_reuse`
- `Linked Implementation Plans`: `design.implementation.coordination_projection_source_reuse`
- `Updated At`: `2026-03-12T15:55:07Z`

## Summary
Prefer explicit command-scoped validated artifact overrides in sync orchestration over broad
passive loader caching.

## Decision Statement
Add explicit validated artifact overrides to the loader and let aggregate sync orchestration
prime and publish current-run coordination projection artifacts instead of introducing a broad
implicit cache.

## Trigger or Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Current Context and Constraints
- Coordination sync currently rereads the same planning indexes from governed source multiple
  times within one deterministic run.
- The loader currently has no explicit way for orchestration to publish a just-built document
  for downstream reuse in dry-run mode.
- A broad passive cache would be risky because not every write path in the repository can
  safely participate in cache invalidation today.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): prefer explicit, bounded composition over hidden mutable behavior.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): preserve fail-closed deterministic behavior while optimizing internal orchestration.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): keep the implementation inside the canonical Python workspace and validate it with the standard toolchain.

## Affected Surfaces
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/

## Options Considered
### Option 1
- Introduce passive memoization in `ControlPlaneLoader` for all validated reads.
- Strength: wider theoretical performance benefit.
- Tradeoff: unsafe unless every read-after-write path participates in invalidation, which the
  repo does not currently guarantee.

### Option 2
- Add explicit validated-document and validated-directory overrides and let sync orchestration
  manage them only for the current run.
- Strength: bounded to the relevant orchestration slice and compatible with dry-run fidelity.
- Tradeoff: requires small orchestration changes and targeted tests.

## Chosen Outcome
Choose explicit command-scoped override support and wire it through coordination or aggregate
sync orchestration for the stable planning inputs and generated coordination projection
artifacts.

## Rationale and Tradeoffs
- This keeps the optimization local to the command and the deterministic dependency chain that
  actually needs it.
- It reduces repeated source reads without creating hidden stale-state risks for unrelated
  commands.
- The approach also improves dry-run fidelity because downstream sync services can consume the
  current-run generated documents even when nothing is written to disk.

## Consequences and Follow-Up Impacts
- The loader gains an explicit override surface that orchestration can use deliberately.
- Aggregate sync code needs to preload stable planning inputs once and update overrides as
  document targets complete.
- Regression coverage needs to measure source-read reduction and generated dependency reuse.

## Risks, Dependencies, and Assumptions
- Override scope must stay narrow and path-specific.
- The design assumes coordination sync ordering remains task index, traceability, initiative,
  planning catalog, coordination index, then trackers.
- Future commands that want similar reuse should opt in explicitly instead of inheriting broad
  cache behavior implicitly.

## References
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/prds/coordination_projection_source_reuse.md)
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/features/coordination_projection_source_reuse.md)
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/coordination_projection_source_reuse.md)
