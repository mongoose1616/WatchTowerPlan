# Plan Documentation Family And Template Catalog Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_documentation_family_and_template_catalog_foundation`
- `trace_id`: `trace.plan_documentation_family_and_template_catalog_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T17:43:02Z`

## Scope and Non-Goals
Adds the missing documentation-family registry and template catalog foundations for live plan guidance families and current rendered plan/project surfaces.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish documentation family and template catalog schemas: Add the governed schema contracts for the plan-owned documentation-family registry and template catalog.
- Seed registry entries and governed template assets: Seed active documentation-family bindings, template catalog entries, and concrete template files for the current live plan surfaces.
- Wire typed helpers and validation coverage: Add typed loader support, helper APIs, and tests that prove the new registries and template assets resolve cleanly.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_documentation_family_and_template_catalog_foundation.publish_documentation_and_template_schema_contracts](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/.wt/tasks/publish_documentation_and_template_schema_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Add the governed schema contracts for the plan-owned documentation-family registry and template catalog. |
| [task.plan_documentation_family_and_template_catalog_foundation.seed_registry_entries_and_template_assets](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/.wt/tasks/seed_registry_entries_and_template_assets/task.json) | `completed` | `high` | `repository_maintainer` | Seed active documentation-family bindings, template catalog entries, and concrete template files for the current live plan surfaces. |
| [task.plan_documentation_family_and_template_catalog_foundation.wire_helpers_and_validation_coverage](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/.wt/tasks/wire_helpers_and_validation_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Add typed loader support, helper APIs, and tests that prove the new registries and template assets resolve cleanly. |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_documentation_family_and_template_catalog_foundation/plan.md.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_documentation_family_and_template_catalog_foundation/progress.md.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_documentation_family_and_template_catalog_foundation/summary.md.
- Discrepancy `discrepancy.plan_documentation_family_and_template_catalog_foundation.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_documentation_family_and_template_catalog_foundation/summary.md)
