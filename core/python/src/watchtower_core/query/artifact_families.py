"""Export-safe artifact-family query helpers."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.artifact_family import ArtifactFamilyHelper, ArtifactFamilyIssue
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import ArtifactFamilyEntry, ArtifactFamilyRegistry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class ArtifactFamilySearchParams:
    """Filter and ranking inputs for artifact-family lookup."""

    query: str | None = None
    family_id: str | None = None
    status_field: str | None = None
    visibility: str | None = None
    renderable: bool | None = None
    derived_index_id: str | None = None
    relative_path: str | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class ArtifactFamilyPathResolution:
    """Path resolution result for one repository-relative artifact path."""

    relative_path: str
    matches: tuple[ArtifactFamilyEntry, ...]
    issues: tuple[ArtifactFamilyIssue, ...]

    @property
    def best_match(self) -> ArtifactFamilyEntry | None:
        """Return the most-specific matching family, if any."""

        if not self.matches:
            return None
        return self.matches[0]


class ArtifactFamilyQueryService:
    """Search and resolve governed artifact-family metadata for one pack."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> None:
        self._loader = loader
        self._pack_settings_path = pack_settings_path

    def search(self, params: ArtifactFamilySearchParams) -> tuple[ArtifactFamilyEntry, ...]:
        """Return artifact families matching the requested filters."""

        registry = self._registry()
        helper = self._helper()
        family_id = params.family_id.casefold() if params.family_id is not None else None
        status_field = params.status_field.casefold() if params.status_field is not None else None
        visibility = params.visibility.casefold() if params.visibility is not None else None
        derived_index_id = (
            params.derived_index_id.casefold()
            if params.derived_index_id is not None
            else None
        )

        candidates = (
            helper.families_for_path(params.relative_path)
            if params.relative_path is not None
            else registry.entries
        )
        matches: list[tuple[int, ArtifactFamilyEntry]] = []
        for entry in candidates:
            if family_id is not None and entry.family_id.casefold() != family_id:
                continue
            if status_field is not None and entry.status_field.casefold() != status_field:
                continue
            if visibility is not None and entry.visibility.casefold() != visibility:
                continue
            if params.renderable is not None and entry.renderable != params.renderable:
                continue
            if derived_index_id is not None and derived_index_id not in {
                value.casefold() for value in entry.derived_index_ids
            }:
                continue

            score = query_score(
                params.query,
                (
                    entry.family_id,
                    entry.entry_status,
                    entry.summary,
                    entry.canonical_schema_id,
                    entry.status_field,
                    entry.visibility,
                    *entry.placement_roots,
                    *entry.allowed_status_values,
                    *entry.rendered_companion_surface_ids,
                    *entry.derived_index_ids,
                    entry.notes or "",
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].family_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)

    def resolve_path(self, relative_path: str) -> ArtifactFamilyPathResolution:
        """Resolve one repository-relative path against the governed artifact families."""

        helper = self._helper()
        normalized_path = relative_path.strip().strip("/")
        return ArtifactFamilyPathResolution(
            relative_path=normalized_path,
            matches=helper.families_for_path(normalized_path),
            issues=helper.validate_relative_path(normalized_path),
        )

    def _helper(self) -> ArtifactFamilyHelper:
        return ArtifactFamilyHelper.from_loader(
            self._loader,
            pack_settings_path=self._pack_settings_path,
        )

    def _registry(self) -> ArtifactFamilyRegistry:
        context = self._loader.load_pack_context(self._pack_settings_path)
        registry = context.registries.get("artifact_family_registry")
        if not isinstance(registry, ArtifactFamilyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed artifact_family_registry."
            )
        return registry


__all__ = [
    "ArtifactFamilyPathResolution",
    "ArtifactFamilyQueryService",
    "ArtifactFamilySearchParams",
]
