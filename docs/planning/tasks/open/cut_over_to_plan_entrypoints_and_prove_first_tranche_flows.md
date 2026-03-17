---
id: task.capture_first_plan_workspace_bootstrap.cutover_proof_follow_up.006
trace_id: trace.capture_first_plan_workspace_bootstrap
title: Cut over to plan entrypoints and prove first-tranche flows
summary: Completes the hard cutover for new work, proves one pack-wide and one
  project-scoped flow, and records the history or retention follow-up tranche.
type: task
status: active
task_status: backlog
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-17T03:30:21Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/
- docs/planning/
- workflows/
related_ids:
- prd.capture_first_plan_workspace_bootstrap
- design.features.capture_first_plan_workspace_bootstrap
- design.implementation.capture_first_plan_workspace_bootstrap
- decision.capture_first_plan_workspace_bootstrap_direction
- contract.acceptance.capture_first_plan_workspace_bootstrap
depends_on:
- task.capture_first_plan_workspace_bootstrap.packwide_views_queries.004
- task.capture_first_plan_workspace_bootstrap.project_scoped_flow.005
---

# Cut over to plan entrypoints and prove first-tranche flows

## Summary
Completes the hard cutover for new work, proves one pack-wide and one project-scoped flow, and records the history or retention follow-up tranche.

## Scope
- Cut new planning and coordination entrypoints over to `plan/**`.
- Prove one pack-wide and one project-scoped initiative through the full capture-first loop.
- Record the named follow-up tranche for history and retention reconciliation.

## Done When
- New work routes through the new authority model instead of through `docs/planning/**`.
- The first milestone is proven for both scope roots and the legacy follow-up is explicitly tracked.
