"""Shared helpers for governed reference-resolution reuse."""

from __future__ import annotations

from typing import cast

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.cache import (
    prepare_document_sync_cache,
    validate_prepared_document_sync_cache,
)
from watchtower_core.sync.reference_index import ReferenceIndexSyncService


def reference_urls_by_path_from_index_document(
    document: dict[str, object],
) -> dict[str, tuple[str, ...]]:
    """Return canonical upstream URLs keyed by reference document path."""

    reference_entries = document.get("entries")
    if not isinstance(reference_entries, list):
        raise ValueError("Generated reference index is missing its entries list.")
    return {
        entry["doc_path"]: tuple(entry.get("canonical_upstream_urls", ()))
        for entry in reference_entries
        if isinstance(entry, dict) and isinstance(entry.get("doc_path"), str)
    }


def build_reference_urls_by_path(
    loader: ControlPlaneLoader,
) -> dict[str, tuple[str, ...]]:
    """Build a fresh reference-resolution map from the governed reference corpus."""

    service = ReferenceIndexSyncService(loader)
    prepared_cache = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )
    validated_cache = validate_prepared_document_sync_cache(loader, prepared_cache)
    if validated_cache is None:
        raise RuntimeError("Reference-index cache preparation unexpectedly returned no state.")
    reference_document = (
        cast(dict[str, object], validated_cache.document) or service.build_document()
    )
    return reference_urls_by_path_from_index_document(reference_document)
