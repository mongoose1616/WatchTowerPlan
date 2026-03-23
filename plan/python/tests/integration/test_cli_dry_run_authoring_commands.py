from __future__ import annotations

from pathlib import Path
from shutil import copytree

import pytest
from watchtower_plan.testing.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_minimal_plan_pack,
)

from tests.cli_command_helpers import run_json_command

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_task_preview_repo(repo_root: Path) -> Path:
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_cli_task_preview",
        title="Example CLI Task Preview",
        summary="Fixture initiative for dry-run task create coverage.",
        approve=True,
    )
    return repo_root


@pytest.fixture(scope="module")
def task_preview_repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_task_preview_repo(tmp_path_factory.mktemp("task_preview_repo") / "repo")


def test_task_create_supports_json_output(
    task_preview_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = task_preview_repo
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "task",
            "create",
            "--task-id",
            "task.example_cli_task_preview.cli_preview_json_output",
            "--trace-id",
            "trace.example_cli_task_preview",
            "--title",
            "Preview the task command",
            "--summary",
            "Previews the task create command without writing a file.",
            "--task-kind",
            "documentation",
            "--priority",
            "medium",
            "--owner",
            "repository_maintainer",
            "--scope",
            "Preview the create command.",
            "--done-when",
            "The dry-run payload is returned.",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan task create"
    assert payload["status"] == "ok"
    assert payload["task_id"] == "task.example_cli_task_preview.cli_preview_json_output"
    assert payload["wrote"] is False
    assert payload["changed"] is True


def test_plan_bootstrap_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "bootstrap",
            "--trace-id",
            "trace.plan_cli_preview",
            "--title",
            "Plan CLI Preview",
            "--summary",
            "Previews the live initiative bootstrap command without writing.",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan bootstrap"
    assert payload["status"] == "ok"
    assert payload["initiative_id"] == "initiative.plan_cli_preview"
    assert payload["initiative_root"] == "plan/initiatives/plan_cli_preview"
    assert payload["wrote"] is False
