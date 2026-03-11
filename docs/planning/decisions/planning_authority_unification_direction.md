---
trace_id: "trace.planning_authority_unification"
id: "decision.planning_authority_unification_direction"
title: "Planning Authority Unification Direction Decision"
summary: "Records the decision to add a canonical planning catalog and machine authority map while keeping current family views as projections or compatibility surfaces."
type: "decision_record"
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
  - "planning catalog direction"
  - "authority map direction"
---

# Planning Authority Unification Direction Decision

## Record Metadata
- `Trace ID`: `trace.planning_authority_unification`
- `Decision ID`: `decision.planning_authority_unification_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.planning_authority_unification`
- `Linked Designs`: `design.features.planning_authority_unification`
- `Linked Implementation Plans`: `design.implementation.planning_authority_unification`
- `Updated At`: `2026-03-11T01:48:43Z`

## Summary
Records the decision to add a canonical planning catalog and machine authority map while keeping current family views as projections or compatibility surfaces.

## Decision Statement
Add one canonical machine planning catalog and one machine-readable authority map, keep existing coordination and family views available as narrower projections or compatibility surfaces, and make the new canonical path the preferred machine route for deep planning lookup.

## Trigger or Source Request
- Whole-repo review follow-up work requested from [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md), specifically the confirmed gaps around planning-authority scatter, missing machine authority discovery, and ambiguous planning status semantics.

## Current Context and Constraints
- The existing planning model works and should not be destabilized by a ground-up rewrite.
- Machines still need too many joins to reach full planning context today.
- Compatibility matters because current query and tracker surfaces are already in use.

## Applied References and Implications
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the chosen direction preserves traceability as the durable join anchor and builds the canonical planning catalog from governed trace-linked sources.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative and coordination views remain valid projections, but they should no longer be treated as the only machine planning answers.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): canonical authority should be explicit and machine-resolvable rather than distributed across several equally plausible surfaces.

## Affected Surfaces
- `core/control_plane/indexes/planning/`
- `core/control_plane/registries/authority_map/`
- `core/python/src/watchtower_core/repo_ops/sync/`
- `core/python/src/watchtower_core/repo_ops/query/`
- `core/python/src/watchtower_core/cli/`
- `docs/planning/README.md`
- `docs/commands/core_python/`
- `docs/standards/data_contracts/`

## Options Considered
### Option 1
- Replace the current planning and coordination surfaces with one new canonical artifact immediately.
- Strength: maximal conceptual cleanliness.
- Tradeoff: too much migration risk and unnecessary churn before product implementation.

### Option 2
- Add a canonical planning catalog and authority map while preserving current family indexes and coordination views as projections or compatibility surfaces.
- Strength: solves the confirmed machine-usability gap with bounded additive change.
- Tradeoff: the repo still carries multiple surfaces, so canonical precedence must be documented and enforced clearly.

### Option 3
- Leave the current planning system unchanged and only add more prose guidance.
- Strength: lowest short-term implementation cost.
- Tradeoff: does not materially reduce machine join cost or canonical-surface ambiguity.

## Chosen Outcome
Adopt option 2. The repo will add one planning catalog as the canonical machine planning join and one machine authority map as the canonical lookup policy for planning and governance questions. Existing coordination, initiative, trace, and family-index views remain, but they will be documented as start-here, focused, or compatibility surfaces rather than the only machine authorities.

## Rationale and Tradeoffs
- The existing repo already contains the needed source data, so an additive canonical join is cheaper and safer than a rewrite.
- The decision resolves the status-semantics problem by introducing a canonical path with explicit field names instead of trying to reinterpret every existing payload in place.
- The main tradeoff is continuing to support multiple projections for now, which is acceptable because the new authority map will make precedence explicit.

## Consequences and Follow-Up Impacts
- The control plane gains two new governed artifact families.
- The query surface gains one new canonical planning command and one new authority-discovery command.
- Standards and navigation docs must explain canonical-versus-projection roles explicitly.
- A later initiative may still choose to derive more human planning trackers directly from the planning catalog once it has stabilized.

## Risks, Dependencies, and Assumptions
- The approach assumes the current traceability and initiative surfaces are reliable enough to serve as planning-catalog source material.
- The authority map will only stay useful if it is treated as maintained policy rather than one-off documentation.
- Compatibility assumptions in current consumers may require keeping some legacy fields or notes during the transition.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [initiative_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/initiative_index.v1.json)
- [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json)
