from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import StandardIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_standard_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = StandardIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["standard_id"] == "std.governance.github_collaboration"
        and entry["owner"] == "repository_maintainer"
        and ".github/" in entry.get("applies_to", [])
        and entry["uses_external_references"] is True
        and "workflow" in entry.get("operationalization_modes", [])
        and ".github/" in entry.get("operationalization_paths", [])
        and "docs/references/github_collaboration_reference.md"
        in entry.get("reference_doc_paths", [])
        for entry in entries
    )
    readme_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.documentation.readme_md"
    )
    assert "README.md" in readme_entry.get("operationalization_paths", [])
    assert "**/README.md" in readme_entry.get("operationalization_paths", [])

    agents_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.documentation.agents_md"
    )
    assert "AGENTS.md" in agents_entry.get("operationalization_paths", [])
    assert "**/AGENTS.md" in agents_entry.get("operationalization_paths", [])

    reference_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.documentation.reference_md"
    )
    assert "docs/references/*_reference.md" in reference_entry.get(
        "operationalization_paths",
        [],
    )

    standard_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.documentation.standard_md"
    )
    assert "docs/standards/*/*_standard.md" in standard_entry.get(
        "operationalization_paths",
        [],
    )


def test_standard_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = StandardIndexSyncService(loader)
    output_path = tmp_path / "standard_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.standards"


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _write_repo_file(path: Path, content: str = "# Placeholder\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_reference_fixture(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        dedent(
            """\
            ---
            id: "ref.example"
            title: "Example Reference"
            summary: "Provides one governed local reference for standard-index tests."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:36:00Z"
            audience: "shared"
            authority: "supporting"
            ---

            # Example Reference

            ## Canonical Upstream
            - [Example upstream](https://example.com/reference)

            ## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## References
            - [README.md](../README.md)

            ## Updated At
            - `2026-03-11T17:36:00Z`
            """
        ),
        encoding="utf-8",
    )


def test_standard_index_sync_extracts_document_relative_reference_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "docs/README.md")
    reference_path = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        dedent(
            """\
            ---
            id: "std.documentation.example"
            title: "Example Standard"
            summary: "Exercises document-relative reference extraction for the standard index."
            type: "standard"
            status: "active"
            tags:
              - "standard"
              - "documentation"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:36:00Z"
            audience: "shared"
            authority: "authoritative"
            ---

            # Example Standard

            ## Summary
            Exercises document-relative reference extraction for the standard index.

            ## Purpose
            Keep the fixture focused on document-relative repo-local links.

            ## Scope
            - Applies to one standard-index fixture.

            ## Use When
            - Rebuilding the governed standard index.

            ## Related Standards and Sources
            - [example_reference.md](../../references/example_reference.md): governed local
              reference doc drives the rule.

            ## Guidance
            - Keep reference extraction source-aware.

            ## Operationalization
            - `Modes`: `documentation`
            - `Operational Surfaces`: `docs/standards/documentation/example_standard.md`

            ## Validation
            - Standard-index sync should preserve document-relative reference paths.

            ## Change Control
            - Update sync and validation helpers together if this rule changes.

            ## References
            - [README.md](../../README.md)

            ## Updated At
            - `2026-03-11T17:36:00Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = StandardIndexSyncService(loader).build_document()

    entry = document["entries"][0]
    assert entry["standard_id"] == "std.documentation.example"
    assert entry["uses_internal_references"] is True
    assert entry["uses_external_references"] is True
    assert entry["reference_doc_paths"] == ["docs/references/example_reference.md"]
    assert entry["internal_reference_paths"] == [
        "docs/references/example_reference.md",
        "docs/README.md",
    ]
