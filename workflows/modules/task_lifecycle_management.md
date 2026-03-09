# Task Lifecycle Management Workflow

## Purpose
Use this workflow to create, update, split, unblock, or close local task records while keeping the derived task tracker, task index, and traced planning joins aligned.

## Use When
- Engineer-sized execution work needs a new tracked task or an existing task needs a material state change.
- A task owner, task status, priority, blockers, dependencies, or linked planning surfaces need to be updated explicitly.
- A task should move between `docs/planning/tasks/open/` and `docs/planning/tasks/closed/`.

## Inputs
- Scoped task-management request or active work item
- Current local task corpus under `docs/planning/tasks/`
- Any linked `trace_id`, planning IDs, repository paths, or existing blocker or dependency IDs
- Current task tracker, task index, and traceability surfaces when the task is traced

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): defines the local task authority model, task-state vocabulary, and same-change rebuild expectations.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): defines the required task-record shape and placement rules.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): defines the machine-readable companion surface that must stay aligned with task records.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traced tasks must preserve explicit links back to planning and forward to derived trace joins.

## Workflow
1. Confirm the task-management boundary.
   - Decide whether the request needs one task update, one new task, a task split, or a terminal task close.
   - Keep one task file per bounded work item instead of merging multiple unrelated execution concerns.
2. Inspect current task and planning state.
   - Check whether a matching task already exists and whether the work belongs to an existing `trace_id`.
   - Resolve current owner, `task_status`, blockers, dependencies, related IDs, and path placement before editing anything.
3. Create or update the authoritative task record.
   - Assign or preserve the stable `task_id`, owner, task kind, priority, and linked planning IDs.
   - Update `task_status`, `depends_on`, `blocked_by`, `related_ids`, and `applies_to` explicitly rather than burying execution state in prose.
   - Place non-terminal tasks under `open/` and terminal tasks under `closed/`.
4. Refresh the derived task surfaces.
   - Rebuild the human-readable task tracker and the machine-readable task index in the same change set.
   - Refresh the traceability index when the task carries a `trace_id` or when its traced links changed materially.
5. Validate the resulting lifecycle state.
   - Check that task placement matches the task-status class and that referenced blocker or dependency IDs resolve.
   - Record the next expected action, follow-up, or handoff explicitly if the task is not terminal.

## Data Structure
- Authoritative task record under `docs/planning/tasks/open/` or `docs/planning/tasks/closed/`
- Derived task tracker and task index
- Optional traceability join updates when the task belongs to a traced initiative

## Outputs
- Created or updated task record files
- Updated `docs/planning/tasks/task_tracking.md` and `core/control_plane/indexes/tasks/task_index.v1.json`
- Updated `core/control_plane/indexes/traceability/traceability_index.v1.json` when traced task state changed

## Done When
- The authoritative task record reflects the intended lifecycle state clearly.
- The derived task tracker and task index agree with the current task corpus.
- Any traced task changes have an explicit traceability outcome or an explicit recorded exception.
