# Plan Discrepancy Helper Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_discrepancy_helper_foundation`
- `trace_id`: `trace.plan_discrepancy_helper_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T21:51:03Z`

## Scope and Non-Goals
Extracts a reusable discrepancy helper for governed discrepancy records and refactors live plan initiative and workspace drift handling onto it so requirements.md and decisions.md no longer rely on ad hoc repo-local discrepancy logic.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish discrepancy helper contracts: Add a reusable helper for governed discrepancy records, severity, and resolution behavior.
- Refactor live plan discrepancy writes onto helper: Move initiative package and plan workspace discrepancy creation and reconciliation onto the reusable helper.
- Validate discrepancy helper and requirements alignment: Add coverage for discrepancy creation and resolution, then update touched requirements rows to current state.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_discrepancy_helper_foundation.publish_discrepancy_helper_contracts](/plan/initiatives/plan_discrepancy_helper_foundation/.wt/tasks/publish_discrepancy_helper_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Add a reusable helper for governed discrepancy records, severity, and resolution behavior. | - |
| [task.plan_discrepancy_helper_foundation.refactor_live_plan_discrepancy_writes_onto_helper](/plan/initiatives/plan_discrepancy_helper_foundation/.wt/tasks/refactor_live_plan_discrepancy_writes_onto_helper/task.json) | `completed` | `high` | `repository_maintainer` | Move initiative package and plan workspace discrepancy creation and reconciliation onto the reusable helper. | task.plan_discrepancy_helper_foundation.publish_discrepancy_helper_contracts |
| [task.plan_discrepancy_helper_foundation.validate_discrepancy_helper_and_requirements_alignment](/plan/initiatives/plan_discrepancy_helper_foundation/.wt/tasks/validate_discrepancy_helper_and_requirements_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Add coverage for discrepancy creation and resolution, then update touched requirements rows to current state. | task.plan_discrepancy_helper_foundation.refactor_live_plan_discrepancy_writes_onto_helper |

## Dependencies and Risks
- Task `task.plan_discrepancy_helper_foundation.refactor_live_plan_discrepancy_writes_onto_helper` depends on `task.plan_discrepancy_helper_foundation.publish_discrepancy_helper_contracts`.
- Task `task.plan_discrepancy_helper_foundation.validate_discrepancy_helper_and_requirements_alignment` depends on `task.plan_discrepancy_helper_foundation.refactor_live_plan_discrepancy_writes_onto_helper`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `3`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/plan_discrepancy_helper_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_discrepancy_helper_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_discrepancy_helper_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_discrepancy_helper_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_discrepancy_helper_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_discrepancy_helper_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_discrepancy_helper_foundation/summary.md)
