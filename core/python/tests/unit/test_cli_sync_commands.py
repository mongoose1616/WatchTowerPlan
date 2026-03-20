from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.integration.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_minimal_plan_pack,
)
from watchtower_core.cli.main import main

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_live_plan_cli_repo(repo_root: Path) -> Path:
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True, exist_ok=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_cli_sync_live_counts",
        title="Example CLI Sync Live Counts",
        summary="Seeds one live initiative so CLI sync output tests assert non-zero live counts against a temp repo.",
    )
    return repo_root


@pytest.fixture(scope="module")
def live_plan_cli_repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_live_plan_cli_repo(tmp_path_factory.mktemp("live_plan_cli_repo") / "repo")


def test_sync_repository_paths_supports_json_output(capsys) -> None:
    result = main(["sync", "repository-paths", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_command_index_supports_json_output(capsys) -> None:
    result = main(["sync", "command-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync command-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_all_supports_json_output(capsys) -> None:
    result = main(["sync", "all", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync all"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert payload["wrote"] is False
    assert payload["output_dir"] is None
    assert any(entry["target"] == "command-index" for entry in payload["results"])
    assert any(entry["target"] == "repository-paths" for entry in payload["results"])


def test_sync_coordination_supports_json_output(capsys) -> None:
    result = main(["sync", "coordination", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync coordination"
    assert payload["status"] == "ok"
    assert payload["result_count"] == 7
    assert payload["wrote"] is False
    assert payload["output_dir"] is None
    assert [entry["target"] for entry in payload["results"]] == [
        "task-index",
        "traceability-index",
        "initiative-index",
        "coordination-index",
        "task-tracking",
        "initiative-tracking",
        "coordination-tracking",
    ]


def test_sync_reference_index_supports_json_output(capsys) -> None:
    result = main(["sync", "reference-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync reference-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_foundation_index_supports_json_output(capsys) -> None:
    result = main(["sync", "foundation-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync foundation-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_standard_index_supports_json_output(capsys) -> None:
    result = main(["sync", "standard-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync standard-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_workflow_index_supports_json_output(capsys) -> None:
    result = main(["sync", "workflow-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync workflow-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_initiative_index_supports_json_output(
    live_plan_cli_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = live_plan_cli_repo
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(["sync", "initiative-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_initiative_tracking_supports_json_output(
    live_plan_cli_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = live_plan_cli_repo
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(["sync", "initiative-tracking", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-tracking"
    assert payload["status"] == "ok"
    assert payload["initiative_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_task_index_supports_json_output(
    live_plan_cli_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = live_plan_cli_repo
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(["sync", "task-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_task_tracking_supports_json_output(
    live_plan_cli_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = live_plan_cli_repo
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(["sync", "task-tracking", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-tracking"
    assert payload["status"] == "ok"
    assert payload["task_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_github_tasks_supports_json_output(
    live_plan_cli_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = live_plan_cli_repo
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(
        [
            "sync",
            "github-tasks",
            "--repo",
            "owner/repo",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync github-tasks"
    assert payload["status"] == "ok"
    assert payload["wrote"] is False
    assert payload["result_count"] >= 1
    assert "labels" in payload["results"][0]


def test_sync_github_tasks_supports_disabling_label_sync(
    live_plan_cli_repo: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = live_plan_cli_repo
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(
        [
            "sync",
            "github-tasks",
            "--repo",
            "owner/repo",
            "--no-label-sync",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync github-tasks"
    assert all(entry["labels"] == [] for entry in payload["results"])


def test_sync_traceability_index_supports_json_output(capsys) -> None:
    result = main(["sync", "traceability-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync traceability-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_repository_paths_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "repository_path_index.json"

    result = main(
        ["sync", "repository-paths", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_command_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "command_index.json"

    result = main(["sync", "command-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync command-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_all_can_write_to_explicit_output_dir(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "sync_all"

    result = main(["sync", "all", "--output-dir", str(output_dir), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync all"
    assert payload["wrote"] is True
    assert payload["output_dir"] == str(output_dir.resolve())
    assert (
        output_dir / "core/control_plane/indexes/commands/command_index.json"
    ).exists()
    assert (output_dir / "plan/tracking/task_tracking.md").exists()


def test_sync_coordination_can_write_to_explicit_output_dir(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "sync_coordination"

    result = main(
        ["sync", "coordination", "--output-dir", str(output_dir), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync coordination"
    assert payload["wrote"] is True
    assert payload["output_dir"] == str(output_dir.resolve())
    assert (output_dir / "plan/.wt/indexes/task_index.json").exists()
    assert (
        output_dir / "core/control_plane/indexes/traceability/traceability_index.json"
    ).exists()
    assert (
        output_dir / "plan/.wt/indexes/coordination_index.json"
    ).exists()
    assert (output_dir / "plan/tracking/task_tracking.md").exists()
    assert (output_dir / "plan/tracking/initiative_tracking.md").exists()
    assert (output_dir / "plan/tracking/coordination_tracking.md").exists()


def test_sync_standard_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "standard_index.json"

    result = main(["sync", "standard-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync standard-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_workflow_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "workflow_index.json"

    result = main(["sync", "workflow-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync workflow-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_foundation_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "foundation_index.json"

    result = main(
        ["sync", "foundation-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync foundation-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_initiative_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "initiative_index.json"

    result = main(
        ["sync", "initiative-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_initiative_tracking_can_write_to_explicit_output(
    tmp_path: Path, capsys
) -> None:
    output_path = tmp_path / "initiative_tracking.md"

    result = main(
        ["sync", "initiative-tracking", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-tracking"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_task_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "task_index.json"

    result = main(["sync", "task-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_task_tracking_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "task_tracking.md"

    result = main(["sync", "task-tracking", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-tracking"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_traceability_index_can_write_to_explicit_output(
    tmp_path: Path, capsys
) -> None:
    output_path = tmp_path / "traceability_index.json"

    result = main(
        ["sync", "traceability-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync traceability-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()
