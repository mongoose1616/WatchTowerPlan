---
id: task.capture_first_plan_workspace_bootstrap.initiative_contracts_gate.003
trace_id: trace.capture_first_plan_workspace_bootstrap
title: Add initiative package contracts and strict readiness gate
summary: Adds initiative-local state, event, deferred-item, discrepancy, approval,
  and gate behavior for the capture-first model.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-17T05:03:37Z'
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

# Add initiative package contracts and strict readiness gate

## Summary
Adds initiative-local state, event, deferred-item, discrepancy, approval, and gate behavior for the capture-first model.

## Scope
- Add dual-id initiative bootstrap, authored intake doc placement, initiative-local `.wt/` contracts, and maximum pre-execution event trail support.
- Enforce doc-proposal and machine-confirmation flow, discrepancy severity handling, deferred-item gating, and `ready_for_execution` approval rules.

## Done When
- A pack-wide initiative package can be created with the full required capture set before execution.
- Readiness fails closed on incomplete capture, blocking deferred items, unconfirmed proposals, or unapproved gate transitions.
