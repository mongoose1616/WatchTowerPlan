---
id: task.capture_first_plan_workspace_bootstrap.project_scoped_flow.005
trace_id: trace.capture_first_plan_workspace_bootstrap
title: Add project container bootstrap and project-scoped initiative flow
summary: Introduces the full project bootstrap package and proves the project-scoped
  initiative path.
type: task
status: active
task_status: backlog
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-17T03:30:21Z'
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
depends_on:
- task.capture_first_plan_workspace_bootstrap.initiative_contracts_gate.003
---

# Add project container bootstrap and project-scoped initiative flow

## Summary
Introduces the full project bootstrap package and proves the project-scoped initiative path.

## Scope
- Add the required project record, repository map, rendered basics, and project-context support under `plan/projects/<project_slug>/`.
- Enforce project bootstrap before project-scoped initiative creation and prove a project-scoped package through the capture-first harness.

## Done When
- A project container can be bootstrapped as a first-class package.
- A project-scoped initiative can be created only after that package exists and passes the required checks.
