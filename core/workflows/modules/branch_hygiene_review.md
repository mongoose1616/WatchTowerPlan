# Branch Hygiene Review Workflow

## Purpose
Use this workflow to evaluate whether local branches and temporary worktrees are still active landing paths, and to apply or defer cleanup explicitly using the repository-standard old-state rules.

## Use When
- A task asks for stale-branch review, worktree cleanup, or explicit branch hygiene.
- Closeout, review, or repo maintenance needs a consistent decision about whether local branch state should be kept, merged, deleted, or removed.
- You want the repository-standard automation path instead of ad hoc git cleanup commands.

## Inputs
- Repo root or current working tree path
- Current branch and worktree state
- Requested cleanup boundary or maintenance scope
- Current base branch or explicit base ref
- Any known defer reasons, handoff state, owner, or supersession context
- [git_workflow_standard.md](/core/docs/standards/engineering/git_workflow_standard.md)
- [watchtower_core_git_hygiene.md](/core/docs/commands/core_python/watchtower_core_git_hygiene.md)

## Workflow
1. Resolve the cleanup scope.
   - Identify the repo root, current branch, current worktree, and the base ref that should govern merge-state comparisons.
   - Confirm whether the goal is read-only review, same-session cleanup, or explicit defer recording.
2. Run the old-state evaluation.
   - Use `uv run watchtower-core git hygiene --format json` or the equivalent repository-local invocation path.
   - Review branch and worktree evaluation records for merge state, unique work, dirtiness, inactivity, supersession, and defer metadata.
3. Decide whether cleanup can be automated safely.
   - Apply only the conservative actions already marked safe by the command, or keep the run read-only when review is still needed.
   - Do not override protected base-branch behavior or remove dirty worktrees implicitly.
4. Record remaining decisions explicitly.
   - When a branch or worktree is kept, record whether it stays active, needs manual review, or is deferred for handoff, comparison, or recovery reasons.
   - When cleanup is deferred, carry forward the explicit reason, owner, or next boundary rather than leaving local residue unexplained.
5. Recheck the post-action state when cleanup was applied.
   - Confirm the resulting local branch and worktree state matches the intended closeout or maintenance boundary.
   - Escalate to commit closeout, review, or follow-up work when cleanup results change the next task boundary.

## Data Structure
- Resolved repo root and base ref
- Branch and worktree evaluation records
- Applied cleanup actions, if any
- Deferred cleanup reasons and ownership when any state remains intentionally
- Post-action status and next workflow boundary

## Outputs
- Explicit keep, review, delete, or remove decisions for local branches and worktrees
- Applied conservative cleanup actions when in scope
- Explicit defer reasons or ownership for any local state intentionally retained
- A clear post-cleanup handoff boundary for closeout, review, or further implementation

## Done When
- The local branch and worktree state has been evaluated with the repository-standard old-state rules.
- Any cleanup that was safe and in scope has either been applied or intentionally deferred.
- Remaining local branch or worktree residue has an explicit reason instead of an implicit assumption.
- The next workflow boundary after cleanup is clear.
