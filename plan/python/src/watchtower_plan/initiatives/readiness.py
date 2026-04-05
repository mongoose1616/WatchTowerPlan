"""Readiness, confirmation, and approval flows for live initiative packages."""

from __future__ import annotations

import json
from typing import Any, cast

from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_core.validation import ArtifactValidationService, ValidationResult
from watchtower_plan.governing_documents import (
    effective_initiative_governing_document_paths,
)
from watchtower_plan.initiatives.discrepancies import InitiativeDiscrepancyCoordinator
from watchtower_plan.initiatives.locations import (
    InitiativeLocation,
    InitiativeLocationManager,
)
from watchtower_plan.initiatives.models import (
    InitiativePackageResult,
    InitiativeReadinessResult,
)
from watchtower_plan.projects import ProjectWorkspaceService
from watchtower_plan.workspace.service import PlanWorkspaceService


class InitiativeReadinessCoordinator:
    """Validate initiative packages and advance them through review and approval."""

    def __init__(
        self,
        context: InitiativeLocationManager,
        discrepancies: InitiativeDiscrepancyCoordinator,
    ) -> None:
        self._context = context
        self._discrepancies = discrepancies

    def validate_initiative(
        self,
        location: InitiativeLocation,
        *,
        write: bool,
        require_approved: bool,
    ) -> InitiativeReadinessResult:
        initiative_state_path = self._context.initiative_path(
            location, ".wt/initiative.json"
        )
        initiative_document = self.reconcile_initiative_state_document(
            location,
            self._context.load_json(initiative_state_path),
        )
        initiative_id = str(initiative_document["initiative_id"])
        trace_id = str(initiative_document["trace_id"])
        previous_lifecycle_stage = str(initiative_document["lifecycle_stage"])

        validator = ArtifactValidationService(self._context.pack_loader())
        artifact_paths = self._context.artifact_paths_for_location(location)
        artifact_results = tuple(
            validator.validate(relative_path) for relative_path in artifact_paths
        )

        issues: list[str] = []
        blocking_reasons: list[str] = []
        if not artifact_results:
            issues.append(
                "No plan initiative artifacts were found under the initiative root."
            )
            blocking_reasons.append("missing_artifacts")
        for result in artifact_results:
            if not result.passed:
                issues.append(
                    f"{result.target_path} failed {result.validator_id} with "
                    f"{result.issue_count} issue(s)."
                )

        if location.scope_type == "project_scoped":
            project_validation = ProjectWorkspaceService(
                self._context.fresh_loader()
            ).validate(
                location.project_slug or "",
                write=False,
            )
            if not project_validation.passed:
                issues.extend(project_validation.issue_messages)
                blocking_reasons.append("project_bootstrap_invalid")

        authored_input_issues = self._discrepancies.authored_input_drift_issues(
            location=location,
            initiative_document=initiative_document,
        )
        issues.extend(issue.summary for issue in authored_input_issues)
        if authored_input_issues:
            blocking_reasons.append("authored_input_drift")

        if write:
            self._context.pack_loader().artifact_store.write_json_object(
                initiative_state_path,
                initiative_document,
            )

        derived_surface_issues = self._discrepancies.stale_derived_surface_issues(
            location
        )
        if location.scope_type == "project_scoped":
            derived_surface_issues = (
                *derived_surface_issues,
                *self._discrepancies.project_surface_issues(location),
            )
        issues.extend(issue.summary for issue in derived_surface_issues)
        if derived_surface_issues:
            blocking_reasons.append("stale_derived_surfaces")

        machine_root_issues = self._discrepancies.machine_root_policy_issues(location)
        issues.extend(machine_root_issues)
        if machine_root_issues:
            blocking_reasons.append("machine_root_policy")

        deferred_issues = self._discrepancies.blocking_deferred_item_issues(location)
        issues.extend(deferred_issues)
        if deferred_issues:
            blocking_reasons.append("blocking_deferred_items")

        if write:
            self._discrepancies.sync_managed_discrepancies(
                location=location,
                initiative_id=initiative_id,
                discrepancy_issues=(*authored_input_issues, *derived_surface_issues),
                updated_at=utc_timestamp_now(),
            )
            if derived_surface_issues:
                PlanWorkspaceService(
                    self._context.fresh_loader()
                ).sync_discrepancy_index(write=True)
        open_discrepancies = self._discrepancies.open_discrepancy_documents(location)
        if open_discrepancies:
            issues.extend(
                f"Open discrepancy {document['discrepancy_id']} blocks readiness."
                for _, document in open_discrepancies
                if document["gate_effect"] != "none"
            )
            if any(
                document["gate_effect"] != "none" for _, document in open_discrepancies
            ):
                blocking_reasons.append("open_discrepancies")

        if (
            require_approved
            and initiative_document["gate_state"]["approval_status"] != "approved"
        ):
            issues.append("The initiative package is not approved for execution.")
            blocking_reasons.append("approval_pending")

        passed = not issues and all(result.passed for result in artifact_results)
        current_lifecycle_stage = str(initiative_document["lifecycle_stage"])
        approval_status = str(initiative_document["gate_state"]["approval_status"])
        lifecycle_stage = current_lifecycle_stage
        execution_started = self._context.has_execution_started(location)
        if passed:
            if current_lifecycle_stage in {
                "closing",
                "completed",
                "superseded",
                "cancelled",
            }:
                lifecycle_stage = current_lifecycle_stage
            elif approval_status == "approved" and execution_started:
                lifecycle_stage = "in_progress"
            elif approval_status == "approved":
                lifecycle_stage = "ready_for_execution"
            else:
                lifecycle_stage = "ready_for_review"
        elif issues:
            if current_lifecycle_stage in {
                "closing",
                "completed",
                "superseded",
                "cancelled",
            }:
                lifecycle_stage = current_lifecycle_stage
            else:
                lifecycle_stage = (
                    "blocked"
                    if current_lifecycle_stage
                    in {"ready_for_execution", "in_progress", "blocked"}
                    or (approval_status == "approved" and execution_started)
                    else "capture_incomplete"
                )

        discrepancy_ids = tuple(
            document["discrepancy_id"] for _, document in open_discrepancies
        )
        if write:
            initiative_document["updated_at"] = utc_timestamp_now()
            initiative_document["lifecycle_stage"] = lifecycle_stage
            initiative_document["review_status"] = (
                "approved"
                if initiative_document["gate_state"]["approval_status"] == "approved"
                else "pending"
            )
            initiative_document["discrepancy_ids"] = list(discrepancy_ids)
            initiative_document["gate_state"] = {
                "capture_complete": not any(
                    reason
                    in {
                        "missing_artifacts",
                        "blocking_deferred_items",
                        "project_bootstrap_invalid",
                    }
                    for reason in blocking_reasons
                ),
                "machine_valid": not issues,
                "approval_status": approval_status,
                "ready_for_execution": (
                    approval_status == "approved"
                    and lifecycle_stage
                    not in {"capture_incomplete", "ready_for_review"}
                ),
                "blocking_reasons": sorted(set(blocking_reasons)),
            }
            self._context.pack_loader().artifact_store.write_json_object(
                initiative_state_path,
                initiative_document,
            )

            if (
                passed
                and lifecycle_stage == "ready_for_review"
                and previous_lifecycle_stage != "ready_for_review"
            ):
                self._discrepancies.append_initiative_event(
                    location=location,
                    initiative_id=initiative_id,
                    trace_id=trace_id,
                    event_type="ready_for_review_marked",
                    summary=(
                        "The initiative package passed capture validation and is "
                        "ready for review."
                    ),
                    actor_id="actor.watchtower_core",
                    recorded_at=str(initiative_document["updated_at"]),
                )
            if not derived_surface_issues:
                self._context.sync_derived_surfaces(location)

        return InitiativeReadinessResult(
            initiative_id=initiative_id,
            trace_id=trace_id,
            initiative_root=location.initiative_root_relative,
            passed=passed,
            lifecycle_stage=lifecycle_stage,
            issue_messages=tuple(issues),
            artifact_results=artifact_results,
            open_discrepancy_ids=tuple(discrepancy_ids),
            blocking_reasons=tuple(sorted(set(blocking_reasons))),
            wrote=write,
        )

    def confirm_authored_inputs(
        self,
        location: InitiativeLocation,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        self._discrepancies.assert_default_authorized_maintainer(approver_actor_id)
        initiative_state_path = self._context.initiative_path(
            location, ".wt/initiative.json"
        )
        initiative_document = self._context.load_json(initiative_state_path)
        updated_at = utc_timestamp_now()

        for record in initiative_document["authored_inputs"]:
            path = str(record["path"])
            record["sha256"] = self._context.sha256_for_relative_path(path)
            record["proposal_status"] = "confirmed"
            record["last_confirmed_at"] = updated_at
            record["last_confirmed_by"] = approver_actor_id
        initiative_document.setdefault("approvals", []).append(
            {
                "approval_kind": "authored_input_confirmation",
                "actor_id": approver_actor_id,
                "approved_at": updated_at,
            }
        )
        initiative_document["governing_document_paths"] = list(
            effective_initiative_governing_document_paths(
                initiative_document,
                repo_root=self._context.pack_loader().repo_root,
            )
        )
        initiative_document["updated_at"] = updated_at
        if write:
            self._context.pack_loader().artifact_store.write_json_object(
                initiative_state_path,
                initiative_document,
            )
            self._discrepancies.append_initiative_event(
                location=location,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="authored_inputs_confirmed",
                summary=(
                    "An authorized maintainer confirmed the authored intake "
                    "documents into machine state."
                ),
                actor_id=approver_actor_id,
                recorded_at=updated_at,
            )
            self._context.sync_derived_surfaces(location)
            readiness = self.validate_initiative(
                location,
                write=True,
                require_approved=False,
            )
        else:
            readiness = self.validate_initiative(
                location,
                write=False,
                require_approved=False,
            )
        refreshed_state = self._context.load_json(initiative_state_path)
        return InitiativePackageResult(
            initiative_id=str(refreshed_state["initiative_id"]),
            trace_id=str(refreshed_state["trace_id"]),
            initiative_root=location.initiative_root_relative,
            lifecycle_stage=str(refreshed_state["lifecycle_stage"]),
            review_status=str(refreshed_state["review_status"]),
            ready_for_execution=bool(
                refreshed_state["gate_state"]["ready_for_execution"]
            ),
            validation_passed=readiness.passed,
            wrote=write,
        )

    def approve_initiative(
        self,
        location: InitiativeLocation,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        self._discrepancies.assert_default_authorized_maintainer(approver_actor_id)
        readiness = self.validate_initiative(
            location,
            write=False,
            require_approved=False,
        )
        if write and not readiness.passed:
            readiness = self.validate_initiative(
                location,
                write=True,
                require_approved=False,
            )
        if not readiness.passed:
            joined = "; ".join(readiness.issue_messages)
            raise ValueError(f"Initiative package is not ready for approval: {joined}")

        initiative_state_path = self._context.initiative_path(
            location, ".wt/initiative.json"
        )
        initiative_document = self._context.load_json(initiative_state_path)
        updated_at = utc_timestamp_now()
        initiative_document.setdefault("approvals", []).append(
            {
                "approval_kind": "ready_for_execution",
                "actor_id": approver_actor_id,
                "approved_at": updated_at,
            }
        )
        initiative_document["updated_at"] = updated_at
        initiative_document["lifecycle_stage"] = "ready_for_execution"
        initiative_document["review_status"] = "approved"
        initiative_document["gate_state"] = {
            "capture_complete": True,
            "machine_valid": True,
            "approval_status": "approved",
            "ready_for_execution": True,
            "blocking_reasons": [],
        }
        if write:
            self._context.pack_loader().artifact_store.write_json_object(
                initiative_state_path,
                initiative_document,
            )
            self._discrepancies.append_initiative_event(
                location=location,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="ready_for_execution_approved",
                summary="An authorized maintainer approved the initiative package for execution.",
                actor_id=approver_actor_id,
                recorded_at=updated_at,
            )
            self._discrepancies.append_initiative_event(
                location=location,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="ready_for_execution_marked",
                summary="The initiative package entered ready_for_execution after approval.",
                actor_id="actor.watchtower_core",
                recorded_at=updated_at,
            )
            self._context.sync_derived_surfaces(location)

        return InitiativePackageResult(
            initiative_id=str(initiative_document["initiative_id"]),
            trace_id=str(initiative_document["trace_id"]),
            initiative_root=location.initiative_root_relative,
            lifecycle_stage="ready_for_execution",
            review_status="approved",
            ready_for_execution=True,
            validation_passed=True,
            wrote=write,
        )

    def reconcile_initiative_state_document(
        self,
        location: InitiativeLocation,
        initiative_document: dict[str, Any],
    ) -> dict[str, Any]:
        reconciled = json.loads(json.dumps(initiative_document))
        reconciled["task_ids"] = sorted(
            str(document["task_id"])
            for document in self._context.task_documents(location)
        )
        reconciled["deferred_item_ids"] = sorted(
            str(document["deferred_item_id"])
            for _, document in self._context.artifact_documents(
                location, ".wt/deferred", "*.json"
            )
        )
        reconciled["evidence_ids"] = sorted(
            str(document["id"])
            for _, document in self._context.artifact_documents(
                location, ".wt/evidence", "*.json"
            )
        )
        reconciled["promotion_ids"] = sorted(
            str(document["id"])
            for _, document in self._context.artifact_documents(
                location, ".wt/promotions", "*.json"
            )
        )
        reconciled["closeout_ids"] = sorted(
            str(document["id"])
            for _, document in self._context.artifact_documents(
                location, ".wt/closeout", "*.json"
            )
        )

        approvals = [
            approval
            for approval in reconciled.get("approvals", ())
            if isinstance(approval, dict)
        ]
        approval_keys = {
            (
                str(approval.get("approval_kind", "")),
                str(approval.get("actor_id", "")),
                str(approval.get("approved_at", "")),
            )
            for approval in approvals
        }
        for document in self._context.initiative_event_documents(location):
            event_type = str(document.get("event_type", ""))
            actor_id = str(document.get("actor_id", ""))
            approved_at = str(document.get("recorded_at", ""))
            if event_type == "ready_for_execution_approved":
                approval_kind = "ready_for_execution"
            elif (
                event_type == "authored_inputs_confirmed"
                and actor_id != "actor.watchtower_core"
            ):
                approval_kind = "authored_input_confirmation"
            else:
                continue
            key = (approval_kind, actor_id, approved_at)
            if key in approval_keys:
                continue
            approvals.append(
                {
                    "approval_kind": approval_kind,
                    "actor_id": actor_id,
                    "approved_at": approved_at,
                }
            )
            approval_keys.add(key)

        approvals.sort(
            key=lambda approval: (
                str(approval.get("approved_at", "")),
                str(approval.get("approval_kind", "")),
                str(approval.get("actor_id", "")),
            )
        )
        reconciled["approvals"] = approvals
        approval_status = (
            "approved"
            if any(
                str(approval.get("approval_kind", "")) == "ready_for_execution"
                for approval in approvals
            )
            else "pending"
        )
        gate_state = reconciled.get("gate_state")
        if not isinstance(gate_state, dict):
            gate_state = {}
        gate_state["approval_status"] = approval_status
        lifecycle_stage = str(reconciled.get("lifecycle_stage", "capture_incomplete"))
        gate_state["ready_for_execution"] = (
            approval_status == "approved"
            and lifecycle_stage not in {"capture_incomplete", "ready_for_review"}
        )
        reconciled["gate_state"] = gate_state
        reconciled["governing_document_paths"] = list(
            effective_initiative_governing_document_paths(
                reconciled,
                repo_root=self._context.pack_loader().repo_root,
            )
        )
        if approval_status == "approved":
            reconciled["review_status"] = "approved"
        return cast(dict[str, Any], reconciled)


__all__ = ["InitiativeReadinessCoordinator", "ValidationResult"]
