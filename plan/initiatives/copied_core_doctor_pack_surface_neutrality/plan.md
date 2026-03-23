# Copied Core Doctor Pack Surface Neutrality Plan

## Initiative Identity
- `initiative_id`: `initiative.copied_core_doctor_pack_surface_neutrality`
- `trace_id`: `trace.copied_core_doctor_pack_surface_neutrality`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-23T22:04:08Z`

## Scope and Non-Goals
Makes the generic doctor command tolerate copied-core repositories whose active pack does not publish plan-style live indexes such as task_index or initiative_index.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Copied Core Doctor Pack Surface Neutrality: Bootstrap Copied Core Doctor Pack Surface Neutrality live initiative package.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.copied_core_doctor_pack_surface_neutrality.bootstrap_copied_core_doctor_pack_surface_neutrality](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/.wt/tasks/bootstrap_copied_core_doctor_pack_surface_neutrality/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Copied Core Doctor Pack Surface Neutrality live initiative package. |

## Dependencies and Risks
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.artifact_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.closeout_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/closeout_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.decision_notes_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/decision_notes.md; machine confirmation is required.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.design_record_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/design_record.md; machine confirmation is required.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.evidence_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/evidence_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.guidance_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/guidance_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.implementation_slice_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/implementation_slice.md; machine confirmation is required.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.initiative_brief_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/initiative_brief.md; machine confirmation is required.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/plan.md.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/progress.md.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.promotion_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/promotion_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Discrepancy `discrepancy.copied_core_doctor_pack_surface_neutrality.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/copied_core_doctor_pack_surface_neutrality/summary.md.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `1`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/copied_core_doctor_pack_surface_neutrality/summary.md)
