from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from watchtower_plan.cli import sync as plan_sync_cli

from watchtower_core.cli import sync_runtime_helpers
from watchtower_host.cli.main import main


class _FakeDocumentSyncService:
    def __init__(self, *, entry_count: int = 3) -> None:
        self._document = {
            "entries": [
                {"id": f"entry.{index}", "path": f"example/{index}.json"}
                for index in range(entry_count)
            ]
        }

    def build_document(self) -> dict[str, object]:
        return self._document

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        if destination is None:
            raise AssertionError("The fake sync service requires an explicit destination in tests.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return destination.resolve()


class _FakeTrackingSyncService:
    def __init__(self, *, content: str, counts: dict[str, int]) -> None:
        self._result = SimpleNamespace(content=content, **counts)

    def build_document(self) -> SimpleNamespace:
        return self._result

    def write_document(
        self,
        result: SimpleNamespace,
        destination: Path | None = None,
    ) -> Path:
        if destination is None:
            raise AssertionError("The fake tracking service requires an explicit destination.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(result.content, encoding="utf-8")
        return destination.resolve()


class _FakeParams:
    def __init__(self, **kwargs: object) -> None:
        self.__dict__.update(kwargs)


def _patch_plan_document_sync(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        plan_sync_cli,
        "load_document_sync_service",
        lambda module_name, class_name: _FakeDocumentSyncService(),
    )


def _patch_plan_tracking_sync(monkeypatch: pytest.MonkeyPatch) -> None:
    def _load_tracking_sync_service(module_name: str, class_name: str) -> object:
        if class_name == "InitiativeTrackingSyncService":
            return _FakeTrackingSyncService(
                content="# initiative tracking\n",
                counts={"initiative_count": 5, "active_count": 1, "closed_count": 4},
            )
        if class_name == "TaskTrackingSyncService":
            return _FakeTrackingSyncService(
                content="# task tracking\n",
                counts={"task_count": 8, "open_count": 3, "closed_count": 5},
            )
        raise AssertionError(f"Unexpected tracking service: {module_name}.{class_name}")

    monkeypatch.setattr(
        sync_runtime_helpers,
        "load_tracking_sync_service",
        _load_tracking_sync_service,
    )


def _patch_multi_target_sync(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    captured: dict[str, object] = {}

    class _FakeMultiTargetSyncService:
        def __init__(self, target_prefix: str) -> None:
            self._target_prefix = target_prefix

        @classmethod
        def from_repo_root(cls) -> _FakeMultiTargetSyncService:
            raise AssertionError("from_repo_root should be provided by the dispatch shim.")

        def run(self, *, write: bool = False, output_dir: Path | None = None) -> SimpleNamespace:
            captured["write"] = write
            captured["output_dir"] = output_dir
            resolved_output_dir = (
                str(output_dir.resolve()) if output_dir is not None else None
            )
            output_path = None
            if output_dir is not None:
                output_path = str(
                    (output_dir / "plan/.wt/indexes/coordination_index.json").resolve()
                )
            records = [
                SimpleNamespace(
                    target=f"{self._target_prefix}-index",
                    artifact_kind="index",
                    relative_output_path=f"plan/.wt/indexes/{self._target_prefix}_index.json",
                    output_path=output_path,
                    wrote=write or output_dir is not None,
                    record_count=2,
                    details={"kind": self._target_prefix},
                )
            ]
            return SimpleNamespace(
                records=records,
                wrote=write or output_dir is not None,
                output_dir=resolved_output_dir,
            )

    def _load_sync_class(module_name: str, class_name: str) -> object:
        if class_name == "AllSyncService":
            class _AllSyncService(_FakeMultiTargetSyncService):
                @classmethod
                def from_repo_root(cls) -> _AllSyncService:
                    return cls("all")

            return _AllSyncService
        if class_name == "CoordinationSyncService":
            class _CoordinationSyncService(_FakeMultiTargetSyncService):
                @classmethod
                def from_repo_root(cls) -> _CoordinationSyncService:
                    return cls("coordination")

            return _CoordinationSyncService
        raise AssertionError(f"Unexpected sync class request: {module_name}.{class_name}")

    monkeypatch.setattr(sync_runtime_helpers, "load_sync_class", _load_sync_class)
    return captured


def _patch_github_task_sync(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    captured: dict[str, object] = {}

    class _FakeGitHubTaskSyncService:
        def __init__(self, loader: object) -> None:
            captured["loader"] = loader

        def sync(
            self,
            params: _FakeParams,
            *,
            write: bool = False,
        ) -> SimpleNamespace:
            captured["params"] = params
            captured["write"] = write
            labels = ["triaged"] if getattr(params, "sync_labels", True) else []
            return SimpleNamespace(
                wrote=write,
                synced_task_count=1,
                local_change_count=0,
                rebuilt_task_index=False,
                rebuilt_task_tracking=False,
                rebuilt_traceability_index=False,
                records=[
                    SimpleNamespace(
                        task_id="task.example.001",
                        doc_path="plan/initiatives/example/.wt/tasks/example/task.json",
                        repository=params.repository,
                        task_status="planned",
                        issue_action="preview",
                        project_action=None,
                        success=True,
                        message="Previewed sync only.",
                        github_issue_number=None,
                        github_issue_url=None,
                        github_project_item_id=None,
                        labels=labels,
                    )
                ],
            )

    def _load_sync_class(module_name: str, class_name: str) -> object:
        if class_name == "GitHubTaskSyncParams":
            return _FakeParams
        if class_name == "GitHubTaskSyncService":
            return _FakeGitHubTaskSyncService
        raise AssertionError(f"Unexpected GitHub sync class request: {module_name}.{class_name}")

    monkeypatch.setattr(plan_sync_cli, "load_sync_class", _load_sync_class)
    monkeypatch.setattr(plan_sync_cli, "build_loader", lambda: object())
    return captured


@pytest.mark.parametrize(
    ("command", "expected_command"),
    (
        (["plan", "sync", "reference-index"], "watchtower-core plan sync reference-index"),
        (["plan", "sync", "foundation-index"], "watchtower-core plan sync foundation-index"),
        (["plan", "sync", "standard-index"], "watchtower-core plan sync standard-index"),
        (["plan", "sync", "workflow-index"], "watchtower-core plan sync workflow-index"),
        (["plan", "sync", "initiative-index"], "watchtower-core plan sync initiative-index"),
        (["plan", "sync", "task-index"], "watchtower-core plan sync task-index"),
        (["plan", "sync", "review-index"], "watchtower-core plan sync review-index"),
        (["plan", "sync", "traceability-index"], "watchtower-core plan sync traceability-index"),
    ),
)
def test_plan_document_sync_commands_support_json_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    command: list[str],
    expected_command: str,
) -> None:
    _patch_plan_document_sync(monkeypatch)

    result = main([*command, "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == expected_command
    assert payload["status"] == "ok"
    assert payload["entry_count"] == 3
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


@pytest.mark.parametrize(
    ("command", "expected_command", "filename"),
    (
        (
            ["plan", "sync", "reference-index"],
            "watchtower-core plan sync reference-index",
            "reference_index.json",
        ),
        (
            ["plan", "sync", "initiative-index"],
            "watchtower-core plan sync initiative-index",
            "initiative_index.json",
        ),
        (
            ["plan", "sync", "traceability-index"],
            "watchtower-core plan sync traceability-index",
            "traceability_index.json",
        ),
    ),
)
def test_plan_document_sync_commands_can_write_to_explicit_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    command: list[str],
    expected_command: str,
    filename: str,
) -> None:
    _patch_plan_document_sync(monkeypatch)
    output_path = tmp_path / filename

    result = main([*command, "--output", str(output_path), "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == expected_command
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_plan_sync_all_supports_json_output_with_lightweight_runtime(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _patch_multi_target_sync(monkeypatch)

    result = main(["plan", "sync", "all", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync all"
    assert payload["status"] == "ok"
    assert payload["result_count"] == 1
    assert payload["wrote"] is False
    assert payload["output_dir"] is None
    assert payload["results"][0]["target"] == "all-index"


def test_plan_sync_all_can_write_to_explicit_output_dir_with_lightweight_runtime(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    captured = _patch_multi_target_sync(monkeypatch)
    output_dir = tmp_path / "sync_all"

    result = main(["plan", "sync", "all", "--output-dir", str(output_dir), "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync all"
    assert payload["wrote"] is True
    assert payload["output_dir"] == str(output_dir.resolve())
    assert captured["write"] is False
    assert captured["output_dir"] == output_dir


def test_plan_sync_coordination_supports_json_output_with_lightweight_runtime(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _patch_multi_target_sync(monkeypatch)

    result = main(["plan", "sync", "coordination", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync coordination"
    assert payload["status"] == "ok"
    assert payload["result_count"] == 1
    assert payload["wrote"] is False
    assert payload["results"][0]["target"] == "coordination-index"


def test_plan_sync_coordination_can_write_to_explicit_output_dir_with_lightweight_runtime(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    captured = _patch_multi_target_sync(monkeypatch)
    output_dir = tmp_path / "sync_coordination"

    result = main(
        ["plan", "sync", "coordination", "--output-dir", str(output_dir), "--format", "json"]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync coordination"
    assert payload["wrote"] is True
    assert payload["output_dir"] == str(output_dir.resolve())
    assert captured["write"] is False
    assert captured["output_dir"] == output_dir


def test_plan_sync_initiative_tracking_supports_json_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _patch_plan_tracking_sync(monkeypatch)

    result = main(["plan", "sync", "initiative-tracking", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync initiative-tracking"
    assert payload["status"] == "ok"
    assert payload["initiative_count"] == 5
    assert payload["active_count"] == 1
    assert payload["closed_count"] == 4
    assert payload["wrote"] is False


def test_plan_sync_task_tracking_supports_json_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _patch_plan_tracking_sync(monkeypatch)

    result = main(["plan", "sync", "task-tracking", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync task-tracking"
    assert payload["status"] == "ok"
    assert payload["task_count"] == 8
    assert payload["open_count"] == 3
    assert payload["closed_count"] == 5
    assert payload["wrote"] is False


def test_sync_github_tasks_supports_json_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    captured = _patch_github_task_sync(monkeypatch)

    result = main(
        [
            "plan",
            "sync",
            "github-tasks",
            "--repo",
            "owner/repo",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync github-tasks"
    assert payload["status"] == "ok"
    assert payload["wrote"] is False
    assert payload["result_count"] == 1
    assert payload["results"][0]["labels"] == ["triaged"]
    params = captured["params"]
    assert params.repository == "owner/repo"
    assert params.sync_labels is True


def test_sync_github_tasks_supports_disabling_label_sync(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    captured = _patch_github_task_sync(monkeypatch)

    result = main(
        [
            "plan",
            "sync",
            "github-tasks",
            "--repo",
            "owner/repo",
            "--no-label-sync",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan sync github-tasks"
    assert payload["results"][0]["labels"] == []
    params = captured["params"]
    assert params.sync_labels is False


def test_sync_repository_paths_supports_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    result = main(["sync", "repository-paths", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_command_index_supports_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    result = main(["sync", "command-index", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync command-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_repository_paths_can_write_to_explicit_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_path = tmp_path / "repository_path_index.json"

    result = main(["sync", "repository-paths", "--output", str(output_path), "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_command_index_can_write_to_explicit_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_path = tmp_path / "command_index.json"

    result = main(["sync", "command-index", "--output", str(output_path), "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync command-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()
