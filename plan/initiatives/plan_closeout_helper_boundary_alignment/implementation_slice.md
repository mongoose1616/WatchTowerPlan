# Plan Closeout Helper Boundary Alignment Implementation Slice

## Summary
Extracts initiative-package closeout coordination into watchtower_core.closeout and validates required evidence, closeout, and promotion artifact handling before terminal transitions.

## Initial Work Breakdown
- `task.plan_closeout_helper_boundary_alignment.add_initiative_package_closeout_helper`: Publish a reusable closeout helper for initiative-package artifact coordination under watchtower_core.closeout.
- `task.plan_closeout_helper_boundary_alignment.refactor_live_plan_closeout_onto_shared_helper`: Route InitiativePackageService terminal closeout through the shared package closeout helper while preserving repo-local path orchestration.
- `task.plan_closeout_helper_boundary_alignment.validate_closeout_boundary_alignment`: Add focused closeout coverage and reconcile the closeout requirements rows to the implemented package boundary.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
