# Plan Evidence Bundle Helper Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_evidence_bundle_helper_foundation`
- `trace_id`: `trace.plan_evidence_bundle_helper_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T01:41:00Z`

## Scope and Non-Goals
Broaden watchtower_core.evidence with a reusable evidence-bundle helper, then route live plan evidence bootstrap and indexing through that boundary.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Define reusable evidence bundle helper contract: Add typed evidence-bundle models and helper surfaces under watchtower_core.evidence.
- Reconcile evidence requirements and package docs: Update requirements.md and evidence package docs to reflect the broadened reusable evidence boundary.
- Refactor live plan evidence callers onto the helper: Use the new helper for initiative bootstrap evidence bundles and evidence-index summaries.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_evidence_bundle_helper_foundation.define_evidence_bundle_helper_contract](/plan/initiatives/plan_evidence_bundle_helper_foundation/.wt/tasks/define_evidence_bundle_helper_contract/task.json) | `completed` | `high` | `repository_maintainer` | Add typed evidence-bundle models and helper surfaces under watchtower_core.evidence. |
| [task.plan_evidence_bundle_helper_foundation.reconcile_evidence_requirements_and_docs](/plan/initiatives/plan_evidence_bundle_helper_foundation/.wt/tasks/reconcile_evidence_requirements_and_docs/task.json) | `completed` | `high` | `repository_maintainer` | Update requirements.md and evidence package docs to reflect the broadened reusable evidence boundary. |
| [task.plan_evidence_bundle_helper_foundation.refactor_live_plan_evidence_callers](/plan/initiatives/plan_evidence_bundle_helper_foundation/.wt/tasks/refactor_live_plan_evidence_callers/task.json) | `completed` | `high` | `repository_maintainer` | Use the new helper for initiative bootstrap evidence bundles and evidence-index summaries. |

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_evidence_bundle_helper_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_evidence_bundle_helper_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_evidence_bundle_helper_foundation/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_evidence_bundle_helper_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_evidence_bundle_helper_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_evidence_bundle_helper_foundation/summary.md)
