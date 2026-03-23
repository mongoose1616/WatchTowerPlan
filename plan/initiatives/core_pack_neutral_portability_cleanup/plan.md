# Core Pack Neutral Portability Cleanup Plan

## Initiative Identity
- `initiative_id`: `initiative.core_pack_neutral_portability_cleanup`
- `trace_id`: `trace.core_pack_neutral_portability_cleanup`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-23T14:55:54Z`

## Scope and Non-Goals
Removes remaining shared-core plan-specific test and documentation coupling so copied core works with any hosted pack.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Core Pack Neutral Portability Cleanup: Bootstrap Core Pack Neutral Portability Cleanup live initiative package.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.core_pack_neutral_portability_cleanup.bootstrap_core_pack_neutral_portability_cleanup](/plan/initiatives/core_pack_neutral_portability_cleanup/.wt/tasks/bootstrap_core_pack_neutral_portability_cleanup/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Core Pack Neutral Portability Cleanup live initiative package. |

## Dependencies and Risks
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.artifact_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.closeout_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/closeout_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.decision_notes_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/decision_notes.md; machine confirmation is required.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.design_record_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/design_record.md; machine confirmation is required.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.discrepancy_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/discrepancy_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.evidence_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/evidence_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.guidance_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/guidance_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.implementation_slice_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/implementation_slice.md; machine confirmation is required.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.initiative_brief_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/initiative_brief.md; machine confirmation is required.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/plan.md.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/progress.md.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.promotion_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/promotion_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Discrepancy `discrepancy.core_pack_neutral_portability_cleanup.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/core_pack_neutral_portability_cleanup/summary.md.

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
- Authored input: [initiative_brief.md](/plan/initiatives/core_pack_neutral_portability_cleanup/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/core_pack_neutral_portability_cleanup/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/core_pack_neutral_portability_cleanup/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/core_pack_neutral_portability_cleanup/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/core_pack_neutral_portability_cleanup/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/core_pack_neutral_portability_cleanup/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/core_pack_neutral_portability_cleanup/summary.md)
