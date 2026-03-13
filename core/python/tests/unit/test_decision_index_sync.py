from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

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


def test_decision_index_sync_rejects_heading_after_list_without_blank_line(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    decision_path = repo_root / "docs/planning/decisions/invalid_spacing_decision.md"
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    decision_path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.invalid_spacing_decision_index
            id: decision.invalid_spacing_decision_index
            title: Invalid Spacing Decision Index Coverage
            summary: Reproduces heading separation enforcement for decision index sync.
            type: decision_record
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T20:38:54Z'
            audience: shared
            authority: supporting
            ---

            # Invalid Spacing Decision Index Coverage

            ## Record Metadata
            - `Trace ID`: `trace.invalid_spacing_decision_index`
            - `Decision ID`: `decision.invalid_spacing_decision_index`
            - `Record Status`: `active`
            - `Decision Status`: `accepted`
            - `Linked PRDs`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-11T20:38:54Z`

            ## Summary
            Reproduces heading separation enforcement for decision index sync.

            ## Decision Statement
            Shared sync should reject headings that follow list blocks without a blank line.

            ## Trigger or Source Request
            - Added to cover shared Markdown semantics in sync.
            ## Current Context and Constraints
            - Decision-index sync loads governed decision records directly.

            ## Applied References and Implications
            - `docs/standards/documentation/decision_record_md_standard.md`: the
              decision record shape stays governed during sync.

            ## Affected Surfaces
            - docs/planning/decisions/invalid_spacing_decision.md

            ## Options Considered
            ### Option 1
            - Keep the invalid spacing.
            - Strength: reproduces the bug.
            - Tradeoff: sync would accept malformed Markdown.

            ### Option 2
            - Reject the malformed spacing.
            - Strength: sync and validation stay aligned.
            - Tradeoff: authored docs must be cleaned up.

            ## Chosen Outcome
            Reject the malformed spacing.

            ## Rationale and Tradeoffs
            - Shared helpers should fail closed in sync and validation paths.

            ## Consequences and Follow-Up Impacts
            - Decision-index sync will stop accepting this invalid shape.

            ## Risks, Dependencies, and Assumptions
            - The shared helper must stay consistent with the semantics standard.

            ## References
            - docs/standards/documentation/decision_record_md_standard.md
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
    service = DecisionIndexSyncService(loader)

    with pytest.raises(ValueError, match="separated from the preceding list by a blank line"):
        service.build_document()


def test_decision_index_sync_filters_stale_related_paths_from_existing_index(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    (repo_root / "docs" / "templates").mkdir(parents=True, exist_ok=True)
    decision_path = repo_root / "docs/planning/decisions/stale_related_paths.md"
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    decision_path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.stale_decision_index
            id: decision.stale_decision_index
            title: Stale Decision Index Coverage
            summary: Exercises stale related-path filtering in decision index sync.
            type: decision_record
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-13T02:00:00Z'
            audience: shared
            authority: supporting
            ---

            # Stale Decision Index Coverage

            ## Record Metadata
            - `Trace ID`: `trace.stale_decision_index`
            - `Decision ID`: `decision.stale_decision_index`
            - `Record Status`: `active`
            - `Decision Status`: `accepted`
            - `Linked PRDs`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-13T02:00:00Z`

            ## Summary
            Exercises stale related-path filtering in decision index sync.

            ## Decision Statement
            Existing indexes should not preserve deleted related paths.

            ## Trigger or Source Request
            - Added for stale related-path regression coverage.

            ## Current Context and Constraints
            - The live fixture path must remain in the repository.

            ## Applied References and Implications
            - `docs/templates/`: live related path fixture.

            ## Affected Surfaces
            - docs/templates/

            ## Options Considered
            ### Option 1
            - Keep stale related paths.
            - Strength: no extra filtering.
            - Tradeoff: rebuilt entries rehydrate deleted paths.

            ### Option 2
            - Keep only existing related paths.
            - Strength: rebuild output stays deterministic.
            - Tradeoff: current-entry carry-over becomes stricter.

            ## Chosen Outcome
            Filter stale related paths.

            ## Rationale and Tradeoffs
            - Rebuilt indexes should not revive deleted references.

            ## Consequences and Follow-Up Impacts
            - Existing-entry carry-over must stay path-aware.

            ## Risks, Dependencies, and Assumptions
            - The live fixture path must exist.

            ## References
            - docs/templates/
            """
        ),
        encoding="utf-8",
    )
    index_path = repo_root / "core/control_plane/indexes/decisions/decision_index.v1.json"
    document = json.loads(index_path.read_text(encoding="utf-8"))
    document["entries"].append(
        {
            "trace_id": "trace.stale_decision_index",
            "decision_id": "decision.stale_decision_index",
            "title": "Stale Decision Index Coverage",
            "summary": "Exercises stale related-path filtering in decision index sync.",
            "record_status": "active",
            "decision_status": "accepted",
            "doc_path": "docs/planning/decisions/stale_related_paths.md",
            "updated_at": "2026-03-13T02:00:00Z",
            "uses_internal_references": False,
            "uses_external_references": False,
            "related_paths": ["docs/missing.md", "docs/templates/"],
        }
    )
    index_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")

    rebuilt = DecisionIndexSyncService(ControlPlaneLoader(repo_root)).build_document()
    entry = next(
        item
        for item in rebuilt["entries"]
        if item["decision_id"] == "decision.stale_decision_index"
    )
    assert entry["related_paths"] == ["docs/templates/"]
