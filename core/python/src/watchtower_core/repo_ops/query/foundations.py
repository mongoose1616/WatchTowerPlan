"""Index-backed query helpers for governed foundation documents."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import FoundationIndexEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class FoundationSearchParams:
    """Filter and ranking inputs for foundation lookup."""

    query: str | None = None
    foundation_id: str | None = None
    audience: str | None = None
    authority: str | None = None
    tag: str | None = None
    related_path: str | None = None
    reference_path: str | None = None
    cited_by_path: str | None = None
    applied_by_path: str | None = None
    limit: int | None = None


class FoundationQueryService:
    """Search the foundation index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: FoundationSearchParams) -> tuple[FoundationIndexEntry, ...]:
        """Return foundation entries matching the requested filters."""
        index = self._loader.load_foundation_index()
        foundation_id = (
            params.foundation_id.casefold() if params.foundation_id is not None else None
        )
        audience = params.audience.casefold() if params.audience is not None else None
        authority = params.authority.casefold() if params.authority is not None else None
        tag = params.tag.casefold() if params.tag is not None else None
        related_path = params.related_path.casefold() if params.related_path is not None else None
        reference_path = (
            params.reference_path.casefold() if params.reference_path is not None else None
        )
        cited_by_path = (
            params.cited_by_path.casefold() if params.cited_by_path is not None else None
        )
        applied_by_path = (
            params.applied_by_path.casefold() if params.applied_by_path is not None else None
        )

        matches: list[tuple[int, FoundationIndexEntry]] = []
        for entry in index.entries:
            if foundation_id is not None and entry.foundation_id.casefold() != foundation_id:
                continue
            if audience is not None and entry.audience.casefold() != audience:
                continue
            if authority is not None and entry.authority.casefold() != authority:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue
            if related_path is not None and related_path not in {
                value.casefold() for value in entry.related_paths
            }:
                continue
            if reference_path is not None and reference_path not in {
                value.casefold() for value in entry.reference_doc_paths
            }:
                continue
            if cited_by_path is not None and cited_by_path not in {
                value.casefold() for value in entry.cited_by_paths
            }:
                continue
            if applied_by_path is not None and applied_by_path not in {
                value.casefold() for value in entry.applied_by_paths
            }:
                continue

            score = query_score(
                params.query,
                (
                    entry.foundation_id,
                    entry.audience,
                    entry.authority,
                    entry.title,
                    entry.summary,
                    *entry.related_paths,
                    *entry.reference_doc_paths,
                    *entry.internal_reference_paths,
                    *entry.external_reference_urls,
                    *entry.cited_by_paths,
                    *entry.applied_by_paths,
                    *entry.aliases,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].foundation_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
