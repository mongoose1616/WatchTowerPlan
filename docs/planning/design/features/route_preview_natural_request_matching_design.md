---
trace_id: trace.route_preview_natural_request_matching
id: design.features.route_preview_natural_request_matching
title: Route Preview Natural Request Matching Design
summary: Define the bounded governed-keyword and regression-coverage changes needed for natural maintenance-request route matching.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T13:51:18Z'
audience: shared
authority: authoritative
applies_to:
- workflows/ROUTING_TABLE.md
- core/control_plane/indexes/routes/route_index.v1.json
- core/python/src/watchtower_core/repo_ops/query/routes.py
- docs/commands/core_python/watchtower_core_route_preview.md
---

# Route Preview Natural Request Matching Design

## Record Metadata
- `Trace ID`: `trace.route_preview_natural_request_matching`
- `Design ID`: `design.features.route_preview_natural_request_matching`
- `Design Status`: `active`
- `Linked PRDs`: `prd.route_preview_natural_request_matching`
- `Linked Decisions`: `decision.route_preview_natural_request_matching_direction`
- `Linked Implementation Plans`: `design.implementation.route_preview_natural_request_matching`
- `Updated At`: `2026-03-11T13:51:18Z`

## Summary
Define the bounded governed-keyword and regression-coverage changes needed for natural maintenance-request route matching.

## Source Request
- Review the regression findings one last time, verify each issue, and fix every still-valid issue through the standard end-to-end task cycle.

## Scope and Feature Boundary
- Covers the reproduced route-preview miss for the final report-review maintenance request.
- Covers governed route-keyword updates, the derived route-index rebuild, route-preview command docs, and targeted route-preview tests.
- Excludes semantic routing, workflow-inventory redesign, and any change to the advisory nature of route preview.

## Current-State Context
- The current route-preview scorer already returns `Repository Review` and `Code Validation` for the live final-review request, which means the engine is functioning but the governed route metadata is incomplete for task and commit intent.
- The route-preview command docs and tests currently protect a different maintenance-request phrase, so the exact live request that reproduced the review issue is not yet covered by regression validation.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): prefer one explicit metadata seam over a larger routing redesign.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): route behavior should stay governed by authored metadata plus same-change validation.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): route preview should keep helping maintainers inside the shared-core workflow model without claiming autonomous execution authority.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): the routed task taxonomy remains authoritative, so the fix belongs in the authored routed keyword layer.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): route-preview behavior changes must ship with aligned command examples and notes.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): derived lookup surfaces must stay aligned with the authored workflow model.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the planning chain, route change, tests, and evidence should remain linked through one trace.

## Design Goals and Constraints
- Make the exact report-review maintenance request match the same workflow set a maintainer would select manually.
- Keep route preview deterministic and governed by authored route metadata.
- Preserve the current routed task types and avoid a semantic-routing expansion.

## Options Considered
### Option 1
- Expand the affected route keywords to include explicit natural maintenance nouns such as `tasks` and `commits`, then refresh docs and tests.
- Strength: smallest auditable fix with no scorer rewrite.
- Tradeoff: relies on careful maintenance of governed keyword coverage.

### Option 2
- Add broader scorer heuristics that infer missing workflow types from partial phrase context.
- Strength: could match more natural language without changing route metadata.
- Tradeoff: risks drifting from the authored routing authority and makes failures harder to reason about.

## Recommended Design
### Architecture
- Keep the current route-preview scorer unchanged and treat the routing-table trigger keywords as the authority surface to extend.
- Add explicit task and commit intent cues to the `Task Lifecycle Management` and `Commit Closeout` route rows.
- Rebuild the derived route index and align route-preview docs plus tests to the exact report-review maintenance request.

### Data and Interface Impacts
- `workflows/ROUTING_TABLE.md` changes the authored keyword examples for two routed task types.
- `core/control_plane/indexes/routes/route_index.v1.json` changes through sync and becomes the machine-readable expression of the new cues.
- `watchtower-core route preview` docs and tests change to protect the exact reproduced request.

### Execution Flow
1. Update the routed keyword examples so natural `tasks` and `commits` intent is explicit in the authored routing surface.
2. Refresh the derived route index and route-preview docs and update the route-preview regression tests to the exact live request.
3. Validate the route-preview behavior, publish acceptance evidence, and close the bounded trace.

### Invariants and Failure Cases
- Route preview must remain advisory and deterministic.
- The fix must not broaden into `Code Review` for the report-review maintenance request.
- If the authored routing surface and the derived route index drift, sync and validation should expose that mismatch in the same change set.

## Affected Surfaces
- workflows/ROUTING_TABLE.md
- core/control_plane/indexes/routes/route_index.v1.json
- core/python/src/watchtower_core/repo_ops/query/routes.py
- docs/commands/core_python/watchtower_core_route_preview.md
- core/python/tests/unit/test_route_index_sync.py
- core/python/tests/unit/test_cli_query_commands.py

## Design Guardrails
- Keep the fix in governed route metadata, docs, and regression tests.
- Do not introduce semantic-routing behavior or hidden runtime-only route aliases.

## Risks
- Single-token route cues could overmatch if they expand beyond explicit maintenance intent, so the added keywords must stay tightly bounded.

## References
- March 2026 workflow and governance review summary for the reproduced route-preview gap.
- [route_preview_natural_request_matching.md](/home/j/WatchTowerPlan/docs/planning/prds/route_preview_natural_request_matching.md)
