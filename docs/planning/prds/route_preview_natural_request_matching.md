---
trace_id: trace.route_preview_natural_request_matching
id: prd.route_preview_natural_request_matching
title: Route Preview Natural Request Matching PRD
summary: Harden advisory route preview so natural maintenance requests route to task-lifecycle and commit-closeout surfaces without requiring exact trigger phrases.
type: prd
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

# Route Preview Natural Request Matching PRD

## Record Metadata
- `Trace ID`: `trace.route_preview_natural_request_matching`
- `PRD ID`: `prd.route_preview_natural_request_matching`
- `Status`: `active`
- `Linked Decisions`: `decision.route_preview_natural_request_matching_direction`
- `Linked Designs`: `design.features.route_preview_natural_request_matching`
- `Linked Implementation Plans`: `design.implementation.route_preview_natural_request_matching`
- `Updated At`: `2026-03-11T13:51:18Z`

## Summary
Harden advisory route preview so natural maintenance requests route to task-lifecycle and commit-closeout surfaces without requiring exact trigger phrases.

## Problem Statement
The final report-review request still reproduces a live routing gap. When route preview is asked to score:

`review /home/j/WatchTower/report and fix the valid issues with planning, tasks, validation, and commits`

the runtime currently returns `Repository Review` and `Code Validation`, but it misses `Task Lifecycle Management` and `Commit Closeout`. That leaves the workflow model weaker in natural maintenance requests than the repository currently claims and keeps the route-first governance layer more advisory than intended.

## Goals
- Make the exact report-review maintenance request route to `Repository Review`, `Task Lifecycle Management`, `Code Validation`, and `Commit Closeout`.
- Keep the fix governed and deterministic by improving authored route metadata rather than introducing semantic inference.
- Keep the routing table, derived route index, command docs, tests, and acceptance evidence aligned in the same traced change set.

## Non-Goals
- Building a semantic router or changing route preview into an execution authority.
- Reopening the broader workflow-operationalization or standards explicitness initiatives.
- Changing the routed task-type taxonomy or the current advisory nature of route preview.

## Requirements
- `req.route_preview_natural_request_matching.001`: The governed routing surfaces must recognize explicit task and commit intent expressed as natural maintenance nouns such as `tasks` and `commits`.
- `req.route_preview_natural_request_matching.002`: The exact report-review request used in this final audit must select `Task Lifecycle Management` and `Commit Closeout` in addition to the already-matched review and validation routes.
- `req.route_preview_natural_request_matching.003`: The solution must remain deterministic and governed by authored route metadata rather than a new semantic-routing layer.
- `req.route_preview_natural_request_matching.004`: Route-preview docs, route-index data, tests, acceptance contract coverage, and validation evidence must refresh in the same traced change set.

## Acceptance Criteria
- `ac.route_preview_natural_request_matching.001`: The planning corpus publishes an active PRD, accepted direction decision, feature design, implementation plan, closed bootstrap task, and bounded route-hardening task for `trace.route_preview_natural_request_matching`.
- `ac.route_preview_natural_request_matching.002`: `watchtower-core route preview --request "review /home/j/WatchTower/report and fix the valid issues with planning, tasks, validation, and commits" --format json` returns `Repository Review`, `Task Lifecycle Management`, `Code Validation`, and `Commit Closeout`, and does not regress into `Code Review`.
- `ac.route_preview_natural_request_matching.003`: The routing table, route index, route-preview docs, and route-preview regression tests all describe and validate the same natural maintenance-request behavior.
- `ac.route_preview_natural_request_matching.004`: The repository passes the closeout baseline for route-index sync, non-acceptance validation, targeted route-preview tests, acceptance validation, `mypy`, and `ruff`.

## Risks and Dependencies
- Single-token route cues can overmatch if they become too generic, so the fix must stay focused on explicit task and commit intent only.
- The trace depends on the earlier workflow-operationalization and standard-runtime route-preview work because those traces established the current advisory route-preview contract.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): close the gap with one explicit, bounded seam instead of a larger routing redesign.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep authored routing guidance, machine-readable lookup, docs, tests, and evidence aligned.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): improve the shared-core workflow support layer without expanding route preview into autonomous product behavior.

## References
- report/04_workflows_and_governance.md
- report/09_remediation_program.md
- [standard_runtime_and_route_explicitness_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md)
