"""Local branch and worktree hygiene evaluation helpers."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from watchtower_core.pack_integration.release_check import GitWorktreeEntry, inspect_git_worktree

RecommendedAction = Literal["keep", "review", "delete_branch", "remove_worktree"]


@dataclass(frozen=True, slots=True)
class GitHygieneRequest:
    """Parameters for one local git-hygiene evaluation run."""

    repo_root: str | None = None
    base_ref: str = "main"
    inactive_days: int = 14
    override_path: str | None = None
    apply: bool = False


@dataclass(frozen=True, slots=True)
class GitHygieneOverride:
    """Local-only override metadata for one branch or worktree."""

    defer_reason: str | None = None
    active_handoff: bool = False
    superseded_by: str | None = None
    keep_until: str | None = None
    owner: str | None = None


@dataclass(frozen=True, slots=True)
class GitHygieneOverrides:
    """Parsed local-only branch and worktree overrides."""

    branch_overrides: dict[str, GitHygieneOverride]
    worktree_overrides: dict[str, GitHygieneOverride]

    def branch(self, branch_name: str) -> GitHygieneOverride:
        return self.branch_overrides.get(branch_name, GitHygieneOverride())

    def worktree(self, worktree_path: str) -> GitHygieneOverride:
        return self.worktree_overrides.get(worktree_path, GitHygieneOverride())


@dataclass(frozen=True, slots=True)
class GitHygieneBranchEvaluation:
    """Evaluation record for one local branch."""

    branch_name: str
    base_ref: str
    current: bool
    upstream: str | None
    ahead_count: int | None
    behind_count: int | None
    merged_into_base: bool
    unique_commit_count: int
    checked_out_in_worktree_paths: tuple[str, ...]
    has_dirty_worktree: bool
    has_staged_worktree_changes: bool
    has_uncommitted_worktree_changes: bool
    last_commit_at: str | None
    inactive_days: int | None
    defer_reason: str | None
    active_handoff: bool
    superseded_by: str | None
    keep_until: str | None
    owner: str | None
    old: bool
    recommended_action: RecommendedAction
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GitHygieneWorktreeEvaluation:
    """Evaluation record for one local worktree."""

    worktree_path: str
    branch_name: str | None
    head_commit: str
    is_primary: bool
    current: bool
    detached: bool
    clean: bool | None
    tracked_change_count: int
    untracked_change_count: int
    staged_change_count: int
    unstaged_change_count: int
    last_activity_at: str | None
    inactive_days: int | None
    defer_reason: str | None
    active_handoff: bool
    superseded_by: str | None
    keep_until: str | None
    owner: str | None
    old: bool
    recommended_action: RecommendedAction
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GitHygieneAppliedAction:
    """One local cleanup action performed by the hygiene command."""

    action: str
    target: str
    status: Literal["applied", "skipped", "failed"]
    message: str | None = None


@dataclass(frozen=True, slots=True)
class GitHygieneResult:
    """Summary of one git-hygiene evaluation run."""

    repo_root: str
    git_root: str
    git_common_dir: str
    base_ref: str
    inactive_days: int
    current_branch: str | None
    current_worktree_path: str
    override_path: str
    overrides_found: bool
    apply: bool
    branches: tuple[GitHygieneBranchEvaluation, ...]
    worktrees: tuple[GitHygieneWorktreeEvaluation, ...]
    actions_applied: tuple[GitHygieneAppliedAction, ...] = ()


@dataclass(frozen=True, slots=True)
class _BranchState:
    """Internal git branch state derived from local refs."""

    branch_name: str
    commit_sha: str
    upstream: str | None
    subject: str
    last_commit_at: datetime | None


@dataclass(frozen=True, slots=True)
class _WorktreeState:
    """Internal git worktree state derived from porcelain output."""

    worktree_path: Path
    head_commit: str
    branch_name: str | None
    detached: bool


class GitHygieneService:
    """Evaluate and optionally apply conservative local branch and worktree cleanup."""

    def run(self, request: GitHygieneRequest) -> GitHygieneResult:
        resolved_repo_root = _resolve_git_root(Path(request.repo_root or Path.cwd()))
        resolved_base_ref = _resolve_base_ref(resolved_repo_root, request.base_ref)
        git_common_dir = _resolve_git_common_dir(resolved_repo_root)
        override_path = _resolve_override_path(git_common_dir, request.override_path)
        overrides = _load_overrides(override_path)
        now = datetime.now(UTC)

        if not request.apply:
            return self._evaluate(
                resolved_repo_root,
                resolved_base_ref,
                request.inactive_days,
                override_path,
                overrides,
                now,
                (),
                apply=False,
            )

        initial = self._evaluate(
            resolved_repo_root,
            resolved_base_ref,
            request.inactive_days,
            override_path,
            overrides,
            now,
            (),
            apply=True,
        )
        actions: list[GitHygieneAppliedAction] = []
        actions.extend(self._apply_worktree_actions(resolved_repo_root, initial.worktrees))

        after_worktrees = self._evaluate(
            resolved_repo_root,
            resolved_base_ref,
            request.inactive_days,
            override_path,
            overrides,
            now,
            tuple(actions),
            apply=True,
        )
        actions.extend(self._apply_branch_actions(resolved_repo_root, after_worktrees.branches))

        return self._evaluate(
            resolved_repo_root,
            resolved_base_ref,
            request.inactive_days,
            override_path,
            overrides,
            now,
            tuple(actions),
            apply=True,
        )

    def _evaluate(
        self,
        repo_root: Path,
        base_ref: str,
        inactive_days: int,
        override_path: Path,
        overrides: GitHygieneOverrides,
        now: datetime,
        actions_applied: tuple[GitHygieneAppliedAction, ...],
        *,
        apply: bool,
    ) -> GitHygieneResult:
        current_branch = _current_branch(repo_root)
        current_worktree_path = str(repo_root)
        branch_states = _list_local_branches(repo_root)
        worktree_states = _list_worktrees(repo_root)
        branch_lookup = {state.branch_name: state for state in branch_states}
        protected_branch_names = _protected_branch_names(base_ref)

        worktree_evaluations_by_path: dict[str, GitHygieneWorktreeEvaluation] = {}
        bound_worktrees_by_branch: dict[str, list[GitHygieneWorktreeEvaluation]] = {}
        for state in worktree_states:
            branch_state = (
                branch_lookup.get(state.branch_name) if state.branch_name is not None else None
            )
            evaluation = _evaluate_worktree(
                repo_root=repo_root,
                worktree_state=state,
                branch_state=branch_state,
                override=overrides.worktree(str(state.worktree_path)),
                current_worktree_path=current_worktree_path,
                inactive_days=inactive_days,
                now=now,
                branch_old=None,
            )
            worktree_evaluations_by_path[evaluation.worktree_path] = evaluation
            if state.branch_name is not None:
                bound_worktrees_by_branch.setdefault(state.branch_name, []).append(evaluation)

        branch_evaluations = tuple(
            _evaluate_branch(
                repo_root=repo_root,
                branch_state=branch_state,
                base_ref=base_ref,
                current_branch=current_branch,
                protected_branch_names=protected_branch_names,
                override=overrides.branch(branch_state.branch_name),
                bound_worktrees=tuple(bound_worktrees_by_branch.get(branch_state.branch_name, ())),
                inactive_days=inactive_days,
                now=now,
            )
            for branch_state in branch_states
        )
        branch_old_by_name = {
            evaluation.branch_name: evaluation.old for evaluation in branch_evaluations
        }
        worktree_evaluations = tuple(
            _evaluate_worktree(
                repo_root=repo_root,
                worktree_state=state,
                branch_state=(
                    branch_lookup.get(state.branch_name)
                    if state.branch_name is not None
                    else None
                ),
                override=overrides.worktree(str(state.worktree_path)),
                current_worktree_path=current_worktree_path,
                inactive_days=inactive_days,
                now=now,
                branch_old=(
                    branch_old_by_name.get(state.branch_name)
                    if state.branch_name is not None
                    else None
                ),
            )
            for state in worktree_states
        )

        return GitHygieneResult(
            repo_root=str(repo_root),
            git_root=str(repo_root),
            git_common_dir=str(_resolve_git_common_dir(repo_root)),
            base_ref=base_ref,
            inactive_days=inactive_days,
            current_branch=current_branch,
            current_worktree_path=current_worktree_path,
            override_path=str(override_path),
            overrides_found=override_path.is_file(),
            apply=apply,
            branches=branch_evaluations,
            worktrees=worktree_evaluations,
            actions_applied=actions_applied,
        )

    def _apply_worktree_actions(
        self,
        repo_root: Path,
        worktrees: tuple[GitHygieneWorktreeEvaluation, ...],
    ) -> list[GitHygieneAppliedAction]:
        actions: list[GitHygieneAppliedAction] = []
        for worktree in worktrees:
            if worktree.recommended_action != "remove_worktree":
                continue
            if worktree.is_primary:
                actions.append(
                    GitHygieneAppliedAction(
                        action="remove_worktree",
                        target=worktree.worktree_path,
                        status="skipped",
                        message="Primary worktree is never auto-removed.",
                    )
                )
                continue
            if worktree.clean is False:
                actions.append(
                    GitHygieneAppliedAction(
                        action="remove_worktree",
                        target=worktree.worktree_path,
                        status="skipped",
                        message="Dirty worktree requires explicit review before removal.",
                    )
                )
                continue
            completed = _run_git(
                repo_root,
                "worktree",
                "remove",
                worktree.worktree_path,
                allow_failure=True,
            )
            if completed.returncode == 0:
                actions.append(
                    GitHygieneAppliedAction(
                        action="remove_worktree",
                        target=worktree.worktree_path,
                        status="applied",
                    )
                )
                continue
            actions.append(
                GitHygieneAppliedAction(
                    action="remove_worktree",
                    target=worktree.worktree_path,
                    status="failed",
                    message=completed.stderr.strip() or "Unable to remove worktree.",
                )
            )
        return actions

    def _apply_branch_actions(
        self,
        repo_root: Path,
        branches: tuple[GitHygieneBranchEvaluation, ...],
    ) -> list[GitHygieneAppliedAction]:
        actions: list[GitHygieneAppliedAction] = []
        for branch in branches:
            if branch.recommended_action != "delete_branch":
                continue
            completed = _run_git(
                repo_root,
                "branch",
                "-d",
                branch.branch_name,
                allow_failure=True,
            )
            if completed.returncode == 0:
                actions.append(
                    GitHygieneAppliedAction(
                        action="delete_branch",
                        target=branch.branch_name,
                        status="applied",
                    )
                )
                continue
            actions.append(
                GitHygieneAppliedAction(
                    action="delete_branch",
                    target=branch.branch_name,
                    status="failed",
                    message=completed.stderr.strip() or "Unable to delete branch.",
                )
            )
        return actions


def _evaluate_branch(
    *,
    repo_root: Path,
    branch_state: _BranchState,
    base_ref: str,
    current_branch: str | None,
    protected_branch_names: set[str],
    override: GitHygieneOverride,
    bound_worktrees: tuple[GitHygieneWorktreeEvaluation, ...],
    inactive_days: int,
    now: datetime,
) -> GitHygieneBranchEvaluation:
    protected_branch = branch_state.branch_name in protected_branch_names
    merged_into_base = _branch_merged_into_base(repo_root, branch_state.branch_name, base_ref)
    unique_commit_count = _branch_unique_commit_count(repo_root, base_ref, branch_state.branch_name)
    ahead_count, behind_count = _upstream_divergence(
        repo_root,
        branch_state.branch_name,
        branch_state.upstream,
    )
    has_dirty_worktree = any(worktree.clean is False for worktree in bound_worktrees)
    has_staged_changes = any(worktree.staged_change_count > 0 for worktree in bound_worktrees)
    has_uncommitted_changes = any(
        worktree.unstaged_change_count > 0 or worktree.untracked_change_count > 0
        for worktree in bound_worktrees
    )
    branch_inactive_days = _inactive_day_count(branch_state.last_commit_at, now)
    defer_active = _defer_active(override, now)
    reasons: list[str] = []
    if merged_into_base:
        reasons.append("merged_into_base")
    if override.superseded_by is not None:
        reasons.append(f"superseded_by:{override.superseded_by}")
    if branch_inactive_days is not None and branch_inactive_days >= inactive_days:
        reasons.append(f"inactive_days:{branch_inactive_days}")
    if has_dirty_worktree:
        reasons.append("bound_worktree_dirty")
    if has_staged_changes:
        reasons.append("bound_worktree_staged_changes")
    if has_uncommitted_changes:
        reasons.append("bound_worktree_uncommitted_changes")
    if defer_active:
        reasons.append("defer_active")
    if protected_branch:
        reasons.append("protected_branch")

    old = False
    if not protected_branch and not defer_active:
        if merged_into_base or override.superseded_by is not None:
            old = True
        elif (
            branch_inactive_days is not None
            and branch_inactive_days >= inactive_days
            and not has_staged_changes
            and not has_uncommitted_changes
            and not has_dirty_worktree
            and not override.active_handoff
        ):
            old = True

    recommended_action: RecommendedAction = "keep"
    if current_branch == branch_state.branch_name:
        recommended_action = "keep"
    elif protected_branch:
        recommended_action = "keep"
    elif defer_active:
        recommended_action = "keep"
    elif (merged_into_base or unique_commit_count == 0) and not bound_worktrees:
        recommended_action = "delete_branch"
    elif old:
        recommended_action = "review"

    return GitHygieneBranchEvaluation(
        branch_name=branch_state.branch_name,
        base_ref=base_ref,
        current=current_branch == branch_state.branch_name,
        upstream=branch_state.upstream,
        ahead_count=ahead_count,
        behind_count=behind_count,
        merged_into_base=merged_into_base,
        unique_commit_count=unique_commit_count,
        checked_out_in_worktree_paths=tuple(
            worktree.worktree_path for worktree in bound_worktrees
        ),
        has_dirty_worktree=has_dirty_worktree,
        has_staged_worktree_changes=has_staged_changes,
        has_uncommitted_worktree_changes=has_uncommitted_changes,
        last_commit_at=_format_datetime(branch_state.last_commit_at),
        inactive_days=branch_inactive_days,
        defer_reason=override.defer_reason,
        active_handoff=override.active_handoff,
        superseded_by=override.superseded_by,
        keep_until=override.keep_until,
        owner=override.owner,
        old=old,
        recommended_action=recommended_action,
        reasons=tuple(reasons),
    )


def _evaluate_worktree(
    *,
    repo_root: Path,
    worktree_state: _WorktreeState,
    branch_state: _BranchState | None,
    override: GitHygieneOverride,
    current_worktree_path: str,
    inactive_days: int,
    now: datetime,
    branch_old: bool | None,
) -> GitHygieneWorktreeEvaluation:
    inspection = inspect_git_worktree(worktree_state.worktree_path)
    staged_change_count = sum(
        1 for entry in inspection.entries if _is_staged_change(entry.raw_status)
    )
    unstaged_change_count = sum(
        1 for entry in inspection.entries if _is_unstaged_change(entry.raw_status)
    )
    last_activity_at = _latest_worktree_activity(
        worktree_state.worktree_path,
        inspection.entries,
        branch_state.last_commit_at if branch_state is not None else None,
    )
    worktree_inactive_days = _inactive_day_count(last_activity_at, now)
    defer_active = _defer_active(override, now)

    reasons: list[str] = []
    if branch_old:
        reasons.append("bound_branch_old")
    if override.superseded_by is not None:
        reasons.append(f"superseded_by:{override.superseded_by}")
    if worktree_inactive_days is not None and worktree_inactive_days >= inactive_days:
        reasons.append(f"inactive_days:{worktree_inactive_days}")
    if inspection.clean is False:
        reasons.append("worktree_dirty")
    if staged_change_count:
        reasons.append("staged_changes_present")
    if defer_active:
        reasons.append("defer_active")

    old = False
    if not defer_active:
        if branch_old or override.superseded_by is not None:
            old = True
        elif worktree_inactive_days is not None and worktree_inactive_days >= inactive_days:
            old = True

    recommended_action: RecommendedAction = "keep"
    if worktree_state.worktree_path.as_posix() == current_worktree_path:
        recommended_action = "keep"
    elif defer_active:
        recommended_action = "keep"
    elif old and not worktree_state.worktree_path.samefile(repo_root) and inspection.clean is True:
        recommended_action = "remove_worktree"
    elif old:
        recommended_action = "review"

    return GitHygieneWorktreeEvaluation(
        worktree_path=str(worktree_state.worktree_path),
        branch_name=worktree_state.branch_name,
        head_commit=worktree_state.head_commit,
        is_primary=worktree_state.worktree_path == repo_root,
        current=worktree_state.worktree_path.as_posix() == current_worktree_path,
        detached=worktree_state.detached,
        clean=inspection.clean,
        tracked_change_count=inspection.tracked_change_count,
        untracked_change_count=inspection.untracked_change_count,
        staged_change_count=staged_change_count,
        unstaged_change_count=unstaged_change_count,
        last_activity_at=_format_datetime(last_activity_at),
        inactive_days=worktree_inactive_days,
        defer_reason=override.defer_reason,
        active_handoff=override.active_handoff,
        superseded_by=override.superseded_by,
        keep_until=override.keep_until,
        owner=override.owner,
        old=old,
        recommended_action=recommended_action,
        reasons=tuple(reasons),
    )


def _resolve_git_root(start_path: Path) -> Path:
    completed = _run_git(start_path, "rev-parse", "--show-toplevel", allow_failure=True)
    if completed.returncode != 0:
        raise ValueError(
            completed.stderr.strip()
            or f"{start_path} is not inside a git worktree."
        )
    root = completed.stdout.strip()
    if not root:
        raise ValueError(f"{start_path} is not inside a git worktree.")
    return Path(root).resolve()


def _resolve_git_common_dir(repo_root: Path) -> Path:
    completed = _run_git(repo_root, "rev-parse", "--git-common-dir")
    common_dir = completed.stdout.strip()
    if not common_dir:
        raise ValueError("Unable to resolve git common directory.")
    candidate = Path(common_dir)
    if not candidate.is_absolute():
        candidate = (repo_root / candidate).resolve()
    return candidate.resolve()


def _resolve_base_ref(repo_root: Path, requested_base_ref: str) -> str:
    candidates = [requested_base_ref]
    if "/" not in requested_base_ref:
        candidates.append(f"origin/{requested_base_ref}")
    for candidate in candidates:
        completed = _run_git(repo_root, "rev-parse", "--verify", candidate, allow_failure=True)
        if completed.returncode == 0:
            return candidate
    raise ValueError(
        f"Unable to resolve base ref {requested_base_ref!r} as a local or remote-tracking ref."
    )


def _resolve_override_path(git_common_dir: Path, override_path: str | None) -> Path:
    if override_path is None:
        return git_common_dir / "watchtower" / "git_hygiene_overrides.json"
    candidate = Path(override_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (Path.cwd() / candidate).resolve()


def _protected_branch_names(base_ref: str) -> set[str]:
    protected = {base_ref}
    if base_ref.startswith("refs/heads/"):
        protected.add(base_ref.removeprefix("refs/heads/"))
    if base_ref.startswith("refs/remotes/"):
        protected.add(base_ref.rsplit("/", maxsplit=1)[-1])
    if "/" in base_ref:
        protected.add(base_ref.rsplit("/", maxsplit=1)[-1])
    return {name for name in protected if name}


def _load_overrides(override_path: Path) -> GitHygieneOverrides:
    if not override_path.exists():
        return GitHygieneOverrides(branch_overrides={}, worktree_overrides={})
    document = json.loads(override_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"{override_path} must contain a JSON object.")
    branch_section = document.get("branches", {})
    worktree_section = document.get("worktrees", {})
    if not isinstance(branch_section, dict) or not isinstance(worktree_section, dict):
        raise ValueError(f"{override_path} must define object-valued branches and worktrees.")
    return GitHygieneOverrides(
        branch_overrides={
            str(key): _parse_override_entry(value, override_path, f"branches.{key}")
            for key, value in branch_section.items()
        },
        worktree_overrides={
            str(Path(str(key)).resolve()): _parse_override_entry(
                value,
                override_path,
                f"worktrees.{key}",
            )
            for key, value in worktree_section.items()
        },
    )


def _parse_override_entry(
    value: object,
    override_path: Path,
    field_name: str,
) -> GitHygieneOverride:
    if not isinstance(value, dict):
        raise ValueError(f"{override_path} field {field_name} must contain an object.")
    defer_reason = _optional_string(value.get("defer_reason"), override_path, field_name)
    active_handoff = _optional_bool(value.get("active_handoff"), override_path, field_name)
    superseded_by = _optional_string(value.get("superseded_by"), override_path, field_name)
    keep_until = _optional_string(value.get("keep_until"), override_path, field_name)
    owner = _optional_string(value.get("owner"), override_path, field_name)
    if keep_until is not None:
        _parse_datetime(keep_until)
    return GitHygieneOverride(
        defer_reason=defer_reason,
        active_handoff=active_handoff or False,
        superseded_by=superseded_by,
        keep_until=keep_until,
        owner=owner,
    )


def _optional_string(value: object, override_path: Path, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{override_path} field {field_name} must be a string when present.")
    normalized = value.strip()
    return normalized or None


def _optional_bool(value: object, override_path: Path, field_name: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"{override_path} field {field_name} must be a boolean when present.")
    return value


def _list_local_branches(repo_root: Path) -> tuple[_BranchState, ...]:
    separator = "\x1f"
    completed = _run_git(
        repo_root,
        "for-each-ref",
        (
            "--format="
            f"%(refname:short){separator}%(objectname){separator}"
            f"%(committerdate:iso-strict){separator}%(upstream:short){separator}%(subject)"
        ),
        "refs/heads",
    )
    states: list[_BranchState] = []
    for line in completed.stdout.splitlines():
        if not line.strip():
            continue
        branch_name, commit_sha, commit_time, upstream, subject = (
            part.strip() for part in line.split("\x1f", 4)
        )
        states.append(
            _BranchState(
                branch_name=branch_name,
                commit_sha=commit_sha,
                upstream=upstream or None,
                subject=subject,
                last_commit_at=_parse_datetime(commit_time) if commit_time else None,
            )
        )
    return tuple(states)


def _list_worktrees(repo_root: Path) -> tuple[_WorktreeState, ...]:
    completed = _run_git(repo_root, "worktree", "list", "--porcelain")
    records: list[_WorktreeState] = []
    current_path: Path | None = None
    current_head = ""
    current_branch: str | None = None
    detached = False

    def flush() -> None:
        nonlocal current_path, current_head, current_branch, detached
        if current_path is None:
            return
        records.append(
            _WorktreeState(
                worktree_path=current_path.resolve(),
                head_commit=current_head,
                branch_name=current_branch,
                detached=detached,
            )
        )
        current_path = None
        current_head = ""
        current_branch = None
        detached = False

    for line in completed.stdout.splitlines():
        if not line.strip():
            flush()
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            flush()
            current_path = Path(value)
        elif key == "HEAD":
            current_head = value
        elif key == "branch":
            current_branch = value.removeprefix("refs/heads/")
            detached = False
        elif key == "detached":
            current_branch = None
            detached = True
    flush()
    return tuple(records)


def _current_branch(repo_root: Path) -> str | None:
    completed = _run_git(repo_root, "branch", "--show-current")
    value = completed.stdout.strip()
    return value or None


def _branch_merged_into_base(repo_root: Path, branch_name: str, base_ref: str) -> bool:
    completed = _run_git(
        repo_root,
        "merge-base",
        "--is-ancestor",
        branch_name,
        base_ref,
        allow_failure=True,
    )
    if completed.returncode not in (0, 1):
        raise ValueError(
            completed.stderr.strip()
            or f"Unable to compare branch {branch_name!r} to {base_ref!r}."
        )
    return completed.returncode == 0


def _branch_unique_commit_count(repo_root: Path, base_ref: str, branch_name: str) -> int:
    completed = _run_git(repo_root, "rev-list", "--count", f"{base_ref}..{branch_name}")
    return int(completed.stdout.strip() or "0")


def _upstream_divergence(
    repo_root: Path,
    branch_name: str,
    upstream: str | None,
) -> tuple[int | None, int | None]:
    if upstream is None:
        return None, None
    completed = _run_git(
        repo_root,
        "rev-list",
        "--left-right",
        "--count",
        f"{branch_name}...{upstream}",
    )
    left_text, right_text = completed.stdout.strip().split(maxsplit=1)
    return int(left_text), int(right_text)


def _latest_worktree_activity(
    worktree_path: Path,
    status_entries: tuple[GitWorktreeEntry, ...],
    branch_last_commit_at: datetime | None,
) -> datetime | None:
    latest = branch_last_commit_at
    for entry in status_entries:
        candidate_paths = [worktree_path / entry.path]
        original_path = entry.original_path
        if original_path:
            candidate_paths.append(worktree_path / original_path)
        for candidate in candidate_paths:
            if not candidate.exists():
                continue
            modified_at = datetime.fromtimestamp(candidate.stat().st_mtime, UTC)
            if latest is None or modified_at > latest:
                latest = modified_at
    return latest


def _defer_active(override: GitHygieneOverride, now: datetime) -> bool:
    if override.defer_reason:
        return True
    if override.active_handoff:
        return True
    if override.keep_until is None:
        return False
    keep_until = _parse_datetime(override.keep_until)
    return keep_until is not None and keep_until >= now


def _inactive_day_count(last_activity_at: datetime | None, now: datetime) -> int | None:
    if last_activity_at is None:
        return None
    return max(0, (now - last_activity_at).days)


def _format_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_datetime(value: str) -> datetime | None:
    normalized = value.strip()
    if not normalized:
        return None
    return datetime.fromisoformat(normalized.replace("Z", "+00:00")).astimezone(UTC)


def _is_staged_change(raw_status: str) -> bool:
    return len(raw_status) >= 1 and raw_status[0] not in {" ", "?"}


def _is_unstaged_change(raw_status: str) -> bool:
    return len(raw_status) >= 2 and raw_status[1] not in {" ", "?"}


def _run_git(
    repo_root: Path,
    *args: str,
    allow_failure: bool = False,
) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ValueError("Git is not available on PATH.") from exc
    if not allow_failure and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "Git command failed."
        raise ValueError(message)
    return completed


__all__ = [
    "GitHygieneAppliedAction",
    "GitHygieneBranchEvaluation",
    "GitHygieneOverrides",
    "GitHygieneOverride",
    "GitHygieneRequest",
    "GitHygieneResult",
    "GitHygieneService",
    "GitHygieneWorktreeEvaluation",
]
