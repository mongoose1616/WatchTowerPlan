---
id: task.capture_first_plan_workspace_bootstrap.plan_workspace_seed.002
trace_id: trace.capture_first_plan_workspace_bootstrap
title: Seed plan workspace roots and Stage 1 bootstrap record
summary: Creates the bare `plan/**` roots and immediately persists the tracked Stage
  1 bootstrap record under `plan/.wt/`.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-17T04:20:21Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/
- workflows/
related_ids:
- prd.capture_first_plan_workspace_bootstrap
- design.features.capture_first_plan_workspace_bootstrap
- design.implementation.capture_first_plan_workspace_bootstrap
- decision.capture_first_plan_workspace_bootstrap_direction
- contract.acceptance.capture_first_plan_workspace_bootstrap
---

# Seed plan workspace roots and Stage 1 bootstrap record

## Summary
Creates the bare `plan/**` roots and immediately persists the tracked Stage 1 bootstrap record under `plan/.wt/`.

## Scope
- Add `plan/`, `plan/.wt/`, `plan/initiatives/`, and `plan/projects/`.
- Add the minimum tracked bootstrap record and aggregate shell needed to keep Stage 1 work itself under machine authority.

## Done When
- The two-step seed exists under canonical repo paths.
- Stage 1 bootstrap work is represented in tracked machine state instead of in ad hoc notes or implicit setup steps.
