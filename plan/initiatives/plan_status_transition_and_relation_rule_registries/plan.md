# Plan Status Transition and Relation Rule Registries Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_status_transition_and_relation_rule_registries`
- `trace_id`: `trace.plan_status_transition_and_relation_rule_registries`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T20:53:00Z`

## Scope and Non-Goals
Adds the missing status transition rules and relation type registries so lifecycle policy and cross-artifact relations stop living only in code and prose.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish rule registry schemas: Add governed schema contracts for the status transition and relation type registries.
- Seed rule registry entries: Seed the initial plan-pack status transition and relation type registry entries.
- Validate rule registry coverage: Add validation coverage proving the new rule registries remain aligned with live plan artifact families.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_status_transition_and_relation_rule_registries.publish_rule_registry_schemas](/plan/initiatives/plan_status_transition_and_relation_rule_registries/.wt/tasks/publish_rule_registry_schemas/task.json) | `completed` | `high` | `repository_maintainer` | Add governed schema contracts for the status transition and relation type registries. | - |
| [task.plan_status_transition_and_relation_rule_registries.seed_rule_registry_entries](/plan/initiatives/plan_status_transition_and_relation_rule_registries/.wt/tasks/seed_rule_registry_entries/task.json) | `completed` | `high` | `repository_maintainer` | Seed the initial plan-pack status transition and relation type registry entries. | task.plan_status_transition_and_relation_rule_registries.publish_rule_registry_schemas |
| [task.plan_status_transition_and_relation_rule_registries.validate_rule_registry_coverage](/plan/initiatives/plan_status_transition_and_relation_rule_registries/.wt/tasks/validate_rule_registry_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Add validation coverage proving the new rule registries remain aligned with live plan artifact families. | task.plan_status_transition_and_relation_rule_registries.publish_rule_registry_schemas, task.plan_status_transition_and_relation_rule_registries.seed_rule_registry_entries |

## Dependencies and Risks
- Task `task.plan_status_transition_and_relation_rule_registries.seed_rule_registry_entries` depends on `task.plan_status_transition_and_relation_rule_registries.publish_rule_registry_schemas`.
- Task `task.plan_status_transition_and_relation_rule_registries.validate_rule_registry_coverage` depends on `task.plan_status_transition_and_relation_rule_registries.publish_rule_registry_schemas`, `task.plan_status_transition_and_relation_rule_registries.seed_rule_registry_entries`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_status_transition_and_relation_rule_registries/summary.md)
