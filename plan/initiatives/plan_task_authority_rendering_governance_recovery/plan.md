# Plan Task Authority, Rendering, and Governance Recovery Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_task_authority_rendering_governance_recovery`
- `trace_id`: `trace.plan_task_authority_rendering_governance_recovery`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T23:45:00Z`

## Scope and Non-Goals
Cuts over live task authority, restores human-readable planning renders, rewrites governance guidance, and validates the repaired operational flows.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Align bootstrap, sync, and fixture flows: Repair planning bootstrap, sync consumers, GitHub preview, and reduced fixture repos to use live plan task state.
- Cut over live task runtime and CLI authority: Replace docs-backed task mutation paths with initiative-local live plan task state and canonical status handling.
- Restore human tracker depth and markdown structure: Recover rich human-facing rendered tracker output and Markdown structure using selective patterns from main.
- Rewrite governance and command guidance: Update AGENTS layers, workflow modules, standards, READMEs, and command docs to the live authority model and restored human renders.
- Validate pack-wide and project-scoped operational flows: Run end-to-end operational scenarios, close the valid report issues, and record any remaining standards gaps with evidence.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_task_authority_rendering_governance_recovery.align_bootstrap_sync_and_fixtures](/plan/initiatives/plan_task_authority_rendering_governance_recovery/.wt/tasks/align_bootstrap_sync_and_fixtures/task.json) | `completed` | `critical` | `repository_maintainer` | Repair planning bootstrap, sync consumers, GitHub preview, and reduced fixture repos to use live plan task state. |
| [task.plan_task_authority_rendering_governance_recovery.cut_over_runtime_and_cli](/plan/initiatives/plan_task_authority_rendering_governance_recovery/.wt/tasks/cut_over_runtime_and_cli/task.json) | `completed` | `critical` | `repository_maintainer` | Replace docs-backed task mutation paths with initiative-local live plan task state and canonical status handling. |
| [task.plan_task_authority_rendering_governance_recovery.validate_operational_flows](/plan/initiatives/plan_task_authority_rendering_governance_recovery/.wt/tasks/validate_operational_flows/task.json) | `completed` | `critical` | `repository_maintainer` | Run end-to-end operational scenarios, close the valid report issues, and record any remaining standards gaps with evidence. |
| [task.plan_task_authority_rendering_governance_recovery.restore_human_render_depth_and_markdown](/plan/initiatives/plan_task_authority_rendering_governance_recovery/.wt/tasks/restore_human_render_depth_and_markdown/task.json) | `completed` | `high` | `repository_maintainer` | Recover rich human-facing rendered tracker output and Markdown structure using selective patterns from main. |
| [task.plan_task_authority_rendering_governance_recovery.rewrite_governance_and_command_guidance](/plan/initiatives/plan_task_authority_rendering_governance_recovery/.wt/tasks/rewrite_governance_and_command_guidance/task.json) | `completed` | `high` | `repository_maintainer` | Update AGENTS layers, workflow modules, standards, READMEs, and command docs to the live authority model and restored human renders. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `5`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_task_authority_rendering_governance_recovery/summary.md)
