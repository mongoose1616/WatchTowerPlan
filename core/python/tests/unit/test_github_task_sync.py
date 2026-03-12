from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest
from fixture_repo_support import materialize_governed_applies_to_targets

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.integrations.github import GitHubApiError, GitHubIssueRef, GitHubProjectContext
from watchtower_core.repo_ops.sync import GitHubTaskSyncParams, GitHubTaskSyncService
from watchtower_core.repo_ops.task_documents import update_task_document_front_matter

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "docs" / "planning", repo_root / "docs" / "planning")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_governed_applies_to_targets(repo_root)
    return repo_root


def test_github_task_sync_dry_run_includes_managed_labels() -> None:
    service = GitHubTaskSyncService(ControlPlaneLoader(REPO_ROOT))

    result = service.sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            task_ids=("task.local_task_tracking.github_sync.001",),
        ),
        write=False,
    )

    assert result.wrote is False
    assert result.synced_task_count == 0
    assert len(result.records) == 1
    assert result.records[0].labels == (
        "source:watchtower",
        "kind:feature",
        "status:done",
        "priority:medium",
    )


def test_github_task_sync_dry_run_can_disable_managed_labels() -> None:
    service = GitHubTaskSyncService(ControlPlaneLoader(REPO_ROOT))

    result = service.sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            task_ids=("task.local_task_tracking.github_sync.001",),
            sync_labels=False,
        ),
        write=False,
    )

    assert result.wrote is False
    assert len(result.records) == 1
    assert result.records[0].labels == ()


def test_github_task_sync_dry_run_reports_missing_repository() -> None:
    service = GitHubTaskSyncService(ControlPlaneLoader(REPO_ROOT))

    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=("task.local_task_tracking.github_sync.001",),
        ),
        write=False,
    )

    assert result.wrote is False
    assert result.records[0].success is False
    assert "No GitHub repository was resolved." in result.records[0].message


def test_github_task_sync_write_updates_local_bindings_and_indexes(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))
    task_path = "docs/planning/tasks/closed/github_task_sync.md"

    class FakeClient:
        def __init__(self) -> None:
            self.ensure_label_calls: list[tuple[str, tuple[str, ...]]] = []
            self.project_status_calls: list[tuple[str, str]] = []

        def load_project_context(
            self,
            *,
            owner: str,
            owner_type: str,
            number: int,
            status_field_name: str = "Status",
        ) -> GitHubProjectContext:
            return GitHubProjectContext(
                owner=owner,
                owner_type=owner_type,
                number=number,
                project_id="PROJECT_ID",
                status_field_name=status_field_name,
                status_field_id="FIELD_ID",
                status_options={"Done": "OPT_DONE"},
            )

        def ensure_labels(self, repository: str, labels) -> None:
            self.ensure_label_calls.append((repository, tuple(label.name for label in labels)))

        def create_issue(
            self,
            repository: str,
            *,
            title: str,
            body: str,
            labels: tuple[str, ...] = (),
            state: str = "open",
            state_reason: str | None = None,
        ) -> GitHubIssueRef:
            assert "## Task Metadata" in body
            assert state == "closed"
            assert state_reason == "completed"
            return GitHubIssueRef(
                repository=repository,
                number=42,
                node_id="ISSUE_NODE",
                html_url="https://example/issues/42",
                state="closed",
            )

        def find_project_item_id(
            self,
            project: GitHubProjectContext,
            *,
            issue_node_id: str,
        ) -> str | None:
            return None

        def add_project_item(
            self,
            project: GitHubProjectContext,
            *,
            issue_node_id: str,
        ) -> str:
            assert issue_node_id == "ISSUE_NODE"
            return "ITEM_ID"

        def update_project_status(
            self,
            project: GitHubProjectContext,
            *,
            item_id: str,
            status_name: str,
        ) -> None:
            self.project_status_calls.append((item_id, status_name))

    client = FakeClient()
    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=("task.local_task_tracking.github_sync.001",),
            repository="owner/repo",
            project_owner="owner",
            project_owner_type="organization",
            project_number=12,
        ),
        write=True,
        client=client,
    )

    assert result.wrote is True
    assert result.synced_task_count == 1
    assert result.local_change_count == 1
    assert result.rebuilt_task_index is True
    assert result.rebuilt_task_tracking is True
    assert result.rebuilt_traceability_index is True
    assert result.records[0].github_issue_number == 42
    assert result.records[0].github_project_item_id == "ITEM_ID"
    assert client.ensure_label_calls
    assert client.project_status_calls == [("ITEM_ID", "Done")]

    written_task = (repo_root / task_path).read_text(encoding="utf-8")
    assert "github_repository:" in written_task
    assert "owner/repo" in written_task
    assert "github_issue_number: 42" in written_task
    assert "github_project_item_id:" in written_task
    assert "ITEM_ID" in written_task

    task_index = json.loads(
        (repo_root / "core/control_plane/indexes/tasks/task_index.v1.json").read_text(
            encoding="utf-8"
        )
    )
    entry = next(
        item
        for item in task_index["entries"]
        if item["task_id"] == "task.local_task_tracking.github_sync.001"
    )
    assert entry["github_repository"] == "owner/repo"
    assert entry["github_issue_number"] == 42


