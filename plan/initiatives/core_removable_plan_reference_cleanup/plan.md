# Core Removable Plan Reference Cleanup Plan

## Initiative Identity
- `initiative_id`: `initiative.core_removable_plan_reference_cleanup`
- `trace_id`: `trace.core_removable_plan_reference_cleanup`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-23T00:04:09Z`

## Scope and Non-Goals
Removes non-essential plan-specific wording and examples from shared core docs, host help, and reusable-core boundaries while preserving only references required by the current repository contract.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Core Removable Plan Reference Cleanup: Bootstrap Core Removable Plan Reference Cleanup live initiative package.
- Remove Removable Plan References From Shared Core: Rewrites shared core docs, host help, reusable-core boundary language, and companion tests so core no longer treats plan as the default reusable pack.
- Validate And Close Core Removable Plan Reference Cleanup: Runs derived-surface rebuild, validation, and regression checks; classifies the remaining necessary plan references in core; and closes the initiative.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.core_removable_plan_reference_cleanup.bootstrap_core_removable_plan_reference_cleanup](/plan/initiatives/core_removable_plan_reference_cleanup/.wt/tasks/bootstrap_core_removable_plan_reference_cleanup/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Core Removable Plan Reference Cleanup live initiative package. | - |
| [task.core_removable_plan_reference_cleanup.remove_removable_plan_references_from_shared_core](/plan/initiatives/core_removable_plan_reference_cleanup/.wt/tasks/remove_removable_plan_references_from_shared_core/task.json) | `completed` | `high` | `repository_maintainer` | Rewrites shared core docs, host help, reusable-core boundary language, and companion tests so core no longer treats plan as the default reusable pack. | - |
| [task.core_removable_plan_reference_cleanup.validate_and_close_core_removable_plan_reference_cleanup](/plan/initiatives/core_removable_plan_reference_cleanup/.wt/tasks/validate_and_close_core_removable_plan_reference_cleanup/task.json) | `completed` | `high` | `repository_maintainer` | Runs derived-surface rebuild, validation, and regression checks; classifies the remaining necessary plan references in core; and closes the initiative. | task.core_removable_plan_reference_cleanup.remove_removable_plan_references_from_shared_core |

## Dependencies and Risks
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.artifact_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.closeout_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/closeout_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.decision_notes_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_removable_plan_reference_cleanup/decision_notes.md; machine confirmation is required.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.design_record_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_removable_plan_reference_cleanup/design_record.md; machine confirmation is required.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.evidence_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/evidence_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.guidance_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/guidance_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.implementation_slice_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_removable_plan_reference_cleanup/implementation_slice.md; machine confirmation is required.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.initiative_brief_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_removable_plan_reference_cleanup/initiative_brief.md; machine confirmation is required.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/core_removable_plan_reference_cleanup/plan.md.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/core_removable_plan_reference_cleanup/progress.md.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.promotion_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/promotion_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Discrepancy `discrepancy.core_removable_plan_reference_cleanup.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/core_removable_plan_reference_cleanup/summary.md.
- Task `task.core_removable_plan_reference_cleanup.validate_and_close_core_removable_plan_reference_cleanup` depends on `task.core_removable_plan_reference_cleanup.remove_removable_plan_references_from_shared_core`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/core_removable_plan_reference_cleanup/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/core_removable_plan_reference_cleanup/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/core_removable_plan_reference_cleanup/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/core_removable_plan_reference_cleanup/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/core_removable_plan_reference_cleanup/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/core_removable_plan_reference_cleanup/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/core_removable_plan_reference_cleanup/summary.md)
