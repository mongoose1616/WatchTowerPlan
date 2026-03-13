---
trace_id: "trace.planning_authority_unification"
id: "prd.planning_authority_unification"
title: "Planning Authority Unification PRD"
summary: "Create one canonical machine planning catalog, publish a machine authority map, and normalize planning query status semantics for machine consumers."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-11T01:48:43Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/"
  - "core/python/"
  - "docs/planning/"
  - "docs/commands/core_python/"
aliases:
  - "planning catalog"
  - "machine authority map"
---

# Planning Authority Unification PRD

## Record Metadata
- `Trace ID`: `trace.planning_authority_unification`
- `PRD ID`: `prd.planning_authority_unification`
- `Status`: `active`
- `Linked Decisions`: `decision.planning_authority_unification_direction`
- `Linked Designs`: `design.features.planning_authority_unification`
- `Linked Implementation Plans`: `design.implementation.planning_authority_unification`
- `Updated At`: `2026-03-11T01:48:43Z`

## Summary
Create one canonical machine planning catalog, publish a machine authority map, and normalize planning query status semantics for machine consumers.

## Problem Statement
The repository's planning model is disciplined, but machine consumers still need to reason across too many partially overlapping surfaces to answer basic planning questions. Current-state lookup starts well with coordination, but a deeper machine consumer must still combine traceability, initiative, task, PRD, design, decision, acceptance-contract, and evidence artifacts manually. At the same time, current query payloads expose a generic `status` field alongside `initiative_status`, which is defensible internally but easy to misread as one unified status model. The result is a repo that is valid and traceable but still unnecessarily expensive for agents and maintainers to navigate safely.

## Goals
- Publish one canonical machine planning catalog that joins trace, coordination, planning-doc, task, acceptance, and evidence state by `trace_id`.
- Make status semantics explicit in the canonical machine planning path by separating artifact lifecycle, initiative outcome, decision outcome, and task execution state.
- Publish a machine-readable authority map that tells consumers which surface is canonical for each planning or governance question.
- Keep existing family indexes, trackers, and query commands available while making their relationship to the canonical planning authority explicit.
- Preserve the repository's current green validation and test baseline throughout the initiative.

## Non-Goals
- Replacing every existing family index or human tracker in one initiative.
- Removing `query coordination`, `query initiatives`, or `query trace` as supported command surfaces.
- Reworking external pack runtime support, pack manifests, or product implementation concerns.
- Broadly redesigning the workflow system or repo routing model outside the planning-authority problem.

## Target Users or Actors
- Agents that need one safe machine entrypoint for deeper planning context after coordination routing.
- Repository maintainers reviewing trace-linked planning state without manually joining multiple indexes.
- Future consuming repos and automation that need to know which planning or governance artifact is canonical for a given question.

## Key Scenarios
- An agent starts at `query coordination`, identifies one trace, then needs one canonical machine surface for the PRD, design, implementation plan, decisions, tasks, acceptance contracts, evidence, and next action for that trace.
- A maintainer needs to know whether `status` means artifact lifecycle, initiative outcome, or task execution state without remembering implementation history.
- A script or agent needs to answer "which surface is canonical for current planning state, trace-linked planning context, or workflow routing?" without reverse engineering the repo layout.

## Requirements
- `req.planning_authority_unification.001`: The repo must publish one canonical machine planning catalog artifact that joins traceability, initiative coordination, planning documents, tasks, acceptance contracts, and validation evidence by trace.
- `req.planning_authority_unification.002`: The canonical planning query path must expose explicit status semantics such as `artifact_status`, `initiative_status`, `task_status`, `record_status`, and `decision_status` instead of relying on one ambiguous `status` field.
- `req.planning_authority_unification.003`: The repo must publish a machine-readable authority map for planning and governance questions, including the canonical artifact path and preferred query command for each supported question.
- `req.planning_authority_unification.004`: Command docs, planning entrypoints, and related standards must explain that the planning catalog is the canonical machine join while existing coordination and family views remain focused projections or compatibility surfaces.
- `req.planning_authority_unification.005`: The initiative must preserve repository validation, traceability, and same-change companion-surface discipline while the new planning-authority surfaces land.

## Acceptance Criteria
- `ac.planning_authority_unification.001`: The planning corpus publishes an active PRD, accepted direction decision, feature design, implementation plan, closed bootstrap task, and bounded open execution tasks for `trace.planning_authority_unification`.
- `ac.planning_authority_unification.002`: The repo publishes a governed planning-catalog artifact family with schema, canonical artifact, schema-catalog entry, artifact-type entry, validator coverage, examples, sync support, and typed loader support.
- `ac.planning_authority_unification.003`: `watchtower-core query planning` returns canonical machine planning records with explicit status semantics and linked planning, task, acceptance, evidence, and coordination sections.
- `ac.planning_authority_unification.004`: The repo publishes a governed machine authority map plus `watchtower-core query authority` so agents and scripts can resolve canonical planning and governance surfaces without architecture memory.
- `ac.planning_authority_unification.005`: Root, planning, and command docs explain the canonical-versus-projection relationship across `query coordination`, `query initiatives`, `query trace`, `query planning`, and the authority map.
- `ac.planning_authority_unification.006`: The repository remains green on the current validation baseline while the initiative lands and closes.

## Success Metrics
- A machine consumer can resolve full trace-linked planning context from one catalog query instead of manually joining multiple indexes.
- The canonical machine path no longer uses a generic `status` field where the intended meaning is initiative outcome or task execution.
- Maintainers have one machine-readable authority map for planning and governance lookup rather than relying on repo memory or prose inference.

## Risks and Dependencies
- The planning catalog could become another redundant artifact if it does not clearly define its canonical scope relative to coordination and family indexes.
- Over-correcting the status-semantic issue could break existing consumers if compatibility needs are ignored.
- The initiative depends on the correctness of the existing traceability, initiative, task, PRD, design, decision, acceptance, and evidence surfaces it will join.

## Open Questions
- Whether later initiatives should derive more human trackers directly from the planning catalog once the canonical machine join has stabilized.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the solution should prefer explicit boundaries, deterministic joins, and export-safe machine interfaces over informal multi-surface navigation.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the repo should reduce authority ambiguity and favor clearly named canonical surfaces instead of preserving equivalent entrypoints indefinitely.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the work belongs in `WatchTowerPlan` because it strengthens the reusable governed core and planning substrate, not product implementation.

## References
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json)
- [initiative_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/initiative_index.v1.json)

## Updated At
- `2026-03-11T01:48:43Z`