def test_github_task_sync_write_updates_existing_issue_and_project_item(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))
    task_path = "docs/planning/tasks/closed/github_task_sync.md"
    update_task_document_front_matter(
        ControlPlaneLoader(repo_root),
        task_path,
        updates={
            "github_repository": "owner/repo",
            "github_issue_number": 7,
            "github_issue_node_id": "ISSUE_NODE",
            "github_project_owner": "owner",
            "github_project_owner_type": "organization",
            "github_project_number": 12,
            "github_project_item_id": "ITEM_ID",
        },
    )

    class FakeClient:
        def __init__(self) -> None:
            self.update_issue_calls: list[int] = []
            self.project_status_calls: list[tuple[str, str]] = []

        def load_project_context(
            self,
            *,
            owner: str,
            owner_type: str,
            number: int,
            status_field_name: str = "Status",
        ) -> GitHubProjectContext:
            return GitHubProjectContext(
                owner=owner,
                owner_type=owner_type,
                number=number,
                project_id="PROJECT_ID",
                status_field_name=status_field_name,
                status_field_id="FIELD_ID",
                status_options={"Done": "OPT_DONE"},
            )

        def ensure_labels(self, repository: str, labels) -> None:
            return None

        def update_issue(
            self,
            repository: str,
            issue_number: int,
            *,
            title: str,
            body: str,
            labels: tuple[str, ...] = (),
            state: str,
            state_reason: str | None = None,
        ) -> GitHubIssueRef:
            self.update_issue_calls.append(issue_number)
            return GitHubIssueRef(
                repository=repository,
                number=issue_number,
                node_id="ISSUE_NODE",
                html_url="https://example/issues/7",
                state=state,
            )

        def find_project_item_id(
            self,
            project: GitHubProjectContext,
            *,
            issue_node_id: str,
        ) -> str | None:
            raise AssertionError("existing project item should be reused directly")

        def add_project_item(
            self,
            project: GitHubProjectContext,
            *,
            issue_node_id: str,
        ) -> str:
            raise AssertionError("existing project item should not be recreated")

        def update_project_status(
            self,
            project: GitHubProjectContext,
            *,
            item_id: str,
            status_name: str,
        ) -> None:
            self.project_status_calls.append((item_id, status_name))

    client = FakeClient()
    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=("task.local_task_tracking.github_sync.001",),
            project_owner="owner",
            project_owner_type="organization",
            project_number=12,
        ),
        write=True,
        client=client,
    )

    assert result.records[0].issue_action == "update_issue"
    assert result.records[0].project_action == "update_project_status"
    assert client.update_issue_calls == [7]
    assert client.project_status_calls == [("ITEM_ID", "Done")]


def test_github_task_sync_reports_binding_validation_errors(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = GitHubTaskSyncService(loader)
    update_task_document_front_matter(
        loader,
        "docs/planning/tasks/closed/github_task_sync.md",
        updates={"github_repository": "bound/repo"},
    )

    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=("task.local_task_tracking.github_sync.001",),
            repository="owner/repo",
        ),
        write=False,
    )

    assert result.records[0].success is False
    assert "already bound to GitHub repository bound/repo" in result.records[0].message


def test_github_task_sync_requires_project_owner_and_type_for_project_sync(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        GitHubApiError,
        match="GitHub project sync requires --project-owner and --project-owner-type",
    ):
        service.sync(
            GitHubTaskSyncParams(
                task_ids=("task.local_task_tracking.github_sync.001",),
                repository="owner/repo",
                project_number=12,
            ),
            write=True,
            client=object(),  # type: ignore[arg-type]
        )


def test_github_task_sync_records_client_failures_without_local_mutation(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    class FailingClient:
        def ensure_labels(self, repository: str, labels) -> None:
            return None

        def create_issue(self, repository: str, **kwargs) -> GitHubIssueRef:
            raise GitHubApiError("permission denied")

    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=("task.local_task_tracking.github_sync.001",),
            repository="owner/repo",
        ),
        write=True,
        client=FailingClient(),  # type: ignore[arg-type]
    )

    assert result.synced_task_count == 0
    assert result.local_change_count == 0
    assert result.records[0].success is False
    assert result.records[0].message == "permission denied"
