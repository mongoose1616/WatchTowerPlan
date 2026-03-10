---
id: "std.governance.task_handling_threshold"
title: "Task Handling Threshold Standard"
summary: "This standard defines when repository work must create, update, transition, or explicitly decline a durable local task record."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "task_threshold"
owner: "repository_maintainer"
updated_at: "2026-03-10T05:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "workflows/modules/task_scope_definition.md"
  - "workflows/modules/task_handoff_review.md"
  - "workflows/modules/commit_closeout.md"
aliases:
  - "task threshold"
  - "durable task requirement"
  - "task handling threshold"
---

# Task Handling Threshold Standard

## Summary
This standard defines when repository work must create, update, transition, or explicitly decline a durable local task record.

## Purpose
- Reduce coordination drift when multiple engineers or agents work in parallel.
- Make task handling explicit instead of leaving execution ownership and follow-up implicit.
- Preserve a lightweight path for truly trivial one-shot changes.

## Scope
- Applies to routed work that changes repository artifacts, code, standards, workflows, planning docs, or governed control-plane surfaces.
- Applies to local task records, handoff review, and commit closeout expectations.
- Does not require a durable task for every trivial one-shot change.

## Use When
- Starting non-trivial work.
- Handing work across phases or owners.
- Closing out a change set or preparing a commit.

## Related Standards and Sources
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): durable local task records remain the authoritative execution-tracking surface once the threshold is crossed.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traced work should keep task handling explicit rather than relying on prose-only history.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): non-trivial changes need trace, task, or explicit no-task metadata in commit history.
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md): hosted pull-request metadata should mirror the local task-handling outcome when GitHub is used.
- [task_scope_definition.md](/home/j/WatchTowerPlan/workflows/modules/task_scope_definition.md): routed work should decide task-handling outcome early instead of improvising it at closeout.
- [task_handoff_review.md](/home/j/WatchTowerPlan/workflows/modules/task_handoff_review.md): handoff review must surface missing task handling when the threshold was crossed.
- [commit_closeout.md](/home/j/WatchTowerPlan/workflows/modules/commit_closeout.md): commit closeout should preserve the task-handling outcome in durable metadata.

## Guidance
- Create, update, transition, or close a durable local task when any of these are true:
  - the work is expected to take more than one meaningful step or session
  - the work will likely span more than one commit
  - the work has blockers, dependencies, or explicit owner changes
  - the work belongs to a traced initiative
  - the work is likely to be handed off, reviewed later, or synchronized to GitHub
  - the work changes code plus companion docs, indexes, schemas, or other governed artifacts
- A durable task is usually not required only when all of these are true:
  - the work is one-shot and low-risk
  - the work is expected to finish in one bounded session
  - the work has no blockers, dependencies, owner handoff, or open follow-up
  - the work does not need GitHub execution visibility
- When a durable task is not required, record an explicit `No-Task-Reason` in the commit or pull-request closeout metadata for non-trivial changes.
- Do not use silence as the signal that no task was needed.
- When a durable task exists, use its stable `task_id` in commit or pull-request metadata instead of inventing parallel ad hoc identifiers.
- Active traced initiatives should not remain active in initiative or traceability projections without linked durable task IDs.

## Structure or Data Model
### Allowed task-handling outcomes
| Outcome | Meaning |
|---|---|
| `task_required` | A durable task record must be created, updated, transitioned, or closed. |
| `no_durable_task_needed` | The change is bounded enough that no durable task record is required, but the reason must be explicit for non-trivial work. |

### Minimum closeout metadata
| Situation | Expected Metadata |
|---|---|
| Traced work with task records | `Trace-ID` and `Task-ID` values |
| Non-trivial work with no durable task | `No-Task-Reason` |
| Trivial one-shot work | No extra metadata beyond the normal commit shape unless a workflow or reviewer asks for it |

## Validation
- Reviewers should reject non-trivial work whose task-handling outcome is implicit.
- Handoff and closeout should make clear whether a durable task exists or why one was not needed.
- Traced work should not reach closeout with neither a linked task nor an explicit no-task reason.
- Active traced initiatives should not remain active in derived coordination views without linked durable task IDs.

## Change Control
- Update this standard when the repository changes its threshold for durable task tracking or the metadata used to record explicit no-task outcomes.
- Update task workflows, commit guidance, and hosted collaboration scaffolding in the same change set when this threshold changes materially.

## References
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/tasks/README.md)

## Updated At
- `2026-03-10T05:00:00Z`
