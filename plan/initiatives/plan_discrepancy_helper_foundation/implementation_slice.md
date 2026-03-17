# Plan Discrepancy Helper Foundation Implementation Slice

## Summary
Extracts a reusable discrepancy helper for governed discrepancy records and refactors live plan initiative and workspace drift handling onto it so requirements.md and decisions.md no longer rely on ad hoc repo-local discrepancy logic.

## Initial Work Breakdown
- `task.plan_discrepancy_helper_foundation.publish_discrepancy_helper_contracts`: Add a reusable helper for governed discrepancy records, severity, and resolution behavior.
- `task.plan_discrepancy_helper_foundation.refactor_live_plan_discrepancy_writes_onto_helper`: Move initiative package and plan workspace discrepancy creation and reconciliation onto the reusable helper.
- `task.plan_discrepancy_helper_foundation.validate_discrepancy_helper_and_requirements_alignment`: Add coverage for discrepancy creation and resolution, then update touched requirements rows to current state.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
