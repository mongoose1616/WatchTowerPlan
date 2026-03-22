"""Typed document and directory helpers for the control-plane loader."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import PurePosixPath
from typing import Any, cast

from watchtower_core.control_plane.loader_constants import TArtifact


def iter_validated_documents_under(
    loader: Any,
    relative_directory: str,
) -> tuple[dict[str, Any], ...]:
    """Load and validate every JSON document directly under one governed directory."""

    return tuple(
        document
        for _, document in iter_validated_documents_with_paths_under(
            loader,
            relative_directory,
        )
    )


def iter_validated_documents_with_paths_under(
    loader: Any,
    relative_directory: str,
) -> tuple[tuple[str, dict[str, Any]], ...]:
    """Load and validate every JSON document directly under one governed directory."""

    override = loader._validated_directory_overrides.get(relative_directory)
    if override is not None:
        return cast(tuple[tuple[str, dict[str, Any]], ...], override)
    cached = loader._validated_directory_cache.get(relative_directory)
    if cached is not None:
        return cast(tuple[tuple[str, dict[str, Any]], ...], cached)
    documents_by_path: dict[str, dict[str, Any]] = dict(
        loader.artifact_source.iter_json_objects(relative_directory)
    )
    for relative_path, document in loader._validated_document_overrides.items():
        if _is_direct_child_of_directory(relative_directory, relative_path):
            documents_by_path[relative_path] = document

    documents: list[tuple[str, dict[str, Any]]] = []
    for relative_path in sorted(documents_by_path):
        document = documents_by_path[relative_path]
        loader.schema_store.validate_instance(document)
        documents.append((relative_path, document))
        loader._validated_document_cache[relative_path] = document
    cached_documents = tuple(documents)
    loader._validated_directory_cache[relative_directory] = cached_documents
    return cached_documents


def load_typed_document(
    loader: Any,
    relative_path: str,
    builder: Callable[[dict[str, Any]], TArtifact],
) -> TArtifact:
    """Load one typed governed document through the loader cache."""

    return _load_typed_document(loader, relative_path, builder)


def load_typed_directory(
    loader: Any,
    relative_directory: str,
    builder: Callable[[str, dict[str, Any]], TArtifact],
) -> tuple[TArtifact, ...]:
    """Load one typed governed directory through the loader cache."""

    return _load_typed_directory(loader, relative_directory, builder)


def _load_typed_document(
    loader: Any,
    relative_path: str,
    builder: Callable[[dict[str, Any]], TArtifact],
) -> TArtifact:
    """Materialize one typed artifact once per loader-backed command run."""

    cached = loader._typed_document_cache.get(relative_path)
    if cached is not None:
        return cast(TArtifact, cached)
    artifact = builder(loader.load_validated_document(relative_path))
    loader._typed_document_cache[relative_path] = artifact
    return artifact


def _load_typed_directory(
    loader: Any,
    relative_directory: str,
    builder: Callable[[str, dict[str, Any]], TArtifact],
) -> tuple[TArtifact, ...]:
    """Materialize one typed directory-backed artifact tuple once per loader run."""

    cached = loader._typed_directory_cache.get(relative_directory)
    if cached is not None:
        return cast(tuple[TArtifact, ...], cached)
    artifacts = tuple(
        builder(relative_path, document)
        for relative_path, document in loader.iter_validated_documents_with_paths_under(
            relative_directory
        )
    )
    loader._typed_directory_cache[relative_directory] = artifacts
    return artifacts


def _is_direct_child_of_directory(relative_directory: str, relative_path: str) -> bool:
    """Return whether one logical path is a direct child of the governed directory."""

    directory = PurePosixPath(relative_directory.rstrip("/"))
    candidate = PurePosixPath(relative_path)
    return candidate.parent == directory
