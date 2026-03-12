---
id: task.workflow_routing_review_accuracy_alignment.validation_closeout.002
trace_id: trace.workflow_routing_review_accuracy_alignment
title: Validate and close workflow routing review alignment
summary: Run the route-preview review sweep, repository validation baseline, and final
  no-new-issues pass before trace closeout.
type: task
status: active
task_status: done
task_kind: governance
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
depends_on:
- task.workflow_routing_review_accuracy_alignment.implementation.001
---

# Validate and close workflow routing review alignment

## Summary
Run the route-preview review sweep, repository validation baseline, and final no-new-issues pass before trace closeout.

## Scope
- Run targeted route-preview regressions, route-index sync, full validation, and full test/tooling checks after implementation lands.
- Repeat the expansive workflow-routing review pass and confirm no new issues remain before closeout.

## Done When
- Acceptance validation, repository validation, tests, typing, linting, and the follow-up routing review pass all succeed.
- The tasks, evidence, initiative, and coordination surfaces are closed in a clean committed state.
