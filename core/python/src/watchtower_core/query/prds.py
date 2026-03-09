"""Index-backed query helpers for PRD records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PrdIndexEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class PrdSearchParams:
    """Filter and ranking inputs for PRD lookup."""

    query: str | None = None
    trace_id: str | None = None
    tag: str | None = None
    requirement_id: str | None = None
    acceptance_id: str | None = None
    limit: int | None = None


class PrdQueryService:
    """Search the PRD index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: PrdSearchParams) -> tuple[PrdIndexEntry, ...]:
        """Return PRD entries matching the requested filters."""
        index = self._loader.load_prd_index()
        trace_id = params.trace_id.casefold() if params.trace_id is not None else None
        tag = params.tag.casefold() if params.tag is not None else None
        requirement_id = (
            params.requirement_id.casefold() if params.requirement_id is not None else None
        )
        acceptance_id = (
            params.acceptance_id.casefold() if params.acceptance_id is not None else None
        )

        matches: list[tuple[int, PrdIndexEntry]] = []
        for entry in index.entries:
            if trace_id is not None and entry.trace_id.casefold() != trace_id:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue
            if requirement_id is not None and requirement_id not in {
                value.casefold() for value in entry.requirement_ids
            }:
                continue
            if acceptance_id is not None and acceptance_id not in {
                value.casefold() for value in entry.acceptance_ids
            }:
                continue

            score = query_score(
                params.query,
                (
                    entry.prd_id,
                    entry.trace_id,
                    entry.title,
                    entry.summary,
                    *entry.requirement_ids,
                    *entry.acceptance_ids,
                    *entry.linked_decision_ids,
                    *entry.linked_design_ids,
                    *entry.linked_plan_ids,
                    *entry.related_paths,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].prd_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
