"""Deterministic rebuild helpers for the repository path index."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import RepositoryPathEntry
from watchtower_core.control_plane.paths import discover_repo_root

REPOSITORY_PATH_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/repository_paths/repository_path_index.v1.json"
)


@dataclass(frozen=True, slots=True)
class InventoryRow:
    """One README inventory row used to derive a path entry."""

    path: str
    summary: str


def _clean_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def _parse_inventory_rows(readme_path: Path) -> list[InventoryRow]:
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    rows: list[InventoryRow] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() != "| Path | Description |":
            index += 1
            continue
        if index + 1 >= len(lines) or not lines[index + 1].startswith("|---|---|"):
            index += 1
            continue
        index += 2
        while index < len(lines) and lines[index].startswith("|"):
            parts = [part.strip() for part in lines[index].split("|")]
            if len(parts) >= 4:
                path = _clean_cell(parts[1])
                summary = _clean_cell(parts[2])
                if path and summary:
                    rows.append(InventoryRow(path=path, summary=summary))
            index += 1
    return rows


def _kind_for_path(repo_root: Path, relative_path: str) -> str:
    if relative_path.endswith("/"):
        return "directory"
    resolved = repo_root / relative_path
    if resolved.is_dir():
        return "directory"
    return "file"


def _parent_path(relative_path: str) -> str:
    normalized = relative_path.rstrip("/")
    if "/" not in normalized:
        return "."
    parent = normalized.rsplit("/", 1)[0]
    if relative_path.endswith("/"):
        return f"{parent}/"
    return f"{parent}/"


def _surface_kind(relative_path: str, kind: str) -> str:
    if relative_path == "README.md":
        return "root_readme"
    if relative_path.endswith("AGENTS.md"):
        return "instruction"
    if relative_path == "workflows/ROUTING_TABLE.md":
        return "routing_table"
    if relative_path.startswith("workflows/modules/"):
        return "workflow_module" if kind == "file" else "workflow_family"
    if relative_path.startswith("docs/commands/"):
        return "command_doc" if kind == "file" else "command_docs"
    if relative_path.startswith("docs/planning/prds/"):
        if relative_path.endswith("prd_tracking.md"):
            return "prd_tracker"
        return "prd" if kind == "file" else "prd_docs"
    if relative_path.startswith("docs/planning/decisions/"):
        if relative_path.endswith("decision_tracking.md"):
            return "decision_tracker"
        return "decision_record" if kind == "file" else "decision_docs"
    if relative_path.startswith("docs/planning/design/features/"):
        return "feature_design" if kind == "file" else "design_docs"
    if relative_path.startswith("docs/planning/design/implementation/"):
        return "implementation_plan" if kind == "file" else "design_docs"
    if relative_path == "docs/planning/design/design_tracking.md":
        return "design_tracker"
    if relative_path.startswith("docs/planning/"):
        return "planning_root" if kind == "directory" else "planning_doc"
    if relative_path.startswith("docs/references/"):
        return "reference_doc" if kind == "file" else "reference"
    if relative_path.startswith("docs/standards/"):
        return "standard_doc" if kind == "file" else "standards"
    if relative_path.startswith("docs/templates/"):
        return "template_doc" if kind == "file" else "templates"
    if relative_path.startswith("docs/foundations/"):
        return "foundation_doc" if kind == "file" else "documentation_family"
    if relative_path.startswith("docs/"):
        return "documentation" if kind == "directory" else "documentation_file"
    if relative_path == "core/python/":
        return "python_workspace"
    if relative_path.startswith("core/python/src/"):
        return "python_source" if kind == "directory" else "python_source_file"
    if relative_path.startswith("core/python/tests/"):
        return "python_tests" if kind == "directory" else "python_test_file"
    if relative_path.startswith("core/python/"):
        return "python_workspace_file" if kind == "file" else "python_workspace"
    if relative_path == "core/control_plane/":
        return "control_plane"
    if relative_path.startswith("core/control_plane/schemas/"):
        return "control_plane_schema" if kind == "file" else "control_plane_schemas"
    if relative_path.startswith("core/control_plane/registries/"):
        return "control_plane_registry" if kind == "file" else "control_plane_registries"
    if relative_path.startswith("core/control_plane/contracts/"):
        return "control_plane_contract" if kind == "file" else "control_plane_contracts"
    if relative_path.startswith("core/control_plane/policies/"):
        return "control_plane_policy" if kind == "file" else "control_plane_policies"
    if relative_path.startswith("core/control_plane/examples/"):
        return "control_plane_example" if kind == "file" else "control_plane_examples"
    if relative_path.startswith("core/control_plane/indexes/"):
        return "control_plane_index" if kind == "file" else "control_plane_indexes"
    if relative_path.startswith("core/control_plane/ledgers/"):
        return "control_plane_ledger" if kind == "file" else "control_plane_ledgers"
    if relative_path.startswith("core/control_plane/"):
        return "control_plane_file" if kind == "file" else "control_plane_family"
    if relative_path.startswith("core/"):
        return "core_surface" if kind == "directory" else "core_file"
    return "repository_surface" if kind == "directory" else "repository_file"


def _entry_to_document(entry: RepositoryPathEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "path": entry.path,
        "kind": entry.kind,
        "surface_kind": entry.surface_kind,
        "summary": entry.summary,
        "parent_path": entry.parent_path,
    }
    if entry.aliases:
        document["aliases"] = list(entry.aliases)
    if entry.tags:
        document["tags"] = list(entry.tags)
    if entry.related_paths:
        document["related_paths"] = list(entry.related_paths)
    return document


class RepositoryPathIndexSyncService:
    """Build and write the curated repository path index from README inventories."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> RepositoryPathIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_index = self._loader.load_repository_path_index()
        existing_entries = {entry.path: entry for entry in existing_index.entries}
        derived_entries: dict[str, RepositoryPathEntry] = {}

        for readme_path in sorted(self._repo_root.rglob("README.md")):
            if any(part.startswith(".") for part in readme_path.relative_to(self._repo_root).parts):
                continue
            for row in _parse_inventory_rows(readme_path):
                resolved_path = self._repo_root / row.path.rstrip("/")
                directory_path = self._repo_root / row.path
                if not resolved_path.exists() and not directory_path.exists():
                    continue

                kind = _kind_for_path(self._repo_root, row.path)
                current = existing_entries.get(row.path)
                derived_entries[row.path] = RepositoryPathEntry(
                    path=row.path,
                    kind=kind,
                    surface_kind=_surface_kind(row.path, kind),
                    summary=row.summary,
                    parent_path=_parent_path(row.path),
                    aliases=current.aliases if current is not None else (),
                    tags=current.tags if current is not None else (),
                    related_paths=current.related_paths if current is not None else (),
                )

        entries = [
            _entry_to_document(derived_entries[path])
            for path in sorted(derived_entries)
        ]
        return {
            "$schema": "urn:watchtower:schema:artifacts:indexes:repository-path-index:v1",
            "id": "index.repository_paths",
            "title": "Repository Path Index",
            "status": "active",
            "coverage_mode": "entrypoints",
            "root_path": ".",
            "entries": entries,
        }

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated path index to disk."""
        target = destination or (self._repo_root / REPOSITORY_PATH_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
