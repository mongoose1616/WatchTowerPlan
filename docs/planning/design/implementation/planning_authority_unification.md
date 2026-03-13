---
trace_id: "trace.planning_authority_unification"
id: "design.implementation.planning_authority_unification"
title: "Planning Authority Unification Implementation Plan"
summary: "Breaks the planning catalog, authority-map, and status-semantics work into bounded executable slices."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-11T01:48:43Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/control_plane/"
  - "core/python/"
  - "docs/planning/"
  - "docs/commands/core_python/"
aliases:
  - "planning catalog execution"
  - "authority map execution"
---

# Planning Authority Unification Implementation Plan

## Record Metadata
- `Trace ID`: `trace.planning_authority_unification`
- `Plan ID`: `design.implementation.planning_authority_unification`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.planning_authority_unification`
- `Linked Decisions`: `decision.planning_authority_unification_direction`
- `Source Designs`: `design.features.planning_authority_unification`
- `Linked Acceptance Contracts`: `contract.acceptance.planning_authority_unification`
- `Updated At`: `2026-03-11T01:48:43Z`

## Summary
Breaks the planning catalog, authority-map, and status-semantics work into bounded executable slices.

## Source Request or Design
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authority_unification.md)
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_authority_unification.md)

## Scope Summary
- Add the planning-catalog index family plus canonical query and sync support.
- Add the machine authority-map registry plus a discovery query surface.
- Update companion standards, docs, and navigation surfaces so machines and humans can trust the new canonical planning path.
- Exclude broad retirement of existing family indexes or trackers.
- Exclude external pack runtime work and incremental maintenance work.

## Assumptions and Constraints
- The current index families remain valid source material and must not be broken while the new catalog lands.
- Compatibility matters more than theoretical purity; existing queries can be clarified without being removed.
- The authority map is authored governance policy, not a fully derived artifact.

## Current-State Context
- An earlier whole-repo review already identified the lack of a canonical machine planning join and the absence of a machine-readable authority map as the highest-leverage remaining coherence issue.
- The repo already has the raw data needed for a planning catalog in its existing indexes, acceptance contracts, and evidence ledgers.
- The command surface can add one new planning query and one new authority query without reopening the broader CLI design.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the implementation should assemble a canonical join from existing trace-linked governed artifacts rather than replacing traceability.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): new artifact families require schema, catalog, validator, and example updates in the same change set.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): new command surfaces need companion documentation and command-index alignment in the same slice.

## Proposed Technical Approach
- Add a new planning-catalog sync service that joins traceability, initiative, planning-document, task, acceptance, and evidence data into one canonical machine artifact.
- Add typed models and loader methods for the planning catalog and authority map.
- Add `query planning` and `query authority` handlers plus command docs and query-root guidance.
- Update standards, README surfaces, and compatibility docs so the canonical-versus-projection model is explicit.
- Keep the implementation additive: existing family indexes and trackers continue to derive from their current sources during this initiative.

## Work Breakdown
1. Bootstrap the initiative, acceptance contract, planning-baseline evidence, accepted direction decision, and bounded task set.
2. Implement the planning-catalog artifact family, typed models, loader support, sync command, canonical planning query, companion docs, and tests.
3. Implement the machine authority-map artifact family, authority query, standards and navigation updates, then validate and close the initiative.

## Risks
- Sync dependency mistakes could create a catalog that looks canonical but is internally stale.
- Status-field compatibility mistakes could confuse existing JSON consumers.
- Authority-map docs could over-document instead of staying focused on canonical lookup.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after each slice.
- Run `./.venv/bin/watchtower-core validate all --format json` after each slice.
- Add unit coverage for planning-catalog sync, authority-map query behavior, and canonical status fields.
- Add CLI query coverage for `query planning` and `query authority`.
- Run `./.venv/bin/watchtower-core doctor --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src`, and `./.venv/bin/ruff check .` before closeout.

## Rollout or Migration Plan
- Land one planning bootstrap commit with the traced docs, acceptance contract, evidence, and bounded tasks.
- Land one code-and-doc slice for the planning catalog and canonical planning query.
- Land one code-and-doc slice for the machine authority map and navigation/standards updates.
- Close the initiative only after the canonical planning and authority surfaces are documented and validated.

## References
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authority_unification.md)
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_authority_unification.md)
