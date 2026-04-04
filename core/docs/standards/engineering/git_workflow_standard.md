---
id: "std.engineering.git_workflow"
title: "Git Workflow Standard"
summary: "This standard defines repository-standard local git workflow behavior, including origin-aware branch naming, branch and temporary-worktree lifecycle, and local sync expectations for human and assistant contributors."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "git_workflow"
owner: "repository_maintainer"
updated_at: "2026-04-04T22:50:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/docs/standards/engineering/git_commit_standard.md"
  - "core/workflows/modules/commit_closeout.md"
aliases:
  - "git workflow"
  - "branch naming"
  - "branch lifecycle"
  - "worktree lifecycle"
---

# Git Workflow Standard

## Summary
This standard defines repository-standard local git workflow behavior, including origin-aware branch naming, branch and temporary-worktree lifecycle, and local sync expectations for human and assistant contributors.

## Purpose
- Keep local git behavior predictable enough for humans and agents to collaborate without hidden branch conventions.
- Make branch names readable, bounded, and easy to relate back to the originating repo or project path plus the change intent.
- Reduce merge noise, orphaned worktrees, and closeout ambiguity by preferring clear branch scope, explicit cleanup, and linear local history.

## Scope
- Applies to local branch and temporary-worktree creation, naming, sync, and closeout behavior for repository work.
- Applies to bounded branch use for traced initiatives, durable task work, and multi-commit changes.
- Does not replace commit-message policy, hosted GitHub pull-request governance, or broader release-management policy.

## Use When
- Starting non-trivial work that should not land directly on `main`.
- Deciding how to name a branch for an initiative, task, fix, docs change, or other bounded change stream.
- Preparing a local branch or temporary worktree for review, closeout, merge, or cleanup.

## Related Standards and Sources
- [engineering_best_practices_standard.md](/core/docs/standards/engineering/engineering_best_practices_standard.md): local git workflow should reinforce small, modular, synchronized changes instead of broad mixed-purpose branches.
- [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md): branch workflow must hand off cleanly into commit-closeout behavior without duplicating commit-message policy.
- Pack-owned collaboration, task-threshold, and traceability standards under `<pack>/docs/standards/governance/`: hosted review rules, durable task handling, and trace metadata should stay aligned with local branch practice when a pack publishes those governance surfaces.

## Guidance
- Create a branch for non-trivial work when any of these are true:
  - the work is expected to span multiple commits or sessions
  - the work belongs to a traced initiative
  - the work will likely require review, handoff, or later coordination
  - the work changes code plus governed companion docs, indexes, schemas, or standards
- Use the branch naming form `<kind>/<origin_context>/<slug>`.
- Approved branch kinds are:
  - `initiative`
  - `feature`
  - `fix`
  - `docs`
  - `chore`
  - `task`
  - `spike`
  - `release`
- Use lower-case ASCII kebab-case for the `<origin_context>` and `<slug>`. When the source context is naturally multi-segment, collapse the durable path segments with `--`.
- `<origin_context>` must identify the durable repo, pack, or project path that launched the branch.
- For work started from the current repository, use the nearest durable local ownership path such as `core`, `plan`, or `plan--projects--watchtower` instead of a generic value like `local`.
- For work started from another repository or pack, prefix the source repo or pack root, such as `watchtoweroversight--core` or `watchtoweroversight--projects--customer-audit`.
- When `<origin_context>` names another repository or pack, start the slug with the primary target surface in the current repository, such as `core-...` or `plan-...`, so the branch still reads clearly after checkout.
- Keep the slug readable and stable for the bounded change stream. Prefer `core-export-readiness-and-optimization` over opaque ticket-only names.
- For traced work, align the branch slug with the initiative or task concept, but do not copy the full `trace.` or `task.` identifier into the branch name.
- Do not encode mutable metadata such as owner, status, date, priority, or ephemeral agent instance IDs into the branch name.
- Start new work branches from the current `main` branch unless the work intentionally continues an active bounded branch.
- Use a temporary worktree only when it materially reduces context switching, conflict risk, or concurrent-change interference for one bounded change stream.
- Bind one bounded branch to one temporary worktree. Do not keep reusing the same auxiliary worktree for unrelated change streams.
- Keep one primary bounded concern per branch. Split unrelated changes into separate branches instead of stacking them indefinitely.
- Prefer rebasing or fast-forwarding local work onto `main` instead of creating routine merge commits from `main` into working branches.
- Before closeout, sync the branch with the current `main`, resolve conflicts locally, and rerun the relevant validation for the touched surfaces.
- Avoid rewriting already shared branch history unless the collaborators on that branch have explicitly coordinated the rewrite.
- Run an explicit human or agent old-state evaluation before deciding that a bounded branch or temporary worktree should be merged, retained, or deleted.
- Treat a bounded branch as `old` when that evaluation shows it is no longer the active landing path and at least one of these is true:
  - its tip is already merged into `main`
  - another branch or commit range has superseded the same bounded intent
  - it has had no new commits for 14 calendar days and there is no active review, handoff, staged local work, or recorded defer reason
- Treat a temporary worktree as `old` when that evaluation shows it is no longer needed for active local execution and at least one of these is true:
  - its bound branch is `old`
  - another worktree or branch now owns the same bounded change stream
  - it has had no new commits or staged changes for 14 calendar days and there is no recorded defer reason
- Delete local branches and remove temporary worktrees after merge, closeout, abandonment, or supersession when they are no longer needed.
- If branch or worktree cleanup must be deferred because review, comparison, or handoff still depends on that local state, record the reason explicitly instead of leaving the residue behind silently.
- Use `watchtower-core git hygiene` when you want the repository-standard old-state evaluation and conservative local cleanup behavior applied consistently by automation.

