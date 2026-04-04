---
id: "std.engineering.git_workflow"
title: "Git Workflow Standard"
summary: "This standard defines repository-standard local git workflow behavior, including origin-aware branch naming, branch lifecycle, and local sync expectations for human and assistant contributors."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "git_workflow"
owner: "repository_maintainer"
updated_at: "2026-04-04T22:10:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/docs/standards/engineering/git_commit_standard.md"
  - "core/workflows/modules/commit_closeout.md"
aliases:
  - "git workflow"
  - "branch naming"
  - "branch lifecycle"
---

# Git Workflow Standard

## Summary
This standard defines repository-standard local git workflow behavior, including origin-aware branch naming, branch lifecycle, and local sync expectations for human and assistant contributors.

## Purpose
- Keep local git behavior predictable enough for humans and agents to collaborate without hidden branch conventions.
- Make branch names readable, bounded, and easy to relate back to the originating repo or project path plus the change intent.
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
| `origin_context` | Required | Lower-case ASCII repo, pack, or project path context. Collapse multi-segment source paths with `--`. |
| `slug` | Required | Lower-case ASCII kebab-case description of the bounded change stream. Start with the target surface when the origin context points to another repo or pack. |
| Separator | Required | Use one `/` between `kind`, `origin_context`, and `slug`. |

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
5. Before review or closeout, verify the branch is still bounded, synced, and validated.
6. Hand off to the hosted pull-request flow only after the local branch is ready for that transition.

## Operationalization
- `Modes`: `workflow`; `documentation`
- `Operational Surfaces`: `core/workflows/modules/commit_closeout.md`; `core/docs/references/github_collaboration_reference.md`; `core/docs/references/conventional_commits_reference.md`

## Validation
- Reviewers should reject branch names that do not follow `<kind>/<origin_context>/<slug>` or that encode mutable status, owner, or ephemeral agent metadata.
- Cross-repository or cross-pack branches should not omit the source repo or durable project-path context from `<origin_context>`.
- Non-trivial work should not proceed indefinitely on `main` without a bounded branch.
- Branches should not accumulate unrelated initiative work that belongs in separate change streams.
- Branch closeout should not skip the local sync and validation pass before hosted review or merge.

## Change Control
- Update this standard when the repository changes its branch naming scheme, approved branch kinds, or local sync expectations.
- Update [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md) and any companion hosted-collaboration, task-threshold, or traceability guidance in the same change set when the local git workflow contract changes materially.

## References
- [engineering_best_practices_standard.md](/core/docs/standards/engineering/engineering_best_practices_standard.md)
- [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md)
- Pack-owned collaboration, task-threshold, and traceability standards under `<pack>/docs/standards/governance/`

## Updated At
- `2026-04-04T22:10:00Z`
