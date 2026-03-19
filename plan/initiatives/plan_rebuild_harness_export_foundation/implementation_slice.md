# Plan Rebuild Harness Export Foundation Implementation Slice

## Summary
Exports a reusable rebuild harness and routes the existing plan and project derived-surface rebuilds through the new boundary.

## Work Breakdown
- `task.plan_rebuild_harness_export_foundation.define_rebuild_harness_contract`
  Implement `watchtower_core.rebuild` with reusable rebuild-output models, service protocols, and a deterministic harness that can run dry or write to the live workspace.
- `task.plan_rebuild_harness_export_foundation.refactor_plan_and_project_rebuild_callers`
  Add repo-local rebuild services for plan and project workspace outputs, then refactor `PlanWorkspaceService.sync()` and `ProjectWorkspaceService.sync()` to delegate their derived-surface writes through the new harness.
- `task.plan_rebuild_harness_export_foundation.validate_rebuild_boundary_and_requirements_alignment`
  Add unit and boundary coverage, keep the plan/project integration expectations green, and update the rebuild rows in `requirements.md` plus companion package docs.

## Acceptance Shape
- `watchtower_core.rebuild` exists as a reusable public package boundary with fail-closed package-root behavior.
- Plan and project workspace rebuilds still emit the same current indexes and rendered views after the refactor.
- Targeted validation proves the reusable harness and its plan-local consumers without relying on the currently noisy broad repo baseline.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
