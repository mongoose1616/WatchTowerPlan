"""Support helpers for GitHub task sync orchestration."""

from __future__ import annotations

from os import environ
from typing import Protocol

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.integrations.github import (
    GitHubApiError,
    GitHubClient,
    GitHubIssueRef,
    GitHubLabelSpec,
    GitHubProjectContext,
)
from watchtower_core.repo_ops.query.tasks import TaskQueryService, TaskSearchParams
from watchtower_core.repo_ops.sync.task_index import TaskIndexSyncService
from watchtower_core.repo_ops.sync.task_tracking import TaskTrackingSyncService
from watchtower_core.repo_ops.sync.traceability import TraceabilityIndexSyncService
from watchtower_core.repo_ops.task_documents import TaskDocument, load_task_document
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


class GitHubTaskSyncParamsLike(Protocol):
    """Minimal parameter contract used by helper functions."""

    @property
    def task_ids(self) -> tuple[str, ...]: ...

    @property
    def trace_id(self) -> str | None: ...

    @property
    def task_status(self) -> str | None: ...

    @property
    def priority(self) -> str | None: ...

    @property
    def owner(self) -> str | None: ...

    @property
    def task_kind(self) -> str | None: ...

    @property
    def blocked_only(self) -> bool: ...

    @property
    def blocked_by_task_id(self) -> str | None: ...

    @property
    def depends_on_task_id(self) -> str | None: ...

    @property
    def repository(self) -> str | None: ...

    @property
    def project_owner(self) -> str | None: ...

    @property
    def project_owner_type(self) -> str | None: ...

    @property
    def project_number(self) -> int | None: ...

    @property
    def project_status_field_name(self) -> str: ...


def select_task_documents(
    loader: ControlPlaneLoader,
    params: GitHubTaskSyncParamsLike,
) -> tuple[TaskDocument, ...]:
    """Resolve the filtered local task set for one sync run."""

    entries = TaskQueryService(loader).search(
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
    return tuple(load_task_document(loader, entry.doc_path) for entry in entries)


def resolve_repository(task: TaskDocument, params: GitHubTaskSyncParamsLike) -> str | None:
    """Resolve the target repository from params, task metadata, or env."""

    if params.repository is not None:
        return params.repository
    if task.github_repository is not None:
        return task.github_repository
    environment_repository = environ.get("GITHUB_REPOSITORY")
    if environment_repository is not None and environment_repository.strip():
        return environment_repository.strip()
    return None


def validate_existing_bindings(
    task: TaskDocument,
    params: GitHubTaskSyncParamsLike,
    repository: str,
) -> None:
    """Reject sync attempts that conflict with persisted GitHub bindings."""

    if task.github_repository is not None and task.github_repository != repository:
        raise GitHubApiError(
            f"{task.task_id} is already bound to GitHub repository "
            f"{task.github_repository}, not {repository}."
        )
    if params.project_number is None:
        return
    if task.github_project_owner is not None and task.github_project_owner != params.project_owner:
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


def load_project_context(
    client: GitHubClient,
    params: GitHubTaskSyncParamsLike,
) -> GitHubProjectContext | None:
    """Load the target project context when project sync was requested."""

    if params.project_number is None:
        return None
    if params.project_owner is None or params.project_owner_type is None:
        raise GitHubApiError(
            "GitHub project sync requires --project-owner and "
            "--project-owner-type with --project-number."
        )
    return client.load_project_context(
        owner=params.project_owner,
        owner_type=params.project_owner_type,
        number=params.project_number,
        status_field_name=params.project_status_field_name,
    )


def sync_issue(
    client: GitHubClient,
    task: TaskDocument,
    *,
    repository: str,
    labels: tuple[GitHubLabelSpec, ...],
) -> GitHubIssueRef:
    """Create or update the GitHub issue mirror for one task."""

    body = issue_body(task, repository=repository)
    state, state_reason = issue_state(task.task_status)
    if labels:
        client.ensure_labels(repository, labels)
    label_names = tuple(label.name for label in labels)
    if task.github_issue_number is None:
        return client.create_issue(
            repository,
            title=task.title,
            body=body,
            labels=label_names,
            state=state,
            state_reason=state_reason,
        )
    return client.update_issue(
        repository,
        task.github_issue_number,
        title=task.title,
        body=body,
        labels=label_names,
        state=state,
        state_reason=state_reason,
    )


def sync_project(
    client: GitHubClient,
    task: TaskDocument,
    *,
    issue_node_id: str,
    project_context: GitHubProjectContext | None,
) -> str | None:
    """Upsert the GitHub project item when a project context is active."""

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


def task_front_matter_updates(
    *,
    task: TaskDocument,
    repository: str,
    issue_number: int,
    issue_node_id: str,
    project_context: GitHubProjectContext | None,
    project_item_id: str | None,
) -> dict[str, object]:
    """Build the task front-matter updates persisted after a write sync."""

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
        return updates
    updates["github_project_owner"] = task.github_project_owner
    updates["github_project_owner_type"] = task.github_project_owner_type
    updates["github_project_number"] = task.github_project_number
    updates["github_project_item_id"] = task.github_project_item_id
    return updates


def issue_state(task_status: str) -> tuple[str, str | None]:
    """Map local task state to GitHub issue state and close reason."""

    if task_status == "done":
        return "closed", "completed"
    if task_status == "cancelled":
        return "closed", "not_planned"
    return "open", None


def project_action(task: TaskDocument, params: GitHubTaskSyncParamsLike) -> str | None:
    """Describe the project action the sync would perform for one task."""

    if params.project_number is None:
        return None
    if task.github_project_item_id is None:
        return "upsert_project_item"
    return "update_project_status"


def issue_labels(task: TaskDocument) -> tuple[GitHubLabelSpec, ...]:
    """Build the managed label set mirrored from local task metadata."""

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
        labels.append(
            GitHubLabelSpec(
                name=name,
                color=LABEL_COLOR_BY_PREFIX.get(prefix, "5319E7"),
                description=label_description(name),
            )
        )
    return tuple(labels)


def label_description(name: str) -> str:
    """Describe one managed label for GitHub."""

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


def issue_body(task: TaskDocument, *, repository: str) -> str:
    """Render the GitHub issue body mirrored from the local task document."""

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


def rebuild_derived_surfaces(loader: ControlPlaneLoader) -> None:
    """Refresh the task and traceability mirrors after a write sync."""

    task_index_service = TaskIndexSyncService(loader)
    task_index_service.write_document(task_index_service.build_document())

    task_tracking_service = TaskTrackingSyncService(loader)
    task_tracking_service.write_document(task_tracking_service.build_document())

    traceability_service = TraceabilityIndexSyncService(loader)
    traceability_service.write_document(traceability_service.build_document())
