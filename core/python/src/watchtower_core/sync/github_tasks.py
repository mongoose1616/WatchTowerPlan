"""Push-only GitHub sync for local-first task records."""

from __future__ import annotations

from dataclasses import dataclass
from os import environ

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.integrations.github import (
    GitHubApiError,
    GitHubClient,
    GitHubIssueRef,
    GitHubLabelSpec,
    GitHubProjectContext,
)
from watchtower_core.query.tasks import TaskQueryService, TaskSearchParams
from watchtower_core.sync.task_documents import (
    TaskDocument,
    load_task_document,
    update_task_document_front_matter,
)
from watchtower_core.sync.task_index import TaskIndexSyncService
from watchtower_core.sync.task_tracking import TaskTrackingSyncService
from watchtower_core.sync.traceability import TraceabilityIndexSyncService
from watchtower_core.utils import utc_timestamp_now

PROJECT_STATUS_BY_TASK_STATUS = {
    "backlog": "Backlog",
    "ready": "Ready",
    "in_progress": "In Progress",
    "blocked": "Blocked",
    "in_review": "In Review",
    "done": "Done",
    "cancelled": "Cancelled",
}

LABEL_COLOR_BY_PREFIX = {
    "source": "0E8A16",
    "kind": "1D76DB",
    "status": "5319E7",
    "priority": "D93F0B",
    "blocked": "B60205",
}


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
        task_documents = self._select_task_documents(params)
        records: list[GitHubTaskSyncRecord] = []
        local_change_count = 0
        synced_task_count = 0
        project_context: GitHubProjectContext | None = None

        if write:
            client = client or GitHubClient.from_env(params.token_env)
            if params.project_number is not None:
                if params.project_owner is None or params.project_owner_type is None:
                    raise GitHubApiError(
                        "GitHub project sync requires --project-owner and "
                        "--project-owner-type with --project-number."
                    )
                project_context = client.load_project_context(
                    owner=params.project_owner,
                    owner_type=params.project_owner_type,
                    number=params.project_number,
                    status_field_name=params.project_status_field_name,
                )

        for task in task_documents:
            repository = self._resolve_repository(task, params)
            issue_action = "create_issue" if task.github_issue_number is None else "update_issue"
            project_action = self._project_action(task, params)
            label_specs = self._issue_labels(task) if params.sync_labels else ()
            label_names = tuple(label.name for label in label_specs)

            if repository is None:
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=None,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_action,
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
                self._validate_existing_bindings(task, params, repository)
            except GitHubApiError as exc:
                records.append(
                    GitHubTaskSyncRecord(
                        task_id=task.task_id,
                        doc_path=task.relative_path,
                        repository=repository,
                        task_status=task.task_status,
                        issue_action=issue_action,
                        project_action=project_action,
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
                        project_action=project_action,
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
                issue_ref = self._sync_issue(
                    client,
                    task,
                    repository=repository,
                    labels=label_specs,
                )
                project_item_id = self._sync_project(
                    client,
                    task,
                    issue_node_id=issue_ref.node_id,
                    project_context=project_context,
                )
                changed = update_task_document_front_matter(
                    self._loader,
                    task.relative_path,
                    updates=self._task_front_matter_updates(
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
                        project_action=project_action,
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
                        project_action=project_action,
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
            TaskIndexSyncService(self._loader).write_document(
                TaskIndexSyncService(self._loader).build_document()
            )
            TaskTrackingSyncService(self._loader).write_document(
                TaskTrackingSyncService(self._loader).build_document()
            )
            TraceabilityIndexSyncService(self._loader).write_document(
                TraceabilityIndexSyncService(self._loader).build_document()
            )
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

    def _select_task_documents(self, params: GitHubTaskSyncParams) -> tuple[TaskDocument, ...]:
        entries = TaskQueryService(self._loader).search(
            TaskSearchParams(
                task_ids=params.task_ids,
                trace_id=params.trace_id,
                task_status=params.task_status,
                priority=params.priority,
                owner=params.owner,
                task_kind=params.task_kind,
                blocked_only=params.blocked_only,
                blocked_by_task_id=params.blocked_by_task_id,
                depends_on_task_id=params.depends_on_task_id,
            )
        )
        return tuple(load_task_document(self._loader, entry.doc_path) for entry in entries)

    def _resolve_repository(
        self,
        task: TaskDocument,
        params: GitHubTaskSyncParams,
    ) -> str | None:
        if params.repository is not None:
            return params.repository
        if task.github_repository is not None:
            return task.github_repository
        environment_repository = environ.get("GITHUB_REPOSITORY")
        if environment_repository is not None and environment_repository.strip():
            return environment_repository.strip()
        return None

    def _validate_existing_bindings(
        self,
        task: TaskDocument,
        params: GitHubTaskSyncParams,
        repository: str,
    ) -> None:
        if task.github_repository is not None and task.github_repository != repository:
            raise GitHubApiError(
                f"{task.task_id} is already bound to GitHub repository "
                f"{task.github_repository}, not {repository}."
            )
        if params.project_number is None:
            return
        if (
            task.github_project_owner is not None
            and task.github_project_owner != params.project_owner
        ):
            raise GitHubApiError(
                f"{task.task_id} is already bound to GitHub project owner "
                f"{task.github_project_owner}, not {params.project_owner}."
            )
        if (
            task.github_project_owner_type is not None
            and task.github_project_owner_type != params.project_owner_type
        ):
            raise GitHubApiError(
                f"{task.task_id} is already bound to GitHub project owner type "
                f"{task.github_project_owner_type}, not {params.project_owner_type}."
            )
        if (
            task.github_project_number is not None
            and task.github_project_number != params.project_number
        ):
            raise GitHubApiError(
                f"{task.task_id} is already bound to GitHub project "
                f"{task.github_project_number}, not {params.project_number}."
            )

    def _sync_issue(
        self,
        client: GitHubClient,
        task: TaskDocument,
        *,
        repository: str,
        labels: tuple[GitHubLabelSpec, ...],
    ) -> GitHubIssueRef:
        title = task.title
        body = self._issue_body(task, repository=repository)
        state, state_reason = self._issue_state(task.task_status)
        if labels:
            client.ensure_labels(repository, labels)
        label_names = tuple(label.name for label in labels)
        if task.github_issue_number is None:
            return client.create_issue(
                repository,
                title=title,
                body=body,
                labels=label_names,
                state=state,
                state_reason=state_reason,
            )
        return client.update_issue(
            repository,
            task.github_issue_number,
            title=title,
            body=body,
            labels=label_names,
            state=state,
            state_reason=state_reason,
        )

    def _sync_project(
        self,
        client: GitHubClient,
        task: TaskDocument,
        *,
        issue_node_id: str,
        project_context: GitHubProjectContext | None,
    ) -> str | None:
        if project_context is None:
            return task.github_project_item_id

        item_id = task.github_project_item_id
        if item_id is None:
            item_id = client.find_project_item_id(project_context, issue_node_id=issue_node_id)
        if item_id is None:
            item_id = client.add_project_item(project_context, issue_node_id=issue_node_id)

        client.update_project_status(
            project_context,
            item_id=item_id,
            status_name=PROJECT_STATUS_BY_TASK_STATUS[task.task_status],
        )
        return item_id

    def _task_front_matter_updates(
        self,
        *,
        task: TaskDocument,
        repository: str,
        issue_number: int,
        issue_node_id: str,
        project_context: GitHubProjectContext | None,
        project_item_id: str | None,
    ) -> dict[str, object]:
        updates: dict[str, object] = {
            "github_repository": repository,
            "github_issue_number": issue_number,
            "github_issue_node_id": issue_node_id,
            "github_synced_at": utc_timestamp_now(),
        }
        if project_context is not None and project_item_id is not None:
            updates["github_project_owner"] = project_context.owner
            updates["github_project_owner_type"] = project_context.owner_type
            updates["github_project_number"] = project_context.number
            updates["github_project_item_id"] = project_item_id
        elif project_context is None:
            updates["github_project_owner"] = task.github_project_owner
            updates["github_project_owner_type"] = task.github_project_owner_type
            updates["github_project_number"] = task.github_project_number
            updates["github_project_item_id"] = task.github_project_item_id
        return updates

    @staticmethod
    def _issue_state(task_status: str) -> tuple[str, str | None]:
        if task_status == "done":
            return "closed", "completed"
        if task_status == "cancelled":
            return "closed", "not_planned"
        return "open", None

    @staticmethod
    def _project_action(task: TaskDocument, params: GitHubTaskSyncParams) -> str | None:
        if params.project_number is None:
            return None
        if task.github_project_item_id is None:
            return "upsert_project_item"
        return "update_project_status"

    @staticmethod
    def _issue_labels(task: TaskDocument) -> tuple[GitHubLabelSpec, ...]:
        names: list[str] = [
            "source:watchtower",
            f"kind:{task.task_kind}",
            f"status:{task.task_status}",
            f"priority:{task.priority}",
        ]
        if task.list_values("blocked_by"):
            names.append("blocked")

        labels: list[GitHubLabelSpec] = []
        seen: set[str] = set()
        for name in names:
            if name in seen:
                continue
            seen.add(name)
            prefix = name.split(":", 1)[0]
            description = GitHubTaskSyncService._label_description(name)
            labels.append(
                GitHubLabelSpec(
                    name=name,
                    color=LABEL_COLOR_BY_PREFIX.get(prefix, "5319E7"),
                    description=description,
                )
            )
        return tuple(labels)

    @staticmethod
    def _label_description(name: str) -> str:
        if name == "source:watchtower":
            return "Managed by the local WatchTower task sync flow."
        if name == "blocked":
            return "Task is currently blocked by another local task."
        if name.startswith("kind:"):
            kind = name.split(":", 1)[1]
            return f"Mirrored from local task kind: {kind}."
        if name.startswith("status:"):
            status = name.split(":", 1)[1]
            return f"Mirrored from local task status: {status}."
        if name.startswith("priority:"):
            priority = name.split(":", 1)[1]
            return f"Mirrored from local task priority: {priority}."
        return "Managed label from the local WatchTower task sync flow."

    @staticmethod
    def _issue_body(task: TaskDocument, *, repository: str) -> str:
        lines = [
            "> This issue is managed from the local WatchTower task record.",
            "> Treat the local task document as the source of truth and use",
            "> GitHub comments for discussion rather than editing this body directly.",
            "",
            "## Task Metadata",
            f"- Task ID: `{task.task_id}`",
            f"- Task Status: `{task.task_status}`",
            f"- Task Kind: `{task.task_kind}`",
            f"- Priority: `{task.priority}`",
            f"- Owner: `{task.owner}`",
            f"- Local Source: `{task.relative_path}`",
            f"- GitHub Repository: `{repository}`",
        ]
        if task.trace_id is not None:
            lines.append(f"- Trace ID: `{task.trace_id}`")
        if task.list_values("related_ids"):
            lines.append(f"- Related IDs: `{'; '.join(task.list_values('related_ids'))}`")
        if task.list_values("depends_on"):
            lines.append(f"- Depends On: `{'; '.join(task.list_values('depends_on'))}`")
        if task.list_values("blocked_by"):
            lines.append(f"- Blocked By: `{'; '.join(task.list_values('blocked_by'))}`")
        lines.extend(
            [
                "",
                "## Summary",
                task.sections["Summary"],
                "",
                "## Context",
                task.sections["Context"],
                "",
                "## Scope",
                task.sections["Scope"],
                "",
                "## Done When",
                task.sections["Done When"],
                "",
                "## Links",
                task.sections["Links"],
            ]
        )
        lines.extend(
            [
                "",
                "## Sync Notes",
                "- Managed fields are mirrored from the repository-local task document.",
                "- Close or reprioritize the task from the local task record first when possible.",
                (
                    "- If this issue becomes materially different from the local task, "
                    "reconcile it in git."
                ),
            ]
        )
        if "Notes" in task.sections and task.sections["Notes"]:
            lines.extend(["", "## Notes", task.sections["Notes"]])
        return "\n".join(lines).strip()
