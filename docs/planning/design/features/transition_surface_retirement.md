---
trace_id: trace.transition_surface_retirement
id: design.features.transition_surface_retirement
title: Transition Surface Retirement Feature Design
summary: Defines the technical design boundary for Transition Surface Retirement.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T19:23:51Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/
- core/python/tests/
- docs/planning/
- docs/standards/
---

# Transition Surface Retirement Feature Design

## Record Metadata
- `Trace ID`: `trace.transition_surface_retirement`
- `Design ID`: `design.features.transition_surface_retirement`
- `Design Status`: `active`
- `Linked PRDs`: `prd.transition_surface_retirement`
- `Linked Decisions`: `decision.transition_surface_retirement_direction`
- `Linked Implementation Plans`: `design.implementation.transition_surface_retirement`
- `Updated At`: `2026-03-16T19:23:51Z`

## Summary
Defines the technical design boundary for Transition Surface Retirement.

## Source Request
- User direction to find and remove remaining issue-driven transition artifacts, finish the work as one initiative, and close only after the repo is fully updated and validated.

## Scope and Feature Boundary
- Covers the remaining live runtime facades, control-plane re-export bridge, marker-style hotspot tests, stale current path references, and any temporary audit helper left behind by adjacent cleanup work.
- Covers runtime code, focused tests, README inventories, active planning docs, acceptance records, evidence ledgers, and derived governed indexes that advertise those paths.
- Excludes redesign of the intentional top-level guardrail roots or reusable validation APIs that still represent current boundary design rather than leftover transition debt.
- Excludes broad historical rewriting outside the bounded surfaces needed to stop current discovery and governance outputs from pointing at retired files.

## Current-State Context
- The direct handler owners already live in `query_coordination_family.py`, `query_coordination_rendered_handlers.py`, and `query_coordination_lookup_handlers.py`.
- The typed control-plane model boundary already resolves through `watchtower_core.control_plane.models` without needing the retired bridge module.
- Focused CLI query suites, focused document-semantics suites, and focused integration suites already cover the behavior that the old hotspot marker files used to front.
- The remaining problem is not missing implementation capability; it is leftover transition naming, dead import paths, dead test paths, and stale current discovery references.

## Foundations References Applied
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): temporary shims should be removed once the real owner is explicit and proven.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): the repo should publish one clear canonical answer per question instead of duplicate transition paths.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md): runtime and test cleanup must stay inside the canonical Python workspace and keep docs aligned with behavior.
- [rewrite_surface_classification_standard.md](/docs/standards/governance/rewrite_surface_classification_standard.md): transition surfaces are temporary and should be deleted once replacement value is proven.
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): planning, tasks, acceptance, and evidence must remain aligned through the cleanup and closeout.

## Design Goals and Constraints
- Remove transition debt with a hard cut rather than preserving local backward compatibility.
- Keep the currently authoritative runtime owners and focused test families intact while deleting only the leftover alternate paths.
- Preserve deterministic current discovery: any live path surfaced by trackers, indexes, contracts, or README inventories must exist and be current after the initiative closes.

## Options Considered
### Option 1
- Leave the leftover files in place but stop documenting them.
- Lowest immediate edit count.
- Still leaves dead paths in the repo, allows accidental imports to continue, and keeps stale discovery pressure alive.

### Option 2
- Keep temporary aliases, markers, or audit helpers until later implementation work begins.
- Preserves short-term transition convenience.
- Violates the current rewrite posture because the product is unreleased and the replacement surfaces are already proven.

### Option 3
- Hard-retire the leftover runtime, test, and discovery surfaces now and regenerate all derived governance outputs from the cleaned source set.
- Produces the smallest, clearest current repository surface.
- Requires coordinated code, doc, and planning cleanup in one slice.

## Recommended Design
### Architecture
- The authoritative runtime owners remain the direct CLI family and handler modules plus the split control-plane model packages.
- The authoritative tests remain the focused CLI-planning, document-semantics, integration, and boundary-proof suites.
- Current docs and governed discovery outputs should point only at live directories or live files, not at retired transition filenames.
- Temporary audit helpers are band-aids and must be deleted before closeout rather than retained as standing policy layers.

### Data and Interface Impacts
- Retired import paths intentionally stop resolving.
- Boundary-proof tests rename to current semantics and assert absence of retired wrappers or bridges.
- Planning trackers, repository-path discovery, and acceptance or evidence surfaces refresh to current paths after source cleanup.

### Execution Flow
1. Delete the leftover facade modules, bridge module, and marker test files; repair direct imports and direct assertions.
2. Rename stale boundary-proof artifacts and rewrite current docs or governance surfaces that still advertise retired paths.
3. Regenerate derived indexes and trackers, then run the full validation and closeout stack.

### Invariants and Failure Cases
- No live source, README inventory, tracker, contract, or index in scope may point at a deleted path after sync completes.
- The cleanup must fail closed if a direct import or direct test still depends on a retired file.
- If a temporary audit helper is required during execution, it must be deleted before initiative closeout.

## Affected Surfaces
- core/python/src/
- core/python/tests/
- docs/planning/
- docs/standards/

## Design Guardrails
- Do not add replacement aliases, compatibility copies, or marker stubs just to keep retired paths importable.
- Do not weaken coverage by deleting a hotspot file without preserving the focused suite coverage that replaced it.
- Do not leave a temporary validator, policy helper, or one-off migration file in the live runtime tree after the cleanup proves out.

## Risks
- Historical planning docs may still carry dead-path references until the current source surfaces are rewritten and synced.
- Broad bulk path cleanup can accidentally over-generalize references if it is not followed by focused review of the active initiative surfaces.

## References
- [transition_surface_retirement.md](/docs/planning/prds/transition_surface_retirement.md)
- [transition_surface_retirement.md](/docs/planning/design/implementation/transition_surface_retirement.md)
- [transition_surface_retirement_direction.md](/docs/planning/decisions/transition_surface_retirement_direction.md)
