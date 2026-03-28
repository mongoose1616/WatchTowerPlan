from __future__ import annotations

from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.testing.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_minimal_plan_pack,
)
from watchtower_plan.validation import DocumentSemanticsValidationService
from watchtower_plan.validation.document_semantics import (
    INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
PROJECT_INITIATIVE_PACKAGE_ROOT = (
    "plan/projects/watchtower/initiatives/"
    "watchtower_ctf_implementation_package_preservation"
)
BOOTSTRAPPED_INITIATIVE_ROOT = "plan/initiatives/generic_document_semantics_bootstrap"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "plan" / ".wt", repo_root / "plan" / ".wt")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _build_bootstrapped_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.generic_document_semantics_bootstrap",
        title="Generic Document Semantics Bootstrap",
        summary="Bootstraps one ordinary initiative to prove the validator stays generic.",
        include_decision_notes=True,
    )
    return repo_root


def _write_fixture_document(
    repo_root: Path,
    *,
    initiative_root: str,
    filename: str,
    section_titles: tuple[str, ...],
) -> None:
    target_path = repo_root / initiative_root / filename
    target_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Example {target_path.stem.replace('_', ' ').title()}", ""]
    for title in section_titles:
        lines.extend((f"## {title}", f"Example content for {title}.", ""))
    target_path.write_text("\n".join(lines), encoding="utf-8")


def test_initiative_handoff_semantics_accepts_bootstrapped_packwide_initiative(
    tmp_path: Path,
) -> None:
    repo_root = _build_bootstrapped_repo(tmp_path)
    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))

    canonical_result = service.validate(
        f"{BOOTSTRAPPED_INITIATIVE_ROOT}/initiative_brief.md"
    )
    rendered_result = service.validate(f"{BOOTSTRAPPED_INITIATIVE_ROOT}/plan.md")

    assert canonical_result.passed is True
    assert (
        canonical_result.validator_id
        == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID
    )
    assert rendered_result.passed is True
    assert (
        rendered_result.validator_id
        == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID
    )


def test_initiative_handoff_semantics_rejects_missing_required_canonical_anchor(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    _write_fixture_document(
        repo_root,
        initiative_root=PROJECT_INITIATIVE_PACKAGE_ROOT,
        filename="initiative_brief.md",
        section_titles=("Summary", "Identity"),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate(f"{PROJECT_INITIATIVE_PACKAGE_ROOT}/initiative_brief.md")

    assert result.passed is False
    assert result.validator_id == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID
    assert result.issue_count == 1
    assert (
        "missing required sections: Initial Task Set / Goals / Execution Task Chain"
        in result.issues[0].message
    )


def test_initiative_handoff_semantics_rejects_missing_required_section_in_rendered_summary(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    _write_fixture_document(
        repo_root,
        initiative_root=PROJECT_INITIATIVE_PACKAGE_ROOT,
        filename="summary.md",
        section_titles=(
            "Outcome Summary",
            "Delivered Outputs",
            "Evidence References",
            "Unresolved Follow-Ups",
            "Closeout State",
        ),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate(f"{PROJECT_INITIATIVE_PACKAGE_ROOT}/summary.md")

    assert result.passed is False
    assert result.validator_id == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID
    assert result.issue_count == 1
    assert "missing required sections: Promoted Guidance" in result.issues[0].message


def test_initiative_handoff_semantics_rejects_cold_start_read_order_that_skips_canonical_docs(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    _write_fixture_document(
        repo_root,
        initiative_root=PROJECT_INITIATIVE_PACKAGE_ROOT,
        filename="cold_start_runbook.md",
        section_titles=(
            "Summary",
            "Cold-Start Findings",
            "Read Order",
            "Questions To Answer",
            "Command Anchors",
            "Where To Record Outcomes",
            "Done When",
        ),
    )
    target_path = repo_root / PROJECT_INITIATIVE_PACKAGE_ROOT / "cold_start_runbook.md"
    target_path.write_text(
        target_path.read_text(encoding="utf-8").replace(
            "Example content for Read Order.",
            "1. Read `README.md`.\n2. Read `implementation_slice.md`.\n3. Read `phase_output_manifest.md`.",
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate(f"{PROJECT_INITIATIVE_PACKAGE_ROOT}/cold_start_runbook.md")

    assert result.passed is False
    assert result.validator_id == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID
    assert result.issue_count == 1
    assert "Read Order is missing required canonical docs" in result.issues[0].message


def test_initiative_handoff_semantics_rejects_rendered_plan_fallback_and_resolved_risk_lines(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    package_root = repo_root / PROJECT_INITIATIVE_PACKAGE_ROOT
    _write_fixture_document(
        repo_root,
        initiative_root=PROJECT_INITIATIVE_PACKAGE_ROOT,
        filename="initiative_brief.md",
        section_titles=("Summary", "Identity", "Goals"),
    )
    _write_fixture_document(
        repo_root,
        initiative_root=PROJECT_INITIATIVE_PACKAGE_ROOT,
        filename="decision_notes.md",
        section_titles=("Summary", "Locked Post-V1 Deferrals"),
    )
    _write_fixture_document(
        repo_root,
        initiative_root=PROJECT_INITIATIVE_PACKAGE_ROOT,
        filename="plan.md",
        section_titles=(
            "Initiative Identity",
            "Scope and Non-Goals",
            "Objectives",
            "Planned Slices or Workstreams",
            "Dependencies and Risks",
            "Validation or Completion Gates",
            "Linked Outputs",
        ),
    )
    (package_root / "initiative_brief.md").write_text(
        (package_root / "initiative_brief.md")
        .read_text(encoding="utf-8")
        .replace(
            "Example content for Goals.",
            "- Do not mutate `/home/j/WatchTower` during this initiative.",
        ),
        encoding="utf-8",
    )
    (package_root / "decision_notes.md").write_text(
        (package_root / "decision_notes.md")
        .read_text(encoding="utf-8")
        .replace(
            "Example content for Locked Post-V1 Deferrals.",
            "- `decision.workflow_catalog`: defer richer workflow catalog behavior beyond v1.",
        ),
        encoding="utf-8",
    )
    (package_root / "plan.md").write_text(
        (package_root / "plan.md")
        .read_text(encoding="utf-8")
        .replace(
            "Example content for Scope and Non-Goals.",
            "- No explicit non-goals or deferred scope items are recorded.",
        )
        .replace(
            "Example content for Dependencies and Risks.",
            "- Discrepancy `discrepancy.example.resolved`: `high` `stale_rendered_surface` / `resolved`. Old resolved drift.",
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate(f"{PROJECT_INITIATIVE_PACKAGE_ROOT}/plan.md")

    assert result.passed is False
    assert result.validator_id == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID
    assert result.issue_count == 1
    assert "non-goals or deferred scope items" in result.issues[0].message
