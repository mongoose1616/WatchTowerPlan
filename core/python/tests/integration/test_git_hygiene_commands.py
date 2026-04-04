from __future__ import annotations

import json
import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from watchtower_host.cli.main import main


def test_git_hygiene_reports_old_branches_and_worktrees(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _initialize_git_repository(tmp_path / "repo")
    _create_merged_branch(repo_root, "fix/merged-cleanup")
    _create_stale_branch(repo_root, "feature/stale-review", days_old=21)
    worktree_path = _create_clean_worktree(repo_root, "chore/worktree-cleanup")
    _run_git(repo_root, "switch", "-c", "task/active-current")

    monkeypatch.chdir(repo_root)
    result = main(["git", "hygiene", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core git hygiene"

    branch_actions = {
        entry["branch_name"]: entry["recommended_action"] for entry in payload["branches"]
    }
    assert branch_actions["fix/merged-cleanup"] == "delete_branch"
    assert branch_actions["feature/stale-review"] == "review"
    assert branch_actions["main"] == "keep"

    worktree_actions = {
        entry["worktree_path"]: entry["recommended_action"] for entry in payload["worktrees"]
    }
    assert worktree_actions[str(worktree_path)] == "remove_worktree"


def test_git_hygiene_apply_removes_clean_worktrees_and_merged_branches(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _initialize_git_repository(tmp_path / "repo")
    _create_merged_branch(repo_root, "fix/merged-cleanup")
    worktree_path = _create_clean_worktree(repo_root, "chore/worktree-cleanup")

    monkeypatch.chdir(repo_root)
    result = main(["git", "hygiene", "--apply", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    applied = {
        (entry["action"], entry["target"]): entry["status"]
        for entry in payload["actions_applied"]
    }
    assert applied[("remove_worktree", str(worktree_path))] == "applied"
    assert applied[("delete_branch", "fix/merged-cleanup")] == "applied"
    assert applied[("delete_branch", "chore/worktree-cleanup")] == "applied"
    assert not worktree_path.exists()

    branches = _git_lines(repo_root, "branch", "--format=%(refname:short)")
    assert "fix/merged-cleanup" not in branches
    assert "chore/worktree-cleanup" not in branches


def _initialize_git_repository(repo_root: Path) -> Path:
    repo_root.mkdir(parents=True, exist_ok=True)
    _run_git(repo_root, "init", "-b", "main")
    _run_git(repo_root, "config", "user.name", "WatchTower Tests")
    _run_git(repo_root, "config", "user.email", "watchtower-tests@example.com")
    (repo_root / "tracked.txt").write_text("base\n", encoding="utf-8")
    _run_git(repo_root, "add", ".")
    _run_git(repo_root, "commit", "-m", "Initial commit")
    return repo_root


def _create_merged_branch(repo_root: Path, branch_name: str) -> None:
    _run_git(repo_root, "switch", "-c", branch_name)
    (repo_root / f"{branch_name.replace('/', '_')}.txt").write_text("merged\n", encoding="utf-8")
    _run_git(repo_root, "add", ".")
    _run_git(repo_root, "commit", "-m", f"Add {branch_name}")
    _run_git(repo_root, "switch", "main")
    _run_git(repo_root, "merge", "--no-ff", branch_name, "-m", f"Merge {branch_name}")


def _create_stale_branch(repo_root: Path, branch_name: str, *, days_old: int) -> None:
    timestamp = datetime.now(UTC) - timedelta(days=days_old)
    date_text = timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    _run_git(repo_root, "switch", "-c", branch_name)
    (repo_root / f"{branch_name.replace('/', '_')}.txt").write_text("stale\n", encoding="utf-8")
    _run_git(repo_root, "add", ".")
    _run_git(
        repo_root,
        "commit",
        "-m",
        f"Add {branch_name}",
        env={
            "GIT_AUTHOR_DATE": date_text,
            "GIT_COMMITTER_DATE": date_text,
        },
    )
    _run_git(repo_root, "switch", "main")


def _create_clean_worktree(repo_root: Path, branch_name: str) -> Path:
    worktree_path = repo_root.parent / branch_name.replace("/", "_")
    _run_git(repo_root, "branch", branch_name, "main")
    _run_git(repo_root, "worktree", "add", str(worktree_path), branch_name)
    return worktree_path


def _git_lines(repo_root: Path, *args: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _run_git(repo_root: Path, *args: str, env: dict[str, str] | None = None) -> None:
    effective_env = os.environ.copy()
    if env is not None:
        effective_env.update(env)
    subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
        env=effective_env,
    )
