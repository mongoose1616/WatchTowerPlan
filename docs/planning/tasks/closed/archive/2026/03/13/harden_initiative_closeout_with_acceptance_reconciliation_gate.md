---
id: task.refactor_umbrella_regression_and_growth_control.closeout_acceptance_gate.002
trace_id: trace.refactor_umbrella_regression_and_growth_control
title: Harden initiative closeout with acceptance reconciliation gate
summary: Make initiative closeout fail closed on acceptance-reconciliation issues
  unless an explicit override records the exception.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T22:39:40Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/closeout/initiative.py
- core/python/src/watchtower_core/cli/closeout_handlers.py
- core/python/tests/unit/test_initiative_closeout.py
- core/python/tests/unit/test_closeout_handlers.py
- core/python/tests/integration/test_task_workflow_end_to_end.py
- docs/commands/core_python/watchtower_core_closeout_initiative.md
- docs/commands/core_python/watchtower_core_closeout.md
- workflows/modules/initiative_closeout.md
- docs/standards/governance/initiative_closeout_standard.md
related_ids:
- prd.refactor_umbrella_regression_and_growth_control
- design.features.refactor_umbrella_regression_and_growth_control
- design.implementation.refactor_umbrella_regression_and_growth_control
- decision.refactor_umbrella_regression_and_growth_control_direction
depends_on:
- task.refactor_umbrella_regression_and_growth_control.audit_matrix.001
---

# Harden initiative closeout with acceptance reconciliation gate

## Summary
Make initiative closeout fail closed on acceptance-reconciliation issues unless an explicit override records the exception.

## Scope
- Extend InitiativeCloseoutService to run acceptance reconciliation before terminal closeout.
- Expose an explicit acceptance-drift override through the closeout CLI and result payload.
- Align unit tests, integration coverage, workflow guidance, and closeout command docs with the new behavior.

## Done When
- A closeout without the explicit override rejects traces that fail acceptance reconciliation.
- The explicit override keeps the exception visible in the runtime result and companion docs.
- Targeted tests for closeout service and handlers pass.
