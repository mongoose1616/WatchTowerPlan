# Plan Status Registry Domain Cleanup Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_status_registry_domain_cleanup`
- `trace_id`: `trace.plan_status_registry_domain_cleanup`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T00:45:00Z`

## Scope and Non-Goals
Removes legacy challenge-specific status leakage from the shared status registry and reconciles the authoritative requirements notes to the current pack-facing interface state.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add focused status registry coverage: Lock the cleaned status-registry shape through targeted pack-context or loader coverage.
- Generalize shared status vocabulary: Replace the legacy challenge-scoped blocked and terminal status entries with plan-domain-neutral status vocabulary.
- Reconcile requirements notes: Update requirements.md so the status-registry and artifact-index leakage notes reflect the current implemented state.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_status_registry_domain_cleanup.add_focused_status_registry_coverage](/plan/initiatives/plan_status_registry_domain_cleanup/.wt/tasks/add_focused_status_registry_coverage/task.json) | `completed` | `high` | `repository_maintainer` | Lock the cleaned status-registry shape through targeted pack-context or loader coverage. |
| [task.plan_status_registry_domain_cleanup.generalize_shared_status_vocabulary](/plan/initiatives/plan_status_registry_domain_cleanup/.wt/tasks/generalize_shared_status_vocabulary/task.json) | `completed` | `high` | `repository_maintainer` | Replace the legacy challenge-scoped blocked and terminal status entries with plan-domain-neutral status vocabulary. |
| [task.plan_status_registry_domain_cleanup.reconcile_requirements_notes](/plan/initiatives/plan_status_registry_domain_cleanup/.wt/tasks/reconcile_requirements_notes/task.json) | `completed` | `high` | `repository_maintainer` | Update requirements.md so the status-registry and artifact-index leakage notes reflect the current implemented state. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_status_registry_domain_cleanup/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_status_registry_domain_cleanup/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_status_registry_domain_cleanup/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_status_registry_domain_cleanup/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_status_registry_domain_cleanup/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_status_registry_domain_cleanup/summary.md)
