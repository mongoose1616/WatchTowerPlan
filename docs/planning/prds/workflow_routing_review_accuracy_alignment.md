---
trace_id: trace.workflow_routing_review_accuracy_alignment
id: prd.workflow_routing_review_accuracy_alignment
title: Workflow Routing Review Accuracy Alignment PRD
summary: Harden advisory route preview for audit-style, documentation-alignment, governed-artifact,
  and foundations-aware review requests while preserving deterministic routing boundaries.
type: prd
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

# Workflow Routing Review Accuracy Alignment PRD

## Record Metadata
- `Trace ID`: `trace.workflow_routing_review_accuracy_alignment`
- `PRD ID`: `prd.workflow_routing_review_accuracy_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.workflow_routing_review_accuracy_alignment.direction`
- `Linked Designs`: `design.features.workflow_routing_review_accuracy_alignment`
- `Linked Implementation Plans`: `design.implementation.workflow_routing_review_accuracy_alignment`
- `Updated At`: `2026-03-12T03:41:22Z`

## Summary
Harden advisory route preview for audit-style, documentation-alignment, governed-artifact, and foundations-aware review requests while preserving deterministic routing boundaries.

## Problem Statement
The current workflow-routing surfaces remain structurally coherent, but live route preview still fails on realistic review prompts in the areas surfaced by the latest workflow audit. A focused 20-scenario review sweep across code-review, repository-review, documentation-versus-implementation, governed-artifact, foundations-aware documentation, and route-boundary prompts reproduced 17 failures. The failures cluster into three causes:

- route preview still relies on broad lexical similarity that lets unrelated words collide across route families
- several routing-table trigger rows are too generic or too sparse for realistic audit and alignment requests
- foundations-aware documentation-alignment work has no explicit review route that loads the existing foundations context module with documentation refresh

The result is a route-preview layer that stays deterministic for explicit task types, but remains too weak or noisy for the exact audit and review requests maintainers are using in practice.

## Goals
- Restore deterministic route-preview accuracy for the reproduced workflow-audit prompts without introducing semantic or probabilistic routing.
- Eliminate the verified false positives across the route pairs surfaced by the review: code validation versus code implementation, initiative closeout versus commit closeout, task phase transition versus task lifecycle, and documentation refresh versus documentation-implementation reconciliation.
- Add explicit routed coverage for foundations-aware documentation alignment so review prompts that mention repository foundations load the right workflow set.
- Keep the route index, route-preview command docs, workflow-module guidance, and regression coverage aligned in the same slice.

## Non-Goals
- Building an autonomous planner, semantic router, embedding-based matcher, or probabilistic classification layer.
- Changing the advisory status of route preview relative to `AGENTS.md`, `workflows/ROUTING_TABLE.md`, and the workflow modules.
- Redesigning the workflow-module library when the existing modules can be recomposed to cover the missing review path.

## Requirements
- `req.workflow_routing_review_accuracy_alignment.001`: `watchtower-core route preview` must stop using broad common-prefix token similarity that causes unrelated task families to match one another.
- `req.workflow_routing_review_accuracy_alignment.002`: The routing table must publish realistic trigger coverage for audit-style code-review, repository-review, documentation-versus-implementation, and governed-artifact alignment requests that currently miss.
- `req.workflow_routing_review_accuracy_alignment.003`: Foundations-aware documentation-alignment requests must route explicitly to a workflow set that includes both documentation refresh and foundations context review.
- `req.workflow_routing_review_accuracy_alignment.004`: The affected route pairs must stop over-routing on generic terms such as `build`, `closeout`, and single-word task terms while preserving the previously closed natural-maintenance route-preview acceptance.
- `req.workflow_routing_review_accuracy_alignment.005`: Command docs, derived route artifacts, and route-preview regression tests must remain aligned with the authored routing surfaces.

## Acceptance Criteria
- `ac.workflow_routing_review_accuracy_alignment.001`: The trace carries a fully authored PRD, accepted decision, feature design, implementation plan, acceptance contract, evidence ledger, and closed task set for this routing slice.
- `ac.workflow_routing_review_accuracy_alignment.002`: The route-preview scorer and authored trigger rows route the reproduced code-review, repository-review, documentation-versus-implementation, and governed-artifact prompts without relying on broad lexical-prefix matching, and the previously reproduced boundary false positives no longer occur.
- `ac.workflow_routing_review_accuracy_alignment.003`: Foundations-aware documentation-alignment prompts route to an explicit workflow set that includes documentation refresh and foundations context review, and the human workflow docs describe that route coherently.
- `ac.workflow_routing_review_accuracy_alignment.004`: Final validation, route-index sync, and a follow-up expansive routing review pass find no additional issues in the discussed workflow-review areas.

## Risks and Dependencies
- The slice depends on keeping the prior route-preview natural-maintenance acceptance intact while tightening matching elsewhere.
- Trigger-keyword changes can shift route-preview behavior broadly, so regression coverage needs to lock both the newly fixed prompts and previously working prompts.
- Adding explicit foundations-aware review coverage changes the live route taxonomy and therefore requires synced route artifacts and companion docs in the same change set.

## References
- docs/planning/prds/route_preview_natural_request_matching.md
- docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md
- docs/planning/prds/workflow_system_operationalization.md
- docs/foundations/engineering_design_principles.md
- docs/foundations/product_direction.md
- docs/standards/workflows/routing_and_context_loading_standard.md
