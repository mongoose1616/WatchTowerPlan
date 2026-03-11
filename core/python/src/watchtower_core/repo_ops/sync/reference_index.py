"""Deterministic rebuild helpers for the reference index."""

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
from watchtower_core.repo_ops.markdown_semantics import (
    validate_blank_line_before_heading_after_list,
)
from watchtower_core.repo_ops.planning_documents import (
    ordered_unique,
    validate_required_section_order,
)

REFERENCE_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/references/reference_index.v1.json"
REFERENCE_FRONT_MATTER_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
)
REFERENCE_DOC_ROOT = "docs/references"
REFERENCE_EXCLUDED_NAMES = {"README.md", "AGENTS.md"}


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    try:
        document = loader.load_validated_document(REFERENCE_INDEX_ARTIFACT_PATH)
    except ArtifactLoadError:
        return {}

    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{REFERENCE_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        reference_id = entry.get("reference_id")
        if isinstance(reference_id, str):
            existing[reference_id] = entry
    return existing


class ReferenceIndexSyncService:
    """Build and write the reference index from governed reference documents."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> ReferenceIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_entries = _load_existing_entries(self._loader)
        citation_maps = self._build_citation_maps()
        entries: list[dict[str, object]] = []

        docs_root = self._repo_root / REFERENCE_DOC_ROOT
        for path in sorted(docs_root.glob("*.md")):
            if path.name in REFERENCE_EXCLUDED_NAMES:
                continue

            relative_path = path.relative_to(self._repo_root).as_posix()
            front_matter = load_front_matter(path)
            self._loader.schema_store.validate_instance(
                front_matter,
                schema_id=REFERENCE_FRONT_MATTER_SCHEMA_ID,
            )

            markdown = load_markdown_body(path)
            validate_blank_line_before_heading_after_list(relative_path, markdown)
            title = extract_title(markdown)
            if title != front_matter["title"]:
                raise ValueError(
                    f"{relative_path} H1 title does not match front matter title: "
                    f"{title!r} != {front_matter['title']!r}"
                )

            sections = extract_sections(markdown)
            required_sections = (
                "Canonical Upstream",
                "Quick Reference or Distilled Reference",
                "References",
                "Updated At",
            )
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

            canonical_upstream_urls = extract_external_urls(sections["Canonical Upstream"])
            if not canonical_upstream_urls:
                raise ValueError(
                    f"{relative_path} Canonical Upstream section does not publish any external URL."
                )

            current = existing_entries.get(front_matter["id"], {})
            related_paths = ordered_unique(
                _front_matter_path_values(front_matter, relative_path),
                extract_repo_path_references(
                    sections.get("Local Mapping in This Repository", ""),
                    self._repo_root,
                    source_path=path,
                ),
                extract_repo_path_references(
                    sections["References"],
                    self._repo_root,
                    source_path=path,
                ),
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
                "reference_id": front_matter["id"],
                "title": front_matter["title"],
                "summary": front_matter["summary"],
                "status": front_matter["status"],
                "doc_path": relative_path,
                "updated_at": updated_at,
                "uses_internal_references": bool(related_paths),
                "uses_external_references": True,
                "canonical_upstream_urls": list(canonical_upstream_urls),
            }
            cited_by_paths = citation_maps["cited_by"].get(relative_path, ())
            applied_by_paths = citation_maps["applied_by"].get(relative_path, ())
            if cited_by_paths:
                entry["cited_by_paths"] = list(cited_by_paths)
            if applied_by_paths:
                entry["applied_by_paths"] = list(applied_by_paths)
            if related_paths:
                entry["related_paths"] = list(related_paths)
            if aliases:
                entry["aliases"] = list(aliases)
            if tags:
                entry["tags"] = list(tags)
            if notes is not None:
                entry["notes"] = notes

            entries.append(entry)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:reference-index:v1",
            "id": "index.references",
            "title": "Reference Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated reference index to disk."""
        target = destination or (self._repo_root / REFERENCE_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _build_citation_maps(self) -> dict[str, dict[str, tuple[str, ...]]]:
        reference_targets = self._load_reference_targets()
        cited_by: dict[str, set[str]] = {path: set() for path in reference_targets}
        applied_by: dict[str, set[str]] = {path: set() for path in reference_targets}

        for (
            relative_path,
            cited_paths,
            cited_urls,
            applied_paths,
            applied_urls,
        ) in iter_citation_audit_documents(self._repo_root):
            for reference_path, canonical_urls in reference_targets.items():
                canonical_url_set = set(canonical_urls)
                if reference_path in cited_paths or canonical_url_set.intersection(cited_urls):
                    cited_by[reference_path].add(relative_path)
                if reference_path in applied_paths or canonical_url_set.intersection(applied_urls):
                    applied_by[reference_path].add(relative_path)

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

    def _load_reference_targets(self) -> dict[str, tuple[str, ...]]:
        targets: dict[str, tuple[str, ...]] = {}
        docs_root = self._repo_root / REFERENCE_DOC_ROOT
        for path in sorted(docs_root.glob("*.md")):
            if path.name in REFERENCE_EXCLUDED_NAMES:
                continue
            relative_path = path.relative_to(self._repo_root).as_posix()
            markdown = load_markdown_body(path)
            sections = extract_sections(markdown)
            canonical_upstream_urls = extract_external_urls(sections.get("Canonical Upstream", ""))
            targets[relative_path] = canonical_upstream_urls
        return targets


def _front_matter_list(front_matter: dict[str, Any], key: str) -> tuple[str, ...]:
    value = front_matter.get(key)
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"Reference front matter key {key} must be a YAML list when present.")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"Reference front matter key {key} must contain only strings.")
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


