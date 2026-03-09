"""Deterministic rebuild helpers for the decision index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.adapters import extract_path_like_references
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.planning_documents import (
    iter_markdown_documents,
    load_governed_document,
    ordered_unique,
)

DECISION_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/decisions/decision_index.v1.json"
DECISION_FRONT_MATTER_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1"
)
DECISION_DOC_ROOT = "docs/planning/decisions"
DECISION_EXCLUDED_NAMES = {"README.md", "decision_tracking.md"}
ALLOWED_DECISION_STATUSES = {"proposed", "accepted", "deferred", "rejected", "superseded"}


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    document = loader.load_validated_document(DECISION_INDEX_ARTIFACT_PATH)
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{DECISION_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        decision_id = entry.get("decision_id")
        if isinstance(decision_id, str):
            existing[decision_id] = entry
    return existing


class DecisionIndexSyncService:
    """Build and write the decision index from governed decision records."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> DecisionIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_entries = _load_existing_entries(self._loader)
        entries: list[dict[str, object]] = []

        for relative_path in iter_markdown_documents(
            self._repo_root,
            DECISION_DOC_ROOT,
            excluded_names=DECISION_EXCLUDED_NAMES,
        ):
            document = load_governed_document(
                self._loader,
                relative_path,
                schema_id=DECISION_FRONT_MATTER_SCHEMA_ID,
                id_label="Decision ID",
                status_label="Record Status",
            )
            current = existing_entries.get(document.document_id, {})

            decision_status = document.metadata_scalar("Decision Status")
            if decision_status not in ALLOWED_DECISION_STATUSES:
                allowed = ", ".join(sorted(ALLOWED_DECISION_STATUSES))
                raise ValueError(
                    f"{relative_path} has unsupported Decision Status {decision_status!r}. "
                    f"Allowed values: {allowed}"
                )

            affected_paths = tuple(
                value
                for value in extract_path_like_references(document.sections["Affected Surfaces"])
                if value != relative_path
            )
            related_paths = ordered_unique(
                document.front_matter_path_values(),
                affected_paths,
                _tuple_of_strings(current.get("related_paths")),
            )
            tags = ordered_unique(
                document.front_matter_list("tags"),
                _tuple_of_strings(current.get("tags")),
            )
            notes = _optional_string(current.get("notes"))

            entry: dict[str, object] = {
                "trace_id": document.trace_id,
                "decision_id": document.document_id,
                "title": document.title,
                "summary": document.summary,
                "record_status": document.status,
                "decision_status": decision_status,
                "doc_path": relative_path,
                "updated_at": document.updated_at,
            }

            linked_prd_ids = document.metadata_ids(
                "Linked PRDs",
                allowed_prefixes=("prd.",),
            )
            linked_design_ids = document.metadata_ids(
                "Linked Designs",
                allowed_prefixes=("design.features.",),
            )
            linked_plan_ids = document.metadata_ids(
                "Linked Implementation Plans",
                allowed_prefixes=("design.implementation.",),
            )

            if linked_prd_ids:
                entry["linked_prd_ids"] = list(linked_prd_ids)
            if linked_design_ids:
                entry["linked_design_ids"] = list(linked_design_ids)
            if linked_plan_ids:
                entry["linked_plan_ids"] = list(linked_plan_ids)
            if related_paths:
                entry["related_paths"] = list(related_paths)
            if tags:
                entry["tags"] = list(tags)
            if notes is not None:
                entry["notes"] = notes

            entries.append(entry)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:decision-index:v1",
            "id": "index.decisions",
            "title": "Decision Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated decision index to disk."""
        target = destination or (self._repo_root / DECISION_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
