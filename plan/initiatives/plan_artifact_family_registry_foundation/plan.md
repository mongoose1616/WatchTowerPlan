# Plan Artifact Family Registry Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_artifact_family_registry_foundation`
- `trace_id`: `trace.plan_artifact_family_registry_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T21:23:00Z`

## Scope and Non-Goals
Adds the missing artifact family registry so plan-pack artifact placement, status subsets, and derived index participation stop living only in path conventions and scattered code.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish artifact family registry schema: Add the governed schema contract for the plan-pack artifact family registry.
- Seed artifact family registry entries: Seed the initial plan-pack artifact family taxonomy for live initiative, task, evidence, promotion, discrepancy, project, and aggregate surfaces.
- Validate artifact family registry coverage: Add validation coverage proving the artifact family registry stays aligned with current live plan artifact schemas and indexes.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_artifact_family_registry_foundation.publish_artifact_family_registry_schema](/plan/initiatives/plan_artifact_family_registry_foundation/.wt/tasks/publish_artifact_family_registry_schema/task.json) | `completed` | `high` | `repository_maintainer` | Add the governed schema contract for the plan-pack artifact family registry. | - |
| [task.plan_artifact_family_registry_foundation.seed_artifact_family_registry_entries](/plan/initiatives/plan_artifact_family_registry_foundation/.wt/tasks/seed_artifact_family_registry_entries/task.json) | `completed` | `high` | `repository_maintainer` | Seed the initial plan-pack artifact family taxonomy for live initiative, task, evidence, promotion, discrepancy, project, and aggregate surfaces. | task.plan_artifact_family_registry_foundation.publish_artifact_family_registry_schema |
| [task.plan_artifact_family_registry_foundation.validate_artifact_family_registry_coverage](/plan/initiatives/plan_artifact_family_registry_foundation/.wt/tasks/validate_artifact_family_registry_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Add validation coverage proving the artifact family registry stays aligned with current live plan artifact schemas and indexes. | task.plan_artifact_family_registry_foundation.publish_artifact_family_registry_schema, task.plan_artifact_family_registry_foundation.seed_artifact_family_registry_entries |

## Dependencies and Risks
- Task `task.plan_artifact_family_registry_foundation.seed_artifact_family_registry_entries` depends on `task.plan_artifact_family_registry_foundation.publish_artifact_family_registry_schema`.
- Task `task.plan_artifact_family_registry_foundation.validate_artifact_family_registry_coverage` depends on `task.plan_artifact_family_registry_foundation.publish_artifact_family_registry_schema`, `task.plan_artifact_family_registry_foundation.seed_artifact_family_registry_entries`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_artifact_family_registry_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_artifact_family_registry_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_artifact_family_registry_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_artifact_family_registry_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_artifact_family_registry_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_artifact_family_registry_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_artifact_family_registry_foundation/summary.md)
