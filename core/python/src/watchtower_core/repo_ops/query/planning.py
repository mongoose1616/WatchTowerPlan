"""Repo-specific query helpers for canonical planning-catalog records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PlanningCatalogEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class PlanningCatalogSearchParams:
    """Filter and ranking inputs for planning-catalog lookup."""

    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    limit: int | None = None


class PlanningCatalogQueryService:
    """Search the canonical planning catalog with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(
        self,
        params: PlanningCatalogSearchParams,
    ) -> tuple[PlanningCatalogEntry, ...]:
        """Return planning-catalog entries matching the requested filters."""
        catalog = self._loader.load_planning_catalog()
        trace_id = params.trace_id.casefold() if params.trace_id is not None else None
        initiative_status = (
            params.initiative_status.casefold() if params.initiative_status is not None else None
        )
        current_phase = (
            params.current_phase.casefold() if params.current_phase is not None else None
        )
        owner = params.owner.casefold() if params.owner is not None else None

        matches: list[tuple[int, PlanningCatalogEntry]] = []
        for entry in catalog.entries:
            if trace_id is not None and entry.trace_id.casefold() != trace_id:
                continue
            if (
                initiative_status is not None
                and entry.initiative_status.casefold() != initiative_status
            ):
                continue
            if current_phase is not None and entry.current_phase.casefold() != current_phase:
                continue
            if owner is not None:
                owner_values = {
                    *(value.casefold() for value in entry.active_owners),
                }
                if entry.primary_owner is not None:
                    owner_values.add(entry.primary_owner.casefold())
                if owner not in owner_values:
                    continue

            score = query_score(
                params.query,
                (
                    entry.trace_id,
                    entry.title,
                    entry.summary,
                    entry.artifact_status,
                    entry.initiative_status,
                    entry.updated_at,
                    entry.coordination.current_phase,
                    entry.coordination.key_surface_path,
                    entry.coordination.next_action,
                    entry.coordination.next_surface_path,
                    entry.coordination.primary_owner or "",
                    *entry.coordination.active_owners,
                    *entry.coordination.active_task_ids,
                    *(task.task_id for task in entry.coordination.active_task_summaries),
                    *(task.title for task in entry.coordination.active_task_summaries),
                    *(item.prd_id for item in entry.prds),
                    *(item.title for item in entry.prds),
                    *(item.decision_id for item in entry.decisions),
                    *(item.title for item in entry.decisions),
                    *(item.document_id for item in entry.design_documents),
                    *(item.title for item in entry.design_documents),
                    *(item.task_id for item in entry.tasks),
                    *(item.title for item in entry.tasks),
                    *(item.contract_id for item in entry.acceptance_contracts),
                    *(item.title for item in entry.acceptance_contracts),
                    *(item.evidence_id for item in entry.validation_evidence),
                    *(item.title for item in entry.validation_evidence),
                    *entry.prd_ids,
                    *entry.decision_ids,
                    *entry.design_ids,
                    *entry.plan_ids,
                    *entry.task_ids,
                    *entry.requirement_ids,
                    *entry.acceptance_ids,
                    *entry.acceptance_contract_ids,
                    *entry.evidence_ids,
                    *entry.validator_ids,
                    *entry.related_paths,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].trace_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)

    def get(self, trace_id: str) -> PlanningCatalogEntry:
        """Return one planning-catalog entry by its trace identifier."""
        return self._loader.load_planning_catalog().get(trace_id)
