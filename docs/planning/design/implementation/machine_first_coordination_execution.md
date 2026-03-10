---
trace_id: "trace.machine_first_coordination_surface"
id: "design.implementation.machine_first_coordination_execution"
title: "Machine-First Coordination Surface Implementation Plan"
summary: "Breaks the coordination-surface work into bounded slices for the coordination index, the generated human byproduct, and aligned planning entrypoint guidance."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T18:54:43Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/"
  - "docs/planning/"
aliases:
  - "coordination execution plan"
---

# Machine-First Coordination Surface Implementation Plan

## Record Metadata
- `Trace ID`: `trace.machine_first_coordination_surface`
- `Plan ID`: `design.implementation.machine_first_coordination_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.machine_first_coordination_surface`
- `Source Designs`: `design.features.machine_first_coordination_surface`
- `Linked Acceptance Contracts`: `contract.acceptance.machine_first_coordination_surface`
- `Updated At`: `2026-03-10T18:54:43Z`

## Summary
Breaks the coordination-surface work into bounded slices for the coordination index, the generated human byproduct, and aligned planning entrypoint guidance.

## Source Request or Design
- Feature design: [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/design/features/machine_first_coordination_surface.md)
- PRD: [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/prds/machine_first_coordination_surface.md)

## Scope Summary
- Add the coordination index, schema, model, loader entry, sync service, and query path.
- Generate a compact human coordination tracker from the same derived state.
- Update planning and agent entrypoint guidance so one coordination surface becomes the default start-here path.
- Keep the existing family-specific indexes and trackers intact.

## Assumptions and Constraints
- The new coordination index is derived only; family-specific indexes remain authoritative.
- The new human coordination tracker must stay smaller than the combined family trackers it summarizes.
- The work should stay bounded to planning coordination rather than reopening broader documentation or code-modularity scope.

## Current-State Context
- The repo is green and has no active initiative after the completed preimplementation hardening pass.
- `query coordination` exists but now exposes the empty-state weakness directly.
- The sync and validation command surfaces already exist, so the main work is adding one derived artifact family and rerouting entrypoint guidance.

## Internal Standards and Canonical References Applied
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the generated human coordination surface must stay proportional.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): family trackers remain available, but default entrypoint guidance can shift to the new coordination layer.

## Proposed Technical Approach
- Add a new coordination-index artifact family and keep it derived from the existing initiative and task families.
- Add a new sync service and include it in the coordination sync slice plus `sync all`.
- Generate one compact human tracking page from the same index and route planning entrypoint docs plus agent guidance to it.

## Work Breakdown
1. Bootstrap the traced planning chain, acceptance contract, planning evidence, decision record, and bounded task set.
2. Add the coordination index schema, example coverage, model, loader method, sync service, and `query coordination` integration.
3. Generate `docs/planning/coordination_tracking.md`, update planning and agent entrypoint docs, and keep command docs aligned.
4. Rebuild derived surfaces, rerun validation, close tasks, and close the initiative.

## Dependencies
- Existing initiative, task, and traceability indexes.
- Existing sync-family registration and command documentation surfaces.

## Risks
- Coordination-state projection can become noisy if it exposes too much low-value detail.
- Empty-state guidance can become too vague if it does not point to a concrete bootstrap surface.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after planning or governed-surface changes.
- Run `./.venv/bin/watchtower-core validate all --format json` after each implementation slice.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, and `./.venv/bin/ruff check .` after code slices.
- Add targeted tests for active-work and ready-for-bootstrap coordination projection, command output, and tracker rendering.

## Rollout or Migration Plan
- Land one planning bootstrap commit first.
- Land one commit for the coordination index code and machine-readable surfaces.
- Land one commit for the human coordination byproduct and entrypoint guidance.
- Land a final closeout commit after the repo is green.

## References
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/prds/machine_first_coordination_surface.md)
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/design/features/machine_first_coordination_surface.md)

## Updated At
- `2026-03-10T18:54:43Z`
