from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.reference_index import ReferenceIndexSyncService

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
        and entry["uses_external_references"] is True
        and ".github/README.md" in entry.get("related_paths", [])
        for entry in entries
    )


def test_reference_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ReferenceIndexSyncService(loader)
    output_path = tmp_path / "reference_index.json"

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
    _write_repo_file(repo_root / "core/docs/README.md")
    reference_path = repo_root / "core/docs/references/example_reference.md"
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
            ### Current Repository Status
            - Supporting authority for current repository docs, standards,
              commands, or control-plane surfaces.

            ### Current Touchpoints
            - [README.md](../README.md)

            ### Why It Matters Here
            - Keep one explicit repo-local touchpoint for the test fixture.

            ## References
            - [README.md](../README.md)

            ## Updated At
            - `2026-03-11T17:37:00Z`
            """
        ),
        encoding="utf-8",
    )

    standard_path = repo_root / "core/docs/standards/documentation/example_standard.md"
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
            - `Operational Surfaces`: `core/docs/standards/documentation/example_standard.md`

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

    entries = document["entries"]
    assert isinstance(entries, list)
    entry = entries[0]
    assert isinstance(entry, dict)
    assert entry["reference_id"] == "ref.example"
    assert entry["repository_status"] == "supporting_authority"
    assert entry["related_paths"] == ["core/docs/README.md"]
    assert entry["applied_by_paths"] == ["core/docs/standards/documentation/example_standard.md"]


def test_reference_index_sync_does_not_count_readme_only_backlinks_as_internal_support(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "core/docs/references/README.md")
    reference_path = repo_root / "core/docs/references/example_reference.md"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.write_text(
        dedent(
            """\
            ---
            id: "ref.example"
            title: "Example Reference"
            summary: "Exercises candidate-reference maturity signaling."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-13T17:30:00Z"
            audience: "shared"
            authority: "supporting"
            ---

            # Example Reference

            ## Canonical Upstream
            - [Example upstream](https://example.com/reference)

            ## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## Local Mapping in This Repository
            ### Current Repository Status
            - Candidate reference. No active standard or workflow in this
              repository links this file directly yet.

            ### Why It Matters Here
            - Keep one candidate reference available for future work.

            ## References
            - [README.md](README.md)

            ## Updated At
            - `2026-03-13T17:30:00Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = ReferenceIndexSyncService(loader).build_document()

    entries = document["entries"]
    assert isinstance(entries, list)
    entry = entries[0]
    assert isinstance(entry, dict)
    assert entry["reference_id"] == "ref.example"
    assert entry["repository_status"] == "candidate_future_guidance"
    assert "related_paths" not in entry
    assert entry["uses_internal_references"] is False


def test_reference_index_sync_tracks_role_workflow_citations(tmp_path: Path) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "core/docs/README.md")
    reference_path = repo_root / "core/docs/references/example_reference.md"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.write_text(
        dedent(
            """\
            ---
            id: "ref.example"
            title: "Example Reference"
            summary: "Exercises workflow-role citation extraction in the reference index."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-24T20:00:00Z"
            audience: "shared"
            authority: "supporting"
            ---

            # Example Reference

            ## Canonical Upstream
            - [Example upstream](https://example.com/reference)

            ## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## Local Mapping in This Repository
            ### Current Repository Status
            - Supporting authority for workflow-role citation extraction.

            ### Current Touchpoints
            - [architecture_reviewer.md](../../workflows/roles/architecture_reviewer.md)

            ### Why It Matters Here
            - Keep one explicit workflow-role citation target in scope.

            ## References
            - [README.md](../README.md)

            ## Updated At
            - `2026-03-24T20:00:00Z`
            """
        ),
        encoding="utf-8",
    )

    role_path = repo_root / "core/workflows/roles/architecture_reviewer.md"
    role_path.parent.mkdir(parents=True, exist_ok=True)
    role_path.write_text(
        dedent(
            """\
            # Architecture Reviewer Role

            ## Purpose
            Use this role to apply one architecture review lens.

            ## Use When
            - Reviewing architecture posture with one supporting reference.

            ## Inputs
            - One scoped architecture review target.

            ## Additional Files to Load
            - [example_reference.md](../../docs/references/example_reference.md):
              grounds the review lens in one governed local reference.

            ## Workflow
            1. Apply the architecture review lens using the loaded reference.

            ## Data Structure
            - One architecture-focused finding set.

            ## Outputs
            - One architecture-focused review result.

            ## Done When
            - The role has applied the scoped architecture lens.
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = ReferenceIndexSyncService(loader).build_document()

    entry = next(item for item in document["entries"] if item["reference_id"] == "ref.example")
    assert entry["cited_by_paths"] == ["core/workflows/roles/architecture_reviewer.md"]
    assert entry["applied_by_paths"] == ["core/workflows/roles/architecture_reviewer.md"]


def test_reference_index_sync_includes_pack_owned_reference_docs_without_self_noise(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    workflow_path = repo_root / "packs/fixture/workflows/modules/example.md"
    _write_repo_file(
        workflow_path,
        dedent(
            """\
            # Example Workflow

            ## Purpose
            Keep one pack-owned workflow surface available for reference indexing.
            """
        ),
    )
    reference_path = repo_root / "packs/fixture/docs/references/example_reference.md"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.write_text(
        dedent(
            """\
            ---
            id: "ref.pack_fixture"
            title: "Pack Fixture Reference"
            summary: "Exercises hosted-pack reference discovery without self-noise."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "fixture"
            owner: "repository_maintainer"
            updated_at: "2026-03-28T23:55:00Z"
            audience: "shared"
            authority: "supporting"
            applies_to:
              - "packs/fixture/docs/references/example_reference.md"
              - "packs/fixture/workflows/modules/example.md"
            ---

            # Pack Fixture Reference

            ## Canonical Upstream
            - [Example upstream](https://example.com/reference)

            ## Quick Reference or Distilled Reference
            One pack-owned governed reference fixture.

            ## Local Mapping in This Repository
            ### Current Repository Status
            - Supporting authority for one pack-owned workflow surface.

            ### Current Touchpoints
            - [reference doc](/packs/fixture/docs/references/example_reference.md)
            - [workflow](/packs/fixture/workflows/modules/example.md)

            ### Why It Matters Here
            - Keep hosted-pack reference indexing generic and deterministic.

            ## References
            - [Example upstream](https://example.com/reference)
            - [workflow](/packs/fixture/workflows/modules/example.md)

            ## Updated At
            - `2026-03-28T23:55:00Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = ReferenceIndexSyncService(loader).build_document()

    entry = next(item for item in document["entries"] if item["reference_id"] == "ref.pack_fixture")
    assert entry["doc_path"] == "packs/fixture/docs/references/example_reference.md"
    assert entry["related_paths"] == ["packs/fixture/workflows/modules/example.md"]
    assert "cited_by_paths" not in entry
    assert "applied_by_paths" not in entry
