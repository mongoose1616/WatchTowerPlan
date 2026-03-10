"""Repo-specific query helpers for initiative coordination records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeIndexEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class InitiativeSearchParams:
    """Filter and ranking inputs for initiative lookup."""

    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    blocked_only: bool = False
    limit: int | None = None


class InitiativeQueryService:
    """Search the initiative index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: InitiativeSearchParams) -> tuple[InitiativeIndexEntry, ...]:
        """Return initiative entries matching the requested filters."""
        index = self._loader.load_initiative_index()
        trace_id = params.trace_id.casefold() if params.trace_id is not None else None
        initiative_status = (
            params.initiative_status.casefold() if params.initiative_status is not None else None
        )
        current_phase = (
            params.current_phase.casefold() if params.current_phase is not None else None
        )
        owner = params.owner.casefold() if params.owner is not None else None

        matches: list[tuple[int, InitiativeIndexEntry]] = []
        for entry in index.entries:
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
            if params.blocked_only and entry.blocked_task_count == 0:
                continue

            score = query_score(
                params.query,
                (
                    entry.trace_id,
                    entry.title,
                    entry.summary,
                    entry.initiative_status,
                    entry.current_phase,
                    entry.primary_owner or "",
                    entry.key_surface_path,
                    entry.next_action,
                    entry.next_surface_path,
                    *entry.active_owners,
                    *entry.active_task_ids,
                    *entry.prd_ids,
                    *entry.decision_ids,
                    *entry.design_ids,
                    *entry.plan_ids,
                    *entry.acceptance_ids,
                    *entry.acceptance_contract_ids,
                    *entry.evidence_ids,
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

    def get(self, trace_id: str) -> InitiativeIndexEntry:
        """Return one initiative entry by its trace identifier."""
        return self._loader.load_initiative_index().get(trace_id)
