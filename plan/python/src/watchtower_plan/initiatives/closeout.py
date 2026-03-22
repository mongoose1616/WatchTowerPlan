"""Terminal closeout flows for live initiative packages."""

from __future__ import annotations

from watchtower_plan.closeout.initiative_package import (
    CloseoutArtifactDocument,
    InitiativePackageCloseoutHelper,
)
from watchtower_core.utils.timestamps import utc_timestamp_now

from watchtower_plan.initiatives.discrepancies import InitiativeDiscrepancyCoordinator
from watchtower_plan.initiatives.locations import (
    InitiativeLocation,
    InitiativeLocationManager,
)
from watchtower_plan.initiatives.models import InitiativeTerminalCloseoutResult
from watchtower_plan.initiatives.readiness import InitiativeReadinessCoordinator


class InitiativeCloseoutCoordinator:
    """Transition initiative packages into terminal closeout states."""

    def __init__(
        self,
        context: InitiativeLocationManager,
        discrepancies: InitiativeDiscrepancyCoordinator,
        readiness: InitiativeReadinessCoordinator,
    ) -> None:
        self._context = context
        self._discrepancies = discrepancies
        self._readiness = readiness

    def close_initiative(
        self,
        location: InitiativeLocation,
        *,
        initiative_status: str,
        closure_reason: str,
        write: bool,
        closed_at: str | None,
        superseded_by_trace_id: str | None,
    ) -> InitiativeTerminalCloseoutResult:
        if initiative_status not in {"completed", "superseded", "cancelled"}:
            raise ValueError(
                "Terminal closeout requires initiative_status in completed, superseded, or cancelled."
            )
        if initiative_status == "superseded" and not superseded_by_trace_id:
            raise ValueError(
                "Superseded terminal closeout requires superseded_by_trace_id."
            )
        if initiative_status != "superseded" and superseded_by_trace_id is not None:
            raise ValueError(
                "superseded_by_trace_id is only valid when initiative_status is superseded."
            )
        initiative_state_path = self._context.initiative_path(
            location, ".wt/initiative.json"
        )
        initiative_document = self._context.load_json(initiative_state_path)
        if superseded_by_trace_id == str(initiative_document["trace_id"]):
            raise ValueError("An initiative cannot supersede itself.")
        if superseded_by_trace_id is not None and not self._context.trace_id_exists(
            superseded_by_trace_id
        ):
            raise ValueError(
                f"Superseded-by trace_id does not exist in the live plan workspace: {superseded_by_trace_id}"
            )
        current_stage = str(initiative_document["lifecycle_stage"])
        if current_stage in {"capture_incomplete", "ready_for_review"}:
            raise ValueError(
                "Terminal closeout requires an execution-ready or closing initiative package."
            )
        if current_stage in {"completed", "superseded", "cancelled"}:
            raise ValueError(
                f"Initiative package is already terminal: {current_stage}."
            )

        readiness = self._readiness.validate_initiative(
            location,
            write=False,
            require_approved=False,
        )
        if not readiness.passed:
            joined = "; ".join(readiness.issue_messages)
            raise ValueError(
                "Initiative package is not clean enough for terminal closeout: "
                + joined
            )

        open_task_ids = tuple(
            str(task_document["task_id"])
            for task_document in self._context.task_documents(location)
            if str(task_document["task_status"]) not in {"completed", "cancelled"}
        )
        closed_at_value = closed_at or utc_timestamp_now()

        evidence_documents = self._context.artifact_documents(
            location, ".wt/evidence", "*.json"
        )
        closeout_documents = self._context.artifact_documents(
            location, ".wt/closeout", "*.json"
        )
        promotion_documents = self._context.artifact_documents(
            location,
            ".wt/promotions",
            "*.json",
        )
        closeout_plan = InitiativePackageCloseoutHelper().prepare_terminal_closeout(
            initiative_document=initiative_document,
            evidence_documents=tuple(
                CloseoutArtifactDocument(relative_path=relative_path, document=document)
                for relative_path, document in evidence_documents
            ),
            closeout_documents=tuple(
                CloseoutArtifactDocument(relative_path=relative_path, document=document)
                for relative_path, document in closeout_documents
            ),
            promotion_documents=tuple(
                CloseoutArtifactDocument(relative_path=relative_path, document=document)
                for relative_path, document in promotion_documents
            ),
            initiative_status=initiative_status,
            closure_reason=closure_reason,
            closed_at=closed_at_value,
            superseded_by_trace_id=superseded_by_trace_id,
            open_task_ids=open_task_ids,
        )

        if write:
            if current_stage != "closing":
                self._discrepancies.append_initiative_event(
                    location=location,
                    initiative_id=str(
                        closeout_plan.initiative_document["initiative_id"]
                    ),
                    trace_id=str(closeout_plan.initiative_document["trace_id"]),
                    event_type="closing_started",
                    summary="The initiative package entered closing before terminal closeout.",
                    actor_id="actor.watchtower_core",
                    recorded_at=closed_at_value,
                )

            self._context.pack_loader().artifact_store.write_json_object(
                initiative_state_path,
                closeout_plan.initiative_document,
            )
            for artifact in closeout_plan.evidence_documents:
                self._context.pack_loader().artifact_store.write_json_object(
                    artifact.relative_path,
                    artifact.document,
                )
            for artifact in closeout_plan.closeout_documents:
                self._context.pack_loader().artifact_store.write_json_object(
                    artifact.relative_path,
                    artifact.document,
                )
            for artifact in closeout_plan.promotion_documents:
                self._context.pack_loader().artifact_store.write_json_object(
                    artifact.relative_path,
                    artifact.document,
                )
            self._discrepancies.append_initiative_event(
                location=location,
                initiative_id=str(closeout_plan.initiative_document["initiative_id"]),
                trace_id=str(closeout_plan.initiative_document["trace_id"]),
                event_type=initiative_status,
                summary=f"The initiative package reached terminal closeout as {initiative_status}.",
                actor_id="actor.repository_maintainer",
                recorded_at=closed_at_value,
            )
            self._context.sync_derived_surfaces(location)

        return InitiativeTerminalCloseoutResult(
            initiative_id=str(closeout_plan.initiative_document["initiative_id"]),
            trace_id=str(closeout_plan.initiative_document["trace_id"]),
            initiative_root=location.initiative_root_relative,
            initiative_status=initiative_status,
            closed_at=closed_at_value,
            closure_reason=closure_reason,
            scope_type=location.scope_type,
            superseded_by_trace_id=superseded_by_trace_id,
            wrote=write,
        )


__all__ = ["InitiativeCloseoutCoordinator"]
