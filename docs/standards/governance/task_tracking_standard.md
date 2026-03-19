---
id: "std.governance.task_tracking"
title: "Task Tracking Standard"
summary: "This standard defines the hard-cutover live task tracking model built on initiative-local plan task state and derived plan-workspace indexes."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "task_tracking"
owner: "repository_maintainer"
updated_at: "2026-03-18T20:35:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "plan/initiatives/"
  - "plan/projects/"
  - "plan/.wt/indexes/task_index.json"
  - "docs/planning/tasks/task_tracking.md"
aliases:
  - "live task tracking"
  - "task board"
  - "work tracking"
---

# Task Tracking Standard

## Summary
This standard defines the repository's hard-cutover live task tracking model so humans and agents coordinate execution from initiative-local `plan/**` task state instead of from docs-backed task Markdown.

## Purpose
- Give the repository one authoritative live task system for active execution coordination.
- Keep machine state, query surfaces, and human trackers aligned around the same initiative-local task authority.
- Stop docs-backed task files, legacy status aliases, and tracker compaction from reintroducing planning sprawl or operational ambiguity.

## Scope
- Applies to live task state under `plan/initiatives/**/.wt/tasks/**/task.json`.
- Applies to live task state under `plan/projects/**/initiatives/**/.wt/tasks/**/task.json`.
- Applies to the derived machine-readable task index under `plan/.wt/indexes/task_index.json`.
- Applies to the derived human-readable task tracker under `docs/planning/tasks/task_tracking.md`.
- Covers task execution status, live authority, human companion rendering, and GitHub-sync authority boundaries.
- Does not replace PRDs, design docs, decisions, initiative state, or the broader traceability model.

## Use When
- Capturing engineer-sized work items that need active ownership and status tracking.
- Coordinating concurrent work across multiple engineers or agents inside one bounded initiative.
- Reviewing whether a change should create or update a live task instead of only touching plan prose.

## Related Standards and Sources
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_handling_threshold_standard.md](/docs/standards/governance/task_handling_threshold_standard.md): companion standard that defines when work must create, update, transition, or explicitly decline a durable task record.
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md): companion standard for the retained docs-backed historical task corpus.
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md): companion standard that constrains the machine-readable live task lookup surface.
- [github_task_sync_standard.md](/docs/standards/governance/github_task_sync_standard.md): companion standard that constrains GitHub foreign-key behavior for live task records.
- [planning_retention_and_purge_standard.md](/docs/standards/governance/planning_retention_and_purge_standard.md): companion standard that constrains how retained historical task Markdown may later be removed.
- [README.md](/docs/planning/tasks/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Treat initiative-local `task.json` plus task events as the authoritative live execution surface.
- Create new live tasks only under the matching initiative root in `plan/initiatives/**` or `plan/projects/**/initiatives/**`.
- Do not create new live execution tasks under `docs/planning/tasks/**`.
- Treat `docs/planning/tasks/**` as retained historical material only.
- Store one live task per bounded work item.
- Use only these canonical live task statuses:
  - `planned`
  - `ready`
  - `in_progress`
  - `in_review`
  - `blocked`
  - `completed`
  - `cancelled`
- Do not use `backlog` or `done` as live task statuses.
- Use only these task priority values:
  - `critical`
  - `high`
  - `medium`
  - `low`
- Use only these task kinds unless a later standard extends the set:
  - `feature`
  - `bug`
  - `chore`
  - `documentation`
  - `governance`
  - `research`
- Treat the initiative package as the authority for `trace_id`, initiative identity, and task root placement.
- Do not start real execution from task state until the initiative package is reviewed, approved, and marked `ready_for_execution`.
- Prefer linking tasks to durable planning artifacts with `related_ids` when those sources exist.
- Use `blocked_by` and `depends_on` to express task-to-task coordination explicitly instead of burying blockers in prose.
- Treat `plan/.wt/indexes/task_index.json` as the canonical machine-readable task lookup surface.
- Treat `docs/planning/tasks/task_tracking.md` as a derived human companion, not as the task source of truth.
- Keep the task tracker summary-first, but retain full active and terminal task tables so humans can review outcomes without falling back to raw JSON for normal browsing.
- GitHub sync may persist foreign keys back onto the live task record, but the initiative-local task record remains authoritative.

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| Initiative-local `task.json` | Authoritative live task record |
| Initiative-local task events | Append-only live task history |
| `plan/.wt/indexes/task_index.json` | Derived machine-readable lookup surface |
| `docs/planning/tasks/task_tracking.md` | Derived human-readable task board |
| `docs/planning/tasks/**` | Retained historical corpus only |

## Process or Workflow
1. Create or update one live task record under the correct initiative root.
2. Confirm the initiative package is already `ready_for_execution` before setting any task to an execution-starting status such as `in_progress`, `in_review`, or `completed`.
3. Keep owner, status, blockers, dependencies, and related IDs explicit in the live task record.
4. Rebuild the live plan indexes and rendered views in the same change set after task mutations.
5. Refresh the human task tracker from the live task index in the same change set.
6. Rebuild traceability and initiative-family companions when traced task state changes materially.

## Examples
- A new implementation slice with one owner and one bounded outcome should be one live `task.json` record under the matching initiative root.
- A completed task should remain in place under the initiative-local task root and change only its live status to `completed`.
- A traced task should publish coherent related IDs that point back to the bounded planning package it executes.

## Operationalization
- `Modes`: `documentation`; `artifact`
- `Operational Surfaces`: `plan/initiatives/`; `plan/projects/`; `plan/.wt/indexes/task_index.json`; `docs/planning/tasks/task_tracking.md`

## Validation
- Live task records should validate against the published live task schema.
- `docs/planning/tasks/task_tracking.md` and `plan/.wt/indexes/task_index.json` should agree with current live task state.
- Every live task `doc_path` in the task index should point to `plan/**/.wt/tasks/**/task.json`.
- Task IDs referenced by `blocked_by` or `depends_on` should exist in the current live task corpus.
- Execution-starting task statuses should fail closed unless the linked initiative package is approved and `ready_for_execution`.
- No active workflow, standard, or command doc should require new live tasks under `docs/planning/tasks/**`.

## Change Control
- Update this standard when the repository changes live task-state vocabulary, plan-root placement rules, or the source-of-truth boundary for task execution.
- Update the task Markdown retention standard, task-index standard, task command docs, and companion sync logic in the same change set when task tracking changes structurally.

## References
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md)
- [task_handling_threshold_standard.md](/docs/standards/governance/task_handling_threshold_standard.md)
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md)
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md)
- [github_task_sync_standard.md](/docs/standards/governance/github_task_sync_standard.md)
- [planning_retention_and_purge_standard.md](/docs/standards/governance/planning_retention_and_purge_standard.md)
- [README.md](/docs/planning/tasks/README.md)

## Updated At
- `2026-03-18T20:35:00Z`
