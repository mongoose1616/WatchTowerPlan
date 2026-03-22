"""Cache and override helpers for :mod:`watchtower_core.control_plane.loader`."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader_constants import _KEEP_ACTIVE_PACK_SETTINGS

if TYPE_CHECKING:
    from watchtower_core.control_plane.loader import ControlPlaneLoader
    from watchtower_core.control_plane.workspace import ArtifactSource, ArtifactStore


def derive(
    loader: Any,
    *,
    artifact_source: ArtifactSource | None = None,
    artifact_store: ArtifactStore | None = None,
    active_pack_settings_path: str | None | object = _KEEP_ACTIVE_PACK_SETTINGS,
) -> ControlPlaneLoader:
    """Return a sibling loader that preserves current-run validated overrides."""

    effective_pack_settings_path = cast(
        str | None,
        (
            loader.active_pack_settings_path
            if active_pack_settings_path is _KEEP_ACTIVE_PACK_SETTINGS
            else active_pack_settings_path
        ),
    )
    from watchtower_core.control_plane.loader import ControlPlaneLoader

    derived = ControlPlaneLoader(
        workspace_config=loader.workspace_config,
        schema_store=loader.schema_store,
        artifact_source=artifact_source or loader.artifact_source,
        artifact_store=artifact_store or loader.artifact_store,
        active_pack_settings_path=effective_pack_settings_path,
    )
    derived._validated_document_overrides = dict(loader._validated_document_overrides)
    derived._validated_directory_overrides = {
        relative_directory: tuple(documents)
        for relative_directory, documents in loader._validated_directory_overrides.items()
    }
    return derived


def set_validated_document_override(
    loader: Any,
    relative_path: str,
    document: dict[str, Any],
) -> None:
    """Publish one current-run validated document for later loader reuse."""

    loader._validated_document_overrides[relative_path] = document
    loader._validated_document_cache[relative_path] = document
    loader._typed_document_cache.pop(relative_path, None)
    loader._invalidate_parent_directory_state(relative_path)


def set_validated_directory_override(
    loader: Any,
    relative_directory: str,
    documents: tuple[tuple[str, dict[str, Any]], ...],
) -> None:
    """Publish one current-run validated governed directory for later reuse."""

    previous_override = loader._validated_directory_overrides.get(relative_directory, ())
    previous_paths = {relative_path for relative_path, _ in previous_override}
    next_paths = {relative_path for relative_path, _ in documents}

    loader._validated_directory_overrides[relative_directory] = documents
    loader._validated_directory_cache[relative_directory] = documents
    loader._typed_directory_cache.pop(relative_directory, None)
    for relative_path, document in documents:
        loader._validated_document_overrides[relative_path] = document
        loader._validated_document_cache[relative_path] = document
        loader._typed_document_cache.pop(relative_path, None)

    for stale_relative_path in previous_paths.difference(next_paths):
        loader._validated_document_overrides.pop(stale_relative_path, None)
        loader._validated_document_cache.pop(stale_relative_path, None)
        loader._typed_document_cache.pop(stale_relative_path, None)


def _invalidate_parent_directory_state(loader: Any, relative_path: str) -> None:
    """Drop stale directory-level override and cache state after one document update."""

    stale_directories = tuple(
        relative_directory
        for relative_directory in {
            *loader._validated_directory_overrides,
            *loader._validated_directory_cache,
            *loader._typed_directory_cache,
        }
        if relative_path.startswith(f"{relative_directory.rstrip('/')}/")
    )
    for relative_directory in stale_directories:
        loader._validated_directory_overrides.pop(relative_directory, None)
        loader._validated_directory_cache.pop(relative_directory, None)
        loader._typed_directory_cache.pop(relative_directory, None)


def load_json_object(loader: Any, relative_path: str) -> dict[str, Any]:
    """Load a repository-relative JSON object."""

    effective_path = loader._current_pack_settings_path(relative_path)
    override = loader._validated_document_overrides.get(effective_path)
    if override is not None:
        return cast(dict[str, Any], override)
    try:
        return cast(dict[str, Any], loader.artifact_source.load_json_object(effective_path))
    except ArtifactLoadError:
        raise
    except FileNotFoundError as exc:
        raise ArtifactLoadError(f"Could not load governed artifact at {effective_path}") from exc


def resolve_path(loader: Any, relative_path: str) -> Path:
    """Resolve one repository-relative path through the current workspace mapping."""

    return cast(
        Path,
        loader.workspace_config.resolve_path(loader._current_pack_settings_path(relative_path)),
    )


def load_validated_document(loader: Any, relative_path: str) -> dict[str, Any]:
    """Load and validate a governed artifact that declares its own $schema."""

    effective_path = loader._current_pack_settings_path(relative_path)
    override = loader._validated_document_overrides.get(effective_path)
    if override is not None:
        return cast(dict[str, Any], override)
    cached = loader._validated_document_cache.get(effective_path)
    if cached is not None:
        return cast(dict[str, Any], cached)
    document = loader.load_json_object(effective_path)
    loader.schema_store.validate_instance(document)
    loader._validated_document_cache[effective_path] = document
    return cast(dict[str, Any], document)
