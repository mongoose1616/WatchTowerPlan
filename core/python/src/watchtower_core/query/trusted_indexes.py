"""Trusted typed-index loaders for read-only query and routing surfaces."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from watchtower_core.control_plane.loader import (
    ROUTE_INDEX_PATH,
    WORKFLOW_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_core.control_plane.models import RouteIndex, WorkflowIndex

_TRUSTED_CACHE_PREFIX = "__trusted_query_index__"


def load_trusted_route_index(loader: ControlPlaneLoader) -> RouteIndex:
    """Load the route index without per-read schema validation for query-only use."""

    return _load_trusted_typed_document(loader, ROUTE_INDEX_PATH, RouteIndex.from_document)


def load_trusted_workflow_index(loader: ControlPlaneLoader) -> WorkflowIndex:
    """Load the workflow index without per-read schema validation for query-only use."""

    return _load_trusted_typed_document(loader, WORKFLOW_INDEX_PATH, WorkflowIndex.from_document)


def _load_trusted_typed_document[TArtifact](
    loader: ControlPlaneLoader,
    relative_path: str,
    builder: Callable[[dict[str, Any]], TArtifact],
) -> TArtifact:
    cache_key = f"{_TRUSTED_CACHE_PREFIX}::{relative_path}"
    cached = loader._typed_document_cache.get(cache_key)
    if cached is not None:
        return cast(TArtifact, cached)
    artifact = builder(loader.load_json_object(relative_path))
    loader._typed_document_cache[cache_key] = artifact
    return artifact


__all__ = ["load_trusted_route_index", "load_trusted_workflow_index"]
