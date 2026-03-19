# Plan Terminal Initiative Closeout Runtime Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_terminal_initiative_closeout_runtime`
- `trace_id`: `trace.plan_terminal_initiative_closeout_runtime`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:35:00Z`

## Scope and Non-Goals
Adds the live terminal closeout mutation path for pack-wide and project-scoped initiative packages so closing initiatives can move into completed, superseded, or cancelled and the coordination surfaces can show recent closeouts instead of stuck active work.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add terminal closeout mutations for live initiative packages: Implement pack-wide and project-scoped terminal closeout state transitions that finalize initiative, evidence, closeout, and promotion shells.
- Expose terminal closeout through a maintained command surface: Add a CLI path and companion docs for closing live plan initiatives without manual JSON edits.
- Validate terminal closeout and clear current closing initiatives: Add tests, rebuild validation, and use the new closeout path to move the current closing initiatives into terminal states.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_terminal_initiative_closeout_runtime.add_terminal_closeout_mutations](/plan/initiatives/plan_terminal_initiative_closeout_runtime/.wt/tasks/add_terminal_closeout_mutations/task.json) | `completed` | `high` | `repository_maintainer` | Implement pack-wide and project-scoped terminal closeout state transitions that finalize initiative, evidence, closeout, and promotion shells. | - |
| [task.plan_terminal_initiative_closeout_runtime.expose_terminal_closeout_command_surface](/plan/initiatives/plan_terminal_initiative_closeout_runtime/.wt/tasks/expose_terminal_closeout_command_surface/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI path and companion docs for closing live plan initiatives without manual JSON edits. | task.plan_terminal_initiative_closeout_runtime.add_terminal_closeout_mutations |
| [task.plan_terminal_initiative_closeout_runtime.validate_terminal_closeout_and_clear_closing_initiatives](/plan/initiatives/plan_terminal_initiative_closeout_runtime/.wt/tasks/validate_terminal_closeout_and_clear_closing_initiatives/task.json) | `completed` | `high` | `repository_maintainer` | Add tests, rebuild validation, and use the new closeout path to move the current closing initiatives into terminal states. | task.plan_terminal_initiative_closeout_runtime.expose_terminal_closeout_command_surface |

## Dependencies and Risks
- Task `task.plan_terminal_initiative_closeout_runtime.expose_terminal_closeout_command_surface` depends on `task.plan_terminal_initiative_closeout_runtime.add_terminal_closeout_mutations`.
- Task `task.plan_terminal_initiative_closeout_runtime.validate_terminal_closeout_and_clear_closing_initiatives` depends on `task.plan_terminal_initiative_closeout_runtime.expose_terminal_closeout_command_surface`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_terminal_initiative_closeout_runtime/summary.md)
