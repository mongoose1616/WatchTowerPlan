---
trace_id: "trace.planning_authority_unification"
id: "design.features.planning_authority_unification"
title: "Planning Authority Unification Feature Design"
summary: "Defines the technical design for a canonical planning catalog, a machine authority map, and explicit planning-status semantics."
type: "feature_design"
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

# Planning Authority Unification Feature Design

## Record Metadata
- `Trace ID`: `trace.planning_authority_unification`
- `Design ID`: `design.features.planning_authority_unification`
- `Design Status`: `active`
- `Linked PRDs`: `prd.planning_authority_unification`
- `Linked Decisions`: `decision.planning_authority_unification_direction`
- `Linked Implementation Plans`: `design.implementation.planning_authority_unification`
- `Updated At`: `2026-03-11T01:48:43Z`

## Summary
Defines the technical design for a canonical planning catalog, a machine authority map, and explicit planning-status semantics.

## Source Request
- User request to review [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md), verify the remaining issues, and complete the still-valid remediation initiatives end to end.

## Scope and Feature Boundary
- Covers one new machine-readable planning catalog artifact family that joins trace-linked planning, task, acceptance, evidence, and initiative-coordination state.
- Covers one new machine-readable authority-map artifact family plus a query command for canonical surface lookup.
- Covers canonical planning query behavior and status-semantics clarification for machine consumers.
- Covers companion standards, command docs, root and planning entrypoint updates, and compatibility notes needed to adopt the canonical machine surfaces cleanly.
- Does not replace existing family indexes or human trackers in this initiative.
- Does not add external pack runtime, incremental maintenance, or product-implementation behavior.

## Current-State Context
- The repo already publishes strong machine-readable surfaces, but deeper planning context is still distributed across traceability, initiative, task, PRD, design, decision, acceptance-contract, and evidence artifacts.
- `query coordination` is a good machine start-here path for current work, but it is not a canonical deep planning join.
- Existing planning and coordination payloads expose `status` alongside `initiative_status`, which is understandable internally but too easy to misread by machine consumers.
- There is no machine-readable authority map that answers which artifact or query surface is canonical for common planning and governance questions.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should make authority explicit, keep joins deterministic, and prefer well-bounded reusable interfaces over implied conventions.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the canonical machine answer for a question should be explicit rather than reconstructed across overlapping surfaces.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): this work belongs inside the repository's governed core and planning substrate, not in future product-pack implementation.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the new canonical planning join must preserve explicit trace links instead of replacing them with undocumented derived assumptions.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative and coordination views remain useful projections, so the design must clarify their role relative to the canonical machine planning catalog.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): the authority and planning surfaces should stay discoverable through machine-readable lookup rather than only through prose docs.

## Design Goals and Constraints
- Provide one canonical machine planning surface without forcing a destabilizing rewrite of all existing family indexes.
- Keep current coordination and initiative views useful for active-work routing while making their canonical boundary explicit.
- Make status semantics obvious in the canonical machine path.
- Preserve compatibility for existing machine and human workflows during the transition.
- Avoid building a catalog that stores duplicate prose-only data not needed for machine planning joins.

## Options Considered
### Option 1
- Rewrite the planning system around one entirely new planning artifact and retire existing family indexes immediately.
- Strength: one clean theoretical authority surface.
- Tradeoff: too disruptive, too much migration risk, and unnecessary because the current indexes already contain most of the needed source data.

### Option 2
- Add one canonical planning catalog and one machine authority map on top of the current index family, then make existing coordination and family views explicit projections or compatibility surfaces.
- Strength: solves the authority and status problems with bounded change and preserves the current working repo model.
- Tradeoff: the repo will still carry multiple derived surfaces, so documentation and standards need to explain precedence clearly.

### Option 3
- Document the current model better without adding a planning catalog or machine authority map.
- Strength: lowest implementation cost.
- Tradeoff: does not actually reduce machine join cost or resolve the `status` semantics trap.

