---
id: task.workflow_routing_review_accuracy_alignment.implementation.001
trace_id: trace.workflow_routing_review_accuracy_alignment
title: Harden workflow route scoring and review coverage
summary: Tighten deterministic route-preview matching, curate the affected route rows,
  add explicit foundations-aware review coverage, and align the companion docs and
  tests.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T03:46:25Z'
audience: shared
authority: authoritative
applies_to:
- workflows/
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
related_ids:
- prd.workflow_routing_review_accuracy_alignment
- design.features.workflow_routing_review_accuracy_alignment
- design.implementation.workflow_routing_review_accuracy_alignment
- decision.workflow_routing_review_accuracy_alignment.direction
- contract.acceptance.workflow_routing_review_accuracy_alignment
---

# Harden workflow route scoring and review coverage

## Summary
Tighten deterministic route-preview matching, curate the affected route rows, add explicit foundations-aware review coverage, and align the companion docs and tests.

## Scope
- Remove the broad lexical-prefix route-preview matcher and keep scoring anchored to explicit authored task-type and trigger-keyword coverage.
- Revise the affected route rows, add a foundations-aware review route, refresh the route index, and align workflow and command docs.
- Add regression coverage for the reproduced misses, over-routes, and previously hardened maintenance-request prompt.

## Done When
- The reproduced workflow-review prompts route to the intended workflow sets without the verified boundary false positives.
- The foundations-aware documentation-alignment route, route index, docs, and tests are aligned in the same change set.
