---
trace_id: trace.route_preview_natural_request_matching
id: decision.route_preview_natural_request_matching_direction
title: Route Preview Natural Request Matching Direction
summary: Record the bounded direction for fixing natural maintenance-request route preview matching without introducing semantic routing.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-11T13:51:18Z'
audience: shared
authority: supporting
applies_to:
- workflows/ROUTING_TABLE.md
- core/control_plane/indexes/routes/route_index.v1.json
- core/python/src/watchtower_core/repo_ops/query/routes.py
---

# Route Preview Natural Request Matching Direction

## Record Metadata
- `Trace ID`: `trace.route_preview_natural_request_matching`
- `Decision ID`: `decision.route_preview_natural_request_matching_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.route_preview_natural_request_matching`
- `Linked Designs`: `design.features.route_preview_natural_request_matching`
- `Linked Implementation Plans`: `design.implementation.route_preview_natural_request_matching`
- `Updated At`: `2026-03-11T13:51:18Z`

## Summary
Record the bounded direction for fixing natural maintenance-request route preview matching without introducing semantic routing.

## Decision Statement
Fix the reproduced route-preview miss by expanding governed route keywords for explicit task and commit intent, then refresh the derived route index, route-preview docs, and regression tests in the same bounded trace.

## Trigger or Source Request
- Review /home/j/WatchTower/report one last time, verify each issue, and fix every still-valid issue through the standard end-to-end task cycle.

## Current Context and Constraints
- The exact final report-review request still misses `Task Lifecycle Management` and `Commit Closeout`.
- The current deterministic scorer already handles explicit single-token route cues, so the live failure is explained by incomplete governed route metadata rather than a broken scoring engine.
- The repository should not reopen a broader semantic-routing initiative for this one reproduced regression.

## Applied References and Implications
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): route preview remains advisory support for governed routing rather than a replacement for workflow authority.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): prefer the smallest explicit and reviewable change over a broader algorithm rewrite.
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): record the choice to keep this fix in governed metadata because it intentionally declines a broader semantic-routing posture.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the report finding, route update, tests, and evidence should remain linked through one trace.

## Affected Surfaces
- workflows/ROUTING_TABLE.md
- core/control_plane/indexes/routes/route_index.v1.json
- core/python/src/watchtower_core/repo_ops/query/routes.py
- docs/commands/core_python/watchtower_core_route_preview.md

## Options Considered
### Option 1
- Expand the governed route keywords for the affected routes and keep the current deterministic scorer.
- Strength: closes the reproduced regression with the smallest auditable change.
- Tradeoff: depends on disciplined maintenance of routed keyword coverage.

### Option 2
- Rewrite route preview around broader semantic inference for free-form maintenance requests.
- Strength: could catch more varied language automatically.
- Tradeoff: exceeds the current authority model and introduces harder-to-audit routing behavior.

## Chosen Outcome
Option 1 is accepted. The repository should fix this regression through explicit routed keyword coverage for natural task and commit intent, not by broadening route preview into a semantic planner.

## Rationale and Tradeoffs
- The live failure is reproducible and is explained by missing governed keyword coverage.
- Keeping the fix in authored routing metadata preserves the current authority model and makes the resulting behavior easy to review, sync, and test.
- A semantic-routing expansion would add complexity and hidden policy for a regression that does not require it.

## Consequences and Follow-Up Impacts
- The routing table, derived route index, route-preview docs, and route-preview tests all need to update together.
- Acceptance evidence should record the exact report-review maintenance request so the regression stays covered.
- Broader routing changes remain future work only if later evidence shows governed lexical routing is no longer sufficient.

## Risks, Dependencies, and Assumptions
- Risk: overly generic single-token cues could cause route overmatching.
- Dependency: the earlier route-preview hardening trace remains the behavioral baseline to preserve.
- Assumption: natural maintenance requests that mention `tasks` and `commits` express explicit enough intent to justify bounded route matches.

## References
- report/04_workflows_and_governance.md
- [route_preview_natural_request_matching.md](/home/j/WatchTowerPlan/docs/planning/prds/route_preview_natural_request_matching.md)
