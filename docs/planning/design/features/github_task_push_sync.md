---
trace_id: "trace.local_task_tracking"
id: "design.features.github_task_push_sync"
title: "GitHub Task Push Sync"
summary: "Defines the first push-only sync from local task records to GitHub issues and optional project items while preserving local task authority."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T18:25:06Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/tasks/task_index.v1.json"
  - "core/python/src/watchtower_core/sync/github_tasks.py"
aliases:
  - "github task push sync"
  - "github issues sync"
---

# GitHub Task Push Sync

## Record Metadata
- `Trace ID`: `trace.local_task_tracking`
- `Design ID`: `design.features.github_task_push_sync`
- `Design Status`: `active`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `2026-03-09T18:25:06Z`

## Summary
This document defines the first push-only sync from local task records to GitHub issues and optional project items while preserving local task authority.

## Source Request
- User request to support a local-first task system that can later sync to GitHub.
- User request to keep the repository modular, queryable, and extensible as coordination needs grow.

## Scope and Feature Boundary
- Covers local task record push sync to GitHub issues.
- Covers optional GitHub Project v2 item creation and status updates.
- Covers local persistence of GitHub foreign keys on task records and in the task index.
- Does not make GitHub the source of truth.
- Does not implement two-way GitHub reconciliation.

## Current-State Context
- The repository already has local task records, a generated task tracker, and a generated task index.
- The task family already reserves optional GitHub foreign-key fields.
- There is no live GitHub sync implementation yet, and no current way to publish local task state to a hosted board.

## Foundations References Applied
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md): keep durable machine-readable authority explicit and reviewable in git.
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md): combine planning, execution, validation, and closeout without hiding state in disconnected tools.
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md): keep Markdown as the human task source and JSON as the machine-readable lookup surface.
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md): keep one authoritative source per concern and derive companion lookup surfaces from it.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): local task Markdown records must stay the authoritative task source.
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): push-only sync, foreign-key persistence, and hosted status mapping must stay deterministic.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): synced GitHub metadata has to land in the machine-readable task index.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): synced tasks still need stable `trace_id` joins back to planning and evidence surfaces.
- [task_template.md](/home/j/WatchTowerPlan/docs/templates/task_template.md): local task records need a consistent document shape so sync can render them predictably.
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md): use the repo-native GitHub reference as the shared summary of the issue and project API assumptions.

## Design Goals and Constraints
- Keep local task files authoritative.
- Keep the sync contract push-only in the first phase.
- Persist enough foreign-key metadata that repeated sync is deterministic.
- Rebuild local derived task surfaces automatically after successful sync writes.
- Avoid introducing a hard dependency on GitHub labels, issue forms, or custom automation before the core mirror works.

## Options Considered
### Option 1
- Use GitHub issues as the only live task source.
- Strengths: simple hosted workflow and native collaboration UI.
- Tradeoffs or reasons not chosen: breaks the local-first planning model and makes git-reviewed task history secondary.

### Option 2
- Push local task records to GitHub issues and optional project items while keeping local records authoritative.
- Strengths: keeps local reviewability and enables hosted coordination at the same time.
- Tradeoffs or reasons not chosen: requires foreign-key persistence and a disciplined local-versus-remote authority boundary.

### Option 3
- Implement two-way reconciliation immediately.
- Strengths: GitHub edits and local edits could converge.
- Tradeoffs or reasons not chosen: conflict handling, authority ambiguity, and drift risk would rise before the local task model stabilizes.

## Recommended Design
### Architecture
- Keep task Markdown records as the source of truth.
- Use a push-only Python sync command to create or update GitHub issues from those task records.
- Optionally add the synced issue to one GitHub Project v2 and update the single-select status field.
- Persist GitHub foreign keys back onto the task records and rebuild the derived task index, task tracker, and traceability index in the same write flow.

### Data and Interface Impacts
- Extend the task front matter and task index with repository, project, and sync timestamp fields.
- Add a modular GitHub integration client under `core/python/src/watchtower_core/integrations/github/`.
- Add a narrow `watchtower-core sync github-tasks` command with explicit task filters and target arguments.

### Execution Flow
1. Select task records by task ID, trace, owner, or execution filters.
2. Resolve the GitHub repository from CLI input, existing task metadata, or `GITHUB_REPOSITORY`.
3. Create or update the GitHub issue from the local task content.
4. Optionally create or update the GitHub Project item and its mapped status field.
5. Persist returned GitHub foreign keys and `github_synced_at` on the task records.
6. Rebuild `task_index.v1.json`, `task_tracking.md`, and `traceability_index.v1.json`.

### Invariants and Failure Cases
- Local task IDs remain stable and do not become GitHub issue identities.
- GitHub repository or project rebinding should fail explicitly instead of silently retargeting a task.
- Project sync should fail clearly if the target project does not expose the expected status field and option set.
- Remote sync failure for one task should not silently claim success for the full selection.

## Affected Surfaces
- `docs/planning/tasks/`
- `docs/standards/governance/github_task_sync_standard.md`
- `docs/standards/governance/task_tracking_standard.md`
- `docs/standards/data_contracts/task_index_standard.md`
- `core/control_plane/schemas/interfaces/documentation/task_front_matter.v1.schema.json`
- `core/control_plane/schemas/artifacts/task_index.v1.schema.json`
- `core/python/src/watchtower_core/integrations/github/`
- `core/python/src/watchtower_core/sync/github_tasks.py`

## Design Guardrails
- Keep GitHub sync push-only until the local model has stable usage and enough conflict evidence to justify two-way reconciliation.
- Keep GitHub-specific metadata optional and integration-scoped.
- Do not require GitHub labels or project automation for baseline sync correctness.

## Implementation-Planning Handoff Notes
- Start with one command that can dry-run or write.
- Make the command persist foreign keys only after successful remote operations.
- Regenerate local derived task surfaces automatically after task metadata changes.

## Dependencies
- Existing task-document parsing and validation in `core/python/src/watchtower_core/sync/task_documents.py`.
- Existing task index and traceability sync flows.
- GitHub Issues REST API and GitHub Project GraphQL surfaces.

## Risks
- If engineers edit the managed issue body directly, drift will reappear quickly.
- If local task metadata is incomplete, sync will require more explicit operator input.
- If the first project field mapping is too permissive, board-state meaning will become inconsistent.

## External Sources Consulted
- [GitHub Issues REST API](https://docs.github.com/en/rest/issues/issues): shaped issue create or update behavior, issue-state mapping, and managed-label expectations.
- [GitHub Projects API](https://docs.github.com/en/graphql/guides/using-the-api-to-manage-projects): shaped project-item creation and single-select status-field updates.

## Open Questions
- Should a later sync phase publish local task dependencies to GitHub issue dependencies as well?
- Should a later sync phase support multiple GitHub repositories per local task corpus, or should one repo remain the normal case?

## References
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md)
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md)

## Updated At
- `2026-03-09T18:25:06Z`
