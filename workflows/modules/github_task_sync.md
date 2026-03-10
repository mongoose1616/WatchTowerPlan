# GitHub Task Sync Workflow

## Purpose
Use this workflow to publish local-first task records to GitHub issues and optional project items while preserving local task files as the authoritative source of truth.

## Use When
- Local task records need hosted GitHub visibility for collaboration or board-level coordination.
- A maintainer wants to dry-run or execute push-only GitHub task sync for selected tasks.
- Existing GitHub foreign keys or project bindings on task records need to be refreshed deterministically.

## Inputs
- Scoped GitHub sync request
- Selected local task IDs or task filters
- Target GitHub repository and optional project boundary
- Current task records plus any existing GitHub foreign-key metadata
- Available GitHub credentials and local derived task surfaces

## Additional Files to Load
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): defines the local-versus-remote authority boundary, foreign-key set, and status mapping this workflow must preserve.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): local task records remain authoritative even when GitHub mirrors exist.
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md): distills the GitHub issue and project behavior this workflow may need to map local tasks onto.
- [watchtower_core_sync_github_tasks.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_github_tasks.md): documents the command surface that performs the actual push-only sync.
- [task_lifecycle_management.md](/home/j/WatchTowerPlan/workflows/modules/task_lifecycle_management.md): GitHub sync writes local task metadata and must leave the authoritative task corpus aligned afterward.

## Workflow
1. Confirm the sync boundary and authority model.
   - Identify which tasks should sync, which repository or project they target, and whether the run is dry-run or write mode.
   - Keep the local task files authoritative and treat GitHub identifiers as foreign keys only.
2. Inspect current selection and bindings.
   - Check that the selected tasks exist, that existing repository or project bindings are still valid, and that any rebinding is explicit.
   - Confirm whether the sync should manage labels and whether a GitHub Project target is in scope.
3. Execute the bounded GitHub sync.
   - Use the narrow task-selection filters and explicit repository or project arguments required by the sync request.
   - In write mode, persist returned GitHub foreign keys back onto the task records only after successful remote operations.
4. Refresh local mirrors after local task metadata changes.
   - Rebuild the task index and task tracker whenever GitHub metadata changes locally.
   - Refresh traceability when the synced tasks carry a `trace_id` and the local task metadata changed.
5. Validate the sync outcome and record exceptions.
   - Make partial failures, unsynced tasks, and binding conflicts explicit instead of claiming a blanket success.
   - Confirm the resulting local task records, tracker, and index still describe the same task state after the sync.

## Data Structure
- Selected authoritative task records
- Optional GitHub issue and project foreign keys
- Rebuilt local task tracker, task index, and traced joins when affected

## Outputs
- Dry-run sync plan or write-mode sync result
- Updated local task records with persisted GitHub foreign keys when write mode succeeds
- Updated derived task surfaces after local metadata changes

## Done When
- The requested GitHub sync boundary is explicit and local authority was preserved.
- Successful write-mode sync persisted only the intended foreign keys and rebuilt the affected local mirrors.
- Any unsynced tasks, partial failures, or rebinding exceptions are explicit.
