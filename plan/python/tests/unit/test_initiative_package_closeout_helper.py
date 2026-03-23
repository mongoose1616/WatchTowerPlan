from __future__ import annotations

import pytest
from watchtower_plan.closeout import (
    CloseoutArtifactDocument,
    InitiativePackageCloseoutHelper,
)


def _initiative_document() -> dict[str, object]:
    return {
        "initiative_id": "initiative.example",
        "trace_id": "trace.example",
        "status": "active",
        "lifecycle_stage": "ready_for_execution",
        "review_status": "approved",
        "updated_at": "2026-03-18T02:50:00Z",
        "evidence_ids": ["evidence.example.bootstrap_validation_bundle"],
        "closeout_ids": ["closeout.example.bootstrap_recap"],
        "promotion_ids": ["promotion.example.bootstrap_shell"],
        "gate_state": {
            "capture_complete": True,
            "machine_valid": True,
            "approval_status": "approved",
            "ready_for_execution": True,
            "blocking_reasons": [],
        },
    }


def test_initiative_package_closeout_helper_coordinates_terminal_artifacts() -> None:
    helper = InitiativePackageCloseoutHelper()

    result = helper.prepare_terminal_closeout(
        initiative_document=_initiative_document(),
        evidence_documents=(
            CloseoutArtifactDocument(
                relative_path="plan/initiatives/example/.wt/evidence/validation_bundle.bootstrap.json",
                document={
                    "id": "evidence.example.bootstrap_validation_bundle",
                    "status": "planned",
                    "updated_at": "2026-03-18T02:50:00Z",
                },
            ),
        ),
        closeout_documents=(
            CloseoutArtifactDocument(
                relative_path="plan/initiatives/example/.wt/closeout/closeout_recap.bootstrap.json",
                document={
                    "id": "closeout.example.bootstrap_recap",
                    "status": "planned",
                    "updated_at": "2026-03-18T02:50:00Z",
                    "promotion_review_required": True,
                },
            ),
        ),
        promotion_documents=(
            CloseoutArtifactDocument(
                relative_path="plan/initiatives/example/.wt/promotions/guidance_promotion_record.bootstrap.json",
                document={
                    "id": "promotion.example.bootstrap_shell",
                    "status": "planned",
                    "updated_at": "2026-03-18T02:50:00Z",
                },
            ),
        ),
        initiative_status="completed",
        closure_reason="Delivered the bounded slice.",
        closed_at="2026-03-18T02:55:00Z",
    )

    assert result.initiative_document["status"] == "completed"
    assert result.initiative_document["lifecycle_stage"] == "completed"
    assert result.initiative_document["closed_at"] == "2026-03-18T02:55:00Z"
    assert result.evidence_documents[0].document["status"] == "completed"
    assert result.closeout_documents[0].document["terminal_state"] == "completed"
    assert result.promotion_documents[0].document["status"] == "candidate"
    assert result.promotion_review_required is True


def test_initiative_package_closeout_helper_requires_declared_companion_artifacts() -> None:
    helper = InitiativePackageCloseoutHelper()

    with pytest.raises(ValueError, match="missing required promotion artifact"):
        helper.prepare_terminal_closeout(
            initiative_document=_initiative_document(),
            evidence_documents=(
                CloseoutArtifactDocument(
                    relative_path="plan/initiatives/example/.wt/evidence/validation_bundle.bootstrap.json",
                    document={"id": "evidence.example.bootstrap_validation_bundle"},
                ),
            ),
            closeout_documents=(
                CloseoutArtifactDocument(
                    relative_path="plan/initiatives/example/.wt/closeout/closeout_recap.bootstrap.json",
                    document={"id": "closeout.example.bootstrap_recap"},
                ),
            ),
            promotion_documents=(),
            initiative_status="completed",
            closure_reason="Delivered the bounded slice.",
            closed_at="2026-03-18T02:55:00Z",
        )
