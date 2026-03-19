# Plan Generic Sync Harness Export Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_generic_sync_harness_export_foundation`
- `trace_id`: `trace.plan_generic_sync_harness_export_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T21:51:00Z`

## Scope and Non-Goals
Exports a reusable sync harness from watchtower_core.sync and refactors repo-local sync orchestration onto that generic layer so requirements.md and decisions.md no longer depend on a repo_ops-only sync coordinator.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish generic sync harness contracts: Add the export-safe sync harness, shared result types, and reusable protocols under watchtower_core.sync.
- Refactor repo sync orchestration onto generic harness: Move all-sync and coordination-sync orchestration onto the generic sync harness without changing current sync target behavior.
- Validate sync harness export and guidance: Add tests and documentation proving watchtower_core.sync now publishes the reusable harness and remains aligned with requirements.md and decisions.md.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_generic_sync_harness_export_foundation.publish_generic_sync_harness_contracts](/plan/initiatives/plan_generic_sync_harness_export_foundation/.wt/tasks/publish_generic_sync_harness_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Add the export-safe sync harness, shared result types, and reusable protocols under watchtower_core.sync. | - |
| [task.plan_generic_sync_harness_export_foundation.refactor_repo_sync_orchestration_onto_generic_harness](/plan/initiatives/plan_generic_sync_harness_export_foundation/.wt/tasks/refactor_repo_sync_orchestration_onto_generic_harness/task.json) | `completed` | `high` | `repository_maintainer` | Move all-sync and coordination-sync orchestration onto the generic sync harness without changing current sync target behavior. | task.plan_generic_sync_harness_export_foundation.publish_generic_sync_harness_contracts |
| [task.plan_generic_sync_harness_export_foundation.validate_sync_harness_export_and_guidance](/plan/initiatives/plan_generic_sync_harness_export_foundation/.wt/tasks/validate_sync_harness_export_and_guidance/task.json) | `completed` | `high` | `repository_maintainer` | Add tests and documentation proving watchtower_core.sync now publishes the reusable harness and remains aligned with requirements.md and decisions.md. | task.plan_generic_sync_harness_export_foundation.publish_generic_sync_harness_contracts, task.plan_generic_sync_harness_export_foundation.refactor_repo_sync_orchestration_onto_generic_harness |

## Dependencies and Risks
- Task `task.plan_generic_sync_harness_export_foundation.refactor_repo_sync_orchestration_onto_generic_harness` depends on `task.plan_generic_sync_harness_export_foundation.publish_generic_sync_harness_contracts`.
- Task `task.plan_generic_sync_harness_export_foundation.validate_sync_harness_export_and_guidance` depends on `task.plan_generic_sync_harness_export_foundation.publish_generic_sync_harness_contracts`, `task.plan_generic_sync_harness_export_foundation.refactor_repo_sync_orchestration_onto_generic_harness`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_generic_sync_harness_export_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_generic_sync_harness_export_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_generic_sync_harness_export_foundation/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_generic_sync_harness_export_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_generic_sync_harness_export_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_generic_sync_harness_export_foundation/summary.md)
