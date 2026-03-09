"""Index-backed query helpers for repository commands."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CommandIndexEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class CommandSearchParams:
    """Filter and ranking inputs for command lookup."""

    query: str | None = None
    kind: str | None = None
    tag: str | None = None
    limit: int | None = None


class CommandQueryService:
    """Search the command index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: CommandSearchParams) -> tuple[CommandIndexEntry, ...]:
        """Return command entries matching the requested filters."""
        index = self._loader.load_command_index()
        kind = params.kind.casefold() if params.kind is not None else None
        tag = params.tag.casefold() if params.tag is not None else None

        matches: list[tuple[int, CommandIndexEntry]] = []
        for entry in index.entries:
            if kind is not None and entry.kind.casefold() != kind:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue

            score = query_score(
                params.query,
                (
                    entry.command,
                    entry.command_id,
                    entry.kind,
                    entry.summary,
                    entry.synopsis,
                    *entry.aliases,
                    *entry.tags,
                    *(entry.output_formats or ()),
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].command))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
