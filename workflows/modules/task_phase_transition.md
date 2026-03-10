# Task Phase Transition Workflow

## Purpose
Use this workflow to hand a task from one owner, phase, or execution stage to the next without losing context, dependencies, or trace links.

## Use When
- Work is moving from planning to design, design to implementation, implementation to review, review to validation, or any similar bounded phase change.
- Ownership of a task is changing and the next responsible person or phase must be explicit.
- A task should hand off into one or more successor tasks instead of continuing as one long-lived ambiguous record.

## Inputs
- Source task or task set that is changing phase
- Intended next phase, next owner, or successor-task boundary
- Current blockers, dependencies, linked planning IDs, and `trace_id` values
- Current task tracker, task index, and traceability surfaces when the transition affects traced work

## Additional Files to Load
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): defines the authoritative task-state vocabulary and explicit dependency rules this workflow must preserve.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): phase transitions must preserve upstream and downstream trace links rather than forcing later readers to infer them.
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): terminal phase transitions may need closeout escalation when no open execution work remains.
- [task_lifecycle_management.md](/home/j/WatchTowerPlan/workflows/modules/task_lifecycle_management.md): source task updates and successor-task creation should stay aligned with the repository's normal task lifecycle rules.

## Workflow
1. Confirm the transition boundary.
   - Identify the source task, the intended next phase or owner, and whether the work continues in-place or should split into successor tasks.
   - Keep the transition bounded so one handoff does not silently rewrite unrelated task state.
2. Inspect the current handoff state.
   - Review current `task_status`, owner, blockers, dependencies, `related_ids`, and task notes.
   - Check whether downstream planning, validation, or closeout surfaces depend on the transition being explicit.
3. Update the source and successor task records.
   - Mark the source task as handed off, complete, cancelled, or still active as appropriate to the real execution boundary.
   - Create or update successor tasks when the next phase needs its own bounded owner, scope, or done-when criteria.
   - Preserve or extend `trace_id`, `related_ids`, `depends_on`, and `blocked_by` so the phase relationship remains queryable.
4. Refresh companion tracking surfaces.
   - Rebuild the task tracker and task index after the phase transition changes task metadata or task files.
   - Refresh traceability when the transition affects traced work or the active task chain for one initiative.
5. Validate the handoff and escalation state.
   - Confirm the next responsible phase or owner is explicit and that no blockers or successor relationships became orphaned.
   - If the transition appears to finish the traced initiative, recommend or merge initiative closeout rather than leaving the terminal state implicit.

## Data Structure
- Source task state before and after transition
- Successor-task set when the work splits by phase or owner
- Dependency and trace-link updates caused by the handoff

## Outputs
- Updated source and successor task records with explicit handoff state
- Updated derived task tracker, task index, and traceability surfaces when affected
- A clear next-phase or closeout recommendation

## Done When
- The next owner or next phase is explicit in the task corpus.
- Successor, dependency, and trace relationships remain queryable after the handoff.
- Any closeout escalation or remaining blocker is explicit rather than implied.
