# Plan Lifecycle Review And Source Vocab Registries Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_lifecycle_review_and_source_vocab_registries`
- `trace_id`: `trace.plan_lifecycle_review_and_source_vocab_registries`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T17:13:00Z`

## Scope and Non-Goals
Adds the missing lifecycle-stage, review-status, and source-type registries plus typed helper coverage so plan-pack workflow semantics stop living only in scattered schema enums and runtime string literals.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish lifecycle review and source registry schemas: Add governed schema contracts for the lifecycle-stage, review-status, and source-type registries.
- Seed lifecycle review and source vocab entries: Seed active registry entries aligned to current plan-workspace lifecycle stages, review states, and provenance categories.
- Wire typed helper and validation coverage: Add typed loader support, a vocabulary helper, and tests proving the registries stay aligned with live schemas and runtime use.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_lifecycle_review_and_source_vocab_registries.publish_lifecycle_review_and_source_registry_schemas](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/.wt/tasks/publish_lifecycle_review_and_source_registry_schemas/task.json) | `completed` | `high` | `repository_maintainer` | Add governed schema contracts for the lifecycle-stage, review-status, and source-type registries. | - |
| [task.plan_lifecycle_review_and_source_vocab_registries.seed_lifecycle_review_and_source_vocab_entries](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/.wt/tasks/seed_lifecycle_review_and_source_vocab_entries/task.json) | `completed` | `high` | `repository_maintainer` | Seed active registry entries aligned to current plan-workspace lifecycle stages, review states, and provenance categories. | task.plan_lifecycle_review_and_source_vocab_registries.publish_lifecycle_review_and_source_registry_schemas |
| [task.plan_lifecycle_review_and_source_vocab_registries.wire_typed_helper_and_validation_coverage](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/.wt/tasks/wire_typed_helper_and_validation_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Add typed loader support, a vocabulary helper, and tests proving the registries stay aligned with live schemas and runtime use. | task.plan_lifecycle_review_and_source_vocab_registries.publish_lifecycle_review_and_source_registry_schemas, task.plan_lifecycle_review_and_source_vocab_registries.seed_lifecycle_review_and_source_vocab_entries |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/plan.md.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/progress.md.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/summary.md.
- Discrepancy `discrepancy.plan_lifecycle_review_and_source_vocab_registries.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.plan_lifecycle_review_and_source_vocab_registries.seed_lifecycle_review_and_source_vocab_entries` depends on `task.plan_lifecycle_review_and_source_vocab_registries.publish_lifecycle_review_and_source_registry_schemas`.
- Task `task.plan_lifecycle_review_and_source_vocab_registries.wire_typed_helper_and_validation_coverage` depends on `task.plan_lifecycle_review_and_source_vocab_registries.publish_lifecycle_review_and_source_registry_schemas`, `task.plan_lifecycle_review_and_source_vocab_registries.seed_lifecycle_review_and_source_vocab_entries`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/summary.md)
