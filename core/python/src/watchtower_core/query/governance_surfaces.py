"""Export-safe governance-surface query helpers."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.governance_surfaces import (
    GovernanceSurfaceResolution,
    GovernanceSurfaceResolver,
)
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class GovernanceSurfaceSearchParams:
    """Filter and ranking inputs for governed surface lookup."""

    query: str | None = None
    surface_name: str | None = None
    surface_kind: str | None = None
    authority: str | None = None
    visibility: str | None = None
    declaration_source: str | None = None
    rebuildable: bool | None = None
    limit: int | None = None


class GovernanceSurfaceQueryService:
    """Search resolved governed pack surfaces across pack settings and governance maps."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> None:
        self._loader = loader
        self._pack_settings_path = pack_settings_path

    def search(
        self,
        params: GovernanceSurfaceSearchParams,
    ) -> tuple[GovernanceSurfaceResolution, ...]:
        """Return governed surfaces matching the requested filters."""

        resolver = GovernanceSurfaceResolver.from_loader(
            self._loader,
            pack_settings_path=self._pack_settings_path,
        )
        surface_name = params.surface_name.casefold() if params.surface_name is not None else None
        surface_kind = params.surface_kind.casefold() if params.surface_kind is not None else None
        authority = params.authority.casefold() if params.authority is not None else None
        visibility = params.visibility.casefold() if params.visibility is not None else None
        declaration_source = (
            params.declaration_source.casefold()
            if params.declaration_source is not None
            else None
        )

        matches: list[tuple[int, GovernanceSurfaceResolution]] = []
        for candidate_name in resolver.all_surface_names():
            resolution = resolver.resolve(candidate_name)
            if surface_name is not None and resolution.surface_name.casefold() != surface_name:
                continue
            if surface_kind is not None and resolution.surface_kind.casefold() != surface_kind:
                continue
            if authority is not None and resolution.authority.casefold() != authority:
                continue
            if visibility is not None and resolution.visibility.casefold() != visibility:
                continue
            if params.rebuildable is not None and resolution.rebuildable != params.rebuildable:
                continue
            if declaration_source is not None and declaration_source not in {
                source.casefold() for source in resolution.declaration_sources
            }:
                continue

            score = query_score(
                params.query,
                (
                    resolution.surface_name,
                    resolution.surface_kind,
                    resolution.path,
                    resolution.authority,
                    resolution.visibility,
                    resolution.builder or "",
                    resolution.source_surface or "",
                    *resolution.depends_on,
                    *resolution.declaration_sources,
                    *resolution.dependent_surface_names,
                ),
            )
            if score is None:
                continue
            matches.append((score, resolution))

        matches.sort(key=lambda item: (-item[0], item[1].surface_name))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)


__all__ = ["GovernanceSurfaceQueryService", "GovernanceSurfaceSearchParams"]
