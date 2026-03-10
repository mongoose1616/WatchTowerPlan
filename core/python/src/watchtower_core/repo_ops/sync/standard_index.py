"""Deterministic rebuild helpers for the standard index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.adapters import (
    extract_external_urls,
    extract_repo_path_references,
    extract_sections,
    extract_title,
    extract_updated_at_from_section,
    load_front_matter,
    load_markdown_body,
)
from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.planning_documents import (
    ordered_unique,
    validate_explained_bullet_section,
    validate_required_section_order,
)
from watchtower_core.repo_ops.sync.reference_index import ReferenceIndexSyncService

STANDARD_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/standards/standard_index.v1.json"
STANDARD_FRONT_MATTER_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1"
)
STANDARD_DOC_ROOT = "docs/standards"
STANDARD_EXCLUDED_NAMES = {"README.md"}


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    try:
        document = loader.load_validated_document(STANDARD_INDEX_ARTIFACT_PATH)
    except ArtifactLoadError:
        return {}
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{STANDARD_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        standard_id = entry.get("standard_id")
        if isinstance(standard_id, str):
            existing[standard_id] = entry
    return existing


class StandardIndexSyncService:
    """Build and write the standard index from governed standards."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> StandardIndexSyncService:
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

        standards_root = self._repo_root / STANDARD_DOC_ROOT
        for path in sorted(standards_root.rglob("*.md")):
            if path.name in STANDARD_EXCLUDED_NAMES:
                continue

            relative_path = path.relative_to(self._repo_root).as_posix()
            front_matter = load_front_matter(path)
            self._loader.schema_store.validate_instance(
                front_matter,
                schema_id=STANDARD_FRONT_MATTER_SCHEMA_ID,
            )

            markdown = load_markdown_body(path)
            visible_title = extract_title(markdown)
            if visible_title != front_matter["title"]:
                raise ValueError(
                    f"{relative_path} H1 title does not match front matter title: "
                    f"{visible_title!r} != {front_matter['title']!r}"
                )

            sections = extract_sections(markdown)
            required_sections = ("Related Standards and Sources", "References", "Updated At")
            missing_sections = [section for section in required_sections if section not in sections]
            if missing_sections:
                joined = ", ".join(missing_sections)
                raise ValueError(f"{relative_path} is missing required sections: {joined}")
            validate_required_section_order(relative_path, sections, required_sections)
            validate_explained_bullet_section(
                relative_path,
                "Related Standards and Sources",
                sections["Related Standards and Sources"],
            )

            updated_at = front_matter["updated_at"]
            if extract_updated_at_from_section(sections["Updated At"]) != updated_at:
                raise ValueError(
                    f"{relative_path} Updated At section does not match front matter updated_at."
                )

            current = existing_entries.get(front_matter["id"], {})
            internal_reference_paths = ordered_unique(
                extract_repo_path_references(
                    sections["Related Standards and Sources"],
                    self._repo_root,
                ),
                extract_repo_path_references(sections["References"], self._repo_root),
            )
            applied_reference_paths = ordered_unique(
                extract_repo_path_references(
                    sections["Related Standards and Sources"],
                    self._repo_root,
                )
            )
            reference_doc_paths = tuple(
                value for value in internal_reference_paths if value.startswith("docs/references/")
            )
            direct_external_urls = ordered_unique(
                extract_external_urls(sections["Related Standards and Sources"]),
                extract_external_urls(sections["References"]),
            )
            applied_direct_external_urls = ordered_unique(
                extract_external_urls(sections["Related Standards and Sources"])
            )
            applied_reference_doc_paths = tuple(
                value for value in applied_reference_paths if value.startswith("docs/references/")
            )
            transitive_external_urls = ordered_unique(
                *(
                    reference_urls_by_path.get(reference_path, ())
                    for reference_path in reference_doc_paths
                )
            )
            applied_transitive_external_urls = ordered_unique(
                *(
                    reference_urls_by_path.get(reference_path, ())
                    for reference_path in applied_reference_doc_paths
                )
            )
            external_reference_urls = ordered_unique(
                direct_external_urls,
                transitive_external_urls,
            )
            applied_external_reference_urls = ordered_unique(
                applied_direct_external_urls,
                applied_transitive_external_urls,
            )
            if direct_external_urls and not reference_doc_paths:
                raise ValueError(
                    f"{relative_path} cites external authority directly but does not cite a "
                    "governed local reference doc under docs/references/."
                )

            related_paths = ordered_unique(
                _front_matter_path_values(front_matter, relative_path),
                _tuple_of_strings(current.get("related_paths")),
            )
            tags = ordered_unique(
                _front_matter_list(front_matter, "tags"),
                _tuple_of_strings(current.get("tags")),
            )
            notes = _optional_string(current.get("notes"))
            category = Path(relative_path).parts[2]

            entry: dict[str, object] = {
                "standard_id": front_matter["id"],
                "category": category,
                "title": front_matter["title"],
                "summary": front_matter["summary"],
                "status": front_matter["status"],
                "doc_path": relative_path,
                "updated_at": updated_at,
                "uses_internal_references": bool(internal_reference_paths),
                "uses_external_references": bool(external_reference_urls),
            }
            if related_paths:
                entry["related_paths"] = list(related_paths)
            if reference_doc_paths:
                entry["reference_doc_paths"] = list(reference_doc_paths)
            if internal_reference_paths:
                entry["internal_reference_paths"] = list(internal_reference_paths)
            if applied_reference_paths:
                entry["applied_reference_paths"] = list(applied_reference_paths)
            if external_reference_urls:
                entry["external_reference_urls"] = list(external_reference_urls)
            if applied_external_reference_urls:
                entry["applied_external_reference_urls"] = list(applied_external_reference_urls)
            if tags:
                entry["tags"] = list(tags)
            if notes is not None:
                entry["notes"] = notes

            entries.append(entry)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:standard-index:v1",
            "id": "index.standards",
            "title": "Standard Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated standard index to disk."""
        target = destination or (self._repo_root / STANDARD_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target


def _front_matter_list(front_matter: dict[str, Any], key: str) -> tuple[str, ...]:
    value = front_matter.get(key)
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"Standard front matter key {key} must be a YAML list when present.")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"Standard front matter key {key} must contain only strings.")
        items.append(item.strip())
    return tuple(items)


def _front_matter_path_values(front_matter: dict[str, Any], relative_path: str) -> tuple[str, ...]:
    return tuple(
        value
        for value in _front_matter_list(front_matter, "applies_to")
        if "/" in value and value != relative_path
    )


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
