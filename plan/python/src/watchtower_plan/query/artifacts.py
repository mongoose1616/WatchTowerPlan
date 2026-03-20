"""Query helpers for the live plan artifact index."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ArtifactIndexEntry
from watchtower_plan.artifact_index import search_artifact_entries


@dataclass(frozen=True, slots=True)
class ArtifactSearchParams:
    """Filter and ranking inputs for artifact-index lookup."""

    query: str | None = None
    artifact_id: str | None = None
    artifact_family: str | None = None
    context_id: str | None = None
    source_context: str | None = None
    source_channel: str | None = None
    status: str | None = None
    authoritative: bool | None = None
    derived: bool | None = None
    hidden: bool | None = None
    limit: int | None = None


class ArtifactQueryService:
    """Search the live plan artifact index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: ArtifactSearchParams) -> tuple[ArtifactIndexEntry, ...]:
        """Return artifact-index entries matching the requested filters."""

        return search_artifact_entries(
            self._loader.load_artifact_index().artifacts,
            query=params.query,
            artifact_id=params.artifact_id,
            artifact_family=params.artifact_family,
            context_id=params.context_id,
            source_context=params.source_context,
            source_channel=params.source_channel,
            status=params.status,
            authoritative=params.authoritative,
            derived=params.derived,
            hidden=params.hidden,
            limit=params.limit,
        )
