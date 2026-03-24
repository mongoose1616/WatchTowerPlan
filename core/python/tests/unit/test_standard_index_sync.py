from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

from tests.unit.control_plane_loader_test_support import (
    materialize_pack_validation_surfaces,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.operationalization_paths import (
    operationalization_path_matches,
)
from watchtower_core.sync.standard_index import StandardIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _default_pack_tracking_root(loader: ControlPlaneLoader) -> str:
    return loader.load_pack_settings().workspace_roots.tracking_root


def _default_pack_docs_root(loader: ControlPlaneLoader) -> str:
    return loader.load_pack_settings().workspace_roots.docs_root


def _default_pack_namespace(loader: ControlPlaneLoader) -> str:
    return loader.load_pack_registry().default_pack().command_namespace


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
        and "core/docs/references/github_collaboration_reference.md"
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
    assert "core/docs/references/*_reference.md" in reference_entry.get(
        "operationalization_paths",
        [],
    )

    standard_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.documentation.standard_md"
    )
    assert "*/docs/standards/*/*_standard.md" in standard_entry.get(
        "operationalization_paths",
        [],
    )

    python_code_design_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.engineering.python_code_design"
    )
    assert python_code_design_entry["doc_path"] == (
        "core/docs/standards/engineering/python_code_design_standard.md"
    )
    assert python_code_design_entry["uses_external_references"] is True
    assert {
        "core/docs/standards/engineering/python_workspace_standard.md",
        "core/docs/standards/engineering/engineering_best_practices_standard.md",
        "core/docs/foundations/engineering_design_principles.md",
        "core/docs/references/pep8_reference.md",
        "core/docs/references/pep257_reference.md",
        "core/docs/references/ruff_reference.md",
        "core/docs/references/mypy_reference.md",
        "core/docs/references/pytest_reference.md",
    }.issubset(set(python_code_design_entry.get("internal_reference_paths", [])))
    assert {
        "core/python/src/watchtower_core/",
        "core/python/tests/",
        "core/python/AGENTS.md",
        "core/python/README.md",
    }.issubset(set(python_code_design_entry.get("operationalization_paths", [])))

    foundation_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.data_contracts.foundation_index"
    )
    assert {"sync", "query", "documentation", "schema", "artifact"}.issubset(
        set(foundation_entry.get("operationalization_modes", []))
    )
    assert "core/python/src/watchtower_core/sync/foundation_index.py" in (
        foundation_entry.get("operationalization_paths", [])
    )
    assert "core/python/src/watchtower_core/query/foundations.py" in (
        foundation_entry.get("operationalization_paths", [])
    )
    assert "core/docs/commands/core_python/watchtower_core_query_foundations.md" in (
        foundation_entry.get("operationalization_paths", [])
    )
    assert "*/docs/commands/core_python/" in (
        foundation_entry.get("operationalization_paths", [])
    )
    assert "core/control_plane/indexes/foundations/README.md" in (
        foundation_entry.get("operationalization_paths", [])
    )

    foundation_doc_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.documentation.foundation_md"
    )
    foundation_doc_paths = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "core" / "docs" / "foundations").glob("*.md")
        if path.name != "README.md"
    )
    published_foundation_doc_paths = sorted(
        path
        for path in foundation_doc_entry.get("operationalization_paths", [])
        if path.startswith("core/docs/foundations/") and path.endswith(".md")
    )
    assert published_foundation_doc_paths == foundation_doc_paths
    assert "core/docs/foundations/" not in foundation_doc_entry.get(
        "operationalization_paths",
        [],
    )
    assert "core/docs/foundations/README.md" not in foundation_doc_entry.get(
        "operationalization_paths",
        [],
    )

    planning_family_entry = next(
        entry
        for entry in entries
        if entry["standard_id"] == "std.data_contracts.planning_index_family"
    )
    assert "planning_index_family" in planning_family_entry.get("tags", [])
    assert "core/docs/commands/core_python/watchtower_core_query_standards.md" in (
        planning_family_entry.get("operationalization_paths", [])
    )

    planning_family_member_ids = {
        "std.data_contracts.coordination_index",
        "std.data_contracts.initiative_index",
        "std.data_contracts.task_index",
        "std.data_contracts.traceability_index",
    }
    for standard_id in planning_family_member_ids:
        entry = next(entry for entry in entries if entry["standard_id"] == standard_id)
        assert "planning_index_family" in entry.get("tags", [])

    compact_entry = next(
        entry
        for entry in entries
        if entry["standard_id"] == "std.documentation.compact_document_authoring"
    )
    assert "<pack>/tracking/" in compact_entry.get("operationalization_paths", [])
    assert "<pack>/initiatives/" in compact_entry.get("operationalization_paths", [])

    git_workflow_entry = next(
        entry for entry in entries if entry["standard_id"] == "std.engineering.git_workflow"
    )
    assert "<pack>/tracking/task_tracking.md" in git_workflow_entry.get(
        "operationalization_paths",
        [],
    )
    assert "<pack>/tracking/coordination_tracking.md" in git_workflow_entry.get(
        "operationalization_paths",
        [],
    )


def test_pack_placeholder_operationalization_paths_match_live_pack_paths() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    tracking_root = _default_pack_tracking_root(loader)
    docs_root = _default_pack_docs_root(loader)
    command_namespace = _default_pack_namespace(loader)

    assert operationalization_path_matches(
        f"{tracking_root}/task_tracking.md",
        "<pack>/tracking/task_tracking.md",
        REPO_ROOT,
    )
    assert operationalization_path_matches(
        f"{tracking_root}/task_tracking.md",
        "<pack>/tracking/",
        REPO_ROOT,
    )
    assert operationalization_path_matches(
        (
            f"{docs_root}/commands/core_python/"
            f"watchtower_core_{command_namespace}_sync_foundation_index.md"
        ),
        "*/docs/commands/core_python/",
        REPO_ROOT,
    )


