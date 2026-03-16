"""Pack-settings-driven governed surface loading for reusable core."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from watchtower_core.control_plane.models import (
    ActorRegistry,
    GovernanceSurfaceMap,
    PackSettings,
    PathPatternRegistry,
    SchemaCatalog,
    StatusRegistry,
)

if TYPE_CHECKING:
    from watchtower_core.control_plane.loader import ControlPlaneLoader


@dataclass(frozen=True, slots=True)
class PackContext:
    """Loaded pack context derived from pack settings plus declared governed surfaces."""

    pack_root: Path
    pack_settings_path: str
    pack_settings: PackSettings
    schema_catalog: SchemaCatalog
    governance_surface_map: GovernanceSurfaceMap
    path_pattern_registry: PathPatternRegistry
    status_registry: StatusRegistry
    actor_registry: ActorRegistry
    registries: dict[str, object]
    indexes: dict[str, object]
    surfaces: dict[str, object]

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str,
    ) -> PackContext:
        """Build one pack context by loading the declared pack settings and surfaces."""

        pack_settings = loader.load_pack_settings(pack_settings_path)
        surfaces: dict[str, object] = {}
        registries: dict[str, object] = {}
        indexes: dict[str, object] = {}
        for declaration in pack_settings.surfaces:
            surface = _load_declared_surface(loader, declaration.path)
            surfaces[declaration.surface_name] = surface
            if declaration.surface_kind == "registry":
                registries[declaration.surface_name] = surface
            elif declaration.surface_kind in {"artifact_index", "index"}:
                indexes[declaration.surface_name] = surface

        return cls(
            pack_root=loader.repo_root,
            pack_settings_path=pack_settings_path,
            pack_settings=pack_settings,
            schema_catalog=_require_surface(
                surfaces,
                "schema_catalog",
                SchemaCatalog,
            ),
            governance_surface_map=_require_surface(
                surfaces,
                "governance_surface_map",
                GovernanceSurfaceMap,
            ),
            path_pattern_registry=_require_surface(
                surfaces,
                "path_pattern_registry",
                PathPatternRegistry,
            ),
            status_registry=_require_surface(
                surfaces,
                "status_registry",
                StatusRegistry,
            ),
            actor_registry=_require_surface(
                surfaces,
                "actor_registry",
                ActorRegistry,
            ),
            registries=registries,
            indexes=indexes,
            surfaces=surfaces,
        )

    def get_surface(self, surface_name: str) -> object:
        """Return one loaded declared surface by name."""

        return self.surfaces[surface_name]


def _load_declared_surface(loader: ControlPlaneLoader, relative_path: str) -> object:
    """Load one declared surface through the loader's generic known-surface resolver."""

    return loader.load_known_surface(relative_path)


def _require_surface[TExpected](
    surfaces: dict[str, object],
    surface_name: str,
    expected_type: type[TExpected],
) -> TExpected:
    """Return one required surface and verify its runtime type."""

    try:
        surface = surfaces[surface_name]
    except KeyError as exc:
        raise ValueError(f"Pack settings are missing required surface: {surface_name}") from exc
    if not isinstance(surface, expected_type):
        raise ValueError(
            "Pack settings surface has the wrong runtime type: "
            f"{surface_name} is {type(surface).__name__}, expected {expected_type.__name__}"
        )
    return surface
