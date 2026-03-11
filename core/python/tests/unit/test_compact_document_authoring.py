from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_documents import (
    DECISION_REQUIRED_EXPLAINED_SECTIONS,
    DECISION_REQUIRED_SECTIONS,
    load_governed_document,
)
from watchtower_core.repo_ops.sync.decision_index import DECISION_FRONT_MATTER_SCHEMA_ID
from watchtower_core.repo_ops.task_documents import load_task_document

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    (repo_root / "docs").mkdir(parents=True)
    return repo_root


def test_load_governed_document_allows_lean_decision_records_with_applied_references(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    decision_path = repo_root / "docs/planning/decisions/lean_decision.md"
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    decision_path.write_text(
        dedent(
            """\
            ---
            trace_id: "trace.example_compact_authoring"
            id: "decision.example_compact_authoring"
            title: "Compact Authoring Decision"
            summary: "Records the compact-authoring choice for a bounded repository slice."
            type: "decision_record"
            status: "active"
            owner: "repository_maintainer"
            updated_at: "2026-03-10T16:11:26Z"
            audience: "shared"
            authority: "supporting"
            applies_to:
              - "docs/templates/"
            aliases:
              - "compact authoring decision"
            ---

            # Compact Authoring Decision

            ## Record Metadata
            - `Trace ID`: `trace.example_compact_authoring`
            - `Decision ID`: `decision.example_compact_authoring`
            - `Record Status`: `active`
            - `Decision Status`: `accepted`
            - `Linked PRDs`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-10T16:11:26Z`

            ## Summary
            Records the compact-authoring choice for a bounded repository slice.

            ## Decision Statement
            Prefer compact default templates and generated tracker outputs.

            ## Trigger or Source Request
            A repository review found that several templates and trackers normalize low-value
            boilerplate.

            ## Current Context and Constraints
            - The repo still needs governed front matter and stable machine-readable indexes.

            ## Applied References and Implications
            - docs/standards/documentation/decision_record_md_standard.md: keeps the compact
              decision shape aligned with the governed decision template.

            ## Affected Surfaces
            - `docs/templates/`
            - `docs/planning/`

            ## Options Considered
            ### Option 1
            - Keep the current verbose defaults.
            - Strength: no implementation work.
            - Tradeoff: continued low-value boilerplate.

            ### Option 2
            - Make compactness the default while preserving machine authority.
            - Strength: better signal density.
            - Tradeoff: requires validator and template alignment.

            ## Chosen Outcome
            Adopt compact defaults and keep machine authority in front matter and indexes.

            ## Rationale and Tradeoffs
            - The human-visible surfaces get shorter without weakening machine lookups.

            ## Consequences and Follow-Up Impacts
            - Templates and validators need to change together.

            ## Risks, Dependencies, and Assumptions
            - If validators stay strict in the wrong places, compact docs will fail needlessly.

            ## References
            - docs/standards/documentation/decision_record_md_standard.md
            """
        ),
        encoding="utf-8",
    )

    document = load_governed_document(
        ControlPlaneLoader(repo_root),
        "docs/planning/decisions/lean_decision.md",
        schema_id=DECISION_FRONT_MATTER_SCHEMA_ID,
        id_label="Decision ID",
        status_label="Record Status",
        required_sections=DECISION_REQUIRED_SECTIONS,
        required_explained_sections=DECISION_REQUIRED_EXPLAINED_SECTIONS,
    )

    assert document.document_id == "decision.example_compact_authoring"


def test_load_task_document_allows_lean_task_body(tmp_path: Path) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    task_path = repo_root / "docs/planning/tasks/open/lean_task.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        dedent(
            """\
            ---
            id: "task.example_compact_authoring.001"
            trace_id: "trace.example_compact_authoring"
            title: "Land compact authoring rules"
            summary: "Adds the compact-authoring standard and aligns the governed templates."
            type: "task"
            status: "active"
            task_status: "ready"
            task_kind: "governance"
            priority: "high"
            owner: "repository_maintainer"
            updated_at: "2026-03-10T16:11:26Z"
            audience: "shared"
            authority: "authoritative"
            applies_to:
              - "docs/templates/"
            related_ids:
              - "design.features.compact_document_authoring_and_tracking"
            ---

            # Land compact authoring rules

            ## Summary
            Adds the compact-authoring standard and aligns the governed templates.

            ## Scope
            - Add the compact-authoring standard.
            - Align templates and validators in the same slice.

            ## Done When
            - Compact defaults are durable and validated.
            """
        ),
        encoding="utf-8",
    )

    document = load_task_document(
        ControlPlaneLoader(repo_root),
        "docs/planning/tasks/open/lean_task.md",
    )

    assert document.task_id == "task.example_compact_authoring.001"
