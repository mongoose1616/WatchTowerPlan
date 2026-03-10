---
id: "std.engineering.git_workflow"
title: "Git Workflow Standard"
summary: "This standard defines repository-standard local git workflow behavior, including branch naming, branch lifecycle, and local sync expectations for human and assistant contributors."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "git_workflow"
owner: "repository_maintainer"
updated_at: "2026-03-10T04:28:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/standards/engineering/git_commit_standard.md"
  - "docs/standards/governance/github_collaboration_standard.md"
  - "workflows/modules/commit_closeout.md"
aliases:
  - "git workflow"
  - "branch naming"
  - "branch lifecycle"
---

# Git Workflow Standard

## Summary
This standard defines repository-standard local git workflow behavior, including branch naming, branch lifecycle, and local sync expectations for human and assistant contributors.

## Purpose
- Keep local git behavior predictable enough for humans and agents to collaborate without hidden branch conventions.
- Make branch names readable, bounded, and easy to relate back to traces, tasks, or change intent.
- Reduce merge noise and closeout ambiguity by preferring clear branch scope and linear local history.

## Scope
- Applies to local branch creation, naming, sync, and closeout behavior for repository work.
- Applies to bounded branch use for traced initiatives, durable task work, and multi-commit changes.
- Does not replace commit-message policy, hosted GitHub pull-request governance, or broader release-management policy.

## Use When
- Starting non-trivial work that should not land directly on `main`.
- Deciding how to name a branch for an initiative, task, fix, docs change, or other bounded change stream.
- Preparing a local branch for review, closeout, or merge.

## Related Standards and Sources
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): local git workflow should reinforce small, modular, synchronized changes instead of broad mixed-purpose branches.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): branch workflow must hand off cleanly into commit-closeout behavior without duplicating commit-message policy.
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md): hosted issue and pull-request rules remain separate from local branch naming and local history maintenance.
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md): non-trivial work should use bounded branches and explicit task handling instead of ad hoc long-lived local changes.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traced work should keep branch names easy to map back to stable initiative or task concepts.

## Guidance
- Create a branch for non-trivial work when any of these are true:
  - the work is expected to span multiple commits or sessions
  - the work belongs to a traced initiative
  - the work will likely require review, handoff, or later coordination
  - the work changes code plus governed companion docs, indexes, schemas, or standards
- Use the branch naming form `<kind>/<slug>`.
- Approved branch kinds are:
  - `initiative`
  - `feature`
  - `fix`
  - `docs`
  - `chore`
  - `task`
  - `spike`
  - `release`
- Use lower-case ASCII kebab-case for the `<slug>`.
- Keep the slug readable and stable for the bounded change stream. Prefer `core-export-readiness-and-optimization` over opaque ticket-only names.
- For traced work, align the branch slug with the initiative or task concept, but do not copy the full `trace.` or `task.` identifier into the branch name.
- Do not encode mutable metadata such as owner, status, date, or priority into the branch name.
- Start new work branches from the current `main` branch unless the work intentionally continues an active bounded branch.
- Keep one primary bounded concern per branch. Split unrelated changes into separate branches instead of stacking them indefinitely.
- Prefer rebasing or fast-forwarding local work onto `main` instead of creating routine merge commits from `main` into working branches.
- Before closeout, sync the branch with the current `main`, resolve conflicts locally, and rerun the relevant validation for the touched surfaces.
- Avoid rewriting already shared branch history unless the collaborators on that branch have explicitly coordinated the rewrite.
- Delete local branches after merge or closeout when they are no longer needed.

## Structure or Data Model
### Branch naming pattern
| Element | Requirement | Notes |
|---|---|---|
| `kind` | Required | Must be one of the approved branch kinds. |
| `slug` | Required | Lower-case ASCII kebab-case description of the bounded change stream. |
| Separator | Required | Use one `/` between kind and slug. |

### Quick examples
| Situation | Recommended Branch |
|---|---|
| New traced initiative | `initiative/core-export-readiness-and-optimization` |
| Bounded feature slice | `feature/registry-backed-command-surface` |
| Bug fix | `fix/task-index-trace-filter` |
| Docs-only change | `docs/git-workflow-standard` |
| Narrow task branch | `task/repo-ops-boundary-split` |

## Process or Workflow
1. Decide whether the work crosses the durable-task threshold or otherwise needs a bounded branch.
2. Start from `main` and create a branch using an approved kind and readable kebab-case slug.
3. Keep commits and changed surfaces aligned to the branch's bounded concern.
4. Rebase or fast-forward from `main` locally when the branch needs the latest base state.
5. Before review or closeout, verify the branch is still bounded, synced, and validated.
6. Hand off to the hosted pull-request flow only after the local branch is ready for that transition.

## Validation
- Reviewers should reject branch names that do not follow `<kind>/<slug>` or that encode mutable status or owner metadata.
- Non-trivial work should not proceed indefinitely on `main` without a bounded branch.
- Branches should not accumulate unrelated initiative work that belongs in separate change streams.
- Branch closeout should not skip the local sync and validation pass before hosted review or merge.

## Change Control
- Update this standard when the repository changes its branch naming scheme, approved branch kinds, or local sync expectations.
- Update [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md), [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md), and related workflow guidance in the same change set when the local git workflow contract changes materially.

## References
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)

## Updated At
- `2026-03-10T04:28:34Z`
