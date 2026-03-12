"""Shared helpers for repo-local reference-resolution reuse."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.reference_index import ReferenceIndexSyncService


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

    reference_document = ReferenceIndexSyncService(loader).build_document()
    return reference_urls_by_path_from_index_document(reference_document)
