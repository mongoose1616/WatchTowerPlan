# Plan Legacy History and Retention Reconciliation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_legacy_history_retention_reconciliation`
- `trace_id`: `trace.plan_legacy_history_retention_reconciliation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:10Z`

## Scope and Non-Goals
Encodes the transitional archive policy and clean-endstate purge rules for legacy docs/planning history and closed initiative packages directly in the live plan authority.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Classify legacy history and transitional archive surfaces: Encode the current and clean-endstate retention policy for docs/planning history, plan initiative archives, promoted guidance, and purge ledgers, and align adjacent entrypoint docs.
- Publish retention-policy registry and loader support: Add the retention_policy_registry schema, registry, typed model support, and helper methods for resolving current versus clean-endstate retention decisions.
- Validate retention policy alignment and follow-up linkage: Add focused tests and close the legacy follow-up task once the new plan initiative and policy artifacts are linked from the capture-first bootstrap package.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_legacy_history_retention_reconciliation.classify_legacy_history_and_transitional_archive_surfaces](/plan/initiatives/plan_legacy_history_retention_reconciliation/.wt/tasks/classify_legacy_history_and_transitional_archive_surfaces/task.json) | `completed` | `high` | `repository_maintainer` | Encode the current and clean-endstate retention policy for docs/planning history, plan initiative archives, promoted guidance, and purge ledgers, and align adjacent entrypoint docs. | - |
| [task.plan_legacy_history_retention_reconciliation.publish_retention_policy_registry_and_loader_support](/plan/initiatives/plan_legacy_history_retention_reconciliation/.wt/tasks/publish_retention_policy_registry_and_loader_support/task.json) | `completed` | `high` | `repository_maintainer` | Add the retention_policy_registry schema, registry, typed model support, and helper methods for resolving current versus clean-endstate retention decisions. | - |
| [task.plan_legacy_history_retention_reconciliation.validate_retention_policy_alignment_and_follow_up_linkage](/plan/initiatives/plan_legacy_history_retention_reconciliation/.wt/tasks/validate_retention_policy_alignment_and_follow_up_linkage/task.json) | `completed` | `high` | `repository_maintainer` | Add focused tests and close the legacy follow-up task once the new plan initiative and policy artifacts are linked from the capture-first bootstrap package. | task.plan_legacy_history_retention_reconciliation.publish_retention_policy_registry_and_loader_support, task.plan_legacy_history_retention_reconciliation.classify_legacy_history_and_transitional_archive_surfaces |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.discrepancy_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/discrepancy_index.json.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_legacy_history_retention_reconciliation/plan.md.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_legacy_history_retention_reconciliation/progress.md.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_legacy_history_retention_reconciliation/summary.md.
- Discrepancy `discrepancy.plan_legacy_history_retention_reconciliation.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.plan_legacy_history_retention_reconciliation.validate_retention_policy_alignment_and_follow_up_linkage` depends on `task.plan_legacy_history_retention_reconciliation.publish_retention_policy_registry_and_loader_support`, `task.plan_legacy_history_retention_reconciliation.classify_legacy_history_and_transitional_archive_surfaces`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_legacy_history_retention_reconciliation/summary.md)
