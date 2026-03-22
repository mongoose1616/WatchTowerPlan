"""Terminal closeout coordination for initiative-package artifacts."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

TERMINAL_INITIATIVE_PACKAGE_STATUSES = frozenset(
    {"completed", "superseded", "cancelled"}
)
_PRE_CLOSEOUT_LIFECYCLE_STAGES = frozenset({"capture_incomplete", "ready_for_review"})
_TERMINAL_LIFECYCLE_STAGES = frozenset({"completed", "superseded", "cancelled"})


def _mapping_value(
    document: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = document.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"Initiative package field {key} must be a mapping.")
    return value


def _iterable_values(
    document: Mapping[str, object],
    key: str,
) -> Iterable[object]:
    value = document.get(key, ())
    if isinstance(value, Iterable) and not isinstance(value, str):
        return value
    raise ValueError(f"Initiative package field {key} must be an iterable.")


@dataclass(frozen=True, slots=True)
class CloseoutArtifactDocument:
    """One initiative-local artifact participating in terminal closeout."""

    relative_path: str
    document: dict[str, object]

    @property
    def artifact_id(self) -> str:
        """Return the governed artifact identifier."""

        return str(self.document["id"])


@dataclass(frozen=True, slots=True)
class InitiativePackageCloseoutPlan:
    """Prepared initiative-package mutations for one terminal closeout."""

    initiative_document: dict[str, object]
    evidence_documents: tuple[CloseoutArtifactDocument, ...]
    closeout_documents: tuple[CloseoutArtifactDocument, ...]
    promotion_documents: tuple[CloseoutArtifactDocument, ...]
    promotion_review_required: bool


class InitiativePackageCloseoutHelper:
    """Coordinate initiative-package closeout recap, evidence, and promotion artifacts."""

    def prepare_terminal_closeout(
        self,
        *,
        initiative_document: dict[str, object],
        evidence_documents: tuple[CloseoutArtifactDocument, ...],
        closeout_documents: tuple[CloseoutArtifactDocument, ...],
        promotion_documents: tuple[CloseoutArtifactDocument, ...],
        initiative_status: str,
        closure_reason: str,
        closed_at: str,
        superseded_by_trace_id: str | None = None,
        open_task_ids: tuple[str, ...] = (),
    ) -> InitiativePackageCloseoutPlan:
        """Validate and prepare initiative-package artifact mutations for closeout."""

        if initiative_status not in TERMINAL_INITIATIVE_PACKAGE_STATUSES:
            allowed = ", ".join(sorted(TERMINAL_INITIATIVE_PACKAGE_STATUSES))
            raise ValueError(
                "Terminal closeout requires initiative_status in " + allowed + "."
            )
        if initiative_status == "superseded" and not superseded_by_trace_id:
            raise ValueError(
                "Superseded terminal closeout requires superseded_by_trace_id."
            )
        if initiative_status != "superseded" and superseded_by_trace_id is not None:
            raise ValueError(
                "superseded_by_trace_id is only valid when initiative_status is superseded."
            )

        current_stage = str(initiative_document["lifecycle_stage"])
        if current_stage in _PRE_CLOSEOUT_LIFECYCLE_STAGES:
            raise ValueError(
                "Terminal closeout requires an execution-ready or closing initiative package."
            )
        if current_stage in _TERMINAL_LIFECYCLE_STAGES:
            raise ValueError(
                f"Initiative package is already terminal: {current_stage}."
            )
        if open_task_ids:
            joined = ", ".join(open_task_ids)
            raise ValueError(
                "Terminal closeout requires every initiative-local task to be completed "
                f"or cancelled: {joined}"
            )

        _require_expected_artifacts(
            initiative_document,
            artifact_documents=evidence_documents,
            artifact_field="evidence_ids",
            artifact_label="evidence",
        )
        _require_expected_artifacts(
            initiative_document,
            artifact_documents=closeout_documents,
            artifact_field="closeout_ids",
            artifact_label="closeout",
        )
        _require_expected_artifacts(
            initiative_document,
            artifact_documents=promotion_documents,
            artifact_field="promotion_ids",
            artifact_label="promotion",
        )

        mutated_initiative = dict(initiative_document)
        mutated_initiative["status"] = initiative_status
        mutated_initiative["lifecycle_stage"] = initiative_status
        mutated_initiative["review_status"] = "approved"
        mutated_initiative["updated_at"] = closed_at
        mutated_initiative["closed_at"] = closed_at
        mutated_initiative["closure_reason"] = closure_reason
        if superseded_by_trace_id is not None:
            mutated_initiative["superseded_by_trace_id"] = superseded_by_trace_id
        else:
            mutated_initiative.pop("superseded_by_trace_id", None)
        gate_state = _mapping_value(initiative_document, "gate_state")
        mutated_initiative["gate_state"] = {
            "capture_complete": True,
            "machine_valid": True,
            "approval_status": str(gate_state["approval_status"]),
            "ready_for_execution": False,
            "blocking_reasons": [],
        }

        mutated_evidence = tuple(
            CloseoutArtifactDocument(
                relative_path=artifact.relative_path,
                document={
                    **artifact.document,
                    "status": "completed",
                    "updated_at": closed_at,
                },
            )
            for artifact in evidence_documents
        )
        mutated_closeouts = tuple(
            CloseoutArtifactDocument(
                relative_path=artifact.relative_path,
                document={
                    **artifact.document,
                    "status": "completed",
                    "updated_at": closed_at,
                    "terminal_state": initiative_status,
                    "closed_at": closed_at,
                    "closure_reason": closure_reason,
                },
            )
            for artifact in closeout_documents
        )
        mutated_promotions = tuple(
            CloseoutArtifactDocument(
                relative_path=artifact.relative_path,
                document={
                    **artifact.document,
                    **(
                        {
                            "status": (
                                "rejected"
                                if initiative_status == "cancelled"
                                else "candidate"
                            )
                        }
                        if str(artifact.document.get("status", "planned")) == "planned"
                        else {}
                    ),
                    "updated_at": closed_at,
                },
            )
            for artifact in promotion_documents
        )

        return InitiativePackageCloseoutPlan(
            initiative_document=mutated_initiative,
            evidence_documents=mutated_evidence,
            closeout_documents=mutated_closeouts,
            promotion_documents=mutated_promotions,
            promotion_review_required=any(
                bool(artifact.document.get("promotion_review_required"))
                for artifact in mutated_closeouts
            ),
        )


def _require_expected_artifacts(
    initiative_document: dict[str, object],
    *,
    artifact_documents: tuple[CloseoutArtifactDocument, ...],
    artifact_field: str,
    artifact_label: str,
) -> None:
    expected_ids = {
        str(value) for value in _iterable_values(initiative_document, artifact_field)
    }
    actual_ids = {artifact.artifact_id for artifact in artifact_documents}
    missing_ids = tuple(sorted(expected_ids - actual_ids))
    if missing_ids:
        raise ValueError(
            f"Initiative package is missing required {artifact_label} artifact(s): "
            + ", ".join(missing_ids)
        )