def test_pack_placeholder_operationalization_paths_match_externalized_pack_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    materialize_pack_validation_surfaces(repo_root / "packs" / "oversight")

    assert operationalization_path_matches(
        "packs/oversight/tracking/task_tracking.md",
        "<pack>/tracking/task_tracking.md",
        repo_root,
    )
    assert operationalization_path_matches(
        "packs/oversight/tracking/task_tracking.md",
        "<pack>/tracking/",
        repo_root,
    )
    assert operationalization_path_matches(
        "packs/oversight/docs/commands/core_python/watchtower_core_oversight_sync_foundation_index.md",
        "*/docs/commands/core_python/",
        repo_root,
    )


def test_standard_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = StandardIndexSyncService(loader)
    output_path = tmp_path / "standard_index.json"

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

            ## Local Mapping in This Repository
            ### Current Repository Status
            - Supporting authority for current repository docs, standards,
              commands, or control-plane surfaces.

            ### Current Touchpoints
            - [README.md](../README.md)

            ### Why It Matters Here
            - Keep one explicit repo-local touchpoint for the reference fixture.

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
    _write_repo_file(repo_root / "core/docs/README.md")
    reference_path = repo_root / "core/docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    standard_path = repo_root / "core/docs/standards/documentation/example_standard.md"
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
            - `Operational Surfaces`: `core/docs/standards/documentation/example_standard.md`

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

    entries = document["entries"]
    assert isinstance(entries, list)
    entry = entries[0]
    assert isinstance(entry, dict)
    assert entry["standard_id"] == "std.documentation.example"
    assert entry["uses_internal_references"] is True
    assert entry["uses_external_references"] is True
    assert entry["reference_doc_paths"] == ["core/docs/references/example_reference.md"]
    assert entry["internal_reference_paths"] == [
        "core/docs/references/example_reference.md",
        "core/docs/README.md",
    ]


def test_standard_index_sync_rejects_noncanonical_directory_operationalization_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "core/docs/README.md")
    (repo_root / "core/docs/commands").mkdir(parents=True, exist_ok=True)
    reference_path = repo_root / "core/docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    standard_path = repo_root / "core/docs/standards/documentation/example_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        dedent(
            """\
            ---
            id: "std.documentation.example"
            title: "Example Standard"
            summary: "Exercises canonical directory operationalization validation."
            type: "standard"
            status: "active"
            tags:
              - "standard"
              - "documentation"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-12T02:06:54Z"
            audience: "shared"
            authority: "authoritative"
            ---

            # Example Standard

            ## Summary
            Exercises canonical directory operationalization validation.

            ## Purpose
            Keep the fixture focused on duplicate directory-path drift.

            ## Scope
            - Applies to one standard-index fixture.

            ## Use When
            - Rebuilding the governed standard index.

            ## Related Standards and Sources
            - [example_reference.md](../../references/example_reference.md): governed local
              reference doc drives the rule.

            ## Guidance
            - Keep operationalization directory syntax canonical.

            ## Operationalization
            - `Modes`: `documentation`
            - `Operational Surfaces`: `core/docs/commands`; `core/docs/commands/`

            ## Validation
            - Standard-index sync should reject semantically duplicate directory paths.

            ## Change Control
            - Update validation and sync helpers together if this rule changes.

            ## References
            - [README.md](../../README.md)

            ## Updated At
            - `2026-03-12T02:06:54Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)

    message = (
        "directory operationalization surfaces must use repo-relative directory paths ending in '/'"
    )
    with pytest.raises(ValueError, match=message):
        StandardIndexSyncService(loader).build_document()


def test_standard_index_sync_allows_pack_placeholder_operationalization_without_live_match(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "README.md")
    _write_repo_file(repo_root / "core/docs/README.md")
    reference_path = repo_root / "core/docs/references/example_reference.md"
    _write_reference_fixture(reference_path)
    standard_path = repo_root / "core/docs/standards/documentation/example_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        dedent(
            """\
            ---
            id: "std.documentation.example"
            title: "Example Standard"
            summary: "Exercises pack-placeholder operationalization without a live pack match."
            type: "standard"
            status: "active"
            tags:
              - "standard"
              - "documentation"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-23T22:20:00Z"
            audience: "shared"
            authority: "authoritative"
            ---

            # Example Standard

            ## Summary
            Exercises pack-placeholder operationalization without a live pack match.

            ## Purpose
            Keep pack-neutral operationalization declarations valid before
            one live pack publishes the surface.

            ## Scope
            - Applies to one pack-neutral standard-index fixture.

            ## Use When
            - Rebuilding the governed standard index before a hosted pack owns the declared file.

            ## Related Standards and Sources
            - [example_reference.md](../../references/example_reference.md): governed local
              reference doc drives the rule.

            ## Guidance
            - Keep pack placeholders stable even when the current repository
              has no matching live file yet.

            ## Operationalization
            - `Modes`: `documentation`
            - `Operational Surfaces`: `<pack>/tracking/task_tracking.md`

            ## Validation
            - Standard-index sync should preserve the pack placeholder instead of rejecting it.

            ## Change Control
            - Update placeholder parsing and matching together if this rule changes.

            ## References
            - [README.md](../../README.md)

            ## Updated At
            - `2026-03-23T22:20:00Z`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)

    document = StandardIndexSyncService(loader).build_document()

    entries = document["entries"]
    assert isinstance(entries, list)
    entry = entries[0]
    assert isinstance(entry, dict)
    assert entry["operationalization_paths"] == ["<pack>/tracking/task_tracking.md"]
