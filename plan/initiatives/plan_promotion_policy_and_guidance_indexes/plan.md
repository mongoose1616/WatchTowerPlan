# Plan Promotion Policy and Guidance Indexes Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_promotion_policy_and_guidance_indexes`
- `trace_id`: `trace.plan_promotion_policy_and_guidance_indexes`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T20:20:00Z`

## Scope and Non-Goals
Adds the missing promotion policy registry and pack-level promotion and guidance indexes so initiative-local promotion records and approved plan guidance are machine-queryable under plan/.wt.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Build promotion and guidance index runtime: Aggregate initiative-local promotion records and approved plan guidance into derived plan/.wt index surfaces.
- Publish promotion policy schema and registry: Add the governed promotion-policy registry contract and seed the initial plan-pack promotion policy entries.
- Validate promotion and guidance lookup: Add validation coverage proving the new promotion policy registry and aggregate indexes stay aligned with live promotion records and plan/docs guidance.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_promotion_policy_and_guidance_indexes.build_promotion_and_guidance_index_runtime](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/.wt/tasks/build_promotion_and_guidance_index_runtime/task.json) | `completed` | `high` | `repository_maintainer` | Aggregate initiative-local promotion records and approved plan guidance into derived plan/.wt index surfaces. | task.plan_promotion_policy_and_guidance_indexes.publish_promotion_policy_schema_and_registry |
| [task.plan_promotion_policy_and_guidance_indexes.publish_promotion_policy_schema_and_registry](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/.wt/tasks/publish_promotion_policy_schema_and_registry/task.json) | `completed` | `high` | `repository_maintainer` | Add the governed promotion-policy registry contract and seed the initial plan-pack promotion policy entries. | - |
| [task.plan_promotion_policy_and_guidance_indexes.validate_promotion_and_guidance_lookup](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/.wt/tasks/validate_promotion_and_guidance_lookup/task.json) | `completed` | `high` | `repository_maintainer` | Add validation coverage proving the new promotion policy registry and aggregate indexes stay aligned with live promotion records and plan/docs guidance. | task.plan_promotion_policy_and_guidance_indexes.publish_promotion_policy_schema_and_registry, task.plan_promotion_policy_and_guidance_indexes.build_promotion_and_guidance_index_runtime |

## Dependencies and Risks
- Task `task.plan_promotion_policy_and_guidance_indexes.build_promotion_and_guidance_index_runtime` depends on `task.plan_promotion_policy_and_guidance_indexes.publish_promotion_policy_schema_and_registry`.
- Task `task.plan_promotion_policy_and_guidance_indexes.validate_promotion_and_guidance_lookup` depends on `task.plan_promotion_policy_and_guidance_indexes.publish_promotion_policy_schema_and_registry`, `task.plan_promotion_policy_and_guidance_indexes.build_promotion_and_guidance_index_runtime`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_promotion_policy_and_guidance_indexes/summary.md)
