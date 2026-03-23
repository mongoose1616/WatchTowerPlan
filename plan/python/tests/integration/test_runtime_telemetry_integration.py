from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest
from watchtower_plan.tasks import lifecycle as task_lifecycle_module
from watchtower_plan.testing.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_governed_applies_to_targets,
    materialize_minimal_plan_pack,
)

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import main

REPO_ROOT = Path(__file__).resolve().parents[4]
CAPTURE_TRACE_ID = "trace.task_lifecycle_capture"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    (repo_root / "core" / "python" / "tests" / "unit").mkdir(parents=True, exist_ok=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    materialize_governed_applies_to_targets(repo_root, REPO_ROOT)
    loader = ControlPlaneLoader(repo_root)
    task_lifecycle_module.PlanWorkspaceService(loader).sync(write=True)
    task_lifecycle_module.CoordinationSyncService(loader).run(write=True)
    return repo_root


def _bootstrap_trace(repo_root: Path, trace_id: str) -> None:
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title=f"{trace_id} Fixture",
        summary="Seeds one live initiative package for runtime telemetry integration coverage.",
        approve=False,
    )


@pytest.fixture(scope="module")
def task_lifecycle_capture_baseline(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    repo_root = _build_fixture_repo(tmp_path_factory.mktemp("task_lifecycle_capture_baseline"))
    _bootstrap_trace(repo_root, CAPTURE_TRACE_ID)
    return repo_root


@pytest.fixture
def task_lifecycle_capture_repo(tmp_path: Path, task_lifecycle_capture_baseline: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(task_lifecycle_capture_baseline, repo_root)
    return repo_root


def _load_telemetry_records(output_dir: Path) -> list[dict[str, object]]:
    telemetry_files = tuple(output_dir.glob("**/*.jsonl"))
    assert len(telemetry_files) == 1
    return [
        json.loads(line)
        for line in telemetry_files[0].read_text(encoding="utf-8").splitlines()
    ]


def test_plan_sync_coordination_records_runtime_telemetry(
    task_lifecycle_capture_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = task_lifecycle_capture_repo
    output_dir = tmp_path / "telemetry"
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(output_dir))

    result = main(["plan", "sync", "coordination", "--format", "json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert result == 0
    assert payload["command"] == "watchtower-core plan sync coordination"
    assert "[telemetry] watchtower-core plan sync coordination status=ok" in captured.err

    records = _load_telemetry_records(output_dir)
    operation_pairs = {
        (record["operation_kind"], record["operation_name"])
        for record in records
        if record.get("record_type") == "operation_result"
    }
    assert ("cli_command", "watchtower-core plan sync coordination") in operation_pairs
    assert ("sync_command", "watchtower-core plan sync coordination") in operation_pairs
    assert any(
        record.get("record_type") == "operation_result"
        and record.get("operation_kind") == "sync_harness"
        for record in records
    )


def test_plan_task_create_records_runtime_telemetry(
    task_lifecycle_capture_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = task_lifecycle_capture_repo
    output_dir = tmp_path / "telemetry"
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(output_dir))

    result = main(
        [
            "plan",
            "task",
            "create",
            "--task-id",
            "task.runtime_telemetry_integration.001",
            "--trace-id",
            CAPTURE_TRACE_ID,
            "--title",
            "Create telemetry integration proof task",
            "--summary",
            "Creates one tracked task to prove telemetry crosses host core and pack seams.",
            "--task-kind",
            "feature",
            "--priority",
            "high",
            "--owner",
            "repository_maintainer",
            "--scope",
            "Capture one task lifecycle write path.",
            "--done-when",
            "The task exists in the initiative package.",
            "--write",
            "--format",
            "json",
        ]
    )
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert result == 0
    assert payload["task_id"] == "task.runtime_telemetry_integration.001"
    assert "[telemetry] watchtower-core plan task create status=ok" in captured.err

    records = _load_telemetry_records(output_dir)
    operation_pairs = {
        (record["operation_kind"], record["operation_name"])
        for record in records
        if record.get("record_type") == "operation_result"
    }
    assert ("cli_command", "watchtower-core plan task create") in operation_pairs
    assert ("plan_task", "plan_task_create") in operation_pairs
    assert any(
        record.get("record_type") == "operation_result"
        and record.get("operation_kind") == "sync_harness"
        for record in records
    )