## Structure or Data Model
### Branch naming pattern
| Element | Requirement | Notes |
|---|---|---|
| `kind` | Required | Must be one of the approved branch kinds. |
| `origin_context` | Required | Lower-case ASCII repo, pack, or project path context. Collapse multi-segment source paths with `--`. |
| `slug` | Required | Lower-case ASCII kebab-case description of the bounded change stream. Start with the target surface when the origin context points to another repo or pack. |
| Separator | Required | Use one `/` between `kind`, `origin_context`, and `slug`. |

### Cleanup expectations
| Surface | Requirement | Notes |
|---|---|---|
| Old-state evaluation | Run it before keeping, merging, or deleting branch-local state. | The evaluator should inspect merge state, unique remaining diff, staged or uncommitted work, last activity age, active review or handoff state, and explicit defer reasons. |
| Old local branch | Treat it as ready for merge-or-delete review. | A branch is `old` once the evaluation shows it is no longer the active landing path and it is merged, superseded, or 14 days inactive without active review, staged work, or a defer reason. |
| Temporary worktree | Remove it after merge, abandonment, supersession, or other completed closeout. | A temporary worktree is `old` once the evaluation shows it is no longer needed and it is tied to an old branch, superseded, or 14 days inactive without staged work or a defer reason. |
| Deferred cleanup | Record the explicit reason and next owner or boundary. | Do not leave branch or worktree residue without explanation. |

### Old-state evaluation questions
| Signal | Branch Question | Worktree Question |
|---|---|---|
| Merge state | Is the branch tip already reachable from `main`? | Is the bound branch already merged, deleted, or otherwise closed? |
| Unique work | Does the branch still carry unique diff worth landing? | Does the worktree still hold staged or uncommitted work not captured elsewhere? |
| Supersession | Has another branch, commit range, or merged change already replaced this intent? | Has another worktree or branch taken over the same bounded change stream? |
| Activity | Has there been a new commit in the last 14 calendar days? | Has there been a new commit or staged change in the last 14 calendar days? |
| Coordination | Is there active review, handoff, recovery use, or a recorded defer reason? | Is there an explicit reason to keep this worktree for review, comparison, or recovery? |

### Quick examples
| Situation | Recommended Branch |
|---|---|
| New traced initiative in the local plan workspace | `initiative/plan--projects--watchtower/core-export-readiness-and-optimization` |
| Bounded feature slice in shared core | `feature/core/registry-backed-command-surface` |
| Bug fix driven from another repository | `fix/watchtoweroversight--projects--customer-audit/core-task-index-trace-filter` |
| Docs-only change in local plan docs | `docs/plan--docs/coordination-tracker-guidance` |
| Narrow task branch | `task/plan--tasks/pack-python-boundary-split` |

## Process or Workflow
1. Decide whether the work crosses the durable-task threshold or otherwise needs a bounded branch.
2. Start from `main` and create a branch using an approved kind, a durable origin context, and a readable kebab-case slug.
3. Keep commits and changed surfaces aligned to the branch's bounded concern.
4. Rebase or fast-forward from `main` locally when the branch needs the latest base state.
5. Before review or closeout, verify the branch and any temporary worktree are still bounded, synced, and validated.
6. Hand off to the hosted pull-request flow only after the local branch or temporary worktree is ready for that transition.
7. After merge, abandonment, or other completed local closeout, run the old-state evaluation and merge-or-delete any `old` bounded branch plus remove any `old` temporary worktree, or record the explicit defer reason.

## Operationalization
- `Modes`: `workflow`; `documentation`; `automation`
- `Operational Surfaces`: `core/workflows/modules/branch_hygiene_review.md`; `core/workflows/modules/commit_closeout.md`; `core/docs/commands/core_python/watchtower_core_git_hygiene.md`; `core/docs/references/github_collaboration_reference.md`; `core/docs/references/conventional_commits_reference.md`

## Validation
- Reviewers should reject branch names that do not follow `<kind>/<origin_context>/<slug>` or that encode mutable status, owner, or ephemeral agent metadata.
- Cross-repository or cross-pack branches should not omit the source repo or durable project-path context from `<origin_context>`.
- Non-trivial work should not proceed indefinitely on `main` without a bounded branch.
- Branches should not accumulate unrelated initiative work that belongs in separate change streams.
- Old bounded branches should not remain unreviewed indefinitely once the evaluation shows they are merged, superseded, or 14 days inactive without active review, staged work, or a defer reason.
- Temporary worktrees should not linger after their bounded change stream has been merged, abandoned, superseded, or otherwise closed unless a defer reason is recorded explicitly.
- Old temporary worktrees should not remain unreviewed indefinitely once the evaluation shows they are tied to an old branch, superseded, or 14 days inactive without staged work or a defer reason.
- Branch closeout should not skip the local sync and validation pass before hosted review or merge.
- Branch or worktree closeout should not leave cleanup status implicit.

## Change Control
- Update this standard when the repository changes its branch naming scheme, approved branch kinds, or local sync expectations.
- Update [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md) and any companion hosted-collaboration, task-threshold, or traceability guidance in the same change set when the local git workflow contract changes materially.

## References
- [engineering_best_practices_standard.md](/core/docs/standards/engineering/engineering_best_practices_standard.md)
- [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md)
- Pack-owned collaboration, task-threshold, and traceability standards under `<pack>/docs/standards/governance/`

## Updated At
- `2026-04-04T22:50:00Z`
