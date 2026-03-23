"""Pack-aware validation context helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    PackSettings,
    PackWorkspaceRoots,
    SchemaCatalog,
    ValidationSuiteRegistry,
    ValidatorRegistry,
)

_REQUIRED_VALIDATION_SURFACE_NAMES = (
    "validator_registry",
    "validation_suite_registry",
)


@dataclass(frozen=True, slots=True)
class PackValidationContext:
    """Loaded pack context used by reusable-core validation services."""

    pack_root: Path
    pack_settings_path: str
    pack_settings: PackSettings
    workspace_roots: PackWorkspaceRoots
    loader: ControlPlaneLoader
    schema_catalog: SchemaCatalog
    validator_registry: ValidatorRegistry
    validation_suite_registry: ValidationSuiteRegistry
    surfaces: dict[str, object]

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> PackValidationContext:
        """Build a pack-aware validation context from one base loader."""

        effective_pack_settings_path = loader.activate_pack_settings(pack_settings_path)
        pack_settings = loader.load_pack_settings(effective_pack_settings_path)
        declared_surfaces = {
            declaration.surface_name: declaration for declaration in pack_settings.surfaces
        }
        surfaces: dict[str, object] = {
            "schema_catalog": loader.load_schema_catalog(),
        }
        for surface_name in _REQUIRED_VALIDATION_SURFACE_NAMES:
            declaration = declared_surfaces.get(surface_name)
            if declaration is None:
                continue
            surfaces[surface_name] = loader.load_declared_surface(
                surface_name=declaration.surface_name,
                relative_path=declaration.path,
            )

        return cls(
            pack_root=loader.resolve_path(pack_settings.workspace_roots.workspace_root),
            pack_settings_path=effective_pack_settings_path,
            pack_settings=pack_settings,
            workspace_roots=pack_settings.workspace_roots,
            loader=loader,
            schema_catalog=_require_surface(surfaces, "schema_catalog", SchemaCatalog),
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
            surfaces=surfaces,
        )


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
