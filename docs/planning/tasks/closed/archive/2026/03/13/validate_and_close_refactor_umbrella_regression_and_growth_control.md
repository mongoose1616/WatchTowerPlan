---
id: task.refactor_umbrella_regression_and_growth_control.validation_and_closeout.003
trace_id: trace.refactor_umbrella_regression_and_growth_control
title: Validate and close refactor umbrella regression and growth control
summary: Run targeted and full validation, repeated confirmation passes, and final
  initiative closeout for the umbrella refactor root-cause hardening trace.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T22:49:36Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/unit/
- docs/planning/
- core/control_plane/contracts/acceptance/refactor_umbrella_regression_and_growth_control_acceptance.v1.json
- core/control_plane/ledgers/validation_evidence/refactor_umbrella_regression_and_growth_control_planning_baseline.v1.json
related_ids:
- prd.refactor_umbrella_regression_and_growth_control
- design.features.refactor_umbrella_regression_and_growth_control
- design.implementation.refactor_umbrella_regression_and_growth_control
- decision.refactor_umbrella_regression_and_growth_control_direction
depends_on:
- task.refactor_umbrella_regression_and_growth_control.closeout_acceptance_gate.002
---

# Validate and close refactor umbrella regression and growth control

## Summary
Run targeted and full validation, repeated confirmation passes, and final initiative closeout for the umbrella refactor root-cause hardening trace.

## Scope
- Run targeted closeout validation after implementation lands.
- Run full repository validation and repeated confirmation passes from a second angle.
- Close the umbrella trace only after the root-cause findings are fixed, validated, and committed.

## Done When
- Targeted validation, full validation, post-fix review, second-angle confirmation, and adversarial confirmation all pass cleanly.
- The umbrella trace shows zero open tasks and terminal closeout state.
