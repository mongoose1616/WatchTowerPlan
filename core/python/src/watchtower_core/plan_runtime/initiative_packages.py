"""Pack-wide initiative package bootstrap and readiness helpers for the plan workspace."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.closeout.initiative_package import (
    CloseoutArtifactDocument,
    InitiativePackageCloseoutHelper,
)
from watchtower_core.control_plane.actors import ActorRegistryHelper
from watchtower_core.control_plane.discrepancy import (
    DiscrepancyDescriptor,
    DiscrepancyHelper,
    DiscrepancyIssue,
)
from watchtower_core.control_plane.event_stream import (
    EventStreamDescriptor,
    EventStreamHelper,
    EventStreamWriteRequest,
)
from watchtower_core.control_plane.human_surface_policy import HumanSurfacePolicyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.path_ids import (
    PlanInitiativeLocation,
    PlanPathIdHelper,
)
from watchtower_core.control_plane.promotion_policy import PromotionPolicyHelper
from watchtower_core.evidence import EvidenceBundleEntrySpec, EvidenceBundleHelper
from watchtower_core.plan_runtime.guidance_promotion import (
    default_mirror_target_paths,
    default_target_family_for_source_kind,
    default_target_path,
    source_artifact_kind_for_path,
)
from watchtower_core.plan_runtime.plan_workspace import PlanWorkspaceService
from watchtower_core.plan_runtime.project_workspace import ProjectWorkspaceService
from watchtower_core.plan_runtime.sync.coordination import CoordinationSyncService
from watchtower_core.plan_runtime.task_lifecycle_support import slugify_file_stem
from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_core.validation import ArtifactValidationService, ValidationResult

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


@dataclass(frozen=True, slots=True)
class InitiativeTaskSpec:
    """Bootstrap-time specification for one initiative-local task."""

    title: str
    summary: str
    slug: str | None = None
    task_id: str | None = None
    task_kind: str = "feature"
    priority: str = "high"
    owner: str = "repository_maintainer"
    depends_on: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DeferredItemSpec:
    """Bootstrap-time specification for one initiative-local deferred item."""

    category: str
    summary: str
    reason: str
    resolution_trigger: str
    blocks_ready_for_execution: bool = False
    slug: str | None = None
    deferred_item_id: str | None = None
    owner: str = "repository_maintainer"
    related_task_id: str | None = None


@dataclass(frozen=True, slots=True)
class InitiativeBootstrapParams:
    """Inputs for one pack-wide initiative package bootstrap."""

    trace_id: str
    title: str
    summary: str
    task_specs: tuple[InitiativeTaskSpec, ...]
    initiative_slug: str | None = None
    initiative_id: str | None = None
    owner: str = "repository_maintainer"
    deferred_items: tuple[DeferredItemSpec, ...] = ()
    include_decision_notes: bool = False
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class InitiativeReadinessResult:
    """Structured validation result for one initiative package."""

    initiative_id: str
    trace_id: str
    initiative_root: str
    passed: bool
    lifecycle_stage: str
    issue_messages: tuple[str, ...]
    artifact_results: tuple[ValidationResult, ...]
    open_discrepancy_ids: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    wrote: bool


@dataclass(frozen=True, slots=True)
class InitiativePackageResult:
    """Output summary for one initiative package mutation."""

    initiative_id: str
    trace_id: str
    initiative_root: str
    lifecycle_stage: str
    review_status: str
    ready_for_execution: bool
    validation_passed: bool
    wrote: bool


@dataclass(frozen=True, slots=True)
class InitiativeTerminalCloseoutResult:
    """Output summary for one terminal live-initiative closeout mutation."""

    initiative_id: str
    trace_id: str
    initiative_root: str
    initiative_status: str
    closed_at: str
    closure_reason: str
    scope_type: str
    superseded_by_trace_id: str | None
    wrote: bool


_InitiativeLocation = PlanInitiativeLocation


class InitiativePackageService:
    """Manage pack-wide initiative packages under plan/initiatives/."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def bootstrap_packwide(
        self,
        params: InitiativeBootstrapParams,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Create one pack-wide initiative package and stage it for review."""

        return self._bootstrap_initiative(
            self._packwide_location(params),
            params,
            write=write,
        )

    def bootstrap_project_scoped(
        self,
        project_slug: str,
        params: InitiativeBootstrapParams,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Create one project-scoped initiative package beneath a bootstrapped project."""

        return self._bootstrap_initiative(
            self._project_scoped_location(project_slug, params),
            params,
            write=write,
        )

    def validate_packwide(
        self,
        initiative_slug: str,
        *,
        write: bool,
        require_approved: bool = False,
    ) -> InitiativeReadinessResult:
        """Validate one pack-wide initiative package and refresh its gate state."""

        return self._validate_initiative(
            self._packwide_location_for_slug(initiative_slug),
            write=write,
            require_approved=require_approved,
        )

    def validate_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        *,
        write: bool,
        require_approved: bool = False,
    ) -> InitiativeReadinessResult:
        """Validate one project-scoped initiative package and refresh its gate state."""

        return self._validate_initiative(
            self._project_scoped_location_for_slug(project_slug, initiative_slug),
            write=write,
            require_approved=require_approved,
        )

    def confirm_authored_inputs(
        self,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Confirm edited authored inputs into machine state."""

        return self._confirm_authored_inputs(
            self._packwide_location_for_slug(initiative_slug),
            approver_actor_id,
            write=write,
        )

    def confirm_project_scoped_inputs(
        self,
        project_slug: str,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Confirm edited authored inputs for one project-scoped initiative package."""

        return self._confirm_authored_inputs(
            self._project_scoped_location_for_slug(project_slug, initiative_slug),
            approver_actor_id,
            write=write,
        )

    def approve_packwide(
        self,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Approve one validated pack-wide initiative into ready_for_execution."""

        return self._approve_initiative(
            self._packwide_location_for_slug(initiative_slug),
            approver_actor_id,
            write=write,
        )

    def approve_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Approve one validated project-scoped initiative into ready_for_execution."""

        return self._approve_initiative(
            self._project_scoped_location_for_slug(project_slug, initiative_slug),
            approver_actor_id,
            write=write,
        )

    def close_packwide(
        self,
        initiative_slug: str,
        *,
        initiative_status: str,
        closure_reason: str,
        write: bool,
        closed_at: str | None = None,
        superseded_by_trace_id: str | None = None,
    ) -> InitiativeTerminalCloseoutResult:
        """Set terminal closeout state for one pack-wide live initiative package."""

        return self._close_initiative(
            self._packwide_location_for_slug(initiative_slug),
            initiative_status=initiative_status,
            closure_reason=closure_reason,
            write=write,
            closed_at=closed_at,
            superseded_by_trace_id=superseded_by_trace_id,
        )

    def close_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        *,
        initiative_status: str,
        closure_reason: str,
        write: bool,
        closed_at: str | None = None,
        superseded_by_trace_id: str | None = None,
    ) -> InitiativeTerminalCloseoutResult:
        """Set terminal closeout state for one project-scoped live initiative package."""

        return self._close_initiative(
            self._project_scoped_location_for_slug(project_slug, initiative_slug),
            initiative_status=initiative_status,
            closure_reason=closure_reason,
            write=write,
            closed_at=closed_at,
            superseded_by_trace_id=superseded_by_trace_id,
        )

    def _bootstrap_initiative(
        self,
        location: _InitiativeLocation,
        params: InitiativeBootstrapParams,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        task_specs = tuple(params.task_specs)
        if not task_specs:
            raise ValueError("Bootstrap requires at least one initiative task.")

        initiative_slug = location.initiative_slug
        trace_id_suffix = PlanPathIdHelper.trace_suffix(params.trace_id)
        if initiative_slug != trace_id_suffix:
            raise ValueError(
                "initiative_slug must match the trace stem derived from trace_id."
            )
        initiative_id = (
            params.initiative_id
            or PlanPathIdHelper.canonical_initiative_id(initiative_slug)
        )
        if initiative_id != PlanPathIdHelper.canonical_initiative_id(initiative_slug):
            raise ValueError("initiative_id must use the canonical initiative.<slug> form.")

        initiative_root = self._initiative_root(location)
        if initiative_root.exists():
            raise ValueError(
                f"Initiative root already exists: {initiative_root.relative_to(self._loader.repo_root)}"
            )
        if self._initiative_identity_exists(initiative_id, params.trace_id):
            raise ValueError(
                "initiative_id and trace_id must remain globally unique across pack-wide and project-scoped initiatives."
            )
        if location.scope_type == "project_scoped":
            project_validation = ProjectWorkspaceService(self._fresh_loader()).validate(
                location.project_slug or "",
                write=False,
            )
            if not project_validation.passed:
                raise ValueError(
                    "Project-scoped initiative bootstrap requires a valid project container: "
                    + "; ".join(project_validation.issue_messages)
                )

        updated_at = params.updated_at or utc_timestamp_now()
        authored_documents = self._build_authored_documents(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            title=params.title,
            summary=params.summary,
            include_decision_notes=params.include_decision_notes,
            task_specs=task_specs,
        )
        authored_input_records = self._authored_input_records(
            authored_documents=authored_documents,
            updated_at=updated_at,
        )
        task_documents = self._build_task_documents(
            location=location,
            initiative_id=initiative_id,
            task_specs=task_specs,
            updated_at=updated_at,
        )
        deferred_documents = self._build_deferred_documents(
            location=location,
            initiative_id=initiative_id,
            deferred_items=params.deferred_items,
            updated_at=updated_at,
        )
        evidence_document = self._build_validation_bundle(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            updated_at=updated_at,
        )
        closeout_document = self._build_closeout_recap(
            location=location,
            initiative_id=initiative_id,
            evidence_id=str(evidence_document["id"]),
            updated_at=updated_at,
        )
        promotion_document = self._build_promotion_shell(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            authored_document_paths=tuple(authored_documents),
            evidence_id=str(evidence_document["id"]),
            updated_at=updated_at,
        )
        initiative_document = self._build_initiative_state(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            title=params.title,
            summary=params.summary,
            owner=params.owner,
            task_documents=task_documents,
            deferred_documents=deferred_documents,
            authored_input_records=authored_input_records,
            evidence_id=str(evidence_document["id"]),
            closeout_id=str(closeout_document["id"]),
            promotion_id=str(promotion_document["id"]),
            updated_at=updated_at,
        )
        initiative_events = self._bootstrap_initiative_events(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            task_documents=task_documents,
            updated_at=updated_at,
            related_paths=tuple(authored_documents),
        )

        if not write:
            return InitiativePackageResult(
                initiative_id=initiative_id,
                trace_id=params.trace_id,
                initiative_root=location.initiative_root_relative,
                lifecycle_stage=str(initiative_document["lifecycle_stage"]),
                review_status=str(initiative_document["review_status"]),
                ready_for_execution=False,
                validation_passed=False,
                wrote=False,
            )

        for relative_path, content in authored_documents.items():
            target = self._loader.repo_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        for relative_path, document in task_documents.items():
            self._loader.artifact_store.write_json_object(relative_path, document)
        for relative_path, document in deferred_documents.items():
            self._loader.artifact_store.write_json_object(relative_path, document)
        self._loader.artifact_store.write_json_object(
            self._initiative_path_for_location(
                location,
                ".wt/evidence/validation_bundle.bootstrap.json",
            ),
            evidence_document,
        )
        self._loader.artifact_store.write_json_object(
            self._initiative_path_for_location(
                location,
                ".wt/closeout/closeout_recap.bootstrap.json",
            ),
            closeout_document,
        )
        self._loader.artifact_store.write_json_object(
            self._initiative_path_for_location(
                location,
                ".wt/promotions/guidance_promotion_record.bootstrap.json",
            ),
            promotion_document,
        )
        self._loader.artifact_store.write_json_object(
            self._initiative_path_for_location(location, ".wt/initiative.json"),
            initiative_document,
        )
        for relative_path, document in initiative_events.items():
            self._loader.artifact_store.write_json_object(relative_path, document)
        self._sync_derived_surfaces(location)

        readiness = self._validate_initiative(
            location,
            write=True,
            require_approved=False,
        )
        state = self._load_json(self._initiative_path_for_location(location, ".wt/initiative.json"))
        return InitiativePackageResult(
            initiative_id=str(state["initiative_id"]),
            trace_id=str(state["trace_id"]),
            initiative_root=location.initiative_root_relative,
            lifecycle_stage=str(state["lifecycle_stage"]),
            review_status=str(state["review_status"]),
            ready_for_execution=bool(state["gate_state"]["ready_for_execution"]),
            validation_passed=readiness.passed,
            wrote=True,
        )

    def _validate_initiative(
        self,
        location: _InitiativeLocation,
        *,
        write: bool,
        require_approved: bool,
    ) -> InitiativeReadinessResult:
        initiative_state_path = self._initiative_path_for_location(location, ".wt/initiative.json")
        initiative_document = self._load_json(initiative_state_path)
        initiative_id = str(initiative_document["initiative_id"])
        trace_id = str(initiative_document["trace_id"])
        previous_lifecycle_stage = str(initiative_document["lifecycle_stage"])

        validator = ArtifactValidationService(self._pack_loader())
        artifact_paths = self._artifact_paths_for_location(location)
        artifact_results = tuple(validator.validate(relative_path) for relative_path in artifact_paths)

        issues: list[str] = []
        blocking_reasons: list[str] = []
        if not artifact_results:
            issues.append("No plan initiative artifacts were found under the initiative root.")
            blocking_reasons.append("missing_artifacts")
        for result in artifact_results:
            if not result.passed:
                issues.append(
                    f"{result.target_path} failed {result.validator_id} with {result.issue_count} issue(s)."
                )

        if location.scope_type == "project_scoped":
            project_validation = ProjectWorkspaceService(self._fresh_loader()).validate(
                location.project_slug or "",
                write=False,
            )
            if not project_validation.passed:
                issues.extend(project_validation.issue_messages)
                blocking_reasons.append("project_bootstrap_invalid")

        authored_input_issues = self._authored_input_drift_issues(
            location=location,
            initiative_document=initiative_document,
        )
        issues.extend(issue.summary for issue in authored_input_issues)
        if authored_input_issues:
            blocking_reasons.append("authored_input_drift")

        derived_surface_issues = self._stale_derived_surface_issues(location)
        if location.scope_type == "project_scoped":
            derived_surface_issues = (
                *derived_surface_issues,
                *self._project_surface_issues(location),
            )
        issues.extend(issue.summary for issue in derived_surface_issues)
        if derived_surface_issues:
            blocking_reasons.append("stale_derived_surfaces")

        machine_root_issues = self._machine_root_policy_issues(location)
        issues.extend(machine_root_issues)
        if machine_root_issues:
            blocking_reasons.append("machine_root_policy")

        deferred_issues = self._blocking_deferred_item_issues(location)
        issues.extend(deferred_issues)
        if deferred_issues:
            blocking_reasons.append("blocking_deferred_items")

        if write:
            self._sync_managed_discrepancies(
                location=location,
                initiative_id=initiative_id,
                discrepancy_issues=(*authored_input_issues, *derived_surface_issues),
                updated_at=utc_timestamp_now(),
            )
        open_discrepancies = self._open_discrepancy_documents(location)
        if open_discrepancies:
            issues.extend(
                f"Open discrepancy {document['discrepancy_id']} blocks readiness."
                for _, document in open_discrepancies
                if document["gate_effect"] != "none"
            )
            if any(document["gate_effect"] != "none" for _, document in open_discrepancies):
                blocking_reasons.append("open_discrepancies")

        if require_approved and initiative_document["gate_state"]["approval_status"] != "approved":
            issues.append("The initiative package is not approved for execution.")
            blocking_reasons.append("approval_pending")

        passed = not issues and all(result.passed for result in artifact_results)
        current_lifecycle_stage = str(initiative_document["lifecycle_stage"])
        approval_status = str(initiative_document["gate_state"]["approval_status"])
        lifecycle_stage = current_lifecycle_stage
        execution_started = self._has_execution_started(location)
        if passed:
            if current_lifecycle_stage in {"closing", "completed", "superseded", "cancelled"}:
                lifecycle_stage = current_lifecycle_stage
            elif approval_status == "approved" and execution_started:
                lifecycle_stage = "in_progress"
            elif approval_status == "approved":
                lifecycle_stage = "ready_for_execution"
            else:
                lifecycle_stage = "ready_for_review"
        elif issues:
            if current_lifecycle_stage in {"closing", "completed", "superseded", "cancelled"}:
                lifecycle_stage = current_lifecycle_stage
            else:
                lifecycle_stage = (
                    "blocked"
                    if current_lifecycle_stage in {"ready_for_execution", "in_progress", "blocked"}
                    or (approval_status == "approved" and execution_started)
                    else "capture_incomplete"
                )

        discrepancy_ids = tuple(document["discrepancy_id"] for _, document in open_discrepancies)
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
                    in {"missing_artifacts", "blocking_deferred_items", "project_bootstrap_invalid"}
                    for reason in blocking_reasons
                ),
                "machine_valid": not issues,
                "approval_status": approval_status,
                "ready_for_execution": (
                    approval_status == "approved" and passed
                ),
                "blocking_reasons": sorted(set(blocking_reasons)),
            }
            self._loader.artifact_store.write_json_object(initiative_state_path, initiative_document)

            if (
                passed
                and lifecycle_stage == "ready_for_review"
                and previous_lifecycle_stage != "ready_for_review"
            ):
                self._append_initiative_event(
                    location=location,
                    initiative_id=initiative_id,
                    trace_id=trace_id,
                    event_type="ready_for_review_marked",
                    summary="The initiative package passed capture validation and is ready for review.",
                    actor_id="actor.watchtower_core",
                    recorded_at=str(initiative_document["updated_at"]),
                )
            self._sync_derived_surfaces(location)

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

    def _confirm_authored_inputs(
        self,
        location: _InitiativeLocation,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        self._assert_default_authorized_maintainer(approver_actor_id)
        initiative_state_path = self._initiative_path_for_location(location, ".wt/initiative.json")
        initiative_document = self._load_json(initiative_state_path)
        updated_at = utc_timestamp_now()

        for record in initiative_document["authored_inputs"]:
            path = str(record["path"])
            record["sha256"] = self._sha256_for_relative_path(path)
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
        initiative_document["updated_at"] = updated_at
        if write:
            self._loader.artifact_store.write_json_object(initiative_state_path, initiative_document)
            self._append_initiative_event(
                location=location,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="authored_inputs_confirmed",
                summary="An authorized maintainer confirmed the authored intake documents into machine state.",
                actor_id=approver_actor_id,
                recorded_at=updated_at,
            )
            self._sync_derived_surfaces(location)
            readiness = self._validate_initiative(
                location,
                write=True,
                require_approved=False,
            )
        else:
            readiness = self._validate_initiative(
                location,
                write=False,
                require_approved=False,
            )
        refreshed_state = self._load_json(initiative_state_path)
        return InitiativePackageResult(
            initiative_id=str(refreshed_state["initiative_id"]),
            trace_id=str(refreshed_state["trace_id"]),
            initiative_root=location.initiative_root_relative,
            lifecycle_stage=str(refreshed_state["lifecycle_stage"]),
            review_status=str(refreshed_state["review_status"]),
            ready_for_execution=bool(refreshed_state["gate_state"]["ready_for_execution"]),
            validation_passed=readiness.passed,
            wrote=write,
        )

    def _approve_initiative(
        self,
        location: _InitiativeLocation,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        self._assert_default_authorized_maintainer(approver_actor_id)
        readiness = self._validate_initiative(
            location,
            write=write,
            require_approved=False,
        )
        if not readiness.passed:
            joined = "; ".join(readiness.issue_messages)
            raise ValueError(f"Initiative package is not ready for approval: {joined}")

        initiative_state_path = self._initiative_path_for_location(location, ".wt/initiative.json")
        initiative_document = self._load_json(initiative_state_path)
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
            self._loader.artifact_store.write_json_object(initiative_state_path, initiative_document)
            self._append_initiative_event(
                location=location,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="ready_for_execution_approved",
                summary="An authorized maintainer approved the initiative package for execution.",
                actor_id=approver_actor_id,
                recorded_at=updated_at,
            )
            self._append_initiative_event(
                location=location,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="ready_for_execution_marked",
                summary="The initiative package entered ready_for_execution after approval.",
                actor_id="actor.watchtower_core",
                recorded_at=updated_at,
            )
            self._sync_derived_surfaces(location)

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

    def _close_initiative(
        self,
        location: _InitiativeLocation,
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
        initiative_state_path = self._initiative_path_for_location(location, ".wt/initiative.json")
        initiative_document = self._load_json(initiative_state_path)
        if superseded_by_trace_id == str(initiative_document["trace_id"]):
            raise ValueError("An initiative cannot supersede itself.")
        if superseded_by_trace_id is not None and not self._trace_id_exists(
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

        readiness = self._validate_initiative(
            location,
            write=False,
            require_approved=False,
        )
        if not readiness.passed:
            joined = "; ".join(readiness.issue_messages)
            raise ValueError(
                "Initiative package is not clean enough for terminal closeout: " + joined
            )

        open_task_ids = tuple(
            str(task_document["task_id"])
            for task_document in self._task_documents(location)
            if str(task_document["task_status"]) not in {"completed", "cancelled"}
        )
        closed_at_value = closed_at or utc_timestamp_now()

        evidence_documents = self._artifact_documents(location, ".wt/evidence", "*.json")
        closeout_documents = self._artifact_documents(location, ".wt/closeout", "*.json")
        promotion_documents = self._artifact_documents(location, ".wt/promotions", "*.json")
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
                self._append_initiative_event(
                    location=location,
                    initiative_id=str(closeout_plan.initiative_document["initiative_id"]),
                    trace_id=str(closeout_plan.initiative_document["trace_id"]),
                    event_type="closing_started",
                    summary="The initiative package entered closing before terminal closeout.",
                    actor_id="actor.watchtower_core",
                    recorded_at=closed_at_value,
                )

            self._loader.artifact_store.write_json_object(
                initiative_state_path,
                closeout_plan.initiative_document,
            )
            for artifact in closeout_plan.evidence_documents:
                self._loader.artifact_store.write_json_object(
                    artifact.relative_path,
                    artifact.document,
                )
            for artifact in closeout_plan.closeout_documents:
                self._loader.artifact_store.write_json_object(
                    artifact.relative_path,
                    artifact.document,
                )
            for artifact in closeout_plan.promotion_documents:
                self._loader.artifact_store.write_json_object(
                    artifact.relative_path,
                    artifact.document,
                )
            self._append_initiative_event(
                location=location,
                initiative_id=str(closeout_plan.initiative_document["initiative_id"]),
                trace_id=str(closeout_plan.initiative_document["trace_id"]),
                event_type=initiative_status,
                summary=f"The initiative package reached terminal closeout as {initiative_status}.",
                actor_id="actor.repository_maintainer",
                recorded_at=closed_at_value,
            )
            self._sync_derived_surfaces(location)

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

    def _build_authored_documents(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        title: str,
        summary: str,
        include_decision_notes: bool,
        task_specs: tuple[InitiativeTaskSpec, ...],
    ) -> dict[str, str]:
        initiative_slug = location.initiative_slug
        task_lines = "\n".join(
            (
                f"- `{task.task_id or PlanPathIdHelper.canonical_task_id(initiative_slug, task.slug or slugify_file_stem(task.title))}`: {task.summary}"
            )
            for task in task_specs
        )
        documents = {
            self._initiative_path_for_location(location, "initiative_brief.md"): "\n".join(
                (
                    f"# {title}",
                    "",
                    "## Summary",
                    summary,
                    "",
                    "## Identity",
                    f"- `initiative_id`: `{initiative_id}`",
                    f"- `trace_id`: `{trace_id}`",
                    f"- `scope_type`: `{location.scope_type}`",
                    *(
                        (f"- `project_id`: `{location.project_id}`",)
                        if location.project_id is not None
                        else ()
                    ),
                    "",
                    "## Initial Task Set",
                    task_lines,
                    "",
                )
            ),
            self._initiative_path_for_location(location, "design_record.md"): "\n".join(
                (
                    f"# {title} Design Record",
                    "",
                    "## Summary",
                    summary,
                    "",
                    "## Initial Design Boundary",
                    f"- The initiative package is machine-first and local to `{location.initiative_root_relative}/.wt/`.",
                    "- Authored intake docs remain editable inputs but require explicit machine confirmation.",
                    "- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.",
                    *(
                        (
                            "- The project container must stay valid and current before a project-scoped initiative may execute.",
                        )
                        if location.scope_type == "project_scoped"
                        else ()
                    ),
                    "",
                )
            ),
            self._initiative_path_for_location(location, "implementation_slice.md"): "\n".join(
                (
                    f"# {title} Implementation Slice",
                    "",
                    "## Summary",
                    summary,
                    "",
                    "## Initial Work Breakdown",
                    task_lines,
                    "",
                    "## Gate",
                    "- No execution starts until the initiative package is approved and marked `ready_for_execution`.",
                    "",
                )
            ),
        }
        if include_decision_notes:
            documents[self._initiative_path_for_location(location, "decision_notes.md")] = "\n".join(
                (
                    f"# {title} Decision Notes",
                    "",
                    "## Summary",
                    "Optional decision notes seeded during initiative bootstrap.",
                    "",
                )
            )
        return documents

    def _authored_input_records(
        self,
        *,
        authored_documents: dict[str, str],
        updated_at: str,
    ) -> list[dict[str, object]]:
        records: list[dict[str, object]] = []
        for relative_path, content in authored_documents.items():
            doc_kind = Path(relative_path).stem
            records.append(
                {
                    "doc_kind": doc_kind,
                    "path": relative_path,
                    "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                    "proposal_status": "confirmed",
                    "last_confirmed_at": updated_at,
                    "last_confirmed_by": "actor.repository_maintainer",
                }
            )
        return records

    def _build_task_documents(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        task_specs: tuple[InitiativeTaskSpec, ...],
        updated_at: str,
    ) -> dict[str, dict[str, object]]:
        initiative_slug = location.initiative_slug
        event_helper = self._event_stream_helper()
        documents: dict[str, dict[str, object]] = {}
        for spec in task_specs:
            task_slug = spec.slug or slugify_file_stem(spec.title)
            task_id = spec.task_id or PlanPathIdHelper.canonical_task_id(
                initiative_slug,
                task_slug,
            )
            task_path = self._initiative_path_for_location(
                location,
                f".wt/tasks/{task_slug}/task.json",
            )
            documents[task_path] = {
                "$schema": "urn:watchtower:schema:artifacts:plan:task-state:v1",
                "task_id": task_id,
                "slug": task_slug,
                "initiative_id": initiative_id,
                "title": spec.title,
                "summary": spec.summary,
                "status": "active",
                "task_status": "planned",
                "task_kind": spec.task_kind,
                "priority": spec.priority,
                "owner": spec.owner,
                "created_at": updated_at,
                "updated_at": updated_at,
                "dependency_task_ids": list(spec.depends_on),
                "blocker_task_ids": list(spec.blocked_by),
                "related_ids": list(spec.related_ids),
            }
            task_event_descriptor = EventStreamDescriptor.task(
                relative_dir=self._initiative_path_for_location(
                    location,
                    f".wt/tasks/{task_slug}/events",
                ),
                event_id_prefix=f"event.{initiative_slug}.{task_slug}",
                initiative_id=initiative_id,
                task_id=task_id,
            )
            documents.update(
                event_helper.build_seed_documents(
                    task_event_descriptor,
                    (
                        EventStreamWriteRequest(
                            event_type="created",
                            actor_id="actor.watchtower_core",
                            recorded_at=updated_at,
                            summary=f"Created task {task_id} during initiative bootstrap.",
                            payload={
                                "status": "active",
                                "task_status": "planned",
                                "owner": spec.owner,
                            },
                        ),
                    ),
                )
            )
        return documents

    def _build_deferred_documents(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        deferred_items: tuple[DeferredItemSpec, ...],
        updated_at: str,
    ) -> dict[str, dict[str, object]]:
        initiative_slug = location.initiative_slug
        documents: dict[str, dict[str, object]] = {}
        for spec in deferred_items:
            deferred_slug = spec.slug or slugify_file_stem(spec.summary)
            deferred_id = spec.deferred_item_id or PlanPathIdHelper.canonical_deferred_item_id(
                initiative_slug,
                deferred_slug,
            )
            documents[
                self._initiative_path_for_location(
                    location,
                    f".wt/deferred/{deferred_slug}.json",
                )
            ] = {
                "$schema": "urn:watchtower:schema:artifacts:plan:deferred-item-record:v1",
                "deferred_item_id": deferred_id,
                "initiative_id": initiative_id,
                "category": spec.category,
                "summary": spec.summary,
                "reason": spec.reason,
                "owner": spec.owner,
                "resolution_trigger": spec.resolution_trigger,
                "status": "open",
                "blocks_ready_for_execution": spec.blocks_ready_for_execution,
                "related_task_id": spec.related_task_id,
                "created_at": updated_at,
                "updated_at": updated_at,
            }
        return documents

    def _build_validation_bundle(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        updated_at: str,
    ) -> dict[str, object]:
        initiative_slug = location.initiative_slug
        return EvidenceBundleHelper(self._pack_loader()).build_document(
            evidence_id=PlanPathIdHelper.canonical_evidence_id(
                initiative_slug,
                "bootstrap_validation_bundle",
            ),
            initiative_id=initiative_id,
            trace_id=trace_id,
            title="Bootstrap Validation Bundle",
            status="planned",
            updated_at=updated_at,
            entries=(
                EvidenceBundleEntrySpec(
                    entry_id=PlanPathIdHelper.canonical_entry_id(
                        initiative_slug,
                        "schema_validation",
                    ),
                    acceptance_label="package_contracts_valid",
                    validation_type="schema_validation",
                    owner="repository_maintainer",
                    target_phase="readiness",
                    expected_output_paths=(
                        self._initiative_path_for_location(location, ".wt/initiative.json"),
                    ),
                ),
                EvidenceBundleEntrySpec(
                    entry_id=PlanPathIdHelper.canonical_entry_id(
                        initiative_slug,
                        "gate_validation",
                    ),
                    acceptance_label="ready_for_execution_gate",
                    validation_type="readiness_gate",
                    owner="repository_maintainer",
                    target_phase="readiness",
                    expected_output_paths=(
                        self._initiative_path_for_location(location, ".wt/discrepancies"),
                    ),
                ),
            ),
        )

    def _build_closeout_recap(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        evidence_id: str,
        updated_at: str,
    ) -> dict[str, object]:
        initiative_slug = location.initiative_slug
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:closeout-recap:v1",
            "id": PlanPathIdHelper.canonical_closeout_id(
                initiative_slug,
                "bootstrap_recap",
            ),
            "initiative_id": initiative_id,
            "title": "Bootstrap Closeout Shell",
            "status": "planned",
            "updated_at": updated_at,
            "expected_outcome": "Close out the initiative with validated capture, readiness, and follow-up accounting.",
            "acceptance_ids": [
                PlanPathIdHelper.canonical_acceptance_id(initiative_slug, "bootstrap")
            ],
            "evidence_ids": [evidence_id],
            "follow_up_handling": "Record unresolved work as deferred items or bounded follow-up initiatives before closeout.",
            "promotion_review_required": True,
            "terminal_state_options": ["completed", "superseded", "cancelled"],
        }

    def _build_promotion_shell(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        authored_document_paths: tuple[str, ...],
        evidence_id: str,
        updated_at: str,
    ) -> dict[str, object]:
        initiative_slug = location.initiative_slug
        policy_helper = PromotionPolicyHelper.from_loader(
            self._pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        candidates: list[dict[str, object]] = []
        review_refs: set[str] = set()
        for path in authored_document_paths:
            source_artifact_kind = source_artifact_kind_for_path(path)
            target_family = default_target_family_for_source_kind(source_artifact_kind)
            policy = policy_helper.resolve(
                source_artifact_kind=source_artifact_kind,
                target_family=target_family,
            )
            review_refs.add(policy.required_review_path)
            target_path = default_target_path(
                initiative_slug=initiative_slug,
                source_path=path,
                target_root=policy.target_root,
            )
            mirror_target_paths = (
                default_mirror_target_paths(
                    target_path=target_path,
                    target_root=policy.target_root,
                    mirror_roots=policy.mirror_roots,
                )
                if policy.mirror_update_mode != "none"
                else ()
            )
            candidates.append(
                {
                    "candidate_path": path,
                    "source_artifact_kind": source_artifact_kind,
                    "target_family": target_family,
                    "target_path": target_path,
                    "review_path": policy.required_review_path,
                    "provenance_expectation": (
                        "Promotions must cite the source initiative id, trace id, and "
                        "evidence bundle id."
                    ),
                    "mirror_update_mode": policy.mirror_update_mode,
                    "mirror_target_paths": list(mirror_target_paths),
                }
            )
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:guidance-promotion-record:v1",
            "id": PlanPathIdHelper.canonical_promotion_id(
                initiative_slug,
                "bootstrap_shell",
            ),
            "initiative_id": initiative_id,
            "trace_id": trace_id,
            "title": "Bootstrap Promotion Shell",
            "status": "planned",
            "approval_state": "pending",
            "review_refs": sorted(review_refs),
            "evidence_refs": [evidence_id],
            "updated_at": updated_at,
            "candidates": candidates,
        }

    def _build_initiative_state(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        title: str,
        summary: str,
        owner: str,
        task_documents: dict[str, dict[str, object]],
        deferred_documents: dict[str, dict[str, object]],
        authored_input_records: list[dict[str, object]],
        evidence_id: str,
        closeout_id: str,
        promotion_id: str,
        updated_at: str,
    ) -> dict[str, object]:
        initiative_slug = location.initiative_slug
        task_ids = [
            document["task_id"]
            for relative_path, document in task_documents.items()
            if relative_path.endswith("/task.json")
        ]
        deferred_ids = [document["deferred_item_id"] for document in deferred_documents.values()]
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:initiative-state:v1",
            "initiative_id": initiative_id,
            "trace_id": trace_id,
            "slug": initiative_slug,
            "title": title,
            "summary": summary,
            "scope_type": location.scope_type,
            **({"project_id": location.project_id} if location.project_id is not None else {}),
            "status": "active",
            "lifecycle_stage": "capture_incomplete",
            "review_status": "pending",
            "owner": owner,
            "created_at": updated_at,
            "updated_at": updated_at,
            "task_ids": task_ids,
            "deferred_item_ids": deferred_ids,
            "discrepancy_ids": [],
            "evidence_ids": [evidence_id],
            "promotion_ids": [promotion_id],
            "closeout_ids": [closeout_id],
            "authored_inputs": authored_input_records,
            "gate_state": {
                "capture_complete": False,
                "machine_valid": False,
                "approval_status": "pending",
                "ready_for_execution": False,
                "blocking_reasons": ["validation_pending"],
            },
            "approvals": [],
        }

    def _bootstrap_initiative_events(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        task_documents: dict[str, dict[str, object]],
        updated_at: str,
        related_paths: tuple[str, ...],
    ) -> dict[str, dict[str, object]]:
        initiative_slug = location.initiative_slug
        event_helper = self._event_stream_helper()
        descriptor = EventStreamDescriptor.initiative(
            relative_dir=self._initiative_path_for_location(location, ".wt/events"),
            event_id_prefix=f"event.{initiative_slug}",
            initiative_id=initiative_id,
            trace_id=trace_id,
        )
        event_types = [
            ("created", "Created the initiative package root."),
            (
                "scope_defined",
                (
                    "Recorded the initial project-scoped initiative scope."
                    if location.scope_type == "project_scoped"
                    else "Recorded the initial pack-wide initiative scope."
                ),
            ),
            ("authored_inputs_confirmed", "Confirmed the authored intake documents into machine state."),
            ("task_state_seeded", "Seeded the initial initiative-local task set."),
            ("evidence_shell_seeded", "Seeded the evidence shell."),
            ("closeout_shell_seeded", "Seeded the closeout shell."),
            ("promotion_shell_seeded", "Seeded the promotion shell."),
        ]
        return event_helper.build_seed_documents(
            descriptor,
            tuple(
                EventStreamWriteRequest(
                    event_type=event_type,
                    actor_id="actor.watchtower_core",
                    recorded_at=updated_at,
                    summary=summary,
                    related_paths=related_paths,
                    payload={
                        "task_count": sum(
                            1 for path in task_documents if path.endswith("/task.json")
                        )
                    },
                )
                for event_type, summary in event_types
            ),
        )

    def _pack_loader(self) -> ControlPlaneLoader:
        return self._fresh_loader(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)

    def _fresh_loader(
        self,
        *,
        active_pack_settings_path: str | None = None,
    ) -> ControlPlaneLoader:
        return ControlPlaneLoader(
            workspace_config=self._loader.workspace_config,
            schema_store=self._loader.schema_store,
            artifact_source=self._loader.artifact_source,
            artifact_store=self._loader.artifact_store,
            active_pack_settings_path=active_pack_settings_path,
        )

    def _artifact_paths_for_location(self, location: _InitiativeLocation) -> tuple[str, ...]:
        initiative_root = self._initiative_root(location)
        relative_paths: list[str] = []
        for path in sorted(initiative_root.rglob("*.json")):
            relative_paths.append(str(path.relative_to(self._loader.repo_root)))
        return tuple(relative_paths)

    def _authored_input_drift_issues(
        self,
        *,
        location: _InitiativeLocation,
        initiative_document: dict[str, object],
    ) -> tuple[DiscrepancyIssue, ...]:
        issues: list[DiscrepancyIssue] = []
        for record in initiative_document["authored_inputs"]:
            relative_path = str(record["path"])
            current_digest = self._sha256_for_relative_path(relative_path)
            if current_digest != record["sha256"]:
                issues.append(
                    DiscrepancyIssue(
                        record_slug=f"{record['doc_kind']}_drift",
                        category="authored_input_drift",
                        source_paths=(relative_path,),
                        summary=(
                            f"Authored input drift detected for {relative_path}; "
                            "machine confirmation is required."
                        ),
                        discrepancy_id=(
                            f"discrepancy.{location.discrepancy_namespace}.{record['doc_kind']}_drift"
                        ),
                    )
                )
        return tuple(issues)

    def _stale_derived_surface_issues(
        self,
        location: _InitiativeLocation,
    ) -> tuple[DiscrepancyIssue, ...]:
        return PlanWorkspaceService(self._fresh_loader()).expected_surface_issues(
            location.initiative_root_relative
        )

    def _project_surface_issues(
        self,
        location: _InitiativeLocation,
    ) -> tuple[DiscrepancyIssue, ...]:
        if location.project_slug is None:
            return ()
        fresh_loader = self._fresh_loader()
        return tuple(
            DiscrepancyIssue(
                record_slug=f"{Path(issue.relative_path).stem}_project_drift",
                category=issue.category,
                source_paths=(issue.relative_path,),
                summary=issue.message,
                discrepancy_id=(
                    f"discrepancy.{location.discrepancy_namespace}.{Path(issue.relative_path).stem}_project_drift"
                ),
            )
            for issue in ProjectWorkspaceService(fresh_loader).expected_surface_issues(
                location.project_slug
            )
        )

    def _machine_root_policy_issues(self, location: _InitiativeLocation) -> tuple[str, ...]:
        helper = HumanSurfacePolicyHelper.from_loader(
            self._pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        machine_root = self._initiative_path_for_location(location, ".wt")
        return tuple(
            issue.message for issue in helper.validate_root(self._loader.repo_root, machine_root)
        )

    def _blocking_deferred_item_issues(self, location: _InitiativeLocation) -> tuple[str, ...]:
        deferred_dir = self._loader.repo_root / self._initiative_path_for_location(
            location,
            ".wt/deferred",
        )
        if not deferred_dir.exists():
            return ()
        issues: list[str] = []
        for path in sorted(deferred_dir.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            if document["status"] == "open" and document["blocks_ready_for_execution"]:
                issues.append(
                    f"Blocking deferred item {document['deferred_item_id']} remains open."
                )
        return tuple(issues)

    def _open_discrepancy_documents(
        self,
        location: _InitiativeLocation,
    ) -> tuple[tuple[str, dict[str, object]], ...]:
        return self._discrepancy_helper().open_records(
            DiscrepancyDescriptor(
                relative_dir=self._initiative_path_for_location(location, ".wt/discrepancies"),
                initiative_id=str(
                    self._load_json(
                        self._initiative_path_for_location(location, ".wt/initiative.json")
                    )["initiative_id"]
                ),
            )
        )

    def _sync_managed_discrepancies(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        discrepancy_issues: tuple[DiscrepancyIssue, ...],
        updated_at: str,
    ) -> None:
        self._discrepancy_helper().sync_records(
            DiscrepancyDescriptor(
                relative_dir=self._initiative_path_for_location(location, ".wt/discrepancies"),
                initiative_id=initiative_id,
            ),
            issues=discrepancy_issues,
            updated_at=updated_at,
            managed_categories=(
                "authored_input_drift",
                "stale_rendered_surface",
                "stale_aggregate_index",
            ),
        )

    def _append_initiative_event(
        self,
        *,
        location: _InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        event_type: str,
        summary: str,
        actor_id: str,
        recorded_at: str,
    ) -> None:
        initiative_slug = location.initiative_slug
        descriptor = EventStreamDescriptor.initiative(
            relative_dir=self._initiative_path_for_location(location, ".wt/events"),
            event_id_prefix=f"event.{initiative_slug}",
            initiative_id=initiative_id,
            trace_id=trace_id,
        )
        self._event_stream_helper().append_event(
            descriptor,
            EventStreamWriteRequest(
                event_type=event_type,
                actor_id=actor_id,
                recorded_at=recorded_at,
                summary=summary,
                payload={},
            ),
        )

    def _event_stream_helper(self) -> EventStreamHelper:
        return EventStreamHelper.from_loader(
            self._pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def _discrepancy_helper(self) -> DiscrepancyHelper:
        return DiscrepancyHelper.from_loader(
            self._pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def _assert_default_authorized_maintainer(self, actor_id: str) -> None:
        helper = ActorRegistryHelper.from_loader(
            self._pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        try:
            helper.require_actor(
                actor_id,
                allowed_types=("user",),
                allowed_roles=("owner",),
                allowed_scopes=("repository",),
            )
        except ValueError as exc:
            raise ValueError(
                "Only default human repository maintainers may approve this initiative package."
            ) from exc

    def _load_json(self, relative_path: str) -> dict[str, object]:
        path = self._loader.repo_root / relative_path
        return json.loads(path.read_text(encoding="utf-8"))

    def _task_documents(self, location: _InitiativeLocation) -> tuple[dict[str, object], ...]:
        return tuple(
            document
            for _, document in self._artifact_documents(
                location,
                ".wt/tasks",
                "task.json",
                task_pattern=True,
            )
        )

    def _artifact_documents(
        self,
        location: _InitiativeLocation,
        suffix: str,
        pattern: str,
        *,
        task_pattern: bool = False,
    ) -> tuple[tuple[str, dict[str, object]], ...]:
        root = self._loader.repo_root / self._initiative_path_for_location(location, suffix)
        if not root.exists():
            return ()
        if task_pattern:
            paths = sorted(root.glob("*/task.json"))
        else:
            paths = sorted(root.glob(pattern))
        return tuple(
            (
                str(path.relative_to(self._loader.repo_root)),
                json.loads(path.read_text(encoding="utf-8")),
            )
            for path in paths
        )

    def _sha256_for_relative_path(self, relative_path: str) -> str:
        path = self._loader.repo_root / relative_path
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _packwide_location(self, params: InitiativeBootstrapParams) -> _InitiativeLocation:
        return PlanPathIdHelper.packwide_initiative_location(
            trace_id=params.trace_id,
            initiative_slug=params.initiative_slug,
        )

    def _packwide_location_for_slug(self, initiative_slug: str) -> _InitiativeLocation:
        return PlanPathIdHelper.packwide_initiative_location(
            initiative_slug=initiative_slug,
        )

    def _project_scoped_location(
        self,
        project_slug: str,
        params: InitiativeBootstrapParams,
    ) -> _InitiativeLocation:
        return PlanPathIdHelper.project_scoped_initiative_location(
            project_slug,
            trace_id=params.trace_id,
            initiative_slug=params.initiative_slug,
        )

    def _project_scoped_location_for_slug(
        self,
        project_slug: str,
        initiative_slug: str,
    ) -> _InitiativeLocation:
        return PlanPathIdHelper.project_scoped_initiative_location(
            project_slug,
            initiative_slug=initiative_slug,
        )

    def _initiative_root(self, location: _InitiativeLocation) -> Path:
        return self._loader.repo_root / location.initiative_root_relative

    def _initiative_path_for_location(self, location: _InitiativeLocation, suffix: str) -> str:
        return location.relative_path(suffix)

    def _initiative_identity_exists(self, initiative_id: str, trace_id: str) -> bool:
        roots = [self._loader.repo_root / "plan" / "initiatives"]
        projects_root = self._loader.repo_root / "plan" / "projects"
        if projects_root.exists():
            roots.extend(sorted(projects_root.glob("*/initiatives")))
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*/.wt/initiative.json")):
                document = json.loads(path.read_text(encoding="utf-8"))
                if (
                    str(document.get("initiative_id")) == initiative_id
                    or str(document.get("trace_id")) == trace_id
                ):
                    return True
        return False

    def _trace_id_exists(self, trace_id: str) -> bool:
        roots = [self._loader.repo_root / "plan" / "initiatives"]
        projects_root = self._loader.repo_root / "plan" / "projects"
        if projects_root.exists():
            roots.extend(sorted(projects_root.glob("*/initiatives")))
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*/.wt/initiative.json")):
                document = json.loads(path.read_text(encoding="utf-8"))
                if str(document.get("trace_id")) == trace_id:
                    return True
        return False

    def _has_execution_started(self, location: _InitiativeLocation) -> bool:
        events_root = self._initiative_root(location) / ".wt" / "events"
        if not events_root.exists():
            return False
        for path in sorted(events_root.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            if str(document.get("event_type")) == "execution_started":
                return True
        return False

    def _sync_derived_surfaces(self, location: _InitiativeLocation) -> None:
        fresh_loader = self._fresh_loader()
        if location.project_slug is not None:
            ProjectWorkspaceService(fresh_loader).sync(write=True)
        PlanWorkspaceService(fresh_loader).sync(write=True)
        CoordinationSyncService(fresh_loader).run(write=True)
