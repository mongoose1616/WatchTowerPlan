"""Pack-settings-driven governed surface loading for reusable core."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.models import (
    ActorRegistry,
    GovernanceSurfaceMap,
    PackSurfaceDeclaration,
    PackSettings,
    PackWorkspaceRoots,
    PathPatternRegistry,
    SchemaCatalog,
    StatusRegistry,
    ValidationSuiteRegistry,
    ValidatorRegistry,
)

if TYPE_CHECKING:
    from watchtower_core.control_plane.loader import ControlPlaneLoader


@dataclass(frozen=True, slots=True)
class PackContext:
    """Loaded pack context derived from pack settings plus declared governed surfaces."""

    pack_root: Path
    pack_settings_path: str
    pack_settings: PackSettings
    workspace_roots: PackWorkspaceRoots
    schema_catalog: SchemaCatalog
    validator_registry: ValidatorRegistry
    validation_suite_registry: ValidationSuiteRegistry
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

        effective_pack_settings_path = loader.effective_pack_settings_path(pack_settings_path)
        effective_loader = (
            loader
            if loader.active_pack_settings_path == effective_pack_settings_path
            else loader.derive(active_pack_settings_path=effective_pack_settings_path)
        )

        pack_settings = effective_loader.load_pack_settings(effective_pack_settings_path)
        surfaces: dict[str, object] = {}
        registries: dict[str, object] = {}
        indexes: dict[str, object] = {}
        for declaration in pack_settings.surfaces:
            if not _should_eager_load_surface(declaration):
                continue
            try:
                surface = _load_declared_surface(
                    effective_loader,
                    surface_name=declaration.surface_name,
                    relative_path=declaration.path,
                )
            except ArtifactLoadError:
                if declaration.rebuildable is not True or declaration.authority != "derived":
                    raise
                continue
            surfaces[declaration.surface_name] = surface
            if declaration.surface_kind == "registry":
                registries[declaration.surface_name] = surface
            elif declaration.surface_kind in {"artifact_index", "index"}:
                indexes[declaration.surface_name] = surface

        return cls(
            pack_root=effective_loader.resolve_path(pack_settings.workspace_roots.workspace_root),
            pack_settings_path=effective_pack_settings_path,
            pack_settings=pack_settings,
            workspace_roots=pack_settings.workspace_roots,
            schema_catalog=_require_surface(
                surfaces,
                "schema_catalog",
                SchemaCatalog,
            ),
            validator_registry=_require_surface(
                surfaces,
                "validator_registry",
                ValidatorRegistry,
            ),
            validation_suite_registry=_require_surface(
                surfaces,
                "validation_suite_registry",
                ValidationSuiteRegistry,
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


def _load_declared_surface(
    loader: ControlPlaneLoader,
    *,
    surface_name: str,
    relative_path: str,
) -> object:
    """Load one declared surface through the loader's declaration-aware resolver."""

    if surface_name == "schema_catalog":
        return loader.load_schema_catalog()
    return loader.load_declared_surface(
        surface_name=surface_name,
        relative_path=relative_path,
    )


def _should_eager_load_surface(declaration: PackSurfaceDeclaration) -> bool:
    """Return whether pack-context construction should eagerly load one surface.

    Pack context is consumed by reusable-core helpers such as terminology, template,
    and policy resolution. Those helpers need stable pack-owned governance surfaces,
    not rebuildable derived indexes from a live domain workspace.
    """

    if declaration.authority == "derived" and declaration.rebuildable is True:
        return False
    return True


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
