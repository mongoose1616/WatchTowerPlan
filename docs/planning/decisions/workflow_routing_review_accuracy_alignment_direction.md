---
trace_id: trace.workflow_routing_review_accuracy_alignment
id: decision.workflow_routing_review_accuracy_alignment.direction
title: Workflow Routing Review Accuracy Alignment Direction Decision
summary: Records the initial direction decision for Workflow Routing Review Accuracy
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T03:41:22Z'
audience: shared
authority: supporting
applies_to:
- workflows/
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
---

# Workflow Routing Review Accuracy Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.workflow_routing_review_accuracy_alignment`
- `Decision ID`: `decision.workflow_routing_review_accuracy_alignment.direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.workflow_routing_review_accuracy_alignment`
- `Linked Designs`: `design.features.workflow_routing_review_accuracy_alignment`
- `Linked Implementation Plans`: `design.implementation.workflow_routing_review_accuracy_alignment`
- `Updated At`: `2026-03-12T03:41:22Z`

## Summary
Records the initial direction decision for Workflow Routing Review Accuracy Alignment.

## Decision Statement
Keep route preview deterministic and authored by removing broad fuzzy token matching, curating the overly generic route triggers, and adding one explicit foundations-aware review route rather than introducing semantic routing.

## Trigger or Source Request
- Conduct an expansive internal review of workflow routing accuracy, route-boundary clarity, and foundations-aware audit coverage based on the latest workflow audit findings, then fix all verified issues end to end.

## Current Context and Constraints
- The live route-preview service still reproduces the workflow-audit failures around audit-style code review, repository review, documentation-versus-implementation review, governed-artifact review, foundations-aware documentation alignment, and route-boundary false positives.
- The current scorer treats broad shared prefixes as a match, and several route rows rely on generic trigger examples such as `build`, `verify`, `closeout`, `task`, and `reconcile docs`, which makes boundary control too weak.
- The repository already has a `foundations_context_review` workflow module, but no explicit review route currently composes it with documentation refresh.

## Applied References and Implications
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): route preview must remain advisory over authored routing surfaces and should improve through explicit routing guidance, not opaque inference.
- [route_preview_natural_request_matching.md](/home/j/WatchTowerPlan/docs/planning/prds/route_preview_natural_request_matching.md): recent route-preview hardening already established the preference for authored keyword coverage over semantic expansion.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the routing fix should stay inspectable and bounded rather than rely on fuzzy logic that is hard to reason about.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): the shared-core workflow system should assist operators without becoming an autonomous planner.

## Affected Surfaces
- workflows/
- docs/
- core/python/src/watchtower_core/
- core/control_plane/

## Options Considered
### Option 1
- Keep the current fuzzy matcher and only add more trigger phrases.
- Strength: smallest code change.
- Tradeoff: leaves the verified boundary collisions in place because broad lexical similarity would still let unrelated routes bleed together.

### Option 2
- Replace broad lexical-prefix matching with exact normalized token matching, tighten the generic trigger rows, add realistic audit-review trigger coverage, and introduce an explicit foundations-aware review route composed from existing modules.
- Strength: fixes the reproduced misses and false positives while preserving the current deterministic, authored route model.
- Tradeoff: requires coordinated updates across routing docs, route-index sync outputs, tests, and command docs.

### Option 3
- Add a semantic-scoring or planner-style layer that infers route intent beyond authored routing phrases.
- Strength: could improve recall for arbitrary prompts.
- Tradeoff: conflicts with the current advisory routing model and materially expands the workflow system beyond the bounded issue set.

## Chosen Outcome
Option 2 is accepted.

## Rationale and Tradeoffs
- The reproduced failures are primarily authored-surface and scorer-boundary issues, not evidence that the repository needs a semantic router.
- Replacing fuzzy prefix matching with exact normalized token coverage makes the route-preview output explainable from the route table again.
- A dedicated foundations-aware review route keeps `Documentation Refresh` narrow while still making the missing foundations-alignment workflow combination explicit and reusable.

## Consequences and Follow-Up Impacts
- `workflows/ROUTING_TABLE.md` will change, which requires route-index regeneration and updated route-preview regression coverage.
- The foundations context workflow guidance will expand beyond planning/design phrasing so the new review route is explicitly supported.
- Route-preview command docs must describe the changed review behavior and the new foundations-aware route outcome.

## Risks, Dependencies, and Assumptions
- The prior natural-maintenance route-preview behavior must remain green after the scorer and trigger cleanup.
- The new foundations-aware route assumes the existing module set is sufficient and does not require a new workflow module.
- Tightening the scorer could surface additional missing trigger phrases during the final follow-up review pass; the initiative should not close until that second review is clean.

## References
- docs/planning/prds/route_preview_natural_request_matching.md
- docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md
- docs/planning/prds/workflow_system_operationalization.md
- docs/foundations/engineering_design_principles.md
- docs/foundations/product_direction.md
- docs/standards/workflows/routing_and_context_loading_standard.md
