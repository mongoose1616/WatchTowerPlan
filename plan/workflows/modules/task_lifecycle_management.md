# Task Lifecycle Management Workflow

## Purpose
Use this workflow to create, update, split, unblock, or close initiative-local live task records while keeping the live task index, initiative coordination view, and human companion trackers aligned.

## Use When
- Engineer-sized execution work needs a new tracked task or an existing task needs a material state change.
- A task owner, task status, priority, blockers, dependencies, or linked planning surfaces need to be updated explicitly.
- The main action is creating, updating, splitting, blocking, unblocking, or closing live task records.
- Use `task_phase_transition.md` when the main action is handing work to the next owner or phase rather than performing broader task management.

## Inputs
- Scoped task-management request or active work item
- Current live task state under the relevant initiative root in `plan/**/.wt/tasks/**`
- Any linked `trace_id`, planning IDs, repository paths, or existing blocker or dependency IDs
- Current live task, initiative, readiness, coordination, and traceability surfaces when the task is traced

## Additional Files to Load
- [task_tracking_standard.md](/plan/docs/standards/governance/task_tracking_standard.md): defines the live task authority model, canonical task-state vocabulary, and same-change rebuild expectations.
- [task_index_standard.md](/plan/docs/standards/data_contracts/task_index_standard.md): defines the machine-readable live task lookup surface that must stay aligned with task state.
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): traced tasks must preserve explicit links back to planning and forward to derived trace joins.
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md): traced task changes may shift the derived initiative phase, owner, blocker state, or next-step projection.

## Workflow
1. Confirm the task-management boundary.
   - Decide whether the request needs one task update, one new task, a task split, or a terminal task close.
   - Keep one live task per bounded work item instead of merging multiple unrelated execution concerns.
2. Inspect current live task and planning state.
   - Check whether a matching task already exists and whether the work belongs to an existing initiative or trace.
   - Resolve current owner, status, blockers, dependencies, related IDs, and initiative root before editing anything.
   - If the requested task status would start real execution (`in_progress`, `in_review`, or `completed`), confirm the initiative package has already been approved into `ready_for_execution`, using [watchtower_core_plan_confirm_inputs.md](/plan/docs/commands/core_python/watchtower_core_plan_confirm_inputs.md) and [watchtower_core_plan_approve.md](/plan/docs/commands/core_python/watchtower_core_plan_approve.md) before changing task state when needed.
3. Create or update the authoritative live task record.
   - Assign or preserve the stable `task_id`, owner, task kind, priority, and linked planning IDs.
   - Keep artifact `status` at the canonical live value `active` and update execution `task_status`, `depends_on`, `blocked_by`, `related_ids`, and `applies_to` explicitly rather than burying lifecycle state in prose.
   - Keep the task under the same initiative-local `.wt/tasks/**` root; terminality is represented by `task_status`, not by moving docs-backed files.
   - Do not start execution by task mutation before the initiative package is reviewed, approved, and `ready_for_execution`; use `watchtower-core plan confirm-inputs` and `watchtower-core plan approve` first when the package is still pre-execution.
4. Refresh the derived task surfaces.
   - Rebuild the task index with [watchtower_core_plan_sync_task_index.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_task_index.md) in the same change set as the authoritative task update.
   - Rebuild the initiative projection with [watchtower_core_plan_sync_initiative_index.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_initiative_index.md) when the task change affects initiative phase, owner, blockers, or next-step projection.
   - Rebuild trace joins with [watchtower_core_plan_sync_traceability_index.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_traceability_index.md) when the task change affects traced links or execution-visible coverage.
   - Refresh GitHub mirrors with [watchtower_core_plan_sync_github_tasks.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_github_tasks.md) when the initiative or task family mirrors open work externally.
5. Validate the resulting lifecycle state.
   - Check that referenced blocker or dependency IDs resolve.
   - Confirm the command-driven task, initiative, traceability, and GitHub companion surfaces now agree with the authoritative task record when those surfaces were in scope.
   - Record the next expected action, follow-up, or handoff explicitly if the task is not terminal.

## Data Structure
- Authoritative initiative-local `task.json` record under `plan/**/.wt/tasks/**`
- Derived task tracker and live task index
- Derived initiative coordination surfaces when the task belongs to a traced initiative
- Optional traceability join updates when the task belongs to a traced initiative

## Outputs
- Created or updated live task record files
- Updated `plan/.wt/indexes/task_index.json` and `plan/tracking/task_tracking.md`
- Updated `plan/.wt/indexes/initiative_index.json`, `plan/.wt/indexes/readiness_index.json`, and `plan/.wt/indexes/coordination_index.json` when traced task state changed
- Updated initiative-local rendered `plan.md`, `progress.md`, or `summary.md` companions when the task change shifted visible execution state
- Updated traceability and related companion surfaces when traced task links changed materially
- Updated initiative lifecycle state and initiative events when the first execution task transitions the package from `ready_for_execution` into `in_progress`

## Done When
- The authoritative live task record reflects the intended lifecycle state clearly.
- The live task index, human task tracker, and initiative/coordination views agree with the current task corpus.
- Any traced task changes have an explicit traceability outcome or an explicit recorded exception.
