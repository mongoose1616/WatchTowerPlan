---
trace_id: "trace.machine_first_coordination_surface"
id: "design.features.machine_first_coordination_surface"
title: "Machine-First Coordination Surface Design"
summary: "Defines the derived coordination index and compact human byproduct needed to make one always-useful coordination surface the default start-here view for planning state."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T18:54:43Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/"
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/repo_ops/"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "coordination surface design"
---

# Machine-First Coordination Surface Design

## Record Metadata
- `Trace ID`: `trace.machine_first_coordination_surface`
- `Design ID`: `design.features.machine_first_coordination_surface`
- `Design Status`: `active`
- `Linked PRDs`: `prd.machine_first_coordination_surface`
- `Linked Decisions`: `decision.machine_first_coordination_entry_surface`
- `Linked Implementation Plans`: `design.implementation.machine_first_coordination_execution`
- `Updated At`: `2026-03-10T18:54:43Z`

## Summary
Defines the derived coordination index and compact human byproduct needed to make one always-useful coordination surface the default start-here view for planning state.

## Source Request
- User request for a full repo review with a stronger machine-first task and initiative coordination model before product implementation begins.

## Scope and Feature Boundary
- Covers one new derived coordination index and its human-readable byproduct.
- Covers query, sync, loader, schema, and planning-entrypoint updates required to make that surface authoritative for machine start-here use.
- Covers no-active-initiative fallback behavior.
- Does not replace the family-specific indexes or authored planning families.

## Current-State Context
- [initiative_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/initiative_index.v1.json) is useful for active traced work, but it is not an always-useful coordination surface.
- `watchtower-core query coordination` currently returns zero results when no initiative is active.
- [task_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/tasks/task_index.v1.json) and the family trackers still hold the details needed after the first pass, but they are not a good default machine entrypoint.
- [docs/planning/README.md](/home/j/WatchTowerPlan/docs/planning/README.md) still explains multiple family entrypoints rather than one derived current-state view.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): coordination should be explicit, compact, and inspectable.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): derived coordination must project from existing authority rather than competing with it.
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md): pre-implementation and later product work both benefit from one machine-first start-here surface.

## Internal Standards and Canonical References Applied
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): initiative state remains authoritative for initiative-family detail.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): tasks remain task-authoritative even when projected into a coordination summary.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the human coordination byproduct should stay compact and scan-first.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the derived surface should keep command entrypoints thin and the sync/query logic modular.

## Design Goals and Constraints
- Make one machine-readable coordination surface the default entrypoint for planning state.
- Keep the coordination surface useful when work is active and when the repo is idle between initiatives.
- Keep the human byproduct compact and generated.
- Avoid denormalizing so much data that the coordination index becomes a second task or traceability authority.

## Options Considered
### Option 1
- Keep the initiative index as the coordination entrypoint and only add better empty-state messaging.
- Would be cheaper.
- Was not chosen because it still leaves machine coordination split across family indexes and does not create one explicit always-useful coordination artifact.

### Option 2
- Add a derived coordination index above the family-specific indexes and derive a compact human coordination view from it.
- Chosen because it creates one start-here surface without disturbing the existing authority model.

### Option 3
- Replace initiative and task tracking with one new authored coordination document.
- Was not chosen because it would create source-of-truth churn and higher merge contention on the human planning layer.

## Recommended Design
### Coordination Index
- Add `core/control_plane/indexes/coordination/coordination_index.v1.json` as a derived machine-readable planning current-state surface.
- Populate it from the existing initiative, task, and traceability indexes plus current planning docs.
- Include:
  - current coordination mode such as `active_execution` or `ready_for_bootstrap`
  - active initiative summaries
  - actionable task summaries
  - blocked task counts
  - recent closed initiative summaries
  - recommended next action and next surface path

### Query and Sync Integration
- Add a typed coordination model to `watchtower_core.control_plane.models`.
- Add a loader entry for the coordination index.
- Add a dedicated sync service for the coordination index and include it in `sync all` and `sync coordination`.
- Change `watchtower-core query coordination` to read from the coordination index instead of inferring state directly from the initiative query service.

### Human Byproduct
- Generate `docs/planning/coordination_tracking.md` from the coordination index.
- Keep it compact: current mode, top active work, actionable tasks, recent closeouts, and the default next surface.
- Position it as the human start-here view while keeping family trackers for detailed family-specific browsing.

### Entry Surface Alignment
- Update planning README and nearby guidance to point humans at `coordination_tracking.md`.
- Update root agent guidance to point machines at `query coordination` first when the main question is current planning state.

## Affected Surfaces
- `core/control_plane/schemas/artifacts/`
- `core/control_plane/indexes/coordination/`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/repo_ops/sync/`
- `core/python/src/watchtower_core/cli/`
- `core/python/tests/`
- `docs/planning/`

## Design Guardrails
- Do not duplicate full task documents or traceability joins inside the coordination index.
- Do not create a second authored planning family.
- Do not make the human coordination byproduct longer than the family trackers it is meant to replace as the default entrypoint.

## Implementation-Planning Handoff Notes
- Land the coordination index schema, model, sync service, and query path first.
- Land the human coordination tracking surface and entrypoint guidance second.
- Keep the existing initiative and task trackers in place while rerouting default entry guidance.

## Dependencies
- Existing initiative, task, and traceability indexes.
- Existing sync-family orchestration and query command-family surfaces.
- The closed preimplementation hardening initiative that made `query coordination` an explicit command surface.

## Risks
- The derived coordination surface could drift if it is not rebuilt alongside the current coordination sync slice.
- Adding a human byproduct without clear entrypoint guidance would only create one more tracker.

## References
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/prds/machine_first_coordination_surface.md)
- [preimplementation_machine_coordination_entrypoint.md](/home/j/WatchTowerPlan/docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md)

## Updated At
- `2026-03-10T18:54:43Z`
