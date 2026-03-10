"""Index-backed query helpers for governed workflow modules."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import WorkflowIndexEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class WorkflowSearchParams:
    """Filter and ranking inputs for workflow lookup."""

    query: str | None = None
    workflow_id: str | None = None
    phase_type: str | None = None
    task_family: str | None = None
    trigger_tag: str | None = None
    related_path: str | None = None
    reference_path: str | None = None
    limit: int | None = None


class WorkflowQueryService:
    """Search the workflow index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: WorkflowSearchParams) -> tuple[WorkflowIndexEntry, ...]:
        """Return workflow entries matching the requested filters."""
        index = self._loader.load_workflow_index()
        workflow_id = params.workflow_id.casefold() if params.workflow_id is not None else None
        phase_type = params.phase_type.casefold() if params.phase_type is not None else None
        task_family = params.task_family.casefold() if params.task_family is not None else None
        trigger_tag = params.trigger_tag.casefold() if params.trigger_tag is not None else None
        related_path = params.related_path.casefold() if params.related_path is not None else None
        reference_path = (
            params.reference_path.casefold() if params.reference_path is not None else None
        )

        matches: list[tuple[int, WorkflowIndexEntry]] = []
        for entry in index.entries:
            if workflow_id is not None and entry.workflow_id.casefold() != workflow_id:
                continue
            if phase_type is not None and entry.phase_type.casefold() != phase_type:
                continue
            if task_family is not None and entry.task_family.casefold() != task_family:
                continue
            if trigger_tag is not None and trigger_tag not in {
                value.casefold() for value in entry.trigger_tags
            }:
                continue
            if related_path is not None and related_path not in {
                value.casefold() for value in entry.related_paths
            }:
                continue
            if reference_path is not None and reference_path not in {
                value.casefold() for value in entry.reference_doc_paths
            }:
                continue

            score = query_score(
                params.query,
                (
                    entry.workflow_id,
                    entry.title,
                    entry.summary,
                    entry.phase_type,
                    entry.task_family,
                    *entry.primary_risks,
                    *entry.trigger_tags,
                    *entry.companion_workflow_ids,
                    *entry.related_paths,
                    *entry.reference_doc_paths,
                    *entry.internal_reference_paths,
                    *entry.external_reference_urls,
                    *entry.aliases,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].workflow_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
