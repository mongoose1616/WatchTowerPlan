from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.adapters import extract_repo_path_references
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_documents import (
    PlanningDocument,
    collect_reference_indicators,
)
from watchtower_core.repo_ops.sync import FoundationIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


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
            summary: "Provides one governed local reference for path-resolution tests."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:38:00Z"
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
            - `2026-03-11T17:38:00Z`
            """
        ),
        encoding="utf-8",
    )


def test_extract_repo_path_references_resolves_document_relative_links_with_source_path(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    reference_path = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    source_path = repo_root / "docs/standards/documentation/example_standard.md"

    result = extract_repo_path_references(
        "- [example_reference.md](../../references/example_reference.md): governed reference.",
        repo_root,
        source_path=source_path,
    )

    assert result == ("docs/references/example_reference.md",)


def test_collect_reference_indicators_resolves_document_relative_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    reference_path = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    document = PlanningDocument(
        relative_path="docs/planning/prds/example.md",
        front_matter={},
        sections={
            "References": (
                "- [example_reference.md](../../references/example_reference.md)\n"
                "- [README.md](../../README.md)"
            ),
        },
        metadata={},
    )
    _write_repo_file(repo_root / "docs/README.md")

    uses_internal, uses_external, internal_paths, external_urls = collect_reference_indicators(
        document,
        repo_root,
        internal_sections=("References",),
        external_sections=("References",),
    )

    assert uses_internal is True
    assert uses_external is False
    assert internal_paths == (
        "docs/references/example_reference.md",
        "docs/README.md",
    )
    assert external_urls == ()


def test_foundation_index_sync_extracts_document_relative_reference_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "docs/README.md")
    reference_path = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    foundation_path = repo_root / "docs/foundations/example_foundation.md"
    foundation_path.parent.mkdir(parents=True, exist_ok=True)
    foundation_path.write_text(
        dedent(
            """\
            ---
            id: "foundation.example"
            title: "Example Foundation"
            summary: "Exercises document-relative extraction in the foundation index."
            type: "foundation"
            status: "active"
            tags:
              - "foundation"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:38:00Z"
            audience: "shared"
            authority: "authoritative"
            ---

            # Example Foundation

            ## References
            - [example_reference.md](../references/example_reference.md)
            - [README.md](../README.md)

            ## Updated At
            - `2026-03-11T17:38:00Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = FoundationIndexSyncService(loader).build_document()

    entry = document["entries"][0]
    assert entry["foundation_id"] == "foundation.example"
    assert entry["uses_internal_references"] is True
    assert entry["uses_external_references"] is True
    assert entry["reference_doc_paths"] == ["docs/references/example_reference.md"]
    assert entry["internal_reference_paths"] == [
        "docs/references/example_reference.md",
        "docs/README.md",
    ]
