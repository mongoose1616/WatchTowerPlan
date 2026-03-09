"""Deterministic rebuild helpers for the design-document index."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.planning_documents import (
    PlanningDocument,
    collect_reference_indicators,
    iter_markdown_documents,
    load_governed_document,
    ordered_unique,
)

DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/design_documents/design_document_index.v1.json"
)
FEATURE_DESIGN_FRONT_MATTER_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1"
)
IMPLEMENTATION_PLAN_FRONT_MATTER_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1"
)
FEATURE_DESIGN_ROOT = "docs/planning/design/features"
IMPLEMENTATION_PLAN_ROOT = "docs/planning/design/implementation"
DESIGN_EXCLUDED_NAMES = {"README.md"}


@dataclass(frozen=True, slots=True)
class DesignSourceRecord:
    """One governed design-family source document used to rebuild the index."""

    family: str
    document: PlanningDocument


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    document = loader.load_json_object(DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH)
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        document_id = entry.get("document_id")
        if isinstance(document_id, str):
            existing[document_id] = entry
    return existing


class DesignDocumentIndexSyncService:
    """Build and write the design-document index from governed design docs."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> DesignDocumentIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_entries = _load_existing_entries(self._loader)
        sources = self._load_sources()
        id_to_path = {
            source.document.document_id: source.document.relative_path
            for source in sources
        }
        entries: list[dict[str, object]] = []

        for source in sources:
            document = source.document
            current = existing_entries.get(document.document_id, {})
            (
                uses_internal_references,
                uses_external_references,
                internal_reference_paths,
                external_reference_urls,
            ) = collect_reference_indicators(
                document,
                self._repo_root,
                internal_sections=(
                    "Foundations References Applied",
                    "Internal Standards and Canonical References Applied",
                    "References",
                ),
                external_sections=("External Sources Consulted", "References"),
            )
            related_paths = ordered_unique(
                _mapped_design_ids(
                    document.metadata_ids(
                        "Linked Implementation Plans",
                        allowed_prefixes=("design.implementation.",),
                    ),
                    id_to_path,
                ),
                document.front_matter_path_values(),
                _tuple_of_strings(current.get("related_paths")),
            )
            tags = ordered_unique(
                document.front_matter_list("tags"),
                _tuple_of_strings(current.get("tags")),
            )
            notes = _optional_string(current.get("notes"))

            entry: dict[str, object] = {
                "document_id": document.document_id,
                "trace_id": document.trace_id,
                "family": source.family,
                "title": document.title,
                "summary": document.summary,
                "status": document.status,
                "doc_path": document.relative_path,
                "updated_at": document.updated_at,
                "uses_internal_references": uses_internal_references,
                "uses_external_references": uses_external_references,
            }

            if source.family == "implementation_plan":
                source_paths = _mapped_design_ids(
                    document.metadata_ids(
                        "Source Designs",
                        allowed_prefixes=("design.features.",),
                    ),
                    id_to_path,
                )
                if not source_paths:
                    raise ValueError(
                        f"{document.relative_path} is missing source design paths for its "
                        "implementation-plan index entry."
                    )
                entry["source_paths"] = list(source_paths)

            if related_paths:
                entry["related_paths"] = list(related_paths)
            if internal_reference_paths:
                entry["internal_reference_paths"] = list(internal_reference_paths)
            if external_reference_urls:
                entry["external_reference_urls"] = list(external_reference_urls)
            if tags:
                entry["tags"] = list(tags)
            if notes is not None:
                entry["notes"] = notes

            entries.append(entry)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:design-document-index:v1",
            "id": "index.design_documents",
            "title": "Design Document Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated design-document index to disk."""
        target = destination or (self._repo_root / DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _load_sources(self) -> tuple[DesignSourceRecord, ...]:
        sources: list[DesignSourceRecord] = []

        for relative_path in iter_markdown_documents(
            self._repo_root,
            FEATURE_DESIGN_ROOT,
            excluded_names=DESIGN_EXCLUDED_NAMES,
        ):
            sources.append(
                DesignSourceRecord(
                    family="feature_design",
                    document=load_governed_document(
                        self._loader,
                        relative_path,
                        schema_id=FEATURE_DESIGN_FRONT_MATTER_SCHEMA_ID,
                        id_label="Design ID",
                        status_label="Design Status",
                        required_sections=(
                            "Foundations References Applied",
                            "Internal Standards and Canonical References Applied",
                            "References",
                        ),
                        required_explained_sections=(
                            "Foundations References Applied",
                            "Internal Standards and Canonical References Applied",
                        ),
                        require_updated_at_section=True,
                    ),
                )
            )

        for relative_path in iter_markdown_documents(
            self._repo_root,
            IMPLEMENTATION_PLAN_ROOT,
            excluded_names=DESIGN_EXCLUDED_NAMES,
        ):
            sources.append(
                DesignSourceRecord(
                    family="implementation_plan",
                    document=load_governed_document(
                        self._loader,
                        relative_path,
                        schema_id=IMPLEMENTATION_PLAN_FRONT_MATTER_SCHEMA_ID,
                        id_label="Plan ID",
                        status_label="Plan Status",
                        required_sections=(
                            "Internal Standards and Canonical References Applied",
                            "References",
                        ),
                        required_explained_sections=(
                            "Internal Standards and Canonical References Applied",
                        ),
                        require_updated_at_section=True,
                    ),
                )
            )

        return tuple(sources)


def _mapped_design_ids(ids: tuple[str, ...], id_to_path: dict[str, str]) -> tuple[str, ...]:
    paths: list[str] = []
    for document_id in ids:
        path = id_to_path.get(document_id)
        if path is None:
            raise ValueError(f"Unknown design document ID referenced in metadata: {document_id}")
        paths.append(path)
    return tuple(paths)


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
