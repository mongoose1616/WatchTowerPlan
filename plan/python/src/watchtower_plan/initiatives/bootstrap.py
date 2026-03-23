"""Bootstrap flows and seeded artifact builders for live initiative packages."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.event_stream import (
    EventStreamDescriptor,
    EventStreamWriteRequest,
)
from watchtower_core.control_plane.path_ids import PlanPathIdHelper
from watchtower_core.control_plane.promotion_policy import PromotionPolicyHelper
from watchtower_core.evidence import EvidenceBundleEntrySpec, EvidenceBundleHelper
from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_plan.projects import ProjectWorkspaceService
from watchtower_plan.promotion import (
    default_mirror_target_paths,
    default_target_family_for_source_kind,
    default_target_path,
    source_artifact_kind_for_path,
)
from watchtower_plan.tasks.support import slugify_file_stem
from watchtower_plan.workspace.constants import PLAN_PACK_SETTINGS_PATH

from watchtower_plan.initiatives.discrepancies import InitiativeDiscrepancyCoordinator
from watchtower_plan.initiatives.locations import (
    InitiativeLocation,
    InitiativeLocationManager,
)
from watchtower_plan.initiatives.models import (
    DeferredItemSpec,
    InitiativeBootstrapParams,
    InitiativePackageResult,
    InitiativeTaskSpec,
)
from watchtower_plan.initiatives.readiness import InitiativeReadinessCoordinator


class InitiativeBootstrapCoordinator:
    """Create initiative packages and seed their initial machine-managed state."""

    def __init__(
        self,
        context: InitiativeLocationManager,
        discrepancies: InitiativeDiscrepancyCoordinator,
        readiness: InitiativeReadinessCoordinator,
    ) -> None:
        self._context = context
        self._discrepancies = discrepancies
        self._readiness = readiness

    def bootstrap_initiative(
        self,
        location: InitiativeLocation,
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
            raise ValueError(
                "initiative_id must use the canonical initiative.<slug> form."
            )

        initiative_root = self._context.initiative_root(location)
        if initiative_root.exists():
            raise ValueError(
                f"Initiative root already exists: {initiative_root.relative_to(self._context.pack_loader().repo_root)}"
            )
        if self._context.initiative_identity_exists(initiative_id, params.trace_id):
            raise ValueError(
                "initiative_id and trace_id must remain globally unique across pack-wide and project-scoped initiatives."
            )
        if location.scope_type == "project_scoped":
            project_validation = ProjectWorkspaceService(
                self._context.fresh_loader()
            ).validate(
                location.project_slug or "",
                write=False,
            )
            if not project_validation.passed:
                raise ValueError(
                    "Project-scoped initiative bootstrap requires a valid project container: "
                    + "; ".join(project_validation.issue_messages)
                )

        updated_at = params.updated_at or utc_timestamp_now()
        authored_documents = self.build_authored_documents(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            title=params.title,
            summary=params.summary,
            include_decision_notes=params.include_decision_notes,
            task_specs=task_specs,
        )
        authored_input_records = self.authored_input_records(
            authored_documents=authored_documents,
            updated_at=updated_at,
        )
        task_documents = self.build_task_documents(
            location=location,
            initiative_id=initiative_id,
            task_specs=task_specs,
            updated_at=updated_at,
        )
        deferred_documents = self.build_deferred_documents(
            location=location,
            initiative_id=initiative_id,
            deferred_items=params.deferred_items,
            updated_at=updated_at,
        )
        evidence_document = self.build_validation_bundle(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            updated_at=updated_at,
        )
        closeout_document = self.build_closeout_recap(
            location=location,
            initiative_id=initiative_id,
            evidence_id=str(evidence_document["id"]),
            updated_at=updated_at,
        )
        promotion_document = self.build_promotion_shell(
            location=location,
            initiative_id=initiative_id,
            trace_id=params.trace_id,
            authored_document_paths=tuple(authored_documents),
            evidence_id=str(evidence_document["id"]),
            updated_at=updated_at,
        )
        initiative_document = self.build_initiative_state(
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
        initiative_events = self.bootstrap_initiative_events(
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
            target = self._context.pack_loader().repo_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        for relative_path, document in task_documents.items():
            self._context.pack_loader().artifact_store.write_json_object(
                relative_path, document
            )
        for relative_path, document in deferred_documents.items():
            self._context.pack_loader().artifact_store.write_json_object(
                relative_path, document
            )
        self._context.pack_loader().artifact_store.write_json_object(
            self._context.initiative_path(
                location,
                ".wt/evidence/validation_bundle.bootstrap.json",
            ),
            evidence_document,
        )
        self._context.pack_loader().artifact_store.write_json_object(
            self._context.initiative_path(
                location,
                ".wt/closeout/closeout_recap.bootstrap.json",
            ),
            closeout_document,
        )
        self._context.pack_loader().artifact_store.write_json_object(
            self._context.initiative_path(
                location,
                ".wt/promotions/guidance_promotion_record.bootstrap.json",
            ),
            promotion_document,
        )
        self._context.pack_loader().artifact_store.write_json_object(
            self._context.initiative_path(location, ".wt/initiative.json"),
            initiative_document,
        )
        for relative_path, document in initiative_events.items():
            self._context.pack_loader().artifact_store.write_json_object(
                relative_path, document
            )
        readiness = self._readiness.validate_initiative(
            location,
            write=True,
            require_approved=False,
        )
        self._context.sync_derived_surfaces(location)
        readiness = self._readiness.validate_initiative(
            location,
            write=True,
            require_approved=False,
        )
        state = self._context.load_json(
            self._context.initiative_path(location, ".wt/initiative.json")
        )
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

    def build_authored_documents(
        self,
        *,
        location: InitiativeLocation,
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
            self._context.initiative_path(location, "initiative_brief.md"): "\n".join(
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
            self._context.initiative_path(location, "design_record.md"): "\n".join(
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
            self._context.initiative_path(
                location, "implementation_slice.md"
            ): "\n".join(
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
            documents[self._context.initiative_path(location, "decision_notes.md")] = (
                "\n".join(
                    (
                        f"# {title} Decision Notes",
                        "",
                        "## Summary",
                        "Optional decision notes seeded during initiative bootstrap.",
                        "",
                    )
                )
            )
        return documents

    def authored_input_records(
        self,
        *,
        authored_documents: dict[str, str],
        updated_at: str,
    ) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
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

    def build_task_documents(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        task_specs: tuple[InitiativeTaskSpec, ...],
        updated_at: str,
    ) -> dict[str, dict[str, Any]]:
        initiative_slug = location.initiative_slug
        event_helper = self._discrepancies.event_stream_helper()
        documents: dict[str, dict[str, Any]] = {}
        for spec in task_specs:
            task_slug = spec.slug or slugify_file_stem(spec.title)
            task_id = spec.task_id or PlanPathIdHelper.canonical_task_id(
                initiative_slug,
                task_slug,
            )
            task_path = self._context.initiative_path(
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
                relative_dir=self._context.initiative_path(
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

    def build_deferred_documents(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        deferred_items: tuple[DeferredItemSpec, ...],
        updated_at: str,
    ) -> dict[str, dict[str, Any]]:
        initiative_slug = location.initiative_slug
        documents: dict[str, dict[str, Any]] = {}
        for spec in deferred_items:
            deferred_slug = spec.slug or slugify_file_stem(spec.summary)
            deferred_id = (
                spec.deferred_item_id
                or PlanPathIdHelper.canonical_deferred_item_id(
                    initiative_slug,
                    deferred_slug,
                )
            )
            documents[
                self._context.initiative_path(
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

    def build_validation_bundle(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        updated_at: str,
    ) -> dict[str, Any]:
        initiative_slug = location.initiative_slug
        return EvidenceBundleHelper(self._context.pack_loader()).build_document(
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
                        self._context.initiative_path(location, ".wt/initiative.json"),
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
                        self._context.initiative_path(location, ".wt/discrepancies"),
                    ),
                ),
            ),
        )

    def build_closeout_recap(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        evidence_id: str,
        updated_at: str,
    ) -> dict[str, Any]:
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

    def build_promotion_shell(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        authored_document_paths: tuple[str, ...],
        evidence_id: str,
        updated_at: str,
    ) -> dict[str, Any]:
        initiative_slug = location.initiative_slug
        policy_helper = PromotionPolicyHelper.from_loader(
            self._context.pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        candidates: list[dict[str, Any]] = []
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
                target_family=target_family,
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

    def build_initiative_state(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        title: str,
        summary: str,
        owner: str,
        task_documents: dict[str, dict[str, Any]],
        deferred_documents: dict[str, dict[str, Any]],
        authored_input_records: list[dict[str, Any]],
        evidence_id: str,
        closeout_id: str,
        promotion_id: str,
        updated_at: str,
    ) -> dict[str, Any]:
        initiative_slug = location.initiative_slug
        task_ids = [
            document["task_id"]
            for relative_path, document in task_documents.items()
            if relative_path.endswith("/task.json")
        ]
        deferred_ids = [
            document["deferred_item_id"] for document in deferred_documents.values()
        ]
        return {
            "$schema": "urn:watchtower:schema:artifacts:plan:initiative-state:v1",
            "initiative_id": initiative_id,
            "trace_id": trace_id,
            "slug": initiative_slug,
            "title": title,
            "summary": summary,
            "scope_type": location.scope_type,
            **(
                {"project_id": location.project_id}
                if location.project_id is not None
                else {}
            ),
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

    def bootstrap_initiative_events(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        task_documents: dict[str, dict[str, Any]],
        updated_at: str,
        related_paths: tuple[str, ...],
    ) -> dict[str, dict[str, Any]]:
        initiative_slug = location.initiative_slug
        event_helper = self._discrepancies.event_stream_helper()
        descriptor = EventStreamDescriptor.initiative(
            relative_dir=self._context.initiative_path(location, ".wt/events"),
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
            (
                "authored_inputs_confirmed",
                "Confirmed the authored intake documents into machine state.",
            ),
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


__all__ = ["InitiativeBootstrapCoordinator"]
