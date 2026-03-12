---
trace_id: trace.coordination_projection_source_reuse
id: design.features.coordination_projection_source_reuse
title: Coordination Projection Source Reuse Feature Design
summary: Defines the technical design boundary for Coordination Projection Source
  Reuse.
type: feature_design
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

# Coordination Projection Source Reuse Feature Design

## Record Metadata
- `Trace ID`: `trace.coordination_projection_source_reuse`
- `Design ID`: `design.features.coordination_projection_source_reuse`
- `Design Status`: `active`
- `Linked PRDs`: `prd.coordination_projection_source_reuse`
- `Linked Decisions`: `decision.coordination_projection_source_reuse_direction`
- `Linked Implementation Plans`: `design.implementation.coordination_projection_source_reuse`
- `Updated At`: `2026-03-12T16:16:44Z`

## Summary
Defines the technical design boundary for Coordination Projection Source Reuse.

## Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope and Feature Boundary
- Covers command-scoped reuse of stable planning projection inputs and newly-built sync
  documents inside aggregate coordination orchestration.
- Covers both dry-run and write or output-directory sync flows because the dependency chain
  must stay faithful in each mode.
- Excludes cross-command caches, repository-wide loader memoization, and any change to the
  published planning or coordination artifact schemas.

## Current-State Context
- `CoordinationSyncService` runs a deterministic projection chain across task index,
  traceability index, initiative index, planning catalog, coordination index, and two human
  trackers.
- Those services currently reload overlapping planning index inputs from governed source even
  when the same loader instance already has the needed artifacts for the current run.
- Newly-built dry-run documents are not published to downstream services, so dependent
  services fall back to on-disk intermediates instead of the current-run results.
- Generated documents also need to cross the same schema-validation boundary before they are
  reusable current-run inputs; otherwise reuse would dilute fail-closed behavior.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should centralize reuse in orchestration and loader boundaries instead of creating hidden caching behavior in individual sync services.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the reuse layer must stay explicit enough that validation and deterministic output guarantees remain reviewable.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the implementation belongs in the canonical Python workspace and should preserve the thin CLI or orchestration boundary.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): the design must keep validation coverage whole instead of trading correctness for speed.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): dry-run and write-mode task or initiative projections must remain coherent within the same coordination slice.

## Design Goals and Constraints
- Reuse already-validated documents within one coordination sync run.
- Keep reuse command-scoped and explicit instead of introducing general-purpose implicit
  caches.
- Preserve the existing dependency order and the current artifact contents for write and
  output-directory sync modes.
- Preserve the same schema-validation boundary for generated documents before they are
  published as reusable overrides.

## Options Considered
### Option 1
- Add broad passive caching to `ControlPlaneLoader`.
- Strength: potentially benefits many command families at once.
- Tradeoff: unsafe unless every write path participates in invalidation, which raises stale
  state risk across non-sync commands.

### Option 2
- Add explicit validated-document overrides that sync orchestration primes and updates as the
  coordination projection chain executes.
- Strength: bounded to the current command and easy to reason about in dependency order.
- Tradeoff: requires orchestration wiring and a small loader extension.

## Recommended Design
### Architecture
- Extend `ControlPlaneLoader` with explicit command-scoped override surfaces for validated
  JSON documents and validated governed directories.
- Let aggregate sync orchestration preload stable planning inputs once and publish newly-built
  document outputs back into the loader as the current run advances.
- Keep individual sync services unchanged where possible so the reuse boundary stays in the
  loader or orchestration layer rather than spreading through each projection service.

### Data and Interface Impacts
- Affected runtime interfaces are limited to repo-local loader and sync orchestration methods.
- Published control-plane schemas, indexes, contracts, and tracker formats stay unchanged.
- Regression coverage needs to assert reduced source reads and correct dependency chaining for
  coordination sync.

### Execution Flow
1. Coordination sync preloads the stable planning index and ledger inputs that do not change
   within the current run.
2. When document sync services build task, traceability, initiative, planning-catalog, and
   coordination artifacts, orchestration schema-validates and stores those results as
   current-run
   overrides.
3. Downstream services load the overridden validated artifacts instead of rereading on-disk
   intermediates, including in dry-run mode.

### Invariants and Failure Cases
- Overrides must never escape the current loader instance, so a later command cannot inherit
  stale data.
- If a generated document is missing its required `entries` list or otherwise fails sync
  expectations, orchestration must still fail closed.
- If a generated document fails schema validation, orchestration must reject it before it can
  shadow the on-disk artifact through an override.
- Output-directory materialization must continue to honor the generated dependency chain even
  when fallback disk artifacts contain stale content.

## Affected Surfaces
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/

## Design Guardrails
- Do not add a general ambient cache that silently changes loader behavior for unrelated
  command families.
- Keep the reuse mechanism explicit enough that instrumentation can prove which source reads
  were eliminated.

## Risks
- Loader override handling could accidentally shadow unrelated reads if path scoping is too
  broad.
- Coordination sync tests need to cover both source-read reduction and dependency correctness
  so the optimization does not mask stale dry-run behavior.

## References
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/prds/coordination_projection_source_reuse.md)
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/coordination_projection_source_reuse.md)
- [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/all.py)
- [coordination.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/coordination.py)
