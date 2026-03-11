from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import DecisionIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_decision_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = DecisionIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["decision_id"] == "decision.core_python_workspace_root"
        and entry["uses_internal_references"] is True
        for entry in entries
    )


def test_decision_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = DecisionIndexSyncService(loader)
    output_path = tmp_path / "decision_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.decisions"


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def test_decision_index_sync_normalizes_document_relative_affected_surfaces(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    (repo_root / "docs" / "templates").mkdir(parents=True, exist_ok=True)
    decision_path = repo_root / "docs/planning/decisions/relative_decision.md"
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    decision_path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.relative_decision_index
            id: decision.relative_decision_index
            title: Relative Decision Index Coverage
            summary: Reproduces document-relative affected-surface handling in decision index sync.
            type: decision_record
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T18:05:00Z'
            audience: shared
            authority: supporting
            ---

            # Relative Decision Index Coverage

            ## Record Metadata
            - `Trace ID`: `trace.relative_decision_index`
            - `Decision ID`: `decision.relative_decision_index`
            - `Record Status`: `active`
            - `Decision Status`: `accepted`
            - `Linked PRDs`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-11T18:05:00Z`

            ## Summary
            Reproduces document-relative affected-surface handling in decision index sync.

            ## Decision Statement
            Normalize document-relative affected-surface paths before projecting them.

            ## Trigger or Source Request
            - Added to reproduce a decision-index projection drift.

            ## Current Context and Constraints
            - Decision semantics already accept document-relative repo-local links.

            ## Applied References and Implications
            - `docs/standards/documentation/decision_record_md_standard.md`: affected
              surfaces should stay queryable as repository-relative paths.

            ## Affected Surfaces
            - [Templates](../../templates/)

            ## Options Considered
            ### Option 1
            - Keep raw extraction.
            - Strength: no code change.
            - Tradeoff: related paths stay document-relative instead of repo-relative.

            ### Option 2
            - Normalize affected-surface paths during sync.
            - Strength: the decision index stays machine-usable.
            - Tradeoff: sync and tests need to change together.

            ## Chosen Outcome
            Normalize the affected-surface path.

            ## Rationale and Tradeoffs
            - Machine-readable indexes should publish repository-relative paths.

            ## Consequences and Follow-Up Impacts
            - Decision-index sync and tests need to stay aligned.

            ## Risks, Dependencies, and Assumptions
            - The target path must stay inside the repository root.

            ## References
            - `docs/standards/documentation/decision_record_md_standard.md`
            """
        ),
        encoding="utf-8",
    )
    standard_path = repo_root / "docs/standards/documentation/decision_record_md_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        (REPO_ROOT / "docs/standards/documentation/decision_record_md_standard.md").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    document = DecisionIndexSyncService(loader).build_document()

    entry = next(
        entry
        for entry in document["entries"]
        if entry["decision_id"] == "decision.relative_decision_index"
    )
    assert entry["related_paths"] == ["docs/templates/"]
