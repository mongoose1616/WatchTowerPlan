from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import ReferenceIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_reference_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ReferenceIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["reference_id"] == "ref.uv"
        and entry["uses_external_references"] is True
        and "canonical_upstream_urls" in entry
        for entry in entries
    )
    assert any(
        entry["reference_id"] == "ref.github_collaboration"
        and "docs/standards/governance/github_collaboration_standard.md"
        in entry.get("applied_by_paths", [])
        for entry in entries
    )


def test_reference_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ReferenceIndexSyncService(loader)
    output_path = tmp_path / "reference_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.references"


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _write_repo_file(path: Path, content: str = "# Placeholder\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_reference_index_sync_extracts_document_relative_related_and_applied_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "docs/README.md")
    reference_path = repo_root / "docs/references/example_reference.md"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.write_text(
        dedent(
            """\
            ---
            id: "ref.example"
            title: "Example Reference"
            summary: "Exercises document-relative extraction in the reference index."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:37:00Z"
            audience: "shared"
            authority: "supporting"
            ---

            # Example Reference

            ## Canonical Upstream
            - [Example upstream](https://example.com/reference)

            ## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## Local Mapping in This Repository
            - [README.md](../README.md)

            ## References
            - [README.md](../README.md)

            ## Updated At
            - `2026-03-11T17:37:00Z`
            """
        ),
        encoding="utf-8",
    )

    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        dedent(
            """\
            ---
            id: "std.documentation.example"
            title: "Example Standard"
            summary: "Provides one applied-by reference fixture."
            type: "standard"
            status: "active"
            tags:
              - "standard"
              - "documentation"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:37:00Z"
            audience: "shared"
            authority: "authoritative"
            ---

            # Example Standard

            ## Summary
            Provides one applied-by reference fixture.

            ## Purpose
            Keep the fixture focused on citation-audit extraction.

            ## Scope
            - Applies to one temporary repo.

            ## Use When
            - Rebuilding the governed reference index.

            ## Related Standards and Sources
            - [example_reference.md](../../references/example_reference.md): governed local
              reference doc shapes this standard.

            ## Guidance
            - Keep citation-audit extraction source-aware.

            ## Operationalization
            - `Modes`: `documentation`
            - `Operational Surfaces`: `docs/standards/documentation/example_standard.md`

            ## Validation
            - Reference-index sync should attribute document-relative applied references.

            ## Change Control
            - Update sync and citation-audit helpers together if this rule changes.

            ## References
            - [README.md](../../README.md)

            ## Updated At
            - `2026-03-11T17:37:00Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = ReferenceIndexSyncService(loader).build_document()

    entry = document["entries"][0]
    assert entry["reference_id"] == "ref.example"
    assert entry["related_paths"] == ["docs/README.md"]
    assert entry["applied_by_paths"] == [
        "docs/standards/documentation/example_standard.md"
    ]
