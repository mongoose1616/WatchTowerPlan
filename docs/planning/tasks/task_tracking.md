# Task Tracking

## Summary
This document provides the human-readable tracking view for local task records under `docs/planning/tasks/`. Rebuild it from the governed task files instead of using it as the primary task source of truth.

## Open Tasks
| Task ID | Task Status | Priority | Owner | Trace ID | Path | Summary | Blocked By |
|---|---|---|---|---|---|---|---|
| `task.core_export_readiness_and_optimization.pack_interfaces.001` | `backlog` | `high` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/open/core_export_pack_interfaces.md` | Add generic pack-facing schemas, examples, and validation hooks for work-item notes, extraction outputs, promoted knowledge, promotion records, and pack indexes without starting domain-pack implementation. | `None` |
| `task.core_export_readiness_and_optimization.workspace_injection.001` | `backlog` | `high` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/open/core_export_workspace_injection.md` | Replace implicit repo-root discovery with injected workspace configuration, artifact sources, and artifact stores so reusable services can run against non-WatchTowerPlan layouts. | `None` |
| `task.core_export_readiness_and_optimization.retrieval_and_coordination.001` | `backlog` | `medium` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/open/core_export_retrieval_and_coordination.md` | Extend retrieval indexes with stronger authority hints and add a deterministic coordination rebuild slice for task, traceability, and initiative surfaces. | `None` |

## Closed Tasks
| Task ID | Task Status | Priority | Owner | Trace ID | Path | Summary | Blocked By |
|---|---|---|---|---|---|---|---|
| `task.core_export_readiness_and_optimization.bootstrap.001` | `done` | `high` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/closed/core_export_initiative_bootstrap.md` | Creates the initiative's PRD, feature design, implementation plan, acceptance baseline artifacts, open execution tasks, and git workflow standard so export-readiness work can proceed from governed local surfaces. | `None` |
| `task.core_export_readiness_and_optimization.command_registry.001` | `done` | `high` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/closed/core_export_command_registry.md` | Introduce registry-backed CLI command authority so parser wiring, command lookup, and command-surface maintenance no longer depend on one monolithic CLI file and doc-derived machine metadata. | `None` |
| `task.core_export_readiness_and_optimization.repo_ops_boundary.001` | `done` | `high` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/closed/core_export_repo_ops_boundary.md` | Move repository-specific query, sync, validation, and planning-document semantics into explicit repo-ops surfaces so reusable layers stop depending on WatchTowerPlan-only behavior. | `None` |
| `task.core_python_foundation.closeout.001` | `done` | `high` | `repository_maintainer` | `trace.core_python_foundation` | `docs/planning/tasks/closed/core_python_foundation_closeout.md` | Tracks the remaining initiative-level closeout for the core Python foundation slice. | `None` |
| `task.local_task_tracking_foundation.001` | `done` | `high` | `repository_maintainer` | `trace.local_task_tracking` | `docs/planning/tasks/closed/local_task_tracking_foundation.md` | Establishes governed local task records, a generated human tracker, a generated machine index, and Python query and sync commands for task coordination. | `None` |
| `task.acceptance_evidence_reconciliation.followup.001` | `done` | `medium` | `repository_maintainer` | `trace.acceptance_evidence_reconciliation` | `docs/planning/tasks/closed/acceptance_evidence_reconciliation_followup.md` | Tracks the remaining closeout and verification follow-up for the acceptance and evidence reconciliation initiative. | `None` |
| `task.command_documentation_and_lookup.followup.001` | `done` | `medium` | `repository_maintainer` | `trace.command_documentation_and_lookup` | `docs/planning/tasks/closed/command_documentation_and_lookup_followup.md` | Tracks the remaining closeout and verification follow-up for the command documentation and lookup initiative. | `None` |
| `task.core_export_readiness_and_optimization.sync_validation_registries.001` | `done` | `medium` | `repository_maintainer` | `trace.core_export_readiness_and_optimization` | `docs/planning/tasks/closed/core_export_sync_validation_registries.md` | Introduce governed sync-family and validation-family registries so orchestration, listing, and coverage checks no longer depend on duplicated manual enumerations. | `None` |
| `task.github_collaboration.followup.001` | `done` | `medium` | `repository_maintainer` | `trace.github_collaboration` | `docs/planning/tasks/closed/github_collaboration_followup.md` | Tracks the remaining closeout and verification follow-up for the GitHub collaboration scaffolding initiative. | `None` |
| `task.initiative_closeout.followup.001` | `done` | `medium` | `repository_maintainer` | `trace.initiative_closeout` | `docs/planning/tasks/closed/initiative_closeout_followup.md` | Tracks the remaining closeout and verification follow-up for the initiative closeout and planning tracker initiative. | `None` |
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
- `2026-03-10T05:45:03Z`
