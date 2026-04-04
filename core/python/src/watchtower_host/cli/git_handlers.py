"""Runtime handlers for local git hygiene commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_command_error, _emit_detail_result
from watchtower_core.telemetry import telemetry_operation
from watchtower_core.utils.git_hygiene import GitHygieneRequest, GitHygieneResult, GitHygieneService


def _run_git_hygiene(args: argparse.Namespace) -> int:
    command_name = "watchtower-core git hygiene"
    try:
        with telemetry_operation(
            "git",
            "hygiene",
            attributes={
                "repo_root": None if args.repo_root is None else str(args.repo_root),
                "base_ref": args.base_ref,
                "inactive_days": args.inactive_days,
                "override_path": None if args.override_path is None else str(args.override_path),
                "apply": bool(args.apply),
            },
        ):
            result = GitHygieneService().run(
                GitHygieneRequest(
                    repo_root=None if args.repo_root is None else str(args.repo_root),
                    base_ref=args.base_ref,
                    inactive_days=args.inactive_days,
                    override_path=None if args.override_path is None else str(args.override_path),
                    apply=bool(args.apply),
                )
            )
    except (OSError, ValueError) as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Git hygiene error")

    return _emit_detail_result(
        args,
        payload_factory=lambda: _build_git_hygiene_payload(command_name, result),
        render_human=lambda: _render_git_hygiene_human(result),
    )


def _build_git_hygiene_payload(
    command_name: str,
    result: GitHygieneResult,
) -> dict[str, object]:
    return {
        "command": command_name,
        "status": "ok",
        "repo_root": result.repo_root,
        "git_root": result.git_root,
        "git_common_dir": result.git_common_dir,
        "base_ref": result.base_ref,
        "inactive_days": result.inactive_days,
        "current_branch": result.current_branch,
        "current_worktree_path": result.current_worktree_path,
        "override_path": result.override_path,
        "overrides_found": result.overrides_found,
        "apply": result.apply,
        "old_branch_count": sum(1 for branch in result.branches if branch.old),
        "old_worktree_count": sum(1 for worktree in result.worktrees if worktree.old),
        "branches": [
            {
                "branch_name": branch.branch_name,
                "base_ref": branch.base_ref,
                "current": branch.current,
                "upstream": branch.upstream,
                "ahead_count": branch.ahead_count,
                "behind_count": branch.behind_count,
                "merged_into_base": branch.merged_into_base,
                "unique_commit_count": branch.unique_commit_count,
                "checked_out_in_worktree_paths": list(branch.checked_out_in_worktree_paths),
                "has_dirty_worktree": branch.has_dirty_worktree,
                "has_staged_worktree_changes": branch.has_staged_worktree_changes,
                "has_uncommitted_worktree_changes": branch.has_uncommitted_worktree_changes,
                "last_commit_at": branch.last_commit_at,
                "inactive_days": branch.inactive_days,
                "defer_reason": branch.defer_reason,
                "active_handoff": branch.active_handoff,
                "superseded_by": branch.superseded_by,
                "keep_until": branch.keep_until,
                "owner": branch.owner,
                "old": branch.old,
                "recommended_action": branch.recommended_action,
                "reasons": list(branch.reasons),
            }
            for branch in result.branches
        ],
        "worktrees": [
            {
                "worktree_path": worktree.worktree_path,
                "branch_name": worktree.branch_name,
                "head_commit": worktree.head_commit,
                "is_primary": worktree.is_primary,
                "current": worktree.current,
                "detached": worktree.detached,
                "clean": worktree.clean,
                "tracked_change_count": worktree.tracked_change_count,
                "untracked_change_count": worktree.untracked_change_count,
                "staged_change_count": worktree.staged_change_count,
                "unstaged_change_count": worktree.unstaged_change_count,
                "last_activity_at": worktree.last_activity_at,
                "inactive_days": worktree.inactive_days,
                "defer_reason": worktree.defer_reason,
                "active_handoff": worktree.active_handoff,
                "superseded_by": worktree.superseded_by,
                "keep_until": worktree.keep_until,
                "owner": worktree.owner,
                "old": worktree.old,
                "recommended_action": worktree.recommended_action,
                "reasons": list(worktree.reasons),
            }
            for worktree in result.worktrees
        ],
        "actions_applied": [
            {
                "action": action.action,
                "target": action.target,
                "status": action.status,
                "message": action.message,
            }
            for action in result.actions_applied
        ],
    }


def _render_git_hygiene_human(result: GitHygieneResult) -> None:
    print("Git hygiene review")
    print(f"Repo Root: {result.repo_root}")
    print(f"Base Ref: {result.base_ref}")
    override_status = "found" if result.overrides_found else "not found"
    print(f"Overrides: {override_status} ({result.override_path})")
    old_branches = [branch for branch in result.branches if branch.old]
    old_worktrees = [worktree for worktree in result.worktrees if worktree.old]
    print(f"Old branches: {len(old_branches)}")
    print(f"Old worktrees: {len(old_worktrees)}")

    actionable_branches = [
        branch for branch in result.branches if branch.recommended_action != "keep"
    ]
    if actionable_branches:
        print("Branch actions:")
        for branch in actionable_branches:
            print(
                f"- {branch.branch_name}: {branch.recommended_action} "
                f"({', '.join(branch.reasons) if branch.reasons else 'no reasons'})"
            )

    actionable_worktrees = [
        worktree for worktree in result.worktrees if worktree.recommended_action != "keep"
    ]
    if actionable_worktrees:
        print("Worktree actions:")
        for worktree in actionable_worktrees:
            branch_label = worktree.branch_name or "<detached>"
            print(
                f"- {worktree.worktree_path} [{branch_label}]: {worktree.recommended_action} "
                f"({', '.join(worktree.reasons) if worktree.reasons else 'no reasons'})"
            )

    if result.actions_applied:
        print("Applied actions:")
        for action in result.actions_applied:
            detail = f" ({action.message})" if action.message else ""
            print(f"- {action.action} {action.target}: {action.status}{detail}")
