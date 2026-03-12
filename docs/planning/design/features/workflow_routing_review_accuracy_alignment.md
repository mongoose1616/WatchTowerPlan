---
trace_id: trace.workflow_routing_review_accuracy_alignment
id: design.features.workflow_routing_review_accuracy_alignment
title: Workflow Routing Review Accuracy Alignment Feature Design
summary: Defines the technical design boundary for Workflow Routing Review Accuracy
  Alignment.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-12T03:41:22Z'
audience: shared
authority: authoritative
applies_to:
- workflows/
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
---

# Workflow Routing Review Accuracy Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.workflow_routing_review_accuracy_alignment`
- `Design ID`: `design.features.workflow_routing_review_accuracy_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.workflow_routing_review_accuracy_alignment`
- `Linked Decisions`: `decision.workflow_routing_review_accuracy_alignment.direction`
- `Linked Implementation Plans`: `design.implementation.workflow_routing_review_accuracy_alignment`
- `Updated At`: `2026-03-12T03:41:22Z`

## Summary
Defines the technical design boundary for Workflow Routing Review Accuracy Alignment.

## Source Request
- Conduct an expansive internal review of workflow routing accuracy, route-boundary clarity, and foundations-aware audit coverage based on the latest workflow audit findings, then fix all verified issues end to end.

## Scope and Feature Boundary
- Covers the deterministic route-preview matcher in `core/python/src/watchtower_core/repo_ops/query/routes.py`, the authored route rows in `workflows/ROUTING_TABLE.md`, the derived route index, the route-preview command docs, and the targeted workflow-module guidance needed for foundations-aware review work.
- Covers only the verified workflow-review gaps from the current audit sweep: audit-style code review, repository review, documentation-versus-implementation review, governed-artifact review, foundations-aware documentation alignment, and the reproduced boundary collisions between adjacent route pairs.
- Excludes semantic routing, machine-learned scoring, autonomous workflow selection, or any redesign of the existing workflow modules beyond explicit recomposition through the routing table.

## Current-State Context
- The route-preview service currently awards scores from exact phrase hits plus token-overlap heuristics, but `_tokens_match()` also treats broad shared prefixes as a match. That lets unrelated words like `command` and `commit`, and related but distinct task nouns like `implementation` and `implement`, bleed across route families.
- The current route table also contains several overly broad single-term or generic trigger examples, including `build`, `verify`, `closeout`, `task`, and `reconcile docs`, which amplify boundary noise even when the rest of the route system is structurally sound.
- Foundations context review already exists as a workflow module, but no review-oriented route currently composes it with documentation refresh, so prompts about aligning docs with repository foundations still miss or route too narrowly.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the routing fix should prefer explicit, inspectable logic over fuzzy heuristics that are hard to reason about.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): route preview should remain assistive shared-core infrastructure rather than expanding into an autonomous planner.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): route preview must remain advisory over authored routing surfaces and route from full request context without becoming a free-form grammar.
- [route_preview_natural_request_matching.md](/home/j/WatchTowerPlan/docs/planning/prds/route_preview_natural_request_matching.md): the prior hardening established that natural maintenance prompts should be fixed through explicit authored coverage rather than semantic inference.
- [workflow_system_operationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_system_operationalization.md): the route index stays derived from the authored routing table, so the design must keep human and machine routing surfaces aligned.

## Design Goals and Constraints
- Make the matched-route set explainable from authored task types and trigger phrases alone.
- Improve natural-language review coverage by curating explicit route keywords instead of reintroducing broad fuzzy matching.
- Preserve compound-route behavior for truly multi-intent requests while eliminating generic single-word false positives.
- Keep the workflow-module inventory stable; prefer recomposition of existing modules to new implementation surfaces unless a missing routed outcome is explicit and bounded.

## Options Considered
### Option 1
- Keep the current fuzzy token matcher and only add more trigger keywords.
- Strength: minimal code churn.
- Tradeoff: the verified boundary collisions remain because broad prefix similarity and generic trigger rows would still leak unrelated routes into results.

### Option 2
- Remove broad lexical-prefix matching, tighten the generic trigger rows, add realistic audit-review trigger coverage, and introduce one explicit foundations-aware review route that composes documentation refresh with foundations context.
- Strength: fixes the reproduced misses and over-routes while keeping route preview deterministic, authored, and auditable.
- Tradeoff: requires coordinated updates across the scorer, routing table, workflow docs, command docs, route index, and regression coverage.

### Option 3
- Introduce a richer semantic-scoring layer or a dedicated workflow-system review planner.
- Strength: could recover more free-form prompts without route-table curation.
- Tradeoff: breaks the current advisory, deterministic, authored-routing model and materially expands the scope of the workflow system.

## Recommended Design
### Architecture
- Replace broad token-prefix matching with exact normalized token matching so route scores only come from authored task-type and trigger-keyword vocabulary.
- Curate the affected route rows to remove the generic trigger examples that currently blur route boundaries and add realistic multi-token review phrases for the verified misses.
- Add a bounded `Foundations Alignment Review` route that reuses the existing `foundations_context_review` and `documentation_refresh` modules for documentation-alignment prompts that explicitly mention repository foundations.

### Data and Interface Impacts
- `workflows/ROUTING_TABLE.md` changes and therefore `core/control_plane/indexes/routes/route_index.v1.json` must be regenerated.
- `watchtower-core route preview` behavior changes for the discussed prompt families, so command docs and regression tests must be updated in the same slice.
- The workflow-module guidance for `foundations_context_review.md` should acknowledge review and documentation-alignment usage in addition to planning/design usage.

### Execution Flow
1. Normalize the request text and candidate phrases, then score only exact phrase hits and exact normalized token coverage for task types and trigger keywords.
2. Curate the affected route rows so the score inputs are specific enough for the reproduced audit prompts and no longer anchored on the generic collision terms.
3. Rebuild the route index, refresh the command/module docs, and validate the resulting route set against a fixed regression matrix plus a follow-up routing review sweep.

### Invariants and Failure Cases
- Route preview stays deterministic and advisory; it should never invent workflows outside the authored route table.
- Route-index sync remains the only machine-readable source of route rows; no hidden routing metadata should be introduced elsewhere.
- A request that mentions foundations-aware documentation alignment must not silently drop the foundations context module.
- Requests that were previously over-routed by generic terms such as `build`, `closeout`, `task`, or `reconcile docs` must fail closed to the narrower intended route rather than selecting unrelated routes.

## Affected Surfaces
- workflows/
- docs/
- core/python/src/watchtower_core/
- core/control_plane/

## Design Guardrails
- Keep route-preview matching inspectable from the authored routing table and the scorer code; do not introduce opaque heuristics.
- Do not weaken the previously landed natural-maintenance request coverage while fixing the new audit-review failures.

## Risks
- Tightening generic triggers can accidentally regress older free-form prompts unless the review matrix includes both the newly failing prompts and the previously hardened maintenance prompt.
- A new routed task type changes user-facing route-preview output, so companion docs and tests must be explicit about the intended foundations-aware outcome.

## References
- docs/planning/prds/route_preview_natural_request_matching.md
- docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md
- docs/planning/prds/workflow_system_operationalization.md
- docs/foundations/engineering_design_principles.md
- docs/foundations/product_direction.md
- docs/standards/workflows/routing_and_context_loading_standard.md
