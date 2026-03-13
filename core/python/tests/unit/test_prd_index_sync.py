from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import PrdIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_prd_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = PrdIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["prd_id"] == "prd.core_python_foundation"
        and entry["uses_internal_references"] is True
        and "internal_reference_paths" in entry
        for entry in entries
    )


def test_prd_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = PrdIndexSyncService(loader)
    output_path = tmp_path / "prd_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.prds"


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def test_prd_index_sync_filters_stale_related_paths_from_existing_index(tmp_path: Path) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    (repo_root / "docs" / "templates").mkdir(parents=True, exist_ok=True)
    prd_path = repo_root / "docs/planning/prds/prd_index_fixture.md"
    prd_path.parent.mkdir(parents=True, exist_ok=True)
    prd_path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.prd_index_fixture
            id: prd.prd_index_fixture
            title: PRD Index Fixture
            summary: Exercises stale related-path filtering in the PRD index.
            type: prd
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-13T02:00:00Z'
            audience: shared
            authority: authoritative
            ---

            # PRD Index Fixture

            ## Record Metadata
            - `Trace ID`: `trace.prd_index_fixture`
            - `PRD ID`: `prd.prd_index_fixture`
            - `Status`: `active`
            - `Linked Decisions`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-13T02:00:00Z`

            ## Summary
            Exercises stale related-path filtering in the PRD index.

            ## Problem Statement
            Existing indexes should not preserve deleted related paths.

            ## Goals
            - Keep only live related paths during rebuild.

            ## Non-Goals
            - Add new document-derived related paths.

            ## Requirements
            - `req.prd_index_fixture.001`: Rebuild filters stale related paths.

            ## Acceptance Criteria
            - `ac.prd_index_fixture.001`: Only live related paths remain in the rebuilt entry.

            ## Risks and Dependencies
            - The live path fixture must exist on disk.

            ## References
            - docs/templates/
            """
        ),
        encoding="utf-8",
    )

    index_path = repo_root / "core/control_plane/indexes/prds/prd_index.v1.json"
    document = json.loads(index_path.read_text(encoding="utf-8"))
    document["entries"].append(
        {
            "trace_id": "trace.prd_index_fixture",
            "prd_id": "prd.prd_index_fixture",
            "title": "PRD Index Fixture",
            "summary": "Exercises stale related-path filtering in the PRD index.",
            "status": "active",
            "doc_path": "docs/planning/prds/prd_index_fixture.md",
            "updated_at": "2026-03-13T02:00:00Z",
            "uses_internal_references": False,
            "uses_external_references": False,
            "related_paths": ["docs/missing.md", "docs/templates/"],
        }
    )
    index_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")

    rebuilt = PrdIndexSyncService(ControlPlaneLoader(repo_root)).build_document()
    entry = next(item for item in rebuilt["entries"] if item["prd_id"] == "prd.prd_index_fixture")
    assert entry["related_paths"] == ["docs/templates/"]
