from __future__ import annotations

from types import SimpleNamespace

from tests.cli_command_helpers import run_json_command
from watchtower_host.cli import git_handlers
from watchtower_host.cli.main import main


def test_git_hygiene_supports_json_output(monkeypatch, capsys) -> None:
    class FakeService:
        def run(self, request: object) -> SimpleNamespace:
            return SimpleNamespace(
                repo_root="/repo",
                git_root="/repo",
                git_common_dir="/repo/.git",
                base_ref="main",
                inactive_days=14,
                current_branch="main",
                current_worktree_path="/repo",
                override_path="/repo/.git/watchtower/git_hygiene_overrides.json",
                overrides_found=False,
                apply=False,
                branches=(
                    SimpleNamespace(
                        branch_name="fix/merged",
                        base_ref="main",
                        current=False,
                        upstream="origin/fix/merged",
                        ahead_count=0,
                        behind_count=0,
                        merged_into_base=True,
                        unique_commit_count=0,
                        checked_out_in_worktree_paths=(),
                        has_dirty_worktree=False,
                        has_staged_worktree_changes=False,
                        has_uncommitted_worktree_changes=False,
                        last_commit_at="2026-04-01T12:00:00Z",
                        inactive_days=3,
                        defer_reason=None,
                        active_handoff=False,
                        superseded_by=None,
                        keep_until=None,
                        owner=None,
                        old=True,
                        recommended_action="delete_branch",
                        reasons=("merged_into_base",),
                    ),
                ),
                worktrees=(),
                actions_applied=(),
            )

    monkeypatch.setattr(git_handlers, "GitHygieneService", FakeService)

    result, payload = run_json_command(capsys, ["git", "hygiene"])

    assert result == 0
    assert payload["command"] == "watchtower-core git hygiene"
    assert payload["status"] == "ok"
    assert payload["old_branch_count"] == 1
    assert payload["branches"][0]["recommended_action"] == "delete_branch"


def test_git_help_lists_hygiene_leaf(capsys) -> None:
    result = main(["git"])

    help_text = capsys.readouterr().out
    assert result == 0
    assert "hygiene" in help_text
