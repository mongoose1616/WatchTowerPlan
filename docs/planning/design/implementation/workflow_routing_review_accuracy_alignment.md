---
trace_id: trace.workflow_routing_review_accuracy_alignment
id: design.implementation.workflow_routing_review_accuracy_alignment
title: Workflow Routing Review Accuracy Alignment Implementation Plan
summary: Breaks Workflow Routing Review Accuracy Alignment into a bounded implementation
  slice.
type: implementation_plan
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

# Workflow Routing Review Accuracy Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.workflow_routing_review_accuracy_alignment`
- `Plan ID`: `design.implementation.workflow_routing_review_accuracy_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.workflow_routing_review_accuracy_alignment`
- `Linked Decisions`: `decision.workflow_routing_review_accuracy_alignment.direction`
- `Source Designs`: `design.features.workflow_routing_review_accuracy_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.workflow_routing_review_accuracy_alignment`
- `Updated At`: `2026-03-12T03:41:22Z`

## Summary
Breaks Workflow Routing Review Accuracy Alignment into a bounded implementation slice.

## Source Request or Design
- Conduct an expansive internal review of workflow routing accuracy, route-boundary clarity, and foundations-aware audit coverage based on the latest workflow audit findings, then fix all verified issues end to end.

## Scope Summary
- Covers one bounded workflow-routing hardening slice across the route-preview scorer, the authored routing table, the derived route index, workflow-module guidance, command docs, and regression tests.
- Excludes broader workflow-inventory redesign, semantic routing research, or any change to non-discussed route families unless final validation surfaces a directly related regression.

## Assumptions and Constraints
- The existing workflow-module inventory is sufficient; the missing foundations-aware review path can be expressed through route-table composition.
- The route-preview service must remain deterministic and derived entirely from authored route rows plus static scorer logic.
- Validation needs to prove both the newly fixed audit prompts and the previously fixed natural-maintenance prompt remain correct.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): constrains the slice to explicit routing-table and workflow-module authority rather than hidden routing logic.
- [route_preview_natural_request_matching.md](/home/j/WatchTowerPlan/docs/planning/prds/route_preview_natural_request_matching.md): requires preservation of the earlier natural-maintenance route-preview behavior.
- [route_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/route_index_standard.md): requires the derived route index to stay aligned with the authored routing table after route taxonomy changes.

## Proposed Technical Approach
- Simplify the route-preview scorer so token matches are exact and route behavior depends on curated route-table coverage rather than broad lexical similarity.
- Revise the affected route rows to remove the reproduced generic collision terms, add realistic audit-review phrases, and introduce an explicit foundations-aware review route that reuses existing workflow modules.
- Refresh the route index, workflow guidance, command docs, and regression tests together so the human routing surfaces and machine-readable route-preview outputs stay coherent.

## Work Breakdown
1. Update the route-preview scoring helper in `core/python/src/watchtower_core/repo_ops/query/routes.py` and add or refresh unit coverage for the reproduced routing failures.
2. Revise `workflows/ROUTING_TABLE.md`, regenerate `core/control_plane/indexes/routes/route_index.v1.json`, and align the affected workflow and command docs with the new route behavior.
3. Run the route-preview regression sweep, targeted tests, full validation, and a follow-up no-new-issues routing review pass before task and initiative closeout.

## Risks
- Removing broad prefix similarity can reduce accidental recall for prompts that currently succeed only because of fuzzy matching. The updated trigger coverage must be broad enough to replace those paths explicitly.
- Introducing a new routed review outcome can surprise existing expectations unless the route-preview docs and regression tests make the foundations-aware intent explicit.

## Validation Plan
- Add targeted route-preview regressions for the reproduced misses and over-routes from the workflow-review scenario sweep.
- Rebuild the route index and validate route-preview command behavior through the CLI-facing test surfaces.
- Run `watchtower-core validate all --format json`, `pytest -q`, `python -m mypy src/watchtower_core`, `ruff check .`, and a final expansive routing review pass over the discussed prompt families.

## References
- docs/planning/prds/route_preview_natural_request_matching.md
- docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md
- docs/planning/prds/workflow_system_operationalization.md
- docs/standards/data_contracts/route_index_standard.md
- docs/standards/workflows/routing_and_context_loading_standard.md
