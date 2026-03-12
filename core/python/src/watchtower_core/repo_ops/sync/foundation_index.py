"""Deterministic rebuild helpers for the foundation index."""

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
from watchtower_core.repo_ops.front_matter_paths import (
    applies_to_path_values,
    normalize_front_matter_applies_to,
)
from watchtower_core.repo_ops.markdown_semantics import (
    validate_blank_line_before_heading_after_list,
)
from watchtower_core.repo_ops.planning_documents import (
    ordered_unique,
    validate_required_section_order,
)
from watchtower_core.repo_ops.sync.reference_index import (
    ReferenceIndexSyncService,
    iter_citation_audit_documents,
)

FOUNDATION_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/foundations/foundation_index.v1.json"
)
FOUNDATION_FRONT_MATTER_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:documentation:foundation-front-matter:v1"
)
FOUNDATION_DOC_ROOT = "docs/foundations"
FOUNDATION_EXCLUDED_NAMES = {"README.md"}


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    try:
        document = loader.load_json_object(FOUNDATION_INDEX_ARTIFACT_PATH)
    except ArtifactLoadError:
        return {}

    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{FOUNDATION_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        foundation_id = entry.get("foundation_id")
        if isinstance(foundation_id, str):
            existing[foundation_id] = entry
    return existing


class FoundationIndexSyncService:
    """Build and write the foundation index from governed foundation documents."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> FoundationIndexSyncService:
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
        citation_maps = self._build_citation_maps()
        entries: list[dict[str, object]] = []

        foundations_root = self._repo_root / FOUNDATION_DOC_ROOT
        for path in sorted(foundations_root.glob("*.md")):
            if path.name in FOUNDATION_EXCLUDED_NAMES:
                continue

            relative_path = path.relative_to(self._repo_root).as_posix()
            front_matter = load_front_matter(path)
            self._loader.schema_store.validate_instance(
                front_matter,
                schema_id=FOUNDATION_FRONT_MATTER_SCHEMA_ID,
            )
            applies_to = normalize_front_matter_applies_to(
                front_matter,
                relative_path=relative_path,
                repo_root=self._repo_root,
            )
            if applies_to:
                front_matter["applies_to"] = list(applies_to)

            markdown = load_markdown_body(path)
            validate_blank_line_before_heading_after_list(relative_path, markdown)
            visible_title = extract_title(markdown)
            if visible_title != front_matter["title"]:
                raise ValueError(
                    f"{relative_path} H1 title does not match front matter title: "
                    f"{visible_title!r} != {front_matter['title']!r}"
                )

            sections = extract_sections(markdown)
            required_sections = ("References", "Updated At")
            missing_sections = [section for section in required_sections if section not in sections]
            if missing_sections:
                joined = ", ".join(missing_sections)
                raise ValueError(f"{relative_path} is missing required sections: {joined}")
            validate_required_section_order(relative_path, sections, required_sections)

            updated_at = front_matter["updated_at"]
            if extract_updated_at_from_section(sections["Updated At"]) != updated_at:
                raise ValueError(
                    f"{relative_path} Updated At section does not match front matter updated_at."
                )

            current = existing_entries.get(front_matter["id"], {})
            internal_reference_paths = ordered_unique(
                extract_repo_path_references(
                    sections["References"],
                    self._repo_root,
                    source_path=path,
                )
            )
            reference_doc_paths = tuple(
                value for value in internal_reference_paths if value.startswith("docs/references/")
            )
            direct_external_urls = ordered_unique(extract_external_urls(sections["References"]))
            transitive_external_urls = ordered_unique(
                *(
                    reference_urls_by_path.get(reference_path, ())
                    for reference_path in reference_doc_paths
                )
            )
            external_reference_urls = ordered_unique(
                direct_external_urls,
                transitive_external_urls,
            )
            related_paths = ordered_unique(
                applies_to_path_values(applies_to, relative_path=relative_path),
                _tuple_of_strings(current.get("related_paths")),
            )
            aliases = ordered_unique(
                _front_matter_list(front_matter, "aliases"),
                _tuple_of_strings(current.get("aliases")),
            )
            tags = ordered_unique(
                _front_matter_list(front_matter, "tags"),
                _tuple_of_strings(current.get("tags")),
            )
            notes = _optional_string(current.get("notes"))

            entry: dict[str, object] = {
                "foundation_id": front_matter["id"],
                "title": front_matter["title"],
                "summary": front_matter["summary"],
                "status": front_matter["status"],
                "audience": front_matter["audience"],
                "authority": front_matter["authority"],
                "doc_path": relative_path,
                "updated_at": updated_at,
                "uses_internal_references": bool(internal_reference_paths),
                "uses_external_references": bool(external_reference_urls),
            }
            cited_by_paths = citation_maps["cited_by"].get(relative_path, ())
            applied_by_paths = citation_maps["applied_by"].get(relative_path, ())
            if related_paths:
                entry["related_paths"] = list(related_paths)
            if reference_doc_paths:
                entry["reference_doc_paths"] = list(reference_doc_paths)
            if internal_reference_paths:
                entry["internal_reference_paths"] = list(internal_reference_paths)
            if external_reference_urls:
                entry["external_reference_urls"] = list(external_reference_urls)
            if cited_by_paths:
                entry["cited_by_paths"] = list(cited_by_paths)
            if applied_by_paths:
                entry["applied_by_paths"] = list(applied_by_paths)
            if aliases:
                entry["aliases"] = list(aliases)
            if tags:
                entry["tags"] = list(tags)
            if notes is not None:
                entry["notes"] = notes

            entries.append(entry)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:foundation-index:v1",
            "id": "index.foundations",
            "title": "Foundation Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated foundation index to disk."""
        target = destination or (self._repo_root / FOUNDATION_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _build_citation_maps(self) -> dict[str, dict[str, tuple[str, ...]]]:
        foundation_paths = self._load_foundation_paths()
        cited_by: dict[str, set[str]] = {path: set() for path in foundation_paths}
        applied_by: dict[str, set[str]] = {path: set() for path in foundation_paths}

        for relative_path, cited_paths, _, applied_paths, _ in iter_citation_audit_documents(
            self._repo_root
        ):
            for foundation_path in foundation_paths:
                if foundation_path in cited_paths:
                    cited_by[foundation_path].add(relative_path)
                if foundation_path in applied_paths:
                    applied_by[foundation_path].add(relative_path)

        return {
            "cited_by": {
                path: tuple(sorted(values))
                for path, values in cited_by.items()
                if values
            },
            "applied_by": {
                path: tuple(sorted(values))
                for path, values in applied_by.items()
                if values
            },
        }

    def _load_foundation_paths(self) -> tuple[str, ...]:
        return tuple(
            path.relative_to(self._repo_root).as_posix()
            for path in sorted((self._repo_root / FOUNDATION_DOC_ROOT).glob("*.md"))
            if path.name not in FOUNDATION_EXCLUDED_NAMES
        )


def _front_matter_list(front_matter: dict[str, Any], key: str) -> tuple[str, ...]:
    value = front_matter.get(key)
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"Foundation front matter key {key} must be a YAML list when present.")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"Foundation front matter key {key} must contain only strings.")
        items.append(item.strip())
    return tuple(items)


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
