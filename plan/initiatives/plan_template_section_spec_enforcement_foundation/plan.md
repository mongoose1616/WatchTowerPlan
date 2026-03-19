# Plan Template Section-Spec Enforcement Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_template_section_spec_enforcement_foundation`
- `trace_id`: `trace.plan_template_section_spec_enforcement_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T18:06:15Z`

## Scope and Non-Goals
Adds governed section-spec schemas and validation coverage for plan template contracts and rendered surface templates.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add template validation coverage: Extend template helpers and tests so section-spec references and template headings fail closed on drift.
- Bind templates to section-spec contracts: Update template catalog entries and related family bindings to reference the new section-spec schemas.
- Publish section-spec schema contracts: Add governed section-spec schemas for the current high-impact plan templates and rendered surfaces.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_template_section_spec_enforcement_foundation.add_template_validation_coverage](/plan/initiatives/plan_template_section_spec_enforcement_foundation/.wt/tasks/add_template_validation_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Extend template helpers and tests so section-spec references and template headings fail closed on drift. | task.plan_template_section_spec_enforcement_foundation.publish_section_spec_schema_contracts, task.plan_template_section_spec_enforcement_foundation.bind_templates_to_section_spec_contracts |
| [task.plan_template_section_spec_enforcement_foundation.bind_templates_to_section_spec_contracts](/plan/initiatives/plan_template_section_spec_enforcement_foundation/.wt/tasks/bind_templates_to_section_spec_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Update template catalog entries and related family bindings to reference the new section-spec schemas. | task.plan_template_section_spec_enforcement_foundation.publish_section_spec_schema_contracts |
| [task.plan_template_section_spec_enforcement_foundation.publish_section_spec_schema_contracts](/plan/initiatives/plan_template_section_spec_enforcement_foundation/.wt/tasks/publish_section_spec_schema_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Add governed section-spec schemas for the current high-impact plan templates and rendered surfaces. | - |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_template_section_spec_enforcement_foundation/plan.md.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_template_section_spec_enforcement_foundation/progress.md.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_template_section_spec_enforcement_foundation/summary.md.
- Discrepancy `discrepancy.plan_template_section_spec_enforcement_foundation.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.plan_template_section_spec_enforcement_foundation.add_template_validation_coverage` depends on `task.plan_template_section_spec_enforcement_foundation.publish_section_spec_schema_contracts`, `task.plan_template_section_spec_enforcement_foundation.bind_templates_to_section_spec_contracts`.
- Task `task.plan_template_section_spec_enforcement_foundation.bind_templates_to_section_spec_contracts` depends on `task.plan_template_section_spec_enforcement_foundation.publish_section_spec_schema_contracts`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_template_section_spec_enforcement_foundation/summary.md)
