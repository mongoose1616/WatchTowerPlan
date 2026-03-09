# Task Tracking

## Summary
This document provides the human-readable tracking view for local task records under `docs/planning/tasks/`. Rebuild it from the governed task files instead of using it as the primary task source of truth.

## Open Tasks
| Task ID | Task Status | Priority | Owner | Trace ID | Path | Summary | Blocked By |
|---|---|---|---|---|---|---|---|
| `None` | `None` | `None` | `None` | `None` | `None` | No tasks in this class. | `None` |

## Closed Tasks
| Task ID | Task Status | Priority | Owner | Trace ID | Path | Summary | Blocked By |
|---|---|---|---|---|---|---|---|
| `task.local_task_tracking_foundation.001` | `done` | `high` | `repository_maintainer` | `trace.local_task_tracking` | `docs/planning/tasks/closed/local_task_tracking_foundation.md` | Establishes governed local task records, a generated human tracker, a generated machine index, and Python query and sync commands for task coordination. | `None` |
| `task.local_task_tracking.github_sync.001` | `done` | `medium` | `repository_maintainer` | `trace.local_task_tracking` | `docs/planning/tasks/closed/github_task_sync.md` | Adds one-way GitHub sync support so local task records can publish to GitHub issues and project items without changing local task identity. | `None` |

## Update Rules
- Treat the task files under `docs/planning/tasks/open/` and `docs/planning/tasks/closed/` as the authoritative local task source.
- Rebuild this tracker in the same change set when task files are added, removed, moved, or materially updated.
- Keep the machine-readable companion index at [task_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/tasks/task_index.v1.json) aligned with this tracker.

## References
- [README.md](/home/j/WatchTowerPlan/docs/planning/tasks/README.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md)
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md)

## Updated At
- `2026-03-09T16:14:14Z`
