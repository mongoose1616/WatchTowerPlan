"""Index-backed query helpers for decision records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import DecisionIndexEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class DecisionSearchParams:
    """Filter and ranking inputs for decision lookup."""

    query: str | None = None
    trace_id: str | None = None
    decision_status: str | None = None
    tag: str | None = None
    linked_prd_id: str | None = None
    limit: int | None = None


class DecisionQueryService:
    """Search the decision index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: DecisionSearchParams) -> tuple[DecisionIndexEntry, ...]:
        """Return decision entries matching the requested filters."""
        index = self._loader.load_decision_index()
        trace_id = params.trace_id.casefold() if params.trace_id is not None else None
        decision_status = (
            params.decision_status.casefold() if params.decision_status is not None else None
        )
        tag = params.tag.casefold() if params.tag is not None else None
        linked_prd_id = (
            params.linked_prd_id.casefold() if params.linked_prd_id is not None else None
        )

        matches: list[tuple[int, DecisionIndexEntry]] = []
        for entry in index.entries:
            if trace_id is not None and entry.trace_id.casefold() != trace_id:
                continue
            if decision_status is not None and entry.decision_status.casefold() != decision_status:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue
            if linked_prd_id is not None and linked_prd_id not in {
                value.casefold() for value in entry.linked_prd_ids
            }:
                continue

            score = query_score(
                params.query,
                (
                    entry.decision_id,
                    entry.trace_id,
                    entry.title,
                    entry.summary,
                    entry.record_status,
                    entry.decision_status,
                    *entry.linked_prd_ids,
                    *entry.linked_design_ids,
                    *entry.linked_plan_ids,
                    *entry.related_paths,
                    *entry.internal_reference_paths,
                    *entry.external_reference_urls,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].decision_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
