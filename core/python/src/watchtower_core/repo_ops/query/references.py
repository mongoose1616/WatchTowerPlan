"""Index-backed query helpers for reference documents."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ReferenceIndexEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class ReferenceSearchParams:
    """Filter and ranking inputs for reference lookup."""

    query: str | None = None
    reference_id: str | None = None
    tag: str | None = None
    related_path: str | None = None
    upstream_url: str | None = None
    cited_by_path: str | None = None
    applied_by_path: str | None = None
    limit: int | None = None


class ReferenceQueryService:
    """Search the reference index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: ReferenceSearchParams) -> tuple[ReferenceIndexEntry, ...]:
        """Return reference entries matching the requested filters."""
        index = self._loader.load_reference_index()
        reference_id = params.reference_id.casefold() if params.reference_id is not None else None
        tag = params.tag.casefold() if params.tag is not None else None
        related_path = params.related_path.casefold() if params.related_path is not None else None
        upstream_url = params.upstream_url.casefold() if params.upstream_url is not None else None
        cited_by_path = (
            params.cited_by_path.casefold() if params.cited_by_path is not None else None
        )
        applied_by_path = (
            params.applied_by_path.casefold() if params.applied_by_path is not None else None
        )

        matches: list[tuple[int, ReferenceIndexEntry]] = []
        for entry in index.entries:
            if reference_id is not None and entry.reference_id.casefold() != reference_id:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue
            if related_path is not None and related_path not in {
                value.casefold() for value in entry.related_paths
            }:
                continue
            if upstream_url is not None and upstream_url not in {
                value.casefold() for value in entry.canonical_upstream_urls
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
                    entry.reference_id,
                    entry.title,
                    entry.summary,
                    *entry.canonical_upstream_urls,
                    *entry.cited_by_paths,
                    *entry.applied_by_paths,
                    *entry.related_paths,
                    *entry.aliases,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].reference_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
