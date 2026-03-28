from __future__ import annotations

from pathlib import Path

from watchtower_plan.workspace.models import PlanReadinessIndexEntry
from watchtower_plan.workspace.rendering import (
    initiative_dependency_and_risk_lines,
    initiative_objective_lines,
    initiative_promotion_lines,
    initiative_scope_lines,
)
from watchtower_plan.workspace.snapshots import PlanInitiativeSnapshot


def _snapshot(
    *,
    initiative_root: str,
    task_documents: tuple[dict[str, object], ...] = (),
    discrepancy_documents: tuple[dict[str, object], ...] = (),
    promotion_documents: tuple[dict[str, object], ...] = (),
    deferred_documents: tuple[dict[str, object], ...] = (),
) -> PlanInitiativeSnapshot:
    return PlanInitiativeSnapshot(
        initiative_document={
            "initiative_id": "initiative.watchtower_ctf_implementation_package_preservation",
            "trace_id": "trace.watchtower_ctf_implementation_package_preservation",
            "title": "WatchTower CTF Implementation Package Preservation",
            "summary": (
                "Captures the full CTF implementation package inside the governed "
                "WatchTower initiative."
            ),
            "scope_type": "project_scoped",
            "owner": "repository_maintainer",
            "lifecycle_stage": "ready_for_execution",
            "review_status": "approved",
        },
        task_documents=task_documents,
        event_documents=(),
        deferred_documents=deferred_documents,
        discrepancy_documents=discrepancy_documents,
        evidence_documents=(),
        closeout_documents=(),
        promotion_documents=promotion_documents,
        initiative_slug="watchtower_ctf_implementation_package_preservation",
        initiative_root=initiative_root,
        project_slug="watchtower",
        project_root="plan/projects/watchtower",
        discrepancy_namespace="watchtower.watchtower_ctf_implementation_package_preservation",
        acceptance_contract_ids=(),
        trace_evidence_ids=(),
    )


def _readiness() -> PlanReadinessIndexEntry:
    return PlanReadinessIndexEntry(
        initiative_id="initiative.watchtower_ctf_implementation_package_preservation",
        project_id="project.watchtower",
        trace_id="trace.watchtower_ctf_implementation_package_preservation",
        title="WatchTower CTF Implementation Package Preservation",
        initiative_root=(
            "plan/projects/watchtower/initiatives/"
            "watchtower_ctf_implementation_package_preservation"
        ),
        lifecycle_stage="ready_for_execution",
        review_status="approved",
        capture_complete=True,
        machine_valid=True,
        approval_status="approved",
        ready_for_execution=True,
        blocking_reasons=(),
        updated_at="2026-03-28T02:00:00Z",
        scope_type="project_scoped",
    )


def test_initiative_scope_lines_surface_non_goals_and_locked_deferrals(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    initiative_root = (
        repo_root
        / "plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation"
    )
    initiative_root.mkdir(parents=True, exist_ok=True)
    (initiative_root / "initiative_brief.md").write_text(
        "\n".join(
            (
                "# Initiative Brief",
                "",
                "## Non-Goals",
                "- Do not mutate `/home/j/WatchTower` during this initiative.",
                "",
            )
        ),
        encoding="utf-8",
    )
    (initiative_root / "decision_notes.md").write_text(
        "\n".join(
            (
                "# Decision Notes",
                "",
                "## Locked Post-V1 Deferrals",
                "- `decision.workflow_catalog`: defer richer workflow catalog behavior beyond v1.",
                "",
            )
        ),
        encoding="utf-8",
    )
    snapshot = _snapshot(
        initiative_root=(
            "plan/projects/watchtower/initiatives/"
            "watchtower_ctf_implementation_package_preservation"
        )
    )

    lines = initiative_scope_lines(snapshot, repo_root=repo_root)

    assert any("Non-goal: Do not mutate `/home/j/WatchTower`" in line for line in lines)
    assert any("Locked post-v1 deferral:" in line for line in lines)


def test_initiative_objective_lines_skip_cancelled_placeholder_tasks() -> None:
    snapshot = _snapshot(
        initiative_root=(
            "plan/projects/watchtower/initiatives/"
            "watchtower_ctf_implementation_package_preservation"
        ),
        task_documents=(
            {
                "task_id": "task.example.bootstrap",
                "title": "Bootstrap Placeholder",
                "summary": "Retired placeholder task.",
                "task_status": "cancelled",
            },
            {
                "task_id": "task.example.phase_0",
                "title": "Phase 0 Shared Contract Adoption And Alignment",
                "summary": "Revalidate the live baseline before target-repo mutation.",
                "task_status": "ready",
            },
        ),
    )

    lines = initiative_objective_lines(snapshot)

    assert any("Phase 0 Shared Contract Adoption And Alignment" in line for line in lines)
    assert not any("Bootstrap Placeholder" in line for line in lines)


def test_initiative_dependency_and_risk_lines_skip_resolved_discrepancies() -> None:
    snapshot = _snapshot(
        initiative_root=(
            "plan/projects/watchtower/initiatives/"
            "watchtower_ctf_implementation_package_preservation"
        ),
        discrepancy_documents=(
            {
                "discrepancy_id": "discrepancy.example.resolved",
                "severity": "high",
                "category": "stale_rendered_surface",
                "status": "resolved",
                "summary": "Resolved discrepancy should not appear in current risks.",
            },
        ),
    )

    lines = initiative_dependency_and_risk_lines(snapshot, readiness=_readiness())

    assert lines == ("- No current blockers, dependencies, or open discrepancy risks are recorded.",)


def test_initiative_promotion_lines_do_not_link_missing_candidate_targets(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    snapshot = _snapshot(
        initiative_root=(
            "plan/projects/watchtower/initiatives/"
            "watchtower_ctf_implementation_package_preservation"
        ),
        promotion_documents=(
            {
                "id": "promotion.watchtower_ctf_implementation_package_preservation.bootstrap_shell",
                "status": "planned",
                "approval_state": "pending",
                "candidates": [
                    {
                        "target_path": (
                            "plan/docs/references/"
                            "watchtower_ctf_implementation_package_preservation_initiative_brief.md"
                        )
                    }
                ],
            },
        ),
    )

    lines = initiative_promotion_lines(snapshot, repo_root=repo_root)

    assert any("Candidate target path (planned, not yet promoted)" in line for line in lines)
    assert not any("](/plan/docs/references/" in line for line in lines)
