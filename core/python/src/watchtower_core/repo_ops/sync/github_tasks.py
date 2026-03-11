"""Push-only GitHub sync for local-first task records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.integrations.github import (
    GitHubApiError,
    GitHubClient,
    GitHubProjectContext,
)
from watchtower_core.repo_ops.sync.github_task_sync_support import (
    issue_labels,
    load_project_context,
    project_action,
    rebuild_derived_surfaces,
    resolve_repository,
    select_task_documents,
    sync_issue,
    sync_project,
    task_front_matter_updates,
    validate_existing_bindings,
)
from watchtower_core.repo_ops.task_documents import (
    update_task_document_front_matter,
)


@dataclass(frozen=True, slots=True)
class GitHubTaskSyncParams:
    """Selection and target inputs for GitHub task sync."""

    task_ids: tuple[str, ...] = ()
    trace_id: str | None = None
    task_status: str | None = None
    priority: str | None = None
    owner: str | None = None
    task_kind: str | None = None
    blocked_only: bool = False
    blocked_by_task_id: str | None = None
    depends_on_task_id: str | None = None
    repository: str | None = None
    project_owner: str | None = None
    project_owner_type: str | None = None
    project_number: int | None = None
    project_status_field_name: str = "Status"
    token_env: str = "GITHUB_TOKEN"
    sync_labels: bool = True


@dataclass(frozen=True, slots=True)
class GitHubTaskSyncRecord:
    """Per-task sync plan or result summary."""

    task_id: str
    doc_path: str
    repository: str | None
    task_status: str
    issue_action: str
    project_action: str | None
    success: bool
    message: str
    github_issue_number: int | None = None
    github_issue_url: str | None = None
    github_project_item_id: str | None = None
    labels: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GitHubTaskSyncResult:
    """Aggregate result for a GitHub task sync run."""

    records: tuple[GitHubTaskSyncRecord, ...]
    wrote: bool
    synced_task_count: int
    local_change_count: int
    rebuilt_task_index: bool
    rebuilt_task_tracking: bool
    rebuilt_traceability_index: bool


class GitHubTaskSyncService:
    """Push local task records to GitHub issues and optional project items."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def sync(
        self,
        params: GitHubTaskSyncParams,
        *,
        write: bool,
        client: GitHubClient | None = None,
    ) -> GitHubTaskSyncResult:
        task_documents = select_task_documents(self._loader, params)
        records: list[GitHubTaskSyncRecord] = []
        local_change_count = 0
        synced_task_count = 0
        project_context: GitHubProjectContext | None = None

        if write:
            client = client or GitHubClient.from_env(params.token_env)
            project_context = load_project_context(client, params)

        for task in task_documents:
            repository = resolve_repository(task, params)
            issue_action = "create_issue" if task.github_issue_number is None else "update_issue"
            project_sync_action = project_action(task, params)
            label_specs = issue_labels(task) if params.sync_labels else ()
            label_names = tuple(label.name for label in label_specs)

            if repository is None:
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=None,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_sync_action,
                        success=False,
                        message=(
                            "No GitHub repository was resolved. Pass --repo, set "
                            "GITHUB_REPOSITORY, or persist github_repository on the task."
                        ),
                        labels=label_names,
                    )
                )
                continue

            try:
                validate_existing_bindings(task, params, repository)
            except GitHubApiError as exc:
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=repository,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_sync_action,
                        success=False,
                        message=str(exc),
                        github_issue_number=task.github_issue_number,
                        github_project_item_id=task.github_project_item_id,
                        labels=label_names,
                    )
                )
                continue

            if not write:
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=repository,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_sync_action,
                        success=True,
                        message="Planned sync only. Use --write to apply the GitHub updates.",
                        github_issue_number=task.github_issue_number,
                        github_project_item_id=task.github_project_item_id,
                        labels=label_names,
                    )
                )
                continue

            assert client is not None
            try:
                issue_ref = sync_issue(
                    client,
                    task,
                    repository=repository,
                    labels=label_specs,
                )
                project_item_id = sync_project(
                    client,
                    task,
                    issue_node_id=issue_ref.node_id,
                    project_context=project_context,
                )
                changed = update_task_document_front_matter(
                    self._loader,
                    task.relative_path,
                    updates=task_front_matter_updates(
                        task=task,
                        repository=repository,
                        issue_number=issue_ref.number,
                        issue_node_id=issue_ref.node_id,
                        project_context=project_context,
                        project_item_id=project_item_id,
                    ),
                )
                if changed:
                    local_change_count += 1
                synced_task_count += 1
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=repository,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_sync_action,
                        success=True,
                        message="GitHub task sync completed successfully.",
                        github_issue_number=issue_ref.number,
                        github_issue_url=issue_ref.html_url,
                        github_project_item_id=project_item_id,
                        labels=label_names,
                    )
                )
            except GitHubApiError as exc:
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=repository,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_sync_action,
                        success=False,
                        message=str(exc),
                        github_issue_number=task.github_issue_number,
                        github_project_item_id=task.github_project_item_id,
                        labels=label_names,
                    )
                )

        rebuilt_task_index = False
        rebuilt_task_tracking = False
        rebuilt_traceability_index = False
        if write and local_change_count > 0:
            rebuild_derived_surfaces(self._loader)
            rebuilt_task_index = True
            rebuilt_task_tracking = True
            rebuilt_traceability_index = True

        return GitHubTaskSyncResult(
            records=tuple(records),
            wrote=write,
            synced_task_count=synced_task_count,
            local_change_count=local_change_count,
            rebuilt_task_index=rebuilt_task_index,
            rebuilt_task_tracking=rebuilt_task_tracking,
            rebuilt_traceability_index=rebuilt_traceability_index,
        )
