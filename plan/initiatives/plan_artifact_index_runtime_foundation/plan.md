# Plan Artifact Index Runtime Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_artifact_index_runtime_foundation`
- `trace_id`: `trace.plan_artifact_index_runtime_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T20:36:00Z`

## Scope and Non-Goals
Publishes the missing live plan artifact index, removes legacy artifact-index field leakage, and exposes the cross-family query surface required by requirements.md and decisions.md.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Build live plan artifact index and query surface: Build plan/.wt/artifact_index.json from live plan artifact families and expose it through a first-class query command.
- Publish artifact index contract and neutralize legacy fields: Update the generic pack artifact-index contract, typed models, and validation so challenge-specific and platform-specific leakage is replaced by plan-safe provenance fields.
- Validate artifact index coverage and guidance: Add tests, validator wiring, and command guidance proving the live artifact index stays aligned with requirements.md and decisions.md.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_artifact_index_runtime_foundation.build_live_plan_artifact_index_and_query_surface](/plan/initiatives/plan_artifact_index_runtime_foundation/.wt/tasks/build_live_plan_artifact_index_and_query_surface/task.json) | `completed` | `high` | `repository_maintainer` | Build plan/.wt/artifact_index.json from live plan artifact families and expose it through a first-class query command. | task.plan_artifact_index_runtime_foundation.publish_artifact_index_contract_and_neutralize_legacy_fields |
| [task.plan_artifact_index_runtime_foundation.publish_artifact_index_contract_and_neutralize_legacy_fields](/plan/initiatives/plan_artifact_index_runtime_foundation/.wt/tasks/publish_artifact_index_contract_and_neutralize_legacy_fields/task.json) | `completed` | `high` | `repository_maintainer` | Update the generic pack artifact-index contract, typed models, and validation so challenge-specific and platform-specific leakage is replaced by plan-safe provenance fields. | - |
| [task.plan_artifact_index_runtime_foundation.validate_artifact_index_coverage_and_guidance](/plan/initiatives/plan_artifact_index_runtime_foundation/.wt/tasks/validate_artifact_index_coverage_and_guidance/task.json) | `completed` | `high` | `repository_maintainer` | Add tests, validator wiring, and command guidance proving the live artifact index stays aligned with requirements.md and decisions.md. | task.plan_artifact_index_runtime_foundation.publish_artifact_index_contract_and_neutralize_legacy_fields, task.plan_artifact_index_runtime_foundation.build_live_plan_artifact_index_and_query_surface |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_artifact_index_runtime_foundation.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_artifact_index_runtime_foundation.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_artifact_index_runtime_foundation.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_artifact_index_runtime_foundation.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_artifact_index_runtime_foundation/summary.md.
- Task `task.plan_artifact_index_runtime_foundation.build_live_plan_artifact_index_and_query_surface` depends on `task.plan_artifact_index_runtime_foundation.publish_artifact_index_contract_and_neutralize_legacy_fields`.
- Task `task.plan_artifact_index_runtime_foundation.validate_artifact_index_coverage_and_guidance` depends on `task.plan_artifact_index_runtime_foundation.publish_artifact_index_contract_and_neutralize_legacy_fields`, `task.plan_artifact_index_runtime_foundation.build_live_plan_artifact_index_and_query_surface`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_artifact_index_runtime_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_artifact_index_runtime_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_artifact_index_runtime_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_artifact_index_runtime_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_artifact_index_runtime_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_artifact_index_runtime_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_artifact_index_runtime_foundation/summary.md)
