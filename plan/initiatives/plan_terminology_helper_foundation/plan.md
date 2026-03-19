# Plan Terminology Helper Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_terminology_helper_foundation`
- `trace_id`: `trace.plan_terminology_helper_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T01:21:00Z`

## Scope and Non-Goals
Generalize the existing planning vocabulary seam into a reusable terminology helper with pack-local lookup, alias resolution, and deprecation awareness.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Define reusable terminology helper contract: Add a reusable terminology helper for pack-local lifecycle, review, source, and task-status vocabulary lookup.
- Reconcile terminology requirements and package docs: Update the authoritative requirements and control-plane package docs to reflect the terminology helper boundary.
- Refactor planning vocabulary callers and add terminology coverage: Route live plan vocabulary callers through the terminology helper and lock alias or deprecation behavior with focused tests.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_terminology_helper_foundation.define_terminology_helper_contract](/plan/initiatives/plan_terminology_helper_foundation/.wt/tasks/define_terminology_helper_contract/task.json) | `completed` | `high` | `repository_maintainer` | Add a reusable terminology helper for pack-local lifecycle, review, source, and task-status vocabulary lookup. |
| [task.plan_terminology_helper_foundation.reconcile_terminology_requirements_and_docs](/plan/initiatives/plan_terminology_helper_foundation/.wt/tasks/reconcile_terminology_requirements_and_docs/task.json) | `completed` | `high` | `repository_maintainer` | Update the authoritative requirements and control-plane package docs to reflect the terminology helper boundary. |
| [task.plan_terminology_helper_foundation.refactor_callers_and_add_terminology_coverage](/plan/initiatives/plan_terminology_helper_foundation/.wt/tasks/refactor_callers_and_add_terminology_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Route live plan vocabulary callers through the terminology helper and lock alias or deprecation behavior with focused tests. |

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_terminology_helper_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_terminology_helper_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_terminology_helper_foundation/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_terminology_helper_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_terminology_helper_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_terminology_helper_foundation/summary.md)
