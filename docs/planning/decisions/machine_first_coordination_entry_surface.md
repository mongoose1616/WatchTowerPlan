---
trace_id: "trace.machine_first_coordination_surface"
id: "decision.machine_first_coordination_entry_surface"
title: "Machine-First Coordination Entry Surface Decision"
summary: "Records the decision to add one derived coordination index above the family-specific planning indexes and use it as the default machine start-here surface."
type: "decision_record"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T18:54:43Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/"
  - "core/control_plane/indexes/coordination/"
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "coordination index decision"
  - "planning start-here decision"
---

# Machine-First Coordination Entry Surface Decision

## Record Metadata
- `Trace ID`: `trace.machine_first_coordination_surface`
- `Decision ID`: `decision.machine_first_coordination_entry_surface`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.machine_first_coordination_surface`
- `Linked Designs`: `design.features.machine_first_coordination_surface`
- `Linked Implementation Plans`: `design.implementation.machine_first_coordination_execution`
- `Updated At`: `2026-03-10T18:54:43Z`

## Summary
This decision records the choice to add one derived coordination index above the family-specific planning indexes and use it as the default machine start-here surface.

## Decision Statement
Publish a derived coordination index and companion human coordination tracker as the default planning start-here surfaces while keeping initiative, task, traceability, PRD, design, and decision indexes authoritative for their own families.

## Trigger or Source Request
The repo review showed that the current coordination path still leaves agents guessing across several family indexes, especially when no initiative is active. A stronger always-useful coordination surface is needed without collapsing existing planning authority.

## Current Context and Constraints
- The family-specific indexes and authored planning families are working and validated.
- `query coordination` already exists, so the command surface can evolve without adding a new command family.
- The repo should not create a second authored planning family just to add a start-here view.

## Applied References and Implications
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative tracking remains available, but default current-state navigation can move up one derived layer.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traceability remains the durable cross-family join, not the human start-here layer.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the human coordination byproduct must stay compact and not recreate the entire family trackers.

## Affected Surfaces
- `docs/planning/README.md`
- `docs/planning/coordination_tracking.md`
- `core/control_plane/indexes/coordination/coordination_index.v1.json`
- `core/python/src/watchtower_core/repo_ops/sync/`
- `core/python/src/watchtower_core/cli/`

## Options Considered
### Option 1
- Keep using the initiative index as the machine coordination entrypoint.
- Strength: no new artifact family.
- Tradeoff: still fails the no-active-initiative case and still leaves machine coordination scattered.

### Option 2
- Add one derived coordination index above the family indexes and one compact human tracker from the same data.
- Strength: creates one always-useful start-here surface while preserving the authority model.
- Tradeoff: adds one more derived artifact family that must stay intentionally compact.

### Option 3
- Replace family trackers with one authored coordination document.
- Strength: fewer visible planning surfaces.
- Tradeoff: destabilizes authority boundaries and increases merge contention on human-authored state.

## Chosen Outcome
Adopt option 2. The coordination index becomes the default machine start-here planning surface, and a compact generated coordination tracker becomes the default human start-here view.

## Rationale and Tradeoffs
- This is the smallest change that gives both humans and agents one explicit current-state entrypoint.
- It preserves the existing authoritative planning families instead of forcing a planning-model migration.
- The tradeoff is one additional derived artifact family, which is acceptable only if it stays compact and clearly above the family-specific views.

## Consequences and Follow-Up Impacts
- `query coordination` should read from the coordination index.
- The coordination sync slice should materialize the coordination index and tracker in the same run as initiative and task current-state surfaces.
- Planning README and agent guidance should route through the new coordination surfaces first.

## Risks, Dependencies, and Assumptions
- The coordination index could sprawl if it tries to subsume task or traceability detail.
- The design assumes humans still need family-specific trackers after the first coordination pass.

## References
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/prds/machine_first_coordination_surface.md)
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/design/features/machine_first_coordination_surface.md)
- [preimplementation_machine_coordination_entrypoint.md](/home/j/WatchTowerPlan/docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md)

## Updated At
- `2026-03-10T18:54:43Z`