CITATION_AUDIT_FAMILIES: tuple[tuple[str, set[str], tuple[str, ...], tuple[str, ...]], ...] = (
    (
        "docs/foundations",
        {"README.md"},
        ("References",),
        (),
    ),
    (
        "docs/standards",
        {"README.md"},
        ("Related Standards and Sources", "References"),
        ("Related Standards and Sources",),
    ),
    (
        "docs/planning/design/features",
        {"README.md"},
        (
            "Foundations References Applied",
            "Internal Standards and Canonical References Applied",
            "External Sources Consulted",
            "References",
        ),
        (
            "Foundations References Applied",
            "Internal Standards and Canonical References Applied",
            "External Sources Consulted",
        ),
    ),
    (
        "docs/planning/design/implementation",
        {"README.md"},
        ("Internal Standards and Canonical References Applied", "References"),
        ("Internal Standards and Canonical References Applied",),
    ),
    (
        "docs/planning/prds",
        {"README.md", "prd_tracking.md"},
        ("Foundations References Applied", "References"),
        ("Foundations References Applied",),
    ),
    (
        "docs/planning/decisions",
        {"README.md", "decision_tracking.md"},
        ("Applied References and Implications", "References"),
        ("Applied References and Implications",),
    ),
    (
        "workflows/modules",
        {"README.md"},
        ("Additional Files to Load",),
        ("Additional Files to Load",),
    ),
)


def iter_citation_audit_documents(
    repo_root: Path,
) -> tuple[tuple[str, set[str], set[str], set[str], set[str]], ...]:
    documents: list[tuple[str, set[str], set[str], set[str], set[str]]] = []
    for (
        relative_directory,
        excluded_names,
        cited_sections,
        applied_sections,
    ) in CITATION_AUDIT_FAMILIES:
        directory = repo_root / relative_directory
        for path in sorted(directory.rglob("*.md")):
            if path.name in excluded_names:
                continue
            relative_path = path.relative_to(repo_root).as_posix()
            markdown = load_markdown_body(path)
            sections = extract_sections(markdown)
            cited_paths: set[str] = set()
            cited_urls: set[str] = set()
            applied_paths: set[str] = set()
            applied_urls: set[str] = set()
            for title in cited_sections:
                section = sections.get(title)
                if section is None:
                    continue
                cited_paths.update(
                    extract_repo_path_references(
                        section,
                        repo_root,
                        source_path=path,
                    )
                )
                cited_urls.update(extract_external_urls(section))
            for title in applied_sections:
                section = sections.get(title)
                if section is None:
                    continue
                applied_paths.update(
                    extract_repo_path_references(
                        section,
                        repo_root,
                        source_path=path,
                    )
                )
                applied_urls.update(extract_external_urls(section))
            documents.append((relative_path, cited_paths, cited_urls, applied_paths, applied_urls))
    return tuple(documents)
