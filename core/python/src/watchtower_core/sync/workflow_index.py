"""Deterministic rebuild helpers for the workflow index."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.adapters import (
    extract_external_urls,
    extract_first_paragraph,
    extract_repo_path_references,
    extract_sections,
    extract_title,
    load_markdown_body,
)
from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.planning_documents import (
    ordered_unique,
    validate_explained_bullet_section,
    validate_required_section_order,
)
from watchtower_core.sync.reference_index import ReferenceIndexSyncService

WORKFLOW_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/workflows/workflow_index.v1.json"
WORKFLOW_DOC_ROOT = "workflows/modules"
WORKFLOW_EXCLUDED_NAMES = {"README.md"}
WORKFLOW_REQUIRED_SECTIONS = (
    "Purpose",
    "Use When",
    "Inputs",
    "Related Standards and Sources",
    "Workflow",
    "Data Structure",
    "Outputs",
    "Done When",
)


@dataclass(frozen=True, slots=True)
class WorkflowDocument:
    """Parsed and validated workflow module used for indexing and validation."""

    workflow_id: str
    title: str
    summary: str
    relative_path: str
    uses_internal_references: bool
    uses_external_references: bool
    related_paths: tuple[str, ...]
    reference_doc_paths: tuple[str, ...]
    internal_reference_paths: tuple[str, ...]
    external_reference_urls: tuple[str, ...]


def load_workflow_document(loader: ControlPlaneLoader, relative_path: str) -> WorkflowDocument:
    """Load and validate one workflow module from its repository-relative path."""
    reference_document = ReferenceIndexSyncService(loader).build_document()
    reference_entries = reference_document.get("entries")
    if not isinstance(reference_entries, list):
        raise ValueError("Generated reference index is missing its entries list.")
    reference_urls_by_path = {
        entry["doc_path"]: tuple(entry.get("canonical_upstream_urls", ()))
        for entry in reference_entries
        if isinstance(entry, dict) and isinstance(entry.get("doc_path"), str)
    }
    return load_workflow_document_with_reference_map(
        loader,
        relative_path,
        reference_urls_by_path=reference_urls_by_path,
    )


def load_workflow_document_with_reference_map(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    reference_urls_by_path: dict[str, tuple[str, ...]],
) -> WorkflowDocument:
    """Load and validate one workflow module using a prebuilt reference-url map."""
    path = loader.repo_root / relative_path
    markdown = load_markdown_body(path)
    title = extract_title(markdown)
    sections = extract_sections(markdown)

    missing_sections = [
        section for section in WORKFLOW_REQUIRED_SECTIONS if section not in sections
    ]
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{relative_path} is missing required sections: {joined}")
    validate_required_section_order(relative_path, sections, WORKFLOW_REQUIRED_SECTIONS)
    validate_explained_bullet_section(
        relative_path,
        "Related Standards and Sources",
        sections["Related Standards and Sources"],
    )
    if not title.endswith(" Workflow"):
        raise ValueError(f"{relative_path} workflow title must end with ' Workflow'.")

    summary = extract_first_paragraph(sections["Purpose"])
    internal_reference_paths = ordered_unique(
        extract_repo_path_references(sections["Related Standards and Sources"], loader.repo_root)
    )
    reference_doc_paths = tuple(
        value for value in internal_reference_paths if value.startswith("docs/references/")
    )

    direct_external_urls = ordered_unique(
        extract_external_urls(sections["Related Standards and Sources"])
    )
    transitive_external_urls = ordered_unique(
        *(
            reference_urls_by_path.get(reference_path, ())
            for reference_path in reference_doc_paths
        )
    )
    external_reference_urls = ordered_unique(direct_external_urls, transitive_external_urls)
    if direct_external_urls and not reference_doc_paths:
        raise ValueError(
            f"{relative_path} cites external authority directly but does not cite a governed "
            "local reference doc under docs/references/."
        )

    return WorkflowDocument(
        workflow_id=f"workflow.{Path(relative_path).stem}",
        title=title,
        summary=summary,
        relative_path=relative_path,
        uses_internal_references=bool(internal_reference_paths),
        uses_external_references=bool(external_reference_urls),
        related_paths=internal_reference_paths,
        reference_doc_paths=reference_doc_paths,
        internal_reference_paths=internal_reference_paths,
        external_reference_urls=external_reference_urls,
    )


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    try:
        document = loader.load_validated_document(WORKFLOW_INDEX_ARTIFACT_PATH)
    except ArtifactLoadError:
        return {}

    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{WORKFLOW_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        workflow_id = entry.get("workflow_id")
        if isinstance(workflow_id, str):
            existing[workflow_id] = entry
    return existing


class WorkflowIndexSyncService:
    """Build and write the workflow index from workflow modules."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> WorkflowIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_entries = _load_existing_entries(self._loader)
        reference_document = ReferenceIndexSyncService(self._loader).build_document()
        reference_entries = reference_document.get("entries")
        if not isinstance(reference_entries, list):
            raise ValueError("Generated reference index is missing its entries list.")
        reference_urls_by_path = {
            entry["doc_path"]: tuple(entry.get("canonical_upstream_urls", ()))
            for entry in reference_entries
            if isinstance(entry, dict) and isinstance(entry.get("doc_path"), str)
        }
        entries: list[dict[str, object]] = []

        workflow_root = self._repo_root / WORKFLOW_DOC_ROOT
        for path in sorted(workflow_root.glob("*.md")):
            if path.name in WORKFLOW_EXCLUDED_NAMES:
                continue

            relative_path = path.relative_to(self._repo_root).as_posix()
            workflow = load_workflow_document_with_reference_map(
                self._loader,
                relative_path,
                reference_urls_by_path=reference_urls_by_path,
            )
            current = existing_entries.get(workflow.workflow_id, {})
            aliases = ordered_unique(_tuple_of_strings(current.get("aliases")))
            tags = ordered_unique(_tuple_of_strings(current.get("tags")))
            notes = _optional_string(current.get("notes"))

            entry: dict[str, object] = {
                "workflow_id": workflow.workflow_id,
                "title": workflow.title,
                "summary": workflow.summary,
                "status": "active",
                "doc_path": workflow.relative_path,
                "uses_internal_references": workflow.uses_internal_references,
                "uses_external_references": workflow.uses_external_references,
            }
            if workflow.related_paths:
                entry["related_paths"] = list(workflow.related_paths)
            if workflow.reference_doc_paths:
                entry["reference_doc_paths"] = list(workflow.reference_doc_paths)
            if workflow.internal_reference_paths:
                entry["internal_reference_paths"] = list(workflow.internal_reference_paths)
            if workflow.external_reference_urls:
                entry["external_reference_urls"] = list(workflow.external_reference_urls)
            if aliases:
                entry["aliases"] = list(aliases)
            if tags:
                entry["tags"] = list(tags)
            if notes is not None:
                entry["notes"] = notes

            entries.append(entry)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:workflow-index:v1",
            "id": "index.workflows",
            "title": "Workflow Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated workflow index to disk."""
        target = destination or (self._repo_root / WORKFLOW_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
