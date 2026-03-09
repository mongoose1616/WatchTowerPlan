---
id: "std.governance.github_task_sync"
title: "GitHub Task Sync Standard"
summary: "This standard defines the repository's first GitHub task sync contract for pushing local task records to GitHub issues and optional project items without making GitHub the source of truth."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "github_sync"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/python/src/watchtower_core/sync/github_tasks.py"
aliases:
  - "github task sync"
  - "issue sync"
  - "project sync"
---

# GitHub Task Sync Standard

## Summary
This standard defines the repository's first GitHub task sync contract for pushing local task records to GitHub issues and optional project items without making GitHub the source of truth.

## Purpose
- Keep the repository local-first while still supporting a hosted execution surface for multi-engineer coordination.
- Standardize how local task metadata maps to GitHub issues and project status.
- Prevent local task identity from collapsing into GitHub issue numbers or project item IDs.

## Scope
- Applies to push sync from task records under `docs/planning/tasks/` to GitHub issues and optional GitHub Projects v2 items.
- Applies to the GitHub foreign-key metadata persisted on task documents and in the derived task index.
- Covers the local-versus-remote authority boundary, required foreign keys, and the first project-status mapping.
- Does not define two-way reconciliation or GitHub as an authoritative planning surface.

## Use When
- A local task needs to appear on GitHub for shared execution visibility.
- Multiple engineers or agents need a hosted issue or board view while the repo remains the durable source of truth.
- Reviewing whether a proposed sync change would let GitHub override local task state.

## Related Standards and Sources
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md): companion planning or design surface this standard should remain consistent with.
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md): local reference surface for the external or canonical guidance this standard depends on.
## Guidance
- Treat local task records as the authoritative source of truth.
- Treat GitHub issue numbers, node IDs, repositories, and project item IDs as foreign keys only.
- The first GitHub sync phase is push-only:
  - local task records create or update GitHub issues
  - local task records optionally add those issues to one GitHub Project v2
  - GitHub should not rewrite local task state automatically
- Use GitHub comments for discussion rather than editing the managed issue body directly.
- Keep the local `task_id` stable even after GitHub foreign keys are added.
- Persist these GitHub task fields when they become known:
  - `github_repository`
  - `github_issue_number`
  - `github_issue_node_id`
  - `github_project_owner`
  - `github_project_owner_type`
  - `github_project_number`
  - `github_project_item_id`
  - `github_synced_at`
- Do not require GitHub metadata for unsynced local tasks.
- Keep `updated_at` for task-content updates and use `github_synced_at` for the last successful remote sync timestamp.
- Manage a small bounded GitHub label set for synced issues:
  - `source:watchtower`
  - `kind:<task_kind>`
  - `status:<task_status>`
  - `priority:<priority>`
  - `blocked` when the local task currently declares blockers
- Map local task execution state to GitHub issue state like this:
  - `backlog`, `ready`, `in_progress`, `blocked`, `in_review` -> open issue
  - `done` -> closed issue with state reason `completed`
  - `cancelled` -> closed issue with state reason `not_planned`
- When also syncing to GitHub Projects v2, use a single-select status field whose options match the local task-status vocabulary:
  - `Backlog`
  - `Ready`
  - `In Progress`
  - `Blocked`
  - `In Review`
  - `Done`
  - `Cancelled`
- Do not silently rebind an already-synced task to a different GitHub repository or project without an explicit operator action.
- Use a stable issue body structure that mirrors:
  - task metadata
  - summary
  - context
  - scope
  - done-when criteria
  - links
  - sync notes about local authority

## Structure or Data Model
### Local-to-GitHub authority boundary
| Surface | Role |
|---|---|
| Task Markdown record | Authoritative task source |
| GitHub Issue | Hosted execution mirror |
| GitHub Project item | Hosted board placement |
| Task index | Local machine-readable lookup including GitHub foreign keys |

### Required GitHub foreign-key metadata
| Field | Meaning |
|---|---|
| `github_repository` | Repository in `owner/name` form that owns the mirrored issue |
| `github_issue_number` | Stable issue number within that repository |
| `github_issue_node_id` | GraphQL node ID for GitHub issue and project-item operations |
| `github_project_owner` | GitHub login that owns the synced project |
| `github_project_owner_type` | `user` or `organization` |
| `github_project_number` | Stable project number for the synced project |
| `github_project_item_id` | GraphQL item ID for the project card |
| `github_synced_at` | Last successful GitHub sync timestamp in UTC |

### Managed GitHub labels
| Label pattern | Meaning |
|---|---|
| `source:watchtower` | Issue is managed by the repo-local sync flow |
| `kind:<task_kind>` | Mirrors the local task kind |
| `status:<task_status>` | Mirrors the local task-status value |
| `priority:<priority>` | Mirrors the local task priority |
| `blocked` | Mirrors the presence of blocker IDs on the local task |

## Process or Workflow
1. Select the local task records that should be published to GitHub.
2. Resolve the target repository and optional project boundary explicitly.
3. Create or update the GitHub issue from the local task record.
4. Optionally add or update the GitHub Project item and mapped status field.
5. Upsert the managed GitHub labels when label sync is enabled.
6. Persist returned GitHub foreign keys back onto the local task record.
7. Rebuild the task index, task tracker, and traceability index in the same change set when local task metadata changed.

## Validation
- Task records with `github_issue_number` should also carry `github_repository`.
- Task records with `github_project_item_id` should also carry the project owner, owner type, and project number.
- The task index should preserve the same GitHub foreign keys published in the task documents.
- Reviewers should reject any sync flow that lets GitHub replace the local `task_id` or local task-status source of truth.
- All GitHub sync timestamps should use UTC RFC 3339 timestamps with a trailing `Z`.
- The managed GitHub labels should remain bounded and deterministic rather than becoming free-form tags.

## Change Control
- Update this standard when the repository changes the GitHub sync authority boundary, foreign-key set, or status mapping.
- Update the task front-matter schema, task index schema, task template, task sync command docs, and implementation surfaces in the same change set when this sync contract changes structurally.

## References
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md)
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md)

## Updated At
- `2026-03-09T23:02:08Z`
