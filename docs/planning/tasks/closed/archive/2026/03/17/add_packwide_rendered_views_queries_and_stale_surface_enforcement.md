---
id: task.capture_first_plan_workspace_bootstrap.packwide_views_queries.004
trace_id: trace.capture_first_plan_workspace_bootstrap
title: Add pack-wide rendered views, queries, and stale-surface enforcement
summary: Rebuilds pack-level and initiative-level visibility from the new authority
  model and fails closed on stale derived surfaces.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-17T05:23:37Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/
- docs/planning/
related_ids:
- prd.capture_first_plan_workspace_bootstrap
- design.features.capture_first_plan_workspace_bootstrap
- design.implementation.capture_first_plan_workspace_bootstrap
- decision.capture_first_plan_workspace_bootstrap_direction
- contract.acceptance.capture_first_plan_workspace_bootstrap
depends_on:
- task.capture_first_plan_workspace_bootstrap.initiative_contracts_gate.003
---

# Add pack-wide rendered views, queries, and stale-surface enforcement

## Summary
Rebuilds pack-level and initiative-level visibility from the new authority model and fails closed on stale derived surfaces.

## Scope
- Add `plan_overview.md`, initiative rendered views, aggregate indexes, and the coordination, readiness, initiative, task, and discrepancy query surfaces for the new authority path.
- Enforce readiness failure when required rendered views or indexes are stale.

## Done When
- Pack-wide visibility and machine query surfaces read from `plan/**` authority rather than docs-backed live planning.
- Stale required derived surfaces create blocking readiness failures instead of silent drift.
