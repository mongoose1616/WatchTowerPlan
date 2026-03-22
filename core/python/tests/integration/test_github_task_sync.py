from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest
from watchtower_plan.initiatives import InitiativeTaskSpec
from watchtower_plan.sync import GitHubTaskSyncParams, GitHubTaskSyncService
from watchtower_plan.tasks import update_task_document
from watchtower_plan.workspace.constants import PLAN_TASK_INDEX_PATH

from tests.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_governed_applies_to_targets,
    materialize_minimal_plan_pack,
    packwide_initiative_root,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.integrations.github import GitHubApiError, GitHubIssueRef, GitHubProjectContext

REPO_ROOT = Path(__file__).resolve().parents[4]
TRACE_ID = "trace.github_task_sync_fixture"
TASK_ID = "task.github_task_sync_fixture.sync_issue"
TASK_SLUG = "github_task_sync"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    materialize_governed_applies_to_targets(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=TRACE_ID,
        title="GitHub Task Sync Fixture",
        summary="Seeds one live initiative-local task record for GitHub sync tests.",
        task_specs=(
            InitiativeTaskSpec(
                title="GitHub task sync",
                summary="Fixture task for GitHub sync tests.",
                slug=TASK_SLUG,
                task_id=TASK_ID,
                priority="medium",
            ),
        ),
    )
    update_task_document(
        ControlPlaneLoader(repo_root),
        _github_task_path(repo_root),
        updates={
            "task_status": "completed",
            "updated_at": "2026-03-18T12:30:00Z",
        },
    )
    return repo_root


def _github_task_path(repo_root: Path) -> str:
    return (
        packwide_initiative_root(repo_root, TRACE_ID)
        .joinpath(".wt", "tasks", TASK_SLUG, "task.json")
        .relative_to(repo_root)
        .as_posix()
    )


def test_github_task_sync_dry_run_includes_managed_labels(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    result = service.sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            task_ids=(TASK_ID,),
        ),
        write=False,
    )

    assert result.wrote is False
    assert result.synced_task_count == 0
    assert len(result.records) == 1
    assert result.records[0].doc_path == _github_task_path(repo_root)
    assert result.records[0].labels == (
        "source:watchtower",
        "kind:feature",
        "status:completed",
        "priority:medium",
    )


def test_github_task_sync_dry_run_can_disable_managed_labels(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    result = service.sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            task_ids=(TASK_ID,),
            sync_labels=False,
        ),
        write=False,
    )

    assert result.wrote is False
    assert len(result.records) == 1
    assert result.records[0].labels == ()


def test_github_task_sync_dry_run_reports_missing_repository(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=(TASK_ID,),
        ),
        write=False,
    )

    assert result.wrote is False
    assert result.records[0].success is False
    assert "No GitHub repository was resolved." in result.records[0].message


def test_github_task_sync_targeted_selection_ignores_unrelated_invalid_task_documents(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    invalid_task = (
        packwide_initiative_root(repo_root, TRACE_ID)
        / ".wt"
        / "tasks"
        / "invalid_fixture"
        / "task.json"
    )
    invalid_task.parent.mkdir(parents=True, exist_ok=True)
    invalid_task.write_text('{"invalid": true}\n', encoding="utf-8")
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=(TASK_ID,),
            repository="owner/repo",
        ),
        write=False,
    )

    assert len(result.records) == 1
    assert result.records[0].task_id == TASK_ID


def test_github_task_sync_rejects_duplicate_task_ids_in_task_index(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    task_index_path = repo_root / PLAN_TASK_INDEX_PATH
    task_index = json.loads(task_index_path.read_text(encoding="utf-8"))
    matching_entry = next(entry for entry in task_index["entries"] if entry["task_id"] == TASK_ID)
    task_index["entries"].append(dict(matching_entry))
    task_index_path.write_text(f"{json.dumps(task_index, indent=2)}\n", encoding="utf-8")
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))

    with pytest.raises(ValueError, match="Duplicate task ID in GitHub task sync selection"):
        service.sync(
            GitHubTaskSyncParams(
                task_ids=(TASK_ID,),
                repository="owner/repo",
            ),
            write=False,
        )


def test_github_task_sync_write_updates_local_bindings_and_indexes(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))
    task_path = _github_task_path(repo_root)

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
                status_options={"Completed": "OPT_COMPLETED"},
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
            task_ids=(TASK_ID,),
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
    assert client.project_status_calls == [("ITEM_ID", "Completed")]

    written_task = json.loads((repo_root / task_path).read_text(encoding="utf-8"))
    assert written_task["github_repository"] == "owner/repo"
    assert written_task["github_issue_number"] == 42
    assert written_task["github_project_item_id"] == "ITEM_ID"

    task_index = json.loads((repo_root / PLAN_TASK_INDEX_PATH).read_text(encoding="utf-8"))
    entry = next(item for item in task_index["entries"] if item["task_id"] == TASK_ID)
    assert entry["github_repository"] == "owner/repo"
    assert entry["github_issue_number"] == 42


def test_github_task_sync_write_updates_existing_issue_and_project_item(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = GitHubTaskSyncService(ControlPlaneLoader(repo_root))
    update_task_document(
        ControlPlaneLoader(repo_root),
        _github_task_path(repo_root),
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
                status_options={"Completed": "OPT_COMPLETED"},
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
            task_ids=(TASK_ID,),
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
    assert client.project_status_calls == [("ITEM_ID", "Completed")]


def test_github_task_sync_reports_binding_validation_errors(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = GitHubTaskSyncService(loader)
    update_task_document(
        loader,
        _github_task_path(repo_root),
        updates={"github_repository": "bound/repo"},
    )

    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=(TASK_ID,),
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
                task_ids=(TASK_ID,),
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
            task_ids=(TASK_ID,),
            repository="owner/repo",
        ),
        write=True,
        client=FailingClient(),  # type: ignore[arg-type]
    )

    assert result.synced_task_count == 0
    assert result.local_change_count == 0
    assert result.records[0].success is False
    assert result.records[0].message == "permission denied"
