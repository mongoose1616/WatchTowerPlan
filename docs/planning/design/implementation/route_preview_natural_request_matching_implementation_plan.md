---
trace_id: trace.route_preview_natural_request_matching
id: design.implementation.route_preview_natural_request_matching
title: Route Preview Natural Request Matching Implementation Plan
summary: Break the natural maintenance-request route matching fix into one bounded implementation and validation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T13:51:18Z'
audience: shared
authority: supporting
applies_to:
- workflows/ROUTING_TABLE.md
- core/control_plane/indexes/routes/route_index.v1.json
- core/python/src/watchtower_core/repo_ops/query/routes.py
- docs/commands/core_python/watchtower_core_route_preview.md
---

# Route Preview Natural Request Matching Implementation Plan

## Record Metadata
- `Trace ID`: `trace.route_preview_natural_request_matching`
- `Plan ID`: `design.implementation.route_preview_natural_request_matching`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.route_preview_natural_request_matching`
- `Linked Decisions`: `decision.route_preview_natural_request_matching_direction`
- `Source Designs`: `design.features.route_preview_natural_request_matching`
- `Linked Acceptance Contracts`: `contract.acceptance.route_preview_natural_request_matching`
- `Updated At`: `2026-03-11T13:51:18Z`

## Summary
Break the natural maintenance-request route matching fix into one bounded implementation and validation slice.

## Source Request or Design
- Feature design: [route_preview_natural_request_matching_design.md](/home/j/WatchTowerPlan/docs/planning/design/features/route_preview_natural_request_matching_design.md)
- Final report-review request: `review /home/j/WatchTower/report and fix the valid issues with planning, tasks, validation, and commits`

## Scope Summary
- Fix the live route-preview miss for the final report-review maintenance request.
- Update the routed keyword authority, derived route index, command docs, regression tests, acceptance contract, and validation evidence in one bounded slice.
- Exclude semantic routing and broader workflow-taxonomy redesign.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): the authored routing table remains the place to encode bounded route intent.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): route-preview docs must refresh with behavior changes.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): the final route-preview baseline needs durable evidence before initiative closeout.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): acceptance contract, evidence, and trackers must stay aligned with the route change.

## Assumptions and Constraints
- Route preview remains advisory and deterministic.
- The current scorer already has sufficient matching mechanics once the governed cues exist.
- The trace should close in one implementation slice rather than reopening a broader workflow initiative.

## Proposed Technical Approach
- Add bounded single-token intent cues to the affected route rows in `workflows/ROUTING_TABLE.md`.
- Rebuild the route index, update route-preview docs, and retarget the regression tests to the exact report-review maintenance request.
- Publish acceptance evidence, rerun validation, close the task, and close the initiative.

## Work Breakdown
1. Finalize the planning chain and publish the acceptance contract for the route-preview regression trace.
2. Patch the routed keyword authority, sync the route index, refresh route-preview docs, and update the route-preview tests.
3. Run sync and validation, publish durable evidence, close the task, and close the initiative.

## Risks
- The added cues could overmatch if they expand beyond explicit maintenance nouns, so the validation set must stay focused on the reproduced report-review request.

## Validation Plan
- Run `./core/python/.venv/bin/watchtower-core sync route-index --write --format json`.
- Run `./core/python/.venv/bin/watchtower-core route preview --request "review /home/j/WatchTower/report and fix the valid issues with planning, tasks, validation, and commits" --format json`.
- Run `./core/python/.venv/bin/pytest -q core/python/tests/unit/test_route_index_sync.py core/python/tests/unit/test_cli_query_commands.py`.
- Run `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`.
- Run `./core/python/.venv/bin/watchtower-core validate acceptance --trace-id trace.route_preview_natural_request_matching --format json`.
- Run `./core/python/.venv/bin/python -m mypy src` and `./core/python/.venv/bin/ruff check .`.

## References
- report/04_workflows_and_governance.md
- [route_preview_natural_request_matching.md](/home/j/WatchTowerPlan/docs/planning/prds/route_preview_natural_request_matching.md)
