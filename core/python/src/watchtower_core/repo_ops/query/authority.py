"""Registry-backed query helpers for canonical planning and governance surfaces."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import AuthorityMapEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class AuthorityMapSearchParams:
    """Filter and ranking inputs for authority-map lookup."""

    query: str | None = None
    question_id: str | None = None
    domain: str | None = None
    artifact_kind: str | None = None
    limit: int | None = None


class AuthorityMapQueryService:
    """Search the authority map for canonical planning and governance surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: AuthorityMapSearchParams) -> tuple[AuthorityMapEntry, ...]:
        """Return authority-map entries matching the requested filters."""
        authority_map = self._loader.load_authority_map()
        question_id = params.question_id.casefold() if params.question_id is not None else None
        domain = params.domain.casefold() if params.domain is not None else None
        artifact_kind = (
            params.artifact_kind.casefold() if params.artifact_kind is not None else None
        )

        matches: list[tuple[int, AuthorityMapEntry]] = []
        for entry in authority_map.entries:
            if question_id is not None and entry.question_id.casefold() != question_id:
                continue
            if domain is not None and entry.domain.casefold() != domain:
                continue
            if artifact_kind is not None and entry.artifact_kind.casefold() != artifact_kind:
                continue

            score = query_score(
                params.query,
                (
                    entry.question_id,
                    entry.domain,
                    entry.question,
                    entry.status,
                    entry.artifact_kind,
                    entry.canonical_path,
                    entry.preferred_command,
                    entry.preferred_human_path or "",
                    *entry.status_fields,
                    *entry.fallback_paths,
                    *entry.aliases,
                    entry.notes or "",
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].question_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)
