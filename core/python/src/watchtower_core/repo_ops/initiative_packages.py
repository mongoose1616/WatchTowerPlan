"""Pack-wide initiative package bootstrap and readiness helpers for the plan workspace."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.plan_workspace import PlanWorkspaceService
from watchtower_core.repo_ops.planning_scaffold_specs import trace_suffix
from watchtower_core.repo_ops.task_lifecycle_support import slugify_file_stem
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

        task_specs = tuple(params.task_specs)
        if not task_specs:
            raise ValueError("Bootstrap requires at least one initiative task.")

        updated_at = params.updated_at or utc_timestamp_now()
        initiative_slug = params.initiative_slug or trace_suffix(params.trace_id)
        trace_id_suffix = trace_suffix(params.trace_id)
        if initiative_slug != trace_id_suffix:
            raise ValueError(
                "initiative_slug must match the trace stem derived from trace_id."
            )
        initiative_id = params.initiative_id or f"initiative.{initiative_slug}"
        if initiative_id != f"initiative.{initiative_slug}":
            raise ValueError("initiative_id must use the canonical initiative.<slug> form.")

        initiative_root = self._initiative_root(initiative_slug)
        if initiative_root.exists():
            raise ValueError(
                f"Initiative root already exists: {initiative_root.relative_to(self._loader.repo_root)}"
            )

        authored_documents = self._build_authored_documents(
            initiative_slug=initiative_slug,
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
            initiative_slug=initiative_slug,
            initiative_id=initiative_id,
            task_specs=task_specs,
            updated_at=updated_at,
        )
        deferred_documents = self._build_deferred_documents(
            initiative_slug=initiative_slug,
            initiative_id=initiative_id,
            deferred_items=params.deferred_items,
            updated_at=updated_at,
        )
        evidence_document = self._build_validation_bundle(
            initiative_slug=initiative_slug,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            updated_at=updated_at,
        )
        closeout_document = self._build_closeout_recap(
            initiative_slug=initiative_slug,
            initiative_id=initiative_id,
            evidence_id=evidence_document["id"],
            updated_at=updated_at,
        )
        promotion_document = self._build_promotion_shell(
            initiative_slug=initiative_slug,
            initiative_id=initiative_id,
            authored_document_paths=tuple(authored_documents),
            updated_at=updated_at,
        )
        initiative_document = self._build_initiative_state(
            initiative_slug=initiative_slug,
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
            initiative_slug=initiative_slug,
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
                initiative_root=str(initiative_root.relative_to(self._loader.repo_root)),
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
            self._initiative_path(initiative_slug, ".wt/evidence/validation_bundle.bootstrap.json"),
            evidence_document,
        )
        self._loader.artifact_store.write_json_object(
            self._initiative_path(initiative_slug, ".wt/closeout/closeout_recap.bootstrap.json"),
            closeout_document,
        )
        self._loader.artifact_store.write_json_object(
            self._initiative_path(
                initiative_slug,
                ".wt/promotions/guidance_promotion_record.bootstrap.json",
            ),
            promotion_document,
        )
        self._loader.artifact_store.write_json_object(
            self._initiative_path(initiative_slug, ".wt/initiative.json"),
            initiative_document,
        )
        for relative_path, document in initiative_events.items():
            self._loader.artifact_store.write_json_object(relative_path, document)
        PlanWorkspaceService(self._loader).sync(write=True)

        readiness = self.validate_packwide(
            initiative_slug,
            write=True,
            require_approved=False,
        )
        state = self._load_json(self._initiative_path(initiative_slug, ".wt/initiative.json"))
        return InitiativePackageResult(
            initiative_id=str(state["initiative_id"]),
            trace_id=str(state["trace_id"]),
            initiative_root=str(initiative_root.relative_to(self._loader.repo_root)),
            lifecycle_stage=str(state["lifecycle_stage"]),
            review_status=str(state["review_status"]),
            ready_for_execution=bool(state["gate_state"]["ready_for_execution"]),
            validation_passed=readiness.passed,
            wrote=True,
        )

    def validate_packwide(
        self,
        initiative_slug: str,
        *,
        write: bool,
        require_approved: bool = False,
    ) -> InitiativeReadinessResult:
        """Validate one pack-wide initiative package and refresh its gate state."""

        initiative_state_path = self._initiative_path(initiative_slug, ".wt/initiative.json")
        initiative_document = self._load_json(initiative_state_path)
        initiative_id = str(initiative_document["initiative_id"])
        trace_id = str(initiative_document["trace_id"])
        previous_lifecycle_stage = str(initiative_document["lifecycle_stage"])

        pack_loader = self._pack_loader()
        validator = ArtifactValidationService(pack_loader)
        artifact_paths = self._artifact_paths_for_initiative(initiative_slug)
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
        authored_input_issues = self._authored_input_drift_issues(
            initiative_slug=initiative_slug,
            initiative_document=initiative_document,
        )
        issues.extend(issue.message for issue in authored_input_issues)
        if authored_input_issues:
            blocking_reasons.append("authored_input_drift")
        derived_surface_issues = self._stale_derived_surface_issues(initiative_slug)
        issues.extend(issue.message for issue in derived_surface_issues)
        if derived_surface_issues:
            blocking_reasons.append("stale_derived_surfaces")

        deferred_issues = self._blocking_deferred_item_issues(initiative_slug)
        issues.extend(deferred_issues)
        if deferred_issues:
            blocking_reasons.append("blocking_deferred_items")

        if write:
            self._sync_managed_discrepancies(
                initiative_slug=initiative_slug,
                initiative_id=initiative_id,
                discrepancy_issues=tuple((*authored_input_issues, *derived_surface_issues)),
                updated_at=utc_timestamp_now(),
            )
        open_discrepancies = self._open_discrepancy_documents(initiative_slug)
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
        lifecycle_stage = (
            "ready_for_review"
            if passed and not require_approved
            else str(initiative_document["lifecycle_stage"])
        )
        if require_approved and passed:
            lifecycle_stage = "ready_for_execution"
        elif issues:
            lifecycle_stage = (
                "blocked"
                if initiative_document["lifecycle_stage"] in {"ready_for_execution", "in_progress"}
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
                    reason in {"missing_artifacts", "blocking_deferred_items"}
                    for reason in blocking_reasons
                ),
                "machine_valid": not issues,
                "approval_status": initiative_document["gate_state"]["approval_status"],
                "ready_for_execution": (
                    initiative_document["gate_state"]["approval_status"] == "approved" and passed
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
                    initiative_slug=initiative_slug,
                    initiative_id=initiative_id,
                    trace_id=trace_id,
                    event_type="ready_for_review_marked",
                    summary="The initiative package passed capture validation and is ready for review.",
                    actor_id="actor.watchtower_core",
                    recorded_at=str(initiative_document["updated_at"]),
                )
            PlanWorkspaceService(self._loader).sync(write=True)

        return InitiativeReadinessResult(
            initiative_id=initiative_id,
            trace_id=trace_id,
            initiative_root=self._initiative_root_relative(initiative_slug),
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
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Confirm edited authored inputs into machine state."""

        self._assert_default_authorized_maintainer(approver_actor_id)
        initiative_state_path = self._initiative_path(initiative_slug, ".wt/initiative.json")
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
                initiative_slug=initiative_slug,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="authored_inputs_confirmed",
                summary="An authorized maintainer confirmed the authored intake documents into machine state.",
                actor_id=approver_actor_id,
                recorded_at=updated_at,
            )
            PlanWorkspaceService(self._loader).sync(write=True)
            readiness = self.validate_packwide(
                initiative_slug,
                write=True,
                require_approved=False,
            )
        else:
            readiness = self.validate_packwide(
                initiative_slug,
                write=False,
                require_approved=False,
            )
        refreshed_state = self._load_json(initiative_state_path)
        return InitiativePackageResult(
            initiative_id=str(refreshed_state["initiative_id"]),
            trace_id=str(refreshed_state["trace_id"]),
            initiative_root=self._initiative_root_relative(initiative_slug),
            lifecycle_stage=str(refreshed_state["lifecycle_stage"]),
            review_status=str(refreshed_state["review_status"]),
            ready_for_execution=bool(refreshed_state["gate_state"]["ready_for_execution"]),
            validation_passed=readiness.passed,
            wrote=write,
        )

    def approve_packwide(
        self,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Approve one validated pack-wide initiative into ready_for_execution."""

        self._assert_default_authorized_maintainer(approver_actor_id)
        readiness = self.validate_packwide(
            initiative_slug,
            write=write,
            require_approved=False,
        )
        if not readiness.passed:
            joined = "; ".join(readiness.issue_messages)
            raise ValueError(f"Initiative package is not ready for approval: {joined}")

        initiative_state_path = self._initiative_path(initiative_slug, ".wt/initiative.json")
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
                initiative_slug=initiative_slug,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="ready_for_execution_approved",
                summary="An authorized maintainer approved the initiative package for execution.",
                actor_id=approver_actor_id,
                recorded_at=updated_at,
            )
            self._append_initiative_event(
                initiative_slug=initiative_slug,
                initiative_id=str(initiative_document["initiative_id"]),
                trace_id=str(initiative_document["trace_id"]),
                event_type="ready_for_execution_marked",
                summary="The initiative package entered ready_for_execution after approval.",
                actor_id="actor.watchtower_core",
                recorded_at=updated_at,
            )
            PlanWorkspaceService(self._loader).sync(write=True)

        return InitiativePackageResult(
            initiative_id=str(initiative_document["initiative_id"]),
            trace_id=str(initiative_document["trace_id"]),
            initiative_root=self._initiative_root_relative(initiative_slug),
            lifecycle_stage="ready_for_execution",
            review_status="approved",
            ready_for_execution=True,
            validation_passed=True,
            wrote=write,
        )

    def _build_authored_documents(
        self,
        *,
        initiative_slug: str,
        initiative_id: str,
        trace_id: str,
        title: str,
        summary: str,
        include_decision_notes: bool,
        task_specs: tuple[InitiativeTaskSpec, ...],
    ) -> dict[str, str]:
        task_lines = "\n".join(
            f"- `{task.task_id or f'task.{initiative_slug}.{task.slug or slugify_file_stem(task.title)}'}`: {task.summary}"
            for task in task_specs
        )
        documents = {
            self._initiative_path(initiative_slug, "initiative_brief.md"): "\n".join(
                (
                    f"# {title}",
                    "",
                    "## Summary",
                    summary,
                    "",
                    "## Identity",
                    f"- `initiative_id`: `{initiative_id}`",
                    f"- `trace_id`: `{trace_id}`",
                    f"- `scope_type`: `pack_wide`",
                    "",
                    "## Initial Task Set",
                    task_lines,
                    "",
                )
            ),
            self._initiative_path(initiative_slug, "design_record.md"): "\n".join(
                (
                    f"# {title} Design Record",
                    "",
                    "## Summary",
                    summary,
                    "",
                    "## Initial Design Boundary",
                    "- The initiative package is machine-first and local to `plan/initiatives/<slug>/.wt/`.",
                    "- Authored intake docs remain editable inputs but require explicit machine confirmation.",
                    "- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.",
                    "",
                )
            ),
            self._initiative_path(initiative_slug, "implementation_slice.md"): "\n".join(
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
            documents[self._initiative_path(initiative_slug, "decision_notes.md")] = "\n".join(
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
        initiative_slug: str,
        initiative_id: str,
        task_specs: tuple[InitiativeTaskSpec, ...],
        updated_at: str,
    ) -> dict[str, dict[str, object]]:
        documents: dict[str, dict[str, object]] = {}
        for spec in task_specs:
            task_slug = spec.slug or slugify_file_stem(spec.title)
            task_id = spec.task_id or f"task.{initiative_slug}.{task_slug}"
            task_path = self._initiative_path(initiative_slug, f".wt/tasks/{task_slug}/task.json")
            documents[task_path] = {
                "$schema": "urn:watchtower:schema:artifacts:plan:task-state:v1",
                "task_id": task_id,
                "slug": task_slug,
                "initiative_id": initiative_id,
                "title": spec.title,
                "summary": spec.summary,
                "status": "planned",
                "task_kind": spec.task_kind,
                "priority": spec.priority,
                "owner": spec.owner,
                "created_at": updated_at,
                "updated_at": updated_at,
                "dependency_task_ids": list(spec.depends_on),
                "blocker_task_ids": list(spec.blocked_by),
                "related_ids": list(spec.related_ids),
            }
            documents[
                self._initiative_path(
                    initiative_slug,
                    f".wt/tasks/{task_slug}/events/0001_created.json",
                )
            ] = {
                "$schema": "urn:watchtower:schema:artifacts:plan:task-event-stream:v1",
                "event_id": f"event.{initiative_slug}.{task_slug}.0001_created",
                "initiative_id": initiative_id,
                "task_id": task_id,
                "sequence": 1,
                "event_type": "created",
                "actor_id": "actor.watchtower_core",
                "recorded_at": updated_at,
                "summary": f"Created task {task_id} during initiative bootstrap.",
                "payload": {
                    "status": "planned",
                    "owner": spec.owner,
                },
            }
        return documents

    def _build_deferred_documents(
        self,
        *,
        initiative_slug: str,
        initiative_id: str,
        deferred_items: tuple[DeferredItemSpec, ...],
        updated_at: str,
    ) -> dict[str, dict[str, object]]:
        documents: dict[str, dict[str, object]] = {}
        for spec in deferred_items:
            deferred_slug = spec.slug or slugify_file_stem(spec.summary)
            deferred_id = spec.deferred_item_id or f"deferred.{initiative_slug}.{deferred_slug}"
            documents[
                self._initiative_path(
                    initiative_slug,
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
        initiative_slug: str,
        initiative_id: str,
        trace_id: str,
        updated_at: str,
    ) -> dict[str, object]:
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:validation-bundle:v1",
            "id": f"evidence.{initiative_slug}.bootstrap_validation_bundle",
            "initiative_id": initiative_id,
            "trace_id": trace_id,
            "title": "Bootstrap Validation Bundle",
            "status": "planned",
            "updated_at": updated_at,
            "entries": [
                {
                    "entry_id": f"entry.{initiative_slug}.schema_validation",
                    "acceptance_label": "package_contracts_valid",
                    "validation_type": "schema_validation",
                    "owner": "repository_maintainer",
                    "target_phase": "readiness",
                    "expected_output_paths": [
                        self._initiative_path(initiative_slug, ".wt/initiative.json")
                    ],
                },
                {
                    "entry_id": f"entry.{initiative_slug}.gate_validation",
                    "acceptance_label": "ready_for_execution_gate",
                    "validation_type": "readiness_gate",
                    "owner": "repository_maintainer",
                    "target_phase": "readiness",
                    "expected_output_paths": [
                        self._initiative_path(initiative_slug, ".wt/discrepancies")
                    ],
                }
            ],
        }

    def _build_closeout_recap(
        self,
        *,
        initiative_slug: str,
        initiative_id: str,
        evidence_id: str,
        updated_at: str,
    ) -> dict[str, object]:
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:closeout-recap:v1",
            "id": f"closeout.{initiative_slug}.bootstrap_recap",
            "initiative_id": initiative_id,
            "title": "Bootstrap Closeout Shell",
            "status": "planned",
            "updated_at": updated_at,
            "expected_outcome": "Close out the initiative with validated capture, readiness, and follow-up accounting.",
            "acceptance_ids": [f"acceptance.{initiative_slug}.bootstrap"],
            "evidence_ids": [evidence_id],
            "follow_up_handling": "Record unresolved work as deferred items or bounded follow-up initiatives before closeout.",
            "promotion_review_required": True,
            "terminal_state_options": ["completed", "superseded", "cancelled"],
        }

    def _build_promotion_shell(
        self,
        *,
        initiative_slug: str,
        initiative_id: str,
        authored_document_paths: tuple[str, ...],
        updated_at: str,
    ) -> dict[str, object]:
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:guidance-promotion-record:v1",
            "id": f"promotion.{initiative_slug}.bootstrap_shell",
            "initiative_id": initiative_id,
            "title": "Bootstrap Promotion Shell",
            "status": "planned",
            "updated_at": updated_at,
            "candidates": [
                {
                    "candidate_path": path,
                    "target_family": "decision_record" if path.endswith("design_record.md") else "reference",
                    "review_path": "repository_maintainer_review",
                    "provenance_expectation": "Promotions must cite the source initiative id, trace id, and evidence bundle id.",
                }
                for path in authored_document_paths
            ],
        }

    def _build_initiative_state(
        self,
        *,
        initiative_slug: str,
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
            "scope_type": "pack_wide",
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
        initiative_slug: str,
        initiative_id: str,
        trace_id: str,
        task_documents: dict[str, dict[str, object]],
        updated_at: str,
        related_paths: tuple[str, ...],
    ) -> dict[str, dict[str, object]]:
        event_types = [
            ("created", "Created the initiative package root."),
            ("scope_defined", "Recorded the initial pack-wide initiative scope."),
            ("authored_inputs_confirmed", "Confirmed the authored intake documents into machine state."),
            ("task_state_seeded", "Seeded the initial initiative-local task set."),
            ("evidence_shell_seeded", "Seeded the evidence shell."),
            ("closeout_shell_seeded", "Seeded the closeout shell."),
            ("promotion_shell_seeded", "Seeded the promotion shell."),
        ]
        events: dict[str, dict[str, object]] = {}
        for sequence, (event_type, summary) in enumerate(event_types, start=1):
            events[
                self._initiative_path(
                    initiative_slug,
                    f".wt/events/{sequence:04d}_{event_type}.json",
                )
            ] = {
                "$schema": "urn:watchtower:schema:artifacts:plan:initiative-event-stream:v1",
                "event_id": f"event.{initiative_slug}.{sequence:04d}_{event_type}",
                "initiative_id": initiative_id,
                "trace_id": trace_id,
                "sequence": sequence,
                "event_type": event_type,
                "actor_id": "actor.watchtower_core",
                "recorded_at": updated_at,
                "summary": summary,
                "related_paths": list(related_paths),
                "payload": {
                    "task_count": sum(1 for path in task_documents if path.endswith("/task.json"))
                },
            }
        return events

    def _pack_loader(self) -> ControlPlaneLoader:
        return ControlPlaneLoader(
            self._loader.repo_root,
            active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def _artifact_paths_for_initiative(self, initiative_slug: str) -> tuple[str, ...]:
        initiative_root = self._initiative_root(initiative_slug)
        relative_paths: list[str] = []
        for path in sorted(initiative_root.rglob("*.json")):
            relative_paths.append(str(path.relative_to(self._loader.repo_root)))
        return tuple(relative_paths)

    def _authored_input_drift_issues(
        self,
        *,
        initiative_slug: str,
        initiative_document: dict[str, object],
    ) -> tuple[_DiscrepancyIssue, ...]:
        issues: list[_DiscrepancyIssue] = []
        for record in initiative_document["authored_inputs"]:
            relative_path = str(record["path"])
            current_digest = self._sha256_for_relative_path(relative_path)
            if current_digest != record["sha256"]:
                issues.append(
                    _DiscrepancyIssue(
                        category="authored_input_drift",
                        doc_kind=str(record["doc_kind"]),
                        relative_paths=(relative_path,),
                        message=(
                            f"Authored input drift detected for {relative_path}; "
                            "machine confirmation is required."
                        ),
                        discrepancy_id=f"discrepancy.{initiative_slug}.{record['doc_kind']}_drift",
                    )
                )
        return tuple(issues)

    def _stale_derived_surface_issues(self, initiative_slug: str) -> tuple[_DiscrepancyIssue, ...]:
        return tuple(
            _DiscrepancyIssue(
                category=issue.category,
                doc_kind=Path(issue.relative_path).stem,
                relative_paths=(issue.relative_path,),
                message=issue.message,
                discrepancy_id=issue.discrepancy_id,
            )
            for issue in PlanWorkspaceService(self._loader).expected_surface_issues(initiative_slug)
        )

    def _blocking_deferred_item_issues(self, initiative_slug: str) -> tuple[str, ...]:
        deferred_dir = self._loader.repo_root / self._initiative_path(initiative_slug, ".wt/deferred")
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
        initiative_slug: str,
    ) -> tuple[tuple[str, dict[str, object]], ...]:
        discrepancy_dir = self._loader.repo_root / self._initiative_path(
            initiative_slug,
            ".wt/discrepancies",
        )
        if not discrepancy_dir.exists():
            return ()
        documents: list[tuple[str, dict[str, object]]] = []
        for path in sorted(discrepancy_dir.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            if document["status"] == "open":
                documents.append((str(path.relative_to(self._loader.repo_root)), document))
        return tuple(documents)

    def _sync_managed_discrepancies(
        self,
        *,
        initiative_slug: str,
        initiative_id: str,
        discrepancy_issues: tuple[_DiscrepancyIssue, ...],
        updated_at: str,
    ) -> None:
        discrepancy_dir = self._loader.repo_root / self._initiative_path(
            initiative_slug,
            ".wt/discrepancies",
        )
        discrepancy_dir.mkdir(parents=True, exist_ok=True)
        issue_map = {issue.discrepancy_id: issue for issue in discrepancy_issues}
        managed_categories = {
            "authored_input_drift",
            "stale_rendered_surface",
            "stale_aggregate_index",
            *(issue.category for issue in discrepancy_issues),
        }

        existing_paths = sorted(discrepancy_dir.glob("*.json"))
        for path in existing_paths:
            document = json.loads(path.read_text(encoding="utf-8"))
            discrepancy_id = str(document["discrepancy_id"])
            if discrepancy_id in issue_map:
                issue = issue_map[discrepancy_id]
                document["category"] = issue.category
                document["severity"] = issue.severity
                document["gate_effect"] = issue.gate_effect
                document["status"] = "open"
                document["summary"] = issue.message
                document["source_paths"] = list(issue.relative_paths)
                document["resolution_owner"] = issue.resolution_owner
                document["updated_at"] = updated_at
                self._loader.artifact_store.write_json_object(
                    str(path.relative_to(self._loader.repo_root)),
                    document,
                )
                issue_map.pop(discrepancy_id, None)
            elif document["category"] in managed_categories and document["status"] == "open":
                document["status"] = "resolved"
                document["updated_at"] = updated_at
                self._loader.artifact_store.write_json_object(
                    str(path.relative_to(self._loader.repo_root)),
                    document,
                )

        for issue in issue_map.values():
            relative_path = self._initiative_path(
                initiative_slug,
                f".wt/discrepancies/{issue.doc_kind}_drift.json",
            )
            self._loader.artifact_store.write_json_object(
                relative_path,
                {
                    "$schema": "urn:watchtower:schema:artifacts:plan:discrepancy-record:v1",
                    "discrepancy_id": issue.discrepancy_id,
                    "initiative_id": initiative_id,
                    "category": issue.category,
                    "severity": issue.severity,
                    "gate_effect": issue.gate_effect,
                    "status": "open",
                    "summary": issue.message,
                    "source_paths": list(issue.relative_paths),
                    "resolution_owner": issue.resolution_owner,
                    "detected_at": updated_at,
                    "updated_at": updated_at,
                },
            )

    def _append_initiative_event(
        self,
        *,
        initiative_slug: str,
        initiative_id: str,
        trace_id: str,
        event_type: str,
        summary: str,
        actor_id: str,
        recorded_at: str,
    ) -> None:
        events_dir = self._loader.repo_root / self._initiative_path(initiative_slug, ".wt/events")
        sequence = len(tuple(events_dir.glob("*.json"))) + 1
        relative_path = self._initiative_path(
            initiative_slug,
            f".wt/events/{sequence:04d}_{event_type}.json",
        )
        self._loader.artifact_store.write_json_object(
            relative_path,
            {
                "$schema": "urn:watchtower:schema:artifacts:plan:initiative-event-stream:v1",
                "event_id": f"event.{initiative_slug}.{sequence:04d}_{event_type}",
                "initiative_id": initiative_id,
                "trace_id": trace_id,
                "sequence": sequence,
                "event_type": event_type,
                "actor_id": actor_id,
                "recorded_at": recorded_at,
                "summary": summary,
                "payload": {},
            },
        )

    def _assert_default_authorized_maintainer(self, actor_id: str) -> None:
        actor = self._loader.load_actor_registry().get(actor_id)
        if actor.actor_type != "user" or actor.role != "owner":
            raise ValueError(
                "Only default human repository maintainers may approve this initiative package."
            )

    def _load_json(self, relative_path: str) -> dict[str, object]:
        path = self._loader.repo_root / relative_path
        return json.loads(path.read_text(encoding="utf-8"))

    def _sha256_for_relative_path(self, relative_path: str) -> str:
        path = self._loader.repo_root / relative_path
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _initiative_root(self, initiative_slug: str) -> Path:
        return self._loader.repo_root / "plan" / "initiatives" / initiative_slug

    def _initiative_root_relative(self, initiative_slug: str) -> str:
        return f"plan/initiatives/{initiative_slug}"

    def _initiative_path(self, initiative_slug: str, suffix: str) -> str:
        return f"{self._initiative_root_relative(initiative_slug)}/{suffix}"


@dataclass(frozen=True, slots=True)
class _DiscrepancyIssue:
    """Internal discrepancy sync record produced by initiative validation."""

    category: str
    doc_kind: str
    relative_paths: tuple[str, ...]
    message: str
    discrepancy_id: str
    severity: str = "high"
    gate_effect: str = "readiness"
    resolution_owner: str = "repository_maintainer"
