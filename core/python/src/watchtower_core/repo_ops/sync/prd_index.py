"""Deterministic rebuild helpers for the PRD index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.adapters import extract_prefixed_ids
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.planning_documents import (
    PRD_OPTIONAL_EXPLAINED_SECTIONS,
    PRD_REQUIRED_SECTIONS,
    collect_reference_indicators,
    iter_markdown_documents,
    load_governed_document,
    ordered_unique,
)

PRD_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/prds/prd_index.v1.json"
PRD_FRONT_MATTER_SCHEMA_ID = "urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1"
PRD_DOC_ROOT = "docs/planning/prds"
PRD_EXCLUDED_NAMES = {"README.md", "prd_tracking.md"}


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    document = loader.load_json_object(PRD_INDEX_ARTIFACT_PATH)
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{PRD_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        prd_id = entry.get("prd_id")
        if isinstance(prd_id, str):
            existing[prd_id] = entry
    return existing


class PrdIndexSyncService:
    """Build and write the PRD index from governed PRD documents."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> PrdIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_entries = _load_existing_entries(self._loader)
        entries: list[dict[str, object]] = []

        for relative_path in iter_markdown_documents(
            self._repo_root,
            PRD_DOC_ROOT,
            excluded_names=PRD_EXCLUDED_NAMES,
        ):
            document = load_governed_document(
                self._loader,
                relative_path,
                schema_id=PRD_FRONT_MATTER_SCHEMA_ID,
                id_label="PRD ID",
                status_label="Status",
                required_sections=PRD_REQUIRED_SECTIONS,
                optional_explained_sections=PRD_OPTIONAL_EXPLAINED_SECTIONS,
            )
            current = existing_entries.get(document.document_id, {})
            (
                uses_internal_references,
                uses_external_references,
                internal_reference_paths,
                external_reference_urls,
            ) = collect_reference_indicators(
                document,
                self._repo_root,
                internal_sections=("Foundations References Applied", "References"),
                external_sections=("References",),
            )

            entry: dict[str, object] = {
                "trace_id": document.trace_id,
                "prd_id": document.document_id,
                "title": document.title,
                "summary": document.summary,
                "status": document.status,
                "doc_path": relative_path,
                "updated_at": document.updated_at,
                "uses_internal_references": uses_internal_references,
                "uses_external_references": uses_external_references,
            }

            requirement_ids = extract_prefixed_ids(document.sections["Requirements"], "req.")
            acceptance_ids = extract_prefixed_ids(
                document.sections["Acceptance Criteria"],
                "ac.",
            )
            linked_decision_ids = document.metadata_ids(
                "Linked Decisions",
                allowed_prefixes=("decision.",),
            )
            linked_design_ids = document.metadata_ids(
                "Linked Designs",
                allowed_prefixes=("design.features.",),
            )
            linked_plan_ids = document.metadata_ids(
                "Linked Implementation Plans",
                allowed_prefixes=("design.implementation.",),
            )
            related_paths = ordered_unique(
                document.front_matter_path_values(),
                _tuple_of_strings(current.get("related_paths")),
            )
            tags = ordered_unique(
                document.front_matter_list("tags"),
                _tuple_of_strings(current.get("tags")),
            )
            notes = _optional_string(current.get("notes"))

            if requirement_ids:
                entry["requirement_ids"] = list(requirement_ids)
            if acceptance_ids:
                entry["acceptance_ids"] = list(acceptance_ids)
            if linked_decision_ids:
                entry["linked_decision_ids"] = list(linked_decision_ids)
            if linked_design_ids:
                entry["linked_design_ids"] = list(linked_design_ids)
            if linked_plan_ids:
                entry["linked_plan_ids"] = list(linked_plan_ids)
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
            "$schema": "urn:watchtower:schema:artifacts:indexes:prd-index:v1",
            "id": "index.prds",
            "title": "PRD Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated PRD index to disk."""
        target = destination or (self._repo_root / PRD_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
