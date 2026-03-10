"""Index-backed query helpers for repository path entries."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import RepositoryPathEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class RepositoryPathSearchParams:
    """Filter and ranking inputs for repository path lookup."""

    query: str | None = None
    surface_kind: str | None = None
    maturity: str | None = None
    priority: str | None = None
    audience_hint: str | None = None
    tag: str | None = None
    parent_path: str | None = None
    limit: int | None = None


_MATURITY_BONUS = {"authoritative": 8, "supporting": 3, "scaffold": 0}
_PRIORITY_BONUS = {"high": 3, "medium": 1, "low": 0}


class RepositoryPathQueryService:
    """Search the repository path index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: RepositoryPathSearchParams) -> tuple[RepositoryPathEntry, ...]:
        """Return repository path entries matching the requested filters."""
        index = self._loader.load_repository_path_index()
        tag = params.tag.casefold() if params.tag is not None else None
        surface_kind = params.surface_kind.casefold() if params.surface_kind is not None else None
        maturity = params.maturity.casefold() if params.maturity is not None else None
        priority = params.priority.casefold() if params.priority is not None else None
        audience_hint = (
            params.audience_hint.casefold() if params.audience_hint is not None else None
        )
        parent_path = params.parent_path

        matches: list[tuple[int, RepositoryPathEntry]] = []
        for entry in index.entries:
            if surface_kind is not None and entry.surface_kind.casefold() != surface_kind:
                continue
            if maturity is not None and entry.maturity.casefold() != maturity:
                continue
            if priority is not None and entry.priority.casefold() != priority:
                continue
            if audience_hint is not None and entry.audience_hint.casefold() != audience_hint:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue
            if parent_path is not None and entry.parent_path != parent_path:
                continue

            score = query_score(
                params.query,
                (
                    entry.path,
                    entry.surface_kind,
                    entry.maturity,
                    entry.priority,
                    entry.audience_hint,
                    entry.summary,
                    *entry.aliases,
                    *entry.tags,
                    *entry.related_paths,
                ),
            )
            if score is None:
                continue
            score += _MATURITY_BONUS.get(entry.maturity, 0)
            score += _PRIORITY_BONUS.get(entry.priority, 0)
            matches.append((score, entry))

        matches.sort(
            key=lambda item: (
                -item[0],
                -_MATURITY_BONUS.get(item[1].maturity, 0),
                -_PRIORITY_BONUS.get(item[1].priority, 0),
                item[1].path,
            )
        )
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
