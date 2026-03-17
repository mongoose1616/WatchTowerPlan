# WatchTower Next Work Selection Design Record

## Summary
Adds a local-first next-work command so operators can ask WatchTower what unfinished work should be picked up next from the current workspace state.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_next_work_selection/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- `watchtower work next` should reuse the current local JSON work-item store instead of creating a separate queue or planner artifact.
- The command should consider only unfinished work items, treating `completed` records as terminal and everything else as candidates.
- Selection should be deterministic so repeated calls over unchanged state return the same answer.
- The returned snapshot should include any latest captured note so the operator can resume without first running a second command.
