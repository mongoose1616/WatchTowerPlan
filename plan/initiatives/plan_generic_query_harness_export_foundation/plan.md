# Plan Generic Query Harness Export Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_generic_query_harness_export_foundation`
- `trace_id`: `trace.plan_generic_query_harness_export_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T22:37:00Z`

## Scope and Non-Goals
Exports a reusable generic query surface from watchtower_core.query and refactors export-safe query services onto that public boundary so requirements.md and decisions.md no longer depend on a guardrail-only query root.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish generic query harness contracts: Add export-safe query modules, search parameter types, and reusable query services under watchtower_core.query.
- Refactor repo query services onto public query surface: Move generic repo-local query implementations onto the reusable-core query surface without moving plan-live query services out of repo_ops.
- Validate query harness export and guidance: Add boundary tests and package guidance proving watchtower_core.query now exports reusable generic query services aligned to requirements.md and decisions.md.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_generic_query_harness_export_foundation.publish_generic_query_harness_contracts](/plan/initiatives/plan_generic_query_harness_export_foundation/.wt/tasks/publish_generic_query_harness_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Add export-safe query modules, search parameter types, and reusable query services under watchtower_core.query. | - |
| [task.plan_generic_query_harness_export_foundation.refactor_repo_query_services_onto_public_query_surface](/plan/initiatives/plan_generic_query_harness_export_foundation/.wt/tasks/refactor_repo_query_services_onto_public_query_surface/task.json) | `completed` | `high` | `repository_maintainer` | Move generic repo-local query implementations onto the reusable-core query surface without moving plan-live query services out of repo_ops. | task.plan_generic_query_harness_export_foundation.publish_generic_query_harness_contracts |
| [task.plan_generic_query_harness_export_foundation.validate_query_harness_export_and_guidance](/plan/initiatives/plan_generic_query_harness_export_foundation/.wt/tasks/validate_query_harness_export_and_guidance/task.json) | `completed` | `high` | `repository_maintainer` | Add boundary tests and package guidance proving watchtower_core.query now exports reusable generic query services aligned to requirements.md and decisions.md. | task.plan_generic_query_harness_export_foundation.refactor_repo_query_services_onto_public_query_surface |

## Dependencies and Risks
- Task `task.plan_generic_query_harness_export_foundation.refactor_repo_query_services_onto_public_query_surface` depends on `task.plan_generic_query_harness_export_foundation.publish_generic_query_harness_contracts`.
- Task `task.plan_generic_query_harness_export_foundation.validate_query_harness_export_and_guidance` depends on `task.plan_generic_query_harness_export_foundation.refactor_repo_query_services_onto_public_query_surface`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_generic_query_harness_export_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_generic_query_harness_export_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_generic_query_harness_export_foundation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_generic_query_harness_export_foundation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_generic_query_harness_export_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_generic_query_harness_export_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_generic_query_harness_export_foundation/summary.md)
