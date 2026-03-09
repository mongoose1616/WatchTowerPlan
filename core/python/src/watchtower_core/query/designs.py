"""Index-backed query helpers for design documents."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import DesignDocumentIndexEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class DesignDocumentSearchParams:
    """Filter and ranking inputs for design-document lookup."""

    query: str | None = None
    trace_id: str | None = None
    family: str | None = None
    tag: str | None = None
    limit: int | None = None


class DesignDocumentQueryService:
    """Search the design-document index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: DesignDocumentSearchParams) -> tuple[DesignDocumentIndexEntry, ...]:
        """Return design-document entries matching the requested filters."""
        index = self._loader.load_design_document_index()
        trace_id = params.trace_id.casefold() if params.trace_id is not None else None
        family = params.family.casefold() if params.family is not None else None
        tag = params.tag.casefold() if params.tag is not None else None

        matches: list[tuple[int, DesignDocumentIndexEntry]] = []
        for entry in index.entries:
            if trace_id is not None and entry.trace_id.casefold() != trace_id:
                continue
            if family is not None and entry.family.casefold() != family:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue

            score = query_score(
                params.query,
                (
                    entry.document_id,
                    entry.trace_id,
                    entry.family,
                    entry.title,
                    entry.summary,
                    *entry.source_paths,
                    *entry.related_paths,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].document_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
