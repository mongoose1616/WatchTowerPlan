---
trace_id: "trace.foundation_scope_and_entrypoint_realignment"
id: "design.features.foundation_scope_and_entrypoint_realignment"
title: "Foundation Scope and EntryPoint Realignment Feature Design"
summary: "Defines the design for separating current repository scope from future product narrative and for keeping root entrypoints thin and explicit."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-11T01:27:13Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/foundations/"
  - "README.md"
  - "docs/planning/README.md"
aliases:
  - "foundation scope"
  - "entrypoint realignment"
---

# Foundation Scope and EntryPoint Realignment Feature Design

## Record Metadata
- `Trace ID`: `trace.foundation_scope_and_entrypoint_realignment`
- `Design ID`: `design.features.foundation_scope_and_entrypoint_realignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.foundation_scope_and_entrypoint_realignment`
- `Linked Decisions`: `decision.foundation_scope_boundary`
- `Linked Implementation Plans`: `design.implementation.foundation_scope_and_entrypoint_realignment`
- `Updated At`: `2026-03-11T01:27:13Z`

## Summary
Defines the design for separating current repository scope from future product narrative and for keeping root entrypoints thin and explicit.

## Source Request
- User request to validate the issues captured in [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md) and execute the necessary follow-up initiatives end to end.

## Scope and Feature Boundary
- Covers one new repository-scope foundation document.
- Covers foundation-layer clarifications that distinguish current repository-operating truth from future WatchTower product direction and narrative.
- Covers root and nearby planning entrypoint updates that keep the root thin while routing contributors through the correct scope and coordination surfaces.
- Does not add a planning graph, root-document validator expansion, or external pack runtime support.

## Current-State Context
- The whole-repo review in [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md) confirmed that the repo is healthy but still blurs current repository scope and future product scope in the foundation layer.
- The root [README.md](/home/j/WatchTowerPlan/README.md) is intentionally thin, but it does not currently route readers through one explicit repository charter document.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md) and [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md) are useful, but they can read as current repository authority instead of future-product framing.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md), [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md), and [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md) need small clarifications so they match the current export-ready boundary and repo scale.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): current repository scope should preserve explicit authority boundaries, compactness, and the reusable-core versus repo-ops split.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): root and foundation surfaces should reduce ambiguity rather than add more co-equal entrypoints.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): future product direction remains a valid foundation, but only when its relationship to current repo scope is explicit.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the design keeps the new scope and entrypoint work explicitly linked to one trace, one decision, one acceptance contract, and bounded tasks.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the fix should reduce ambiguity with minimal new prose and avoid replacing a thin root router with another large narrative document.
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md): the feature scope is constrained to issues evidenced in the durable whole-repo review rather than reopening unrelated review findings.

## Design Goals and Constraints
- Publish one explicit repository-scope foundation instead of relying on inference across several documents.
- Keep product-direction and customer-narrative context available without letting it override current repository scope.
- Preserve the thin-root strategy; the fix is better routing, not more root prose.
- Avoid creating a second broad entrypoint document outside the foundation layer.
- Keep the foundation layer small and high-signal.

## Options Considered
### Option 1
- Add disclaimer language to the existing product-direction and customer-story docs only.
- Lowest editing cost.
- Rejected because it still leaves no single authoritative repository charter document and keeps contributors reconstructing current scope by inference.

### Option 2
- Add an authoritative repository-scope foundation, realign the existing foundation documents around it, and keep the root README thin with explicit links to scope and coordination.
- Chosen because it creates one clear current-scope authority while preserving future-product context.
- Tradeoff: adds one more foundation document, so the foundation README and routes must stay intentional and compact.

### Option 3
- Move future product direction and customer narrative out of the foundations layer entirely.
- Would maximize present-scope purity.
- Rejected because future product direction still materially shapes planning and design work in this repository.

## Recommended Design
### Architecture
- Add `docs/foundations/repository_scope.md` as the authoritative statement of current repository ownership and non-goals.
- Keep `product_direction.md` authoritative for future WatchTower product direction, but make it explicitly subordinate to `repository_scope.md` for current repo ownership questions.
- Keep `customer_story.md` as supporting future-state product narrative and state clearly that it is not current repository-operating guidance.
- Clarify `engineering_design_principles.md`, `engineering_stack_direction.md`, and `repository_standards_posture.md` so they reflect the export-ready core boundary, compactness requirements, and current runtime/tooling reality.
- Keep the root [README.md](/home/j/WatchTowerPlan/README.md) as a router that points to repository scope, whole-repo review, and coordination state instead of carrying broader narrative explanation.

### Data and Interface Impacts
- No new machine-readable schema family is added in this initiative.
- The planning corpus gains one new foundation doc and the existing foundation-index projection should include it after sync.
- Root and planning entrypoint docs change, but they remain human-readable routers rather than machine authority.

### Execution Flow
1. Establish the repository-scope boundary in the decision record and planning chain.
2. Add the repository-scope foundation and realign the existing foundation docs around it.
3. Tighten the root and nearby planning entrypoints so they route to repository scope and coordination.
4. Rebuild derived indexes and trackers, validate the repo, close the initiative.

### Invariants and Failure Cases
- Root entrypoint docs must remain routing surfaces, not expansive handbooks.
- Future product direction must remain visible, but it must stop competing with current repository scope as the answer to "what does this repo own today?"
- The initiative must not rewrite planning authority or root validation behavior by accident while touching adjacent docs.

## Affected Surfaces
- `docs/foundations/`
- `README.md`
- `docs/planning/README.md`
- `SUMMARY.md`

## Design Guardrails
- Do not turn the new repository-scope document into a duplicate of the root README.
- Do not move product-direction content into root entrypoints.
- Do not let the customer-story document read like current repository-operating policy after this initiative.
- Do not expand this initiative into planning-graph or validator work.

## Implementation-Planning Handoff Notes
- Land the planning bootstrap, decision, acceptance contract, and bounded task set first.
- Land the foundation realignment slice before the root-entrypoint slice because the entrypoint docs should point at the new repository-scope authority.
- Keep the root-entrypoint slice documentation-only and explicitly avoid new validator or query behavior.

## Dependencies
- The existing foundation layer and its foundation-index projection.
- The current root README strategy and planning coordination entrypoint.

## Risks
- Reviewers may disagree on how much future product specificity should remain in the foundations layer.
- Adding a new foundation doc could backfire if the foundation README does not make the new precedence model obvious.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [README.md](/home/j/WatchTowerPlan/README.md)
- [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)

## Updated At
- `2026-03-11T01:27:13Z`
