# Task Coordinator Role

## Purpose
Use this role to orchestrate live task creation, phase transitions, and optional GitHub mirroring so execution state changes stay bounded, queryable, and synchronized across task surfaces.

## Use When
- The request spans multiple task operations such as lifecycle updates, handoffs, successor-task creation, and GitHub mirroring.
- The main risk is fragmented execution coordination rather than one isolated task mutation.
- The task needs a dedicated orchestration layer that keeps live task state, handoff state, and optional external mirrors aligned.

## Inputs
- Scoped task-coordination request
- Current live task records, initiative state, and traced planning context when applicable
- Existing GitHub mirror expectations when external task sync is in scope

## Composes Modules
- [task_lifecycle_management.md](../modules/task_lifecycle_management.md): updates the authoritative live task records and their command-driven derived surfaces.
- [task_phase_transition.md](../modules/task_phase_transition.md): preserves handoff boundaries, successor-task relationships, and next-owner clarity.
- [github_task_sync.md](../modules/github_task_sync.md): mirrors open local task state to GitHub when external issue tracking is part of the coordination boundary.

## Workflow
1. Confirm whether the request is a broad coordination task or one narrow task mutation that should stay on a module-only route.
2. Use `task_lifecycle_management.md` for the authoritative task-state mutation and keep one bounded work item per task record.
3. Use `task_phase_transition.md` when the coordination problem includes ownership or phase changes that should not remain implicit in task notes.
4. Use `github_task_sync.md` only when external GitHub mirrors are in scope, keeping GitHub publication downstream of the authoritative local task state.
5. Close with explicit next-owner, next-phase, blocker, and mirror-sync status so execution coordination does not depend on oral context.

## Data Structure
- Authoritative live task state plus explicit handoff or successor-task relationships
- Optional GitHub mirror status when external publication is in scope

## Outputs
- Coordinated task-state, handoff-state, and GitHub-mirror updates for the scoped work
- Explicit next-action or remaining-blocker guidance when execution is not yet complete

## Done When
- Live task state and phase-transition state remain bounded and queryable.
- Optional GitHub mirroring follows the authoritative local task corpus rather than diverging from it.
- The role has coordinated the task workflows without duplicating their task-level procedures.