## Recommended Design
### Architecture
- Add a new `planning_catalog` index artifact family under `core/control_plane/indexes/planning/`.
- Build each planning-catalog entry by joining:
  - the traceability entry for durable trace-linked IDs and initiative outcome,
  - the initiative index entry for current phase, owners, next action, and active-task summaries,
  - PRD, decision, design-document, and task index entries for document and execution detail,
  - acceptance contracts and validation evidence artifacts for validation coverage.
- Add a new machine-readable authority-map registry under `core/control_plane/registries/authority_map/` that maps supported planning and governance questions to:
  - the canonical artifact or document path,
  - the preferred query command,
  - the main status semantics to trust,
  - and explicit fallback surfaces when the canonical path is not enough.
- Add `watchtower-core query planning` as the canonical machine planning query and `watchtower-core query authority` as the canonical surface-discovery query.
- Keep `query coordination`, `query initiatives`, and `query trace` as narrower views, but document them as start-here or compatibility projections rather than the canonical deep planning join.

### Data and Interface Impacts
- New schema: `urn:watchtower:schema:artifacts:indexes:planning-catalog:v1`.
- New schema: `urn:watchtower:schema:artifacts:registries:authority-map:v1`.
- New canonical artifact: `core/control_plane/indexes/planning/planning_catalog.v1.json`.
- New canonical artifact: `core/control_plane/registries/authority_map/authority_map.v1.json`.
- Loader support gains `load_planning_catalog()` and `load_authority_map()`.
- Query support gains typed planning-catalog and authority-map query services.
- Sync support gains `watchtower-core sync planning-catalog`.
- Status semantics in the new catalog and planning query use explicit field names:
  - `artifact_status`
  - `initiative_status`
  - `task_status`
  - `record_status`
  - `decision_status`

### Execution Flow
1. Build and validate the new planning-catalog artifact family and its loader, sync, and query surfaces.
2. Add the machine authority-map registry, its loader and query surface, and the companion standards and docs that define canonical precedence.
3. Update command docs, root and planning entrypoints, and compatibility notes so machines and humans can route to the canonical planning and authority surfaces safely.

### Invariants and Failure Cases
- The planning catalog must never invent trace-linked relationships not already grounded in governed source artifacts.
- `query planning` must fail closed on missing trace-linked artifacts rather than silently omitting broken joins without explanation.
- The authority map must remain authored policy; it should not guess canonical precedence dynamically from filenames alone.
- Existing coordination and family indexes must remain valid until a future explicit retirement initiative changes them.

## Affected Surfaces
- `core/control_plane/indexes/planning/`
- `core/control_plane/registries/authority_map/`
- `core/control_plane/schemas/artifacts/`
- `core/control_plane/examples/valid/`
- `core/control_plane/registries/schema_catalog/schema_catalog.v1.json`
- `core/control_plane/registries/artifact_types/artifact_type_registry.v1.json`
- `core/control_plane/registries/validators/validator_registry.v1.json`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/repo_ops/sync/`
- `core/python/src/watchtower_core/repo_ops/query/`
- `core/python/src/watchtower_core/cli/`
- `docs/commands/core_python/`
- `docs/planning/README.md`
- `README.md`
- `docs/standards/data_contracts/`
- `docs/standards/governance/`

## Design Guardrails
- Do not overload the planning catalog as a second coordination tracker or as a prose-heavy review artifact.
- Do not change existing query command names or remove fields without an explicit compatibility strategy.
- Do not let the authority map become a generic repository encyclopedia; it should answer canonical-surface questions, not duplicate every index.
- Do not start external pack mounting or runtime composition work in this initiative.

## Risks
- The planning catalog could drift from its source indexes if sync ordering or tests are incomplete.
- The authority map could become stale if it is not explicitly covered by standards, validator registration, and command docs.
- Existing command consumers may rely on current JSON shapes, so compatibility notes and tests must be deliberate.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [initiative_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/initiative_index.v1.json)
- [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json)
