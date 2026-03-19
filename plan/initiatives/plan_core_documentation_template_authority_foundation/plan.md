# Plan Core Documentation Template Authority Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_core_documentation_template_authority_foundation`
- `trace_id`: `trace.plan_core_documentation_template_authority_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T18:20:33Z`

## Scope and Non-Goals
Adds the missing core-owned documentation family registry, template catalog, reusable templates, and validation coverage required by requirements.md.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add core validation coverage: Extend loader and tests so the core-owned documentation governance stack validates cleanly and resolves explicitly by path.
- Publish core documentation schema contracts: Add core-owned schema contracts for documentation family bindings, template catalog metadata, and core section-spec schemas.
- Seed core registries and templates: Create core control-plane documentation family bindings, template catalog entries, and reusable template files for core docs and workflows.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_core_documentation_template_authority_foundation.add_core_validation_coverage](/plan/initiatives/plan_core_documentation_template_authority_foundation/.wt/tasks/add_core_validation_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Extend loader and tests so the core-owned documentation governance stack validates cleanly and resolves explicitly by path. | task.plan_core_documentation_template_authority_foundation.publish_core_documentation_schema_contracts, task.plan_core_documentation_template_authority_foundation.seed_core_registries_and_templates |
| [task.plan_core_documentation_template_authority_foundation.publish_core_documentation_schema_contracts](/plan/initiatives/plan_core_documentation_template_authority_foundation/.wt/tasks/publish_core_documentation_schema_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Add core-owned schema contracts for documentation family bindings, template catalog metadata, and core section-spec schemas. | - |
| [task.plan_core_documentation_template_authority_foundation.seed_core_registries_and_templates](/plan/initiatives/plan_core_documentation_template_authority_foundation/.wt/tasks/seed_core_registries_and_templates/task.json) | `completed` | `high` | `repository_maintainer` | Create core control-plane documentation family bindings, template catalog entries, and reusable template files for core docs and workflows. | task.plan_core_documentation_template_authority_foundation.publish_core_documentation_schema_contracts |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_core_documentation_template_authority_foundation/plan.md.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_core_documentation_template_authority_foundation/progress.md.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_core_documentation_template_authority_foundation/summary.md.
- Discrepancy `discrepancy.plan_core_documentation_template_authority_foundation.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.plan_core_documentation_template_authority_foundation.add_core_validation_coverage` depends on `task.plan_core_documentation_template_authority_foundation.publish_core_documentation_schema_contracts`, `task.plan_core_documentation_template_authority_foundation.seed_core_registries_and_templates`.
- Task `task.plan_core_documentation_template_authority_foundation.seed_core_registries_and_templates` depends on `task.plan_core_documentation_template_authority_foundation.publish_core_documentation_schema_contracts`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_core_documentation_template_authority_foundation/summary.md)
