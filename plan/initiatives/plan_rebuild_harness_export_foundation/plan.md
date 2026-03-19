# Plan Rebuild Harness Export Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_rebuild_harness_export_foundation`
- `trace_id`: `trace.plan_rebuild_harness_export_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T00:34:00Z`

## Scope and Non-Goals
Exports a reusable rebuild harness and routes the existing plan and project derived-surface rebuilds through the new boundary.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Define reusable rebuild harness contract: Add the export-safe rebuild target and result model under watchtower_core.rebuild.
- Refactor plan and project rebuild callers: Route plan and project derived-surface rebuild writes through the new harness without changing the current outputs.
- Validate rebuild boundary and requirements alignment: Add focused tests, boundary coverage, and update the authoritative requirements rows for the rebuild export.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_rebuild_harness_export_foundation.define_rebuild_harness_contract](/plan/initiatives/plan_rebuild_harness_export_foundation/.wt/tasks/define_rebuild_harness_contract/task.json) | `completed` | `high` | `repository_maintainer` | Add the export-safe rebuild target and result model under watchtower_core.rebuild. |
| [task.plan_rebuild_harness_export_foundation.refactor_plan_and_project_rebuild_callers](/plan/initiatives/plan_rebuild_harness_export_foundation/.wt/tasks/refactor_plan_and_project_rebuild_callers/task.json) | `completed` | `high` | `repository_maintainer` | Route plan and project derived-surface rebuild writes through the new harness without changing the current outputs. |
| [task.plan_rebuild_harness_export_foundation.validate_rebuild_boundary_and_requirements_alignment](/plan/initiatives/plan_rebuild_harness_export_foundation/.wt/tasks/validate_rebuild_boundary_and_requirements_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Add focused tests, boundary coverage, and update the authoritative requirements rows for the rebuild export. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_rebuild_harness_export_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_rebuild_harness_export_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_rebuild_harness_export_foundation/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_rebuild_harness_export_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_rebuild_harness_export_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_rebuild_harness_export_foundation/summary.md)
