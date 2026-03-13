from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import DesignDocumentIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]

FEATURE_DESIGN_REQUIRED_REFERENCE_SECTIONS = """\

            ## Foundations References Applied
            - `docs/references/commonmark_reference.md`: The fixture keeps the Markdown
              structure aligned with the governed parsing rules.

            ## Internal Standards and Canonical References Applied
            - `docs/standards/documentation/feature_design_md_standard.md`: The fixture
              stays aligned with the enforced feature-design authoring contract.
"""

IMPLEMENTATION_PLAN_REQUIRED_REFERENCE_SECTIONS = """\

            ## Internal Standards and Canonical References Applied
            - `docs/standards/documentation/implementation_plan_md_standard.md`: The
              fixture stays aligned with the enforced implementation-plan authoring
              contract.
"""


def test_design_document_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = DesignDocumentIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["document_id"] == "design.features.command_documentation_and_lookup"
        and entry["uses_internal_references"] is True
        for entry in entries
    )
    assert any(
        entry["document_id"] == "design.implementation.control_plane_loaders_and_schema_store"
        and "source_paths" in entry
        for entry in entries
    )


def test_design_document_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = DesignDocumentIndexSyncService(loader)
    output_path = tmp_path / "design_document_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.design_documents"


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _write_prd_fixture(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.design_index_fixture
            id: prd.design_index_fixture
            title: Design Index Fixture PRD
            summary: Provides one PRD-backed source path for the design-index fixture.
            type: prd
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T19:30:00Z'
            audience: shared
            authority: authoritative
            ---

            # Design Index Fixture PRD

            ## Record Metadata
            - `Trace ID`: `trace.design_index_fixture`
            - `PRD ID`: `prd.design_index_fixture`
            - `Status`: `active`
            - `Linked Decisions`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `design.implementation.design_index_fixture`
            - `Updated At`: `2026-03-11T19:30:00Z`

            ## Summary
            Provides one PRD-backed source path for the design-index fixture.

            ## Problem Statement
            The fixture PRD anchors one implementation-plan source path.

            ## Goals
            - Keep the design-index fixture focused on source derivation.

            ## Non-Goals
            - Add a feature-design source to this PRD-backed fixture.

            ## Requirements
            - `req.design_index_fixture.001`: The design index can resolve this PRD path.

            ## Acceptance Criteria
            - `ac.design_index_fixture.001`: The implementation-plan entry includes the PRD path.

            ## Risks and Dependencies
            - Sync should fail only when no traceable source path exists.

            ## References
            - `docs/planning/design/implementation/design_index_fixture.md`
            """
        ),
        encoding="utf-8",
    )


def test_design_document_index_sync_projects_feature_design_affected_surfaces(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    (repo_root / "docs" / "commands" / "core_python").mkdir(parents=True, exist_ok=True)
    (repo_root / "docs" / "commands" / "core_python" / "README.md").write_text(
        "# Commands\n",
        encoding="utf-8",
    )
    feature_path = repo_root / "docs/planning/design/features/design_index_fixture.md"
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text(
        dedent(
            f"""\
            ---
            trace_id: trace.design_index_fixture
            id: design.features.design_index_fixture
            title: Design Index Fixture Feature Design
            summary: Exercises feature-design affected-surface projection.
            type: feature_design
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T19:30:00Z'
            audience: shared
            authority: authoritative
            ---

            # Design Index Fixture Feature Design

            ## Record Metadata
            - `Trace ID`: `trace.design_index_fixture`
            - `Design ID`: `design.features.design_index_fixture`
            - `Design Status`: `active`
            - `Linked PRDs`: `None`
            - `Linked Decisions`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-11T19:30:00Z`

            ## Summary
            Exercises feature-design affected-surface projection.

            ## Source Request
            - Added to reproduce missing related-path projection.

            ## Scope and Feature Boundary
            - Keep the fixture focused on one affected-surface path.

            ## Current-State Context
            - The design index should retain affected-surface paths.

            ## Design Goals and Constraints
            - Preserve normalized repository-relative paths.

            {FEATURE_DESIGN_REQUIRED_REFERENCE_SECTIONS}
            ## Options Considered
            ### Option 1
            - Keep the current omission.
            - Strength: no code change.
            - Tradeoff: the index drops required relationship data.

            ### Option 2
            - Project the affected-surface path.
            - Strength: matches the governed design document.
            - Tradeoff: requires sync coverage.

            ## Recommended Design
            Project the affected-surface path into related_paths.

            ## Affected Surfaces
            - [README.md](../../../commands/core_python/README.md)

            ## Design Guardrails
            - Keep the projected path normalized.

            ## Risks
            - Missing paths make the index incomplete.

            ## References
            - `docs/standards/documentation/feature_design_md_standard.md`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = DesignDocumentIndexSyncService(loader).build_document()

    entry = document["entries"][0]
    assert entry["document_id"] == "design.features.design_index_fixture"
    assert entry["related_paths"] == ["docs/commands/core_python/README.md"]


def test_design_document_index_sync_accepts_prd_and_repo_local_source_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    (repo_root / "docs" / "commands" / "core_python").mkdir(parents=True, exist_ok=True)
    (repo_root / "docs" / "commands" / "core_python" / "README.md").write_text(
        "# Commands\n",
        encoding="utf-8",
    )
    _write_prd_fixture(repo_root / "docs/planning/prds/design_index_fixture.md")
    plan_path = repo_root / "docs/planning/design/implementation/design_index_fixture.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        dedent(
            f"""\
            ---
            trace_id: trace.design_index_fixture
            id: design.implementation.design_index_fixture
            title: Design Index Fixture Implementation Plan
            summary: Exercises broadened implementation-plan source-path derivation.
            type: implementation_plan
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T19:30:00Z'
            audience: shared
            authority: supporting
            ---

            # Design Index Fixture Implementation Plan

            ## Record Metadata
            - `Trace ID`: `trace.design_index_fixture`
            - `Plan ID`: `design.implementation.design_index_fixture`
            - `Plan Status`: `active`
            - `Linked PRDs`: `prd.design_index_fixture`
            - `Linked Decisions`: `None`
            - `Source Designs`: `None`
            - `Linked Acceptance Contracts`: `None`
            - `Updated At`: `2026-03-11T19:30:00Z`

            ## Summary
            Exercises broadened implementation-plan source-path derivation.

            ## Source Request or Design
            - `docs/planning/prds/design_index_fixture.md`
            - [README.md](../../../commands/core_python/README.md)

            ## Scope Summary
            - Keep the fixture focused on source-path derivation.

            ## Assumptions and Constraints
            - The implementation plan is driven by a PRD and one repo-local source path.

            {IMPLEMENTATION_PLAN_REQUIRED_REFERENCE_SECTIONS}
            ## Proposed Technical Approach
            - Derive source paths from the linked PRD and the repo-local source path.

            ## Work Breakdown
            1. Build the design index.

            ## Risks
            - The sync path may still require a source design.

            ## Validation Plan
            - Build the design index successfully.

            ## References
            - `docs/planning/prds/design_index_fixture.md`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = DesignDocumentIndexSyncService(loader).build_document()

    entry = document["entries"][0]
    assert entry["document_id"] == "design.implementation.design_index_fixture"
    assert entry["source_paths"] == [
        "docs/planning/prds/design_index_fixture.md",
        "docs/commands/core_python/README.md",
    ]


def test_design_document_index_sync_rejects_implementation_plan_without_traceable_sources(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    plan_path = repo_root / "docs/planning/design/implementation/design_index_fixture.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        dedent(
            f"""\
            ---
            trace_id: trace.design_index_fixture
            id: design.implementation.design_index_fixture
            title: Design Index Fixture Implementation Plan
            summary: Exercises fail-closed source-path validation.
            type: implementation_plan
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T19:30:00Z'
            audience: shared
            authority: supporting
            ---

            # Design Index Fixture Implementation Plan

            ## Record Metadata
            - `Trace ID`: `trace.design_index_fixture`
            - `Plan ID`: `design.implementation.design_index_fixture`
            - `Plan Status`: `active`
            - `Linked PRDs`: `None`
            - `Linked Decisions`: `None`
            - `Source Designs`: `None`
            - `Linked Acceptance Contracts`: `None`
            - `Updated At`: `2026-03-11T19:30:00Z`

            ## Summary
            Exercises fail-closed source-path validation.

            ## Source Request or Design
            - Direct user request without any repo-local source path.

            ## Scope Summary
            - Keep the fixture focused on the missing-source-path failure.

            ## Assumptions and Constraints
            - No source design or PRD is linked.

            {IMPLEMENTATION_PLAN_REQUIRED_REFERENCE_SECTIONS}
            ## Proposed Technical Approach
            - Build the design index.

            ## Work Breakdown
            1. Build the design index.

            ## Risks
            - The sync should fail clearly.

            ## Validation Plan
            - Confirm the sync raises the expected error.

            ## References
            - `docs/standards/documentation/implementation_plan_md_standard.md`
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)

    try:
        DesignDocumentIndexSyncService(loader).build_document()
    except ValueError as exc:
        assert "missing traceable source paths" in str(exc)
    else:
        raise AssertionError("Expected design-document index sync to fail without source paths.")


def test_design_document_index_sync_filters_stale_related_paths_from_existing_index(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    (repo_root / "docs" / "commands" / "core_python").mkdir(parents=True, exist_ok=True)
    (repo_root / "docs" / "commands" / "core_python" / "README.md").write_text(
        "# Commands\n",
        encoding="utf-8",
    )
    feature_path = repo_root / "docs/planning/design/features/stale_related_paths.md"
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text(
        dedent(
            f"""\
            ---
            trace_id: trace.design_index_stale_related_paths
            id: design.features.design_index_stale_related_paths
            title: Design Index Stale Related Paths
            summary: Exercises stale related-path filtering in design index sync.
            type: feature_design
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-13T02:00:00Z'
            audience: shared
            authority: authoritative
            ---

            # Design Index Stale Related Paths

            ## Record Metadata
            - `Trace ID`: `trace.design_index_stale_related_paths`
            - `Design ID`: `design.features.design_index_stale_related_paths`
            - `Design Status`: `active`
            - `Linked PRDs`: `None`
            - `Linked Decisions`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-13T02:00:00Z`

            ## Summary
            Exercises stale related-path filtering in design index sync.

            ## Source Request
            - Added for stale related-path regression coverage.

            ## Scope and Feature Boundary
            - Keep the fixture focused on existing-entry carry-over.

            ## Current-State Context
            - The live fixture path must remain in the repository.

            ## Design Goals and Constraints
            - Rebuilt related paths should keep only existing entries.

            {FEATURE_DESIGN_REQUIRED_REFERENCE_SECTIONS}
            ## Options Considered
            ### Option 1
            - Keep stale current related paths.
            - Strength: no filtering.
            - Tradeoff: deleted references reappear.

            ### Option 2
            - Filter stale current related paths.
            - Strength: rebuild output stays truthful.
            - Tradeoff: carry-over becomes stricter.

            ## Recommended Design
            Keep only existing current related paths.

            ## Affected Surfaces
            - docs/commands/core_python/README.md

            ## Design Guardrails
            - Do not reintroduce deleted paths.

            ## Risks
            - The live fixture path must exist.

            ## References
            - `docs/standards/documentation/feature_design_md_standard.md`
            """
        ),
        encoding="utf-8",
    )

    index_path = (
        repo_root / "core/control_plane/indexes/design_documents/design_document_index.v1.json"
    )
    document = json.loads(index_path.read_text(encoding="utf-8"))
    document["entries"].append(
        {
            "document_id": "design.features.design_index_stale_related_paths",
            "trace_id": "trace.design_index_stale_related_paths",
            "family": "feature_design",
            "title": "Design Index Stale Related Paths",
            "summary": "Exercises stale related-path filtering in design index sync.",
            "status": "active",
            "doc_path": "docs/planning/design/features/stale_related_paths.md",
            "updated_at": "2026-03-13T02:00:00Z",
            "uses_internal_references": False,
            "uses_external_references": False,
            "related_paths": ["docs/missing.md", "docs/commands/core_python/README.md"],
        }
    )
    index_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")

    rebuilt = DesignDocumentIndexSyncService(ControlPlaneLoader(repo_root)).build_document()
    entry = next(
        item
        for item in rebuilt["entries"]
        if item["document_id"] == "design.features.design_index_stale_related_paths"
    )
    assert entry["related_paths"] == ["docs/commands/core_python/README.md"]
