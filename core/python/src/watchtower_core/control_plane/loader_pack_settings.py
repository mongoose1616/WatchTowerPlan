"""Pack-settings activation and path helpers for the control-plane loader."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any, cast

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader_constants import (
    CORE_PACK_SETTINGS_PATH,
    PACK_RUNTIME_MANIFEST_FILENAME,
    PACK_SETTINGS_PATH,
    VALIDATION_SUITE_REGISTRY_PATH,
    VALIDATOR_REGISTRY_PATH,
)
from watchtower_core.control_plane.pack_settings_discovery import (
    discover_pack_settings_paths,
)
from watchtower_core.control_plane.schemas import SCHEMA_CATALOG_ARTIFACT_PATH


def _activate_pack_settings(loader: Any, pack_settings_path: str) -> None:
    """Configure pack-aware validation surfaces for one active pack settings path."""

    pack_settings = loader.load_pack_settings(pack_settings_path)
    loader.active_pack_settings_path = pack_settings_path
    loader._active_pack_settings = pack_settings
    loader._active_surface_paths = {
        declaration.surface_name: declaration.path for declaration in pack_settings.surfaces
    }

    try:
        schema_catalog_path = pack_settings.get("schema_catalog").path
    except KeyError as exc:
        raise ValueError("Active pack settings must declare a schema_catalog surface.") from exc
    loader._active_schema_catalog_path = schema_catalog_path
    if schema_catalog_path != SCHEMA_CATALOG_ARTIFACT_PATH:
        loader.schema_store = loader.schema_store.with_additional_catalog_paths(
            (schema_catalog_path,)
        )
        loader.supplemental_schema_ids = loader.schema_store.supplemental_schema_ids

    try:
        validator_registry_path = pack_settings.get("validator_registry").path
    except KeyError as exc:
        raise ValueError("Active pack settings must declare a validator_registry surface.") from exc
    loader._active_validator_registry_path = validator_registry_path
    loader._active_validation_suite_registry_path = loader._active_surface_paths.get(
        "validation_suite_registry"
    )
    loader._active_documentation_family_registry_path = loader._active_surface_paths.get(
        "documentation_family_registry"
    )
    loader._active_template_catalog_path = loader._active_surface_paths.get("template_catalog")
    loader._active_artifact_family_registry_path = loader._active_surface_paths.get(
        "artifact_family_registry"
    )
    loader._active_lifecycle_stage_registry_path = loader._active_surface_paths.get(
        "lifecycle_stage_registry"
    )
    loader._active_review_status_registry_path = loader._active_surface_paths.get(
        "review_status_registry"
    )
    loader._active_source_type_registry_path = loader._active_surface_paths.get(
        "source_type_registry"
    )
    loader._active_promotion_policy_registry_path = loader._active_surface_paths.get(
        "promotion_policy_registry"
    )
    loader._active_project_surface_policy_registry_path = loader._active_surface_paths.get(
        "project_surface_policy_registry"
    )
    loader._active_human_surface_policy_registry_path = loader._active_surface_paths.get(
        "human_surface_policy_registry"
    )
    loader._active_retention_policy_registry_path = loader._active_surface_paths.get(
        "retention_policy_registry"
    )
    loader._active_artifact_index_path = loader._active_surface_paths.get("artifact_index")


def pack_runtime_manifest_path(
    loader: Any,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> str:
    """Return the hosted runtime-manifest path for one pack settings surface."""

    effective_pack_settings_path = loader.effective_pack_settings_path(pack_settings_path)
    default_path = str(
        PurePosixPath(effective_pack_settings_path).with_name(PACK_RUNTIME_MANIFEST_FILENAME)
    )
    try:
        pack_settings = loader.load_pack_settings(effective_pack_settings_path)
        registry_entry = loader.load_pack_registry().get_by_pack_id(pack_settings.pack_id)
    except (ArtifactLoadError, KeyError, ValueError):
        return default_path
    return cast(str, registry_entry.pack_runtime_manifest_path)


def _current_pack_settings_path(loader: Any, relative_path: str) -> str:
    """Resolve the effective pack-settings path for this loader instance."""

    if relative_path == PACK_SETTINGS_PATH and loader.active_pack_settings_path is not None:
        return cast(str, loader.active_pack_settings_path)
    if relative_path == PACK_SETTINGS_PATH:
        return cast(str, loader.default_pack_settings_path())
    return relative_path


def default_pack_settings_path(loader: Any) -> str:
    """Return the repository-default active pack-settings path for this loader."""

    if loader.active_pack_settings_path is not None:
        return cast(str, loader.active_pack_settings_path)
    registered_default = _registered_default_pack_settings_path(loader)
    if registered_default is not None:
        return registered_default
    discovered = loader._discover_default_pack_settings_path()
    return discovered or CORE_PACK_SETTINGS_PATH


def effective_pack_settings_path(
    loader: Any,
    relative_path: str = PACK_SETTINGS_PATH,
) -> str:
    """Resolve one requested pack-settings token into a concrete repository path."""

    return cast(str, loader._current_pack_settings_path(relative_path))


def _current_validator_registry_path(loader: Any) -> str:
    """Return the validator registry path active for this loader instance."""

    if loader._active_validator_registry_path is not None:
        return cast(str, loader._active_validator_registry_path)
    return cast(
        str,
        loader._default_pack_surface_path("validator_registry", VALIDATOR_REGISTRY_PATH),
    )


def _current_validation_suite_registry_path(loader: Any) -> str:
    """Return the validation-suite registry path active for this loader instance."""

    if loader._active_validation_suite_registry_path is not None:
        return cast(str, loader._active_validation_suite_registry_path)
    return cast(
        str,
        loader._default_pack_surface_path(
            "validation_suite_registry",
            VALIDATION_SUITE_REGISTRY_PATH,
        ),
    )


def _current_surface_path(
    loader: Any,
    surface_name: str,
    relative_path: str,
    *,
    default_path: str,
) -> str:
    """Return the active declared path for one surface or the provided default."""

    active_path = loader._active_surface_paths.get(surface_name)
    if active_path is not None and relative_path == default_path:
        return cast(str, active_path)
    if relative_path == default_path:
        return cast(str, loader._default_pack_surface_path(surface_name, default_path))
    return relative_path


def _required_surface_path(
    loader: Any,
    surface_name: str,
    relative_path: str | None = None,
) -> str:
    """Return one explicit path or the required active pack-declared path."""

    if relative_path is not None:
        return relative_path
    active_path = loader._active_surface_paths.get(surface_name)
    if active_path is not None:
        return cast(str, active_path)
    default_pack_settings = loader._current_pack_settings_path(PACK_SETTINGS_PATH)
    pack_settings = loader.load_pack_settings(default_pack_settings)
    try:
        declaration = pack_settings.get(surface_name)
    except KeyError as exc:
        raise ValueError(f"Active pack settings must declare a {surface_name} surface.") from exc
    loader._active_surface_paths[surface_name] = declaration.path
    return cast(str, declaration.path)


def _surface_name_for_active_path(loader: Any, relative_path: str) -> str | None:
    """Return the active declared surface name for one path, if any."""

    for surface_name, declared_path in loader._active_surface_paths.items():
        if relative_path == declared_path:
            return cast(str, surface_name)
    return None


def _default_pack_surface_path(loader: Any, surface_name: str, fallback_path: str) -> str:
    """Return one default-pack surface path when the default pack is available."""

    try:
        declaration = loader.load_pack_settings(PACK_SETTINGS_PATH).get(surface_name)
    except (ArtifactLoadError, KeyError, ValueError):
        return fallback_path
    return cast(str, declaration.path)


def _discover_default_pack_settings_path(loader: Any) -> str | None:
    """Discover one repo-local default pack settings path when available."""

    candidates = discover_pack_settings_paths(loader.repo_root)
    if not candidates:
        return None
    return candidates[0]


def _registered_default_pack_settings_path(loader: Any) -> str | None:
    """Return the valid registry-default pack settings path when one exists."""

    try:
        pack_settings_path = cast(
            str,
            loader.load_pack_registry().default_pack().pack_settings_path,
        )
        loader.load_pack_settings(pack_settings_path)
    except (ArtifactLoadError, KeyError, ValueError):
        return None
    return pack_settings_path
