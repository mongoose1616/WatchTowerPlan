"""Deterministic rebuild helpers for the task index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import TaskIndexEntry
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.task_documents import iter_task_documents

TASK_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/tasks/task_index.v1.json"


def _entry_to_document(entry: TaskIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "task_id": entry.task_id,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "task_status": entry.task_status,
        "task_kind": entry.task_kind,
        "priority": entry.priority,
        "owner": entry.owner,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    if entry.trace_id is not None:
        document["trace_id"] = entry.trace_id
    if entry.blocked_by:
        document["blocked_by"] = list(entry.blocked_by)
    if entry.depends_on:
        document["depends_on"] = list(entry.depends_on)
    if entry.related_ids:
        document["related_ids"] = list(entry.related_ids)
    if entry.applies_to:
        document["applies_to"] = list(entry.applies_to)
    if entry.github_repository is not None:
        document["github_repository"] = entry.github_repository
    if entry.github_issue_number is not None:
        document["github_issue_number"] = entry.github_issue_number
    if entry.github_issue_node_id is not None:
        document["github_issue_node_id"] = entry.github_issue_node_id
    if entry.github_project_owner is not None:
        document["github_project_owner"] = entry.github_project_owner
    if entry.github_project_owner_type is not None:
        document["github_project_owner_type"] = entry.github_project_owner_type
    if entry.github_project_number is not None:
        document["github_project_number"] = entry.github_project_number
    if entry.github_project_item_id is not None:
        document["github_project_item_id"] = entry.github_project_item_id
    if entry.github_synced_at is not None:
        document["github_synced_at"] = entry.github_synced_at
    if entry.tags:
        document["tags"] = list(entry.tags)
    if entry.notes is not None:
        document["notes"] = entry.notes
    return document


class TaskIndexSyncService:
    """Build and write the task index from governed task documents."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> TaskIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        entries: list[TaskIndexEntry] = []
        for task in iter_task_documents(self._loader):
            entries.append(
                TaskIndexEntry(
                    task_id=task.task_id,
                    trace_id=task.trace_id,
                    title=task.title,
                    summary=task.summary,
                    status=task.status,
                    task_status=task.task_status,
                    task_kind=task.task_kind,
                    priority=task.priority,
                    owner=task.owner,
                    doc_path=task.relative_path,
                    updated_at=task.updated_at,
                    blocked_by=task.list_values("blocked_by"),
                    depends_on=task.list_values("depends_on"),
                    related_ids=task.list_values("related_ids"),
                    applies_to=task.list_values("applies_to"),
                    github_repository=task.github_repository,
                    github_issue_number=task.optional_int("github_issue_number"),
                    github_issue_node_id=task.optional_string("github_issue_node_id"),
                    github_project_owner=task.github_project_owner,
                    github_project_owner_type=task.github_project_owner_type,
                    github_project_number=task.github_project_number,
                    github_project_item_id=task.optional_string("github_project_item_id"),
                    github_synced_at=task.github_synced_at,
                    tags=task.list_values("tags"),
                )
            )

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:task-index:v1",
            "id": "index.tasks",
            "title": "Task Index",
            "status": "active",
            "entries": [
                _entry_to_document(entry)
                for entry in sorted(entries, key=lambda entry: entry.task_id)
            ],
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated task index to disk."""
        target = destination or (self._repo_root / TASK_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
