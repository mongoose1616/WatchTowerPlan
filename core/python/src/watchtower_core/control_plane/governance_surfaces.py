"""Helpers for resolving governed surfaces across pack settings and governance maps."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    GovernanceSurfaceMap,
    PackSettings,
    PackSurfaceDeclaration,
)


@dataclass(frozen=True, slots=True)
class GovernanceSurfaceResolution:
    """One resolved governed surface with its effective declaration metadata."""

    surface_name: str
    surface_kind: str
    path: str
    authority: str
    visibility: str
    rebuildable: bool
    depends_on: tuple[str, ...]
    builder: str | None
    source_surface: str | None
    declaration_sources: tuple[str, ...]
    dependent_surface_names: tuple[str, ...]

    @property
    def authoritative(self) -> bool:
        """Return whether this resolved surface is authoritative."""

        return self.authority == "authoritative"


class GovernanceSurfaceResolver:
    """Resolve governed surfaces through pack settings plus the governance surface map."""

    def __init__(
        self,
        *,
        pack_settings: PackSettings,
        governance_surface_map: GovernanceSurfaceMap,
    ) -> None:
        self._pack_settings = pack_settings
        self._governance_surface_map = governance_surface_map

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> GovernanceSurfaceResolver:
        """Build one resolver from a loader and pack-settings path."""

        return cls(
            pack_settings=loader.load_pack_settings(pack_settings_path),
            governance_surface_map=loader.load_governance_surface_map(),
        )

    def resolve(self, surface_name: str) -> GovernanceSurfaceResolution:
        """Resolve one governed surface by name."""

        declarations = self._declarations_for_surface(surface_name)
        if not declarations:
            raise KeyError(surface_name)
        primary = _choose_primary(declarations)
        dependent_surface_names = tuple(
            sorted(
                {
                    declaration.surface_name
                    for _, declaration in self._all_declarations()
                    if declaration.surface_name != surface_name
                    and (
                        declaration.source_surface == surface_name
                        or surface_name in declaration.depends_on
                    )
                }
            )
        )
        return GovernanceSurfaceResolution(
            surface_name=primary.surface_name,
            surface_kind=primary.surface_kind,
            path=primary.path,
            authority=primary.authority,
            visibility=primary.visibility,
            rebuildable=bool(primary.rebuildable),
            depends_on=primary.depends_on,
            builder=primary.builder,
            source_surface=primary.source_surface,
            declaration_sources=tuple(source for source, _ in declarations),
            dependent_surface_names=dependent_surface_names,
        )

    def all_surface_names(self) -> tuple[str, ...]:
        """Return the combined governed surface names visible to this resolver."""

        return tuple(
            sorted({declaration.surface_name for _, declaration in self._all_declarations()})
        )

    def _all_declarations(self) -> tuple[tuple[str, PackSurfaceDeclaration], ...]:
        return (
            tuple(
                ("pack_settings", declaration) for declaration in self._pack_settings.surfaces
            )
            + tuple(
                ("governance_surface_map", declaration)
                for declaration in self._governance_surface_map.surfaces
            )
        )

    def _declarations_for_surface(
        self,
        surface_name: str,
    ) -> tuple[tuple[str, PackSurfaceDeclaration], ...]:
        return tuple(
            (source, declaration)
            for source, declaration in self._all_declarations()
            if declaration.surface_name == surface_name
        )


def _choose_primary(
    declarations: tuple[tuple[str, PackSurfaceDeclaration], ...]
) -> PackSurfaceDeclaration:
    for source, declaration in declarations:
        if source == "pack_settings":
            return declaration
    return declarations[0][1]


__all__ = ["GovernanceSurfaceResolution", "GovernanceSurfaceResolver"]
