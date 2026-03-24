"""Document builders for plan-workspace indexes and rendered surface inputs."""

from __future__ import annotations

from typing import Any

from watchtower_core.adapters.front_matter import (
    FrontMatterParseError,
    load_front_matter,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    CoordinationRecentInitiativeSummary,
    CoordinationTaskSummary,
    InitiativeActiveTaskSummary,
    InitiativeIndexEntry,
    TraceabilityEntry,
)
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_core.evidence import EvidenceBundleHelper
from watchtower_core.rebuild import RebuildOutput

from watchtower_plan.rendering import serialize_initiative_entry
from watchtower_plan.workspace.constants import (
    PHASE_ORDER,
    PRIORITY_ORDER,
    TERMINAL_TASK_STATUSES,
)
from watchtower_plan.governing_documents import (
    effective_initiative_governing_document_paths,
    effective_task_governing_document_paths,
)
from watchtower_plan.workspace.models import (
    PlanCloseoutIndexEntry,
    PlanDiscrepancyIndexEntry,
    PlanEvidenceIndexEntry,
    PlanGuidanceIndexEntry,
    PlanPromotionIndexEntry,
    PlanReadinessIndexEntry,
    PlanReviewIndexEntry,
    PlanTaskIndexEntry,
)
from watchtower_plan.workspace.rendering import PlanWorkspaceRenderer
from watchtower_plan.workspace.snapshots import (
    PlanInitiativeSnapshot,
    existing_document_updated_at,
    latest_timestamp,
    snapshot_updated_at,
)
from watchtower_plan.workspace.support import (
    current_phase_for_snapshot,
    initiative_status,
    json_document,
    markdown_content,
    next_action,
    next_surface_path,
    ordered_unique_strings,
    task_status_for_id,
    task_status_order,
)


class PlanWorkspaceDocumentBuilder:
    """Build machine-readable plan-workspace documents from initiative snapshots."""

    def __init__(
        self,
        *,
        loader: ControlPlaneLoader,
        pack_loader: ControlPlaneLoader,
        workspace_paths: PackWorkspacePaths,
        initiative_index_path: str,
        task_index_path: str,
        readiness_index_path: str,
        discrepancy_index_path: str,
        evidence_index_path: str,
        closeout_index_path: str,
        review_index_path: str,
        promotion_index_path: str,
        guidance_index_path: str,
        coordination_index_path: str,
        artifact_index_path: str,
        overview_path: str,
        evidence_bundles: EvidenceBundleHelper,
        vocabulary: TerminologyHelper,
        renderer: PlanWorkspaceRenderer,
    ) -> None:
        self._loader = loader
        self._pack_loader = pack_loader
        self._workspace_paths = workspace_paths
        self._initiative_index_path = initiative_index_path
        self._task_index_path = task_index_path
        self._readiness_index_path = readiness_index_path
        self._discrepancy_index_path = discrepancy_index_path
        self._evidence_index_path = evidence_index_path
        self._closeout_index_path = closeout_index_path
        self._review_index_path = review_index_path
        self._promotion_index_path = promotion_index_path
        self._guidance_index_path = guidance_index_path
        self._coordination_index_path = coordination_index_path
        self._artifact_index_path = artifact_index_path
        self._overview_path = overview_path
        self._evidence_bundles = evidence_bundles
        self._vocabulary = vocabulary
        self._renderer = renderer
        self._traceability_entries_by_trace: dict[str, TraceabilityEntry] | None = None

    def artifact_aggregate_overrides(
        self,
        documents: dict[str, Any],
    ) -> dict[str, dict[str, object]]:
        return {
            self._initiative_index_path: self._json_doc(documents["initiative_index"]),
            self._task_index_path: self._json_doc(documents["task_index"]),
            self._readiness_index_path: self._json_doc(documents["readiness_index"]),
            self._discrepancy_index_path: self._json_doc(
                documents["discrepancy_index"]
            ),
            self._evidence_index_path: self._json_doc(documents["evidence_index"]),
            self._closeout_index_path: self._json_doc(documents["closeout_index"]),
            self._review_index_path: self._json_doc(documents["review_index"]),
            self._promotion_index_path: self._json_doc(documents["promotion_index"]),
            self._guidance_index_path: self._json_doc(documents["guidance_index"]),
            self._coordination_index_path: self._json_doc(
                documents["coordination_index"]
            ),
        }

    def build_documents(
        self,
        snapshots: tuple[PlanInitiativeSnapshot, ...],
    ) -> dict[str, Any]:
        existing_workspace_updated_at = latest_timestamp(
            (
                existing_document_updated_at(self._loader.repo_root / relative_path)
                for relative_path in (
                    self._initiative_index_path,
                    self._task_index_path,
                    self._readiness_index_path,
                    self._discrepancy_index_path,
                    self._evidence_index_path,
                    self._closeout_index_path,
                    self._review_index_path,
                    self._promotion_index_path,
                    self._guidance_index_path,
                    self._coordination_index_path,
                    self._artifact_index_path,
                )
            ),
            fallback="",
        )
        workspace_updated_at = latest_timestamp(
            (snapshot_updated_at(snapshot) for snapshot in snapshots),
            fallback=existing_workspace_updated_at,
        )
        initiative_entries = tuple(
            sorted(
                (self._build_initiative_entry(snapshot) for snapshot in snapshots),
                key=lambda entry: entry.trace_id,
            )
        )
        task_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_task_entries(snapshot)
                ),
                key=lambda entry: entry.task_id,
            )
        )
        readiness_entries = tuple(
            sorted(
                (self._build_readiness_entry(snapshot) for snapshot in snapshots),
                key=lambda entry: entry.initiative_id,
            )
        )
        discrepancy_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_discrepancy_entries(snapshot)
                ),
                key=lambda entry: entry.discrepancy_id,
            )
        )
        evidence_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_evidence_entries(snapshot)
                ),
                key=lambda entry: entry.evidence_id,
            )
        )
        closeout_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_closeout_entries(snapshot)
                ),
                key=lambda entry: entry.closeout_id,
            )
        )
        review_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_review_entries(snapshot)
                ),
                key=lambda entry: (entry.subject_kind, entry.review_subject_id),
            )
        )
        promotion_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_promotion_entries(snapshot)
                ),
                key=lambda entry: entry.promotion_id,
            )
        )
        guidance_entries = tuple(
            sorted(
                self._build_guidance_entries(),
                key=lambda entry: entry.doc_path,
            )
        )
        initiative_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:initiative-index:v1",
            "id": "index.initiatives",
            "title": "Plan Workspace Initiative Index",
            "status": "active",
            "entries": [
                serialize_initiative_entry(entry, compact=True)
                for entry in initiative_entries
            ],
        }
        coordination_index = self._build_coordination_document(initiative_entries)
        task_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:task-summary-index:v1",
            "id": "index.plan_tasks",
            "title": "Plan Workspace Task Index",
            "status": "active",
            "entries": [self._serialize_task_entry(entry) for entry in task_entries],
        }
        readiness_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:readiness-index:v1",
            "id": "index.readiness",
            "title": "Plan Workspace Readiness Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [
                    *(entry.updated_at for entry in readiness_entries),
                    workspace_updated_at,
                ]
            ),
            "entries": [
                self._serialize_readiness_entry(entry) for entry in readiness_entries
            ],
        }
        discrepancy_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:discrepancy-index:v1",
            "id": "index.plan_discrepancies",
            "title": "Plan Workspace Discrepancy Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [
                    *(entry.updated_at for entry in discrepancy_entries),
                    workspace_updated_at,
                ]
            ),
            "entries": [
                self._serialize_discrepancy_entry(entry)
                for entry in discrepancy_entries
            ],
        }
        evidence_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:evidence-index:v1",
            "id": "index.evidence",
            "title": "Plan Workspace Evidence Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [
                    *(entry.updated_at for entry in evidence_entries),
                    workspace_updated_at,
                ]
            ),
            "entries": [
                self._serialize_evidence_entry(entry) for entry in evidence_entries
            ],
        }
        closeout_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:closeout-index:v1",
            "id": "index.closeouts",
            "title": "Plan Workspace Closeout Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [
                    *(entry.updated_at for entry in closeout_entries),
                    workspace_updated_at,
                ]
            ),
            "entries": [
                self._serialize_closeout_entry(entry) for entry in closeout_entries
            ],
        }
        review_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:review-index:v1",
            "id": "index.reviews",
            "title": "Plan Workspace Review Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [*(entry.updated_at for entry in review_entries), workspace_updated_at]
            ),
            "entries": [
                self._serialize_review_entry(entry) for entry in review_entries
            ],
        }
        promotion_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:promotion-index:v1",
            "id": "index.promotions",
            "title": "Plan Workspace Promotion Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [
                    *(entry.updated_at for entry in promotion_entries),
                    workspace_updated_at,
                ]
            ),
            "entries": [
                self._serialize_promotion_entry(entry) for entry in promotion_entries
            ],
        }
        guidance_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:guidance-index:v1",
            "id": "index.guidance",
            "title": "Plan Workspace Guidance Index",
            "status": "active",
            "updated_at": latest_timestamp(
                [
                    *(entry.updated_at for entry in guidance_entries),
                    workspace_updated_at,
                ]
            ),
            "entries": [
                self._serialize_guidance_entry(entry) for entry in guidance_entries
            ],
        }
        for document in (
            initiative_index,
            coordination_index,
            task_index,
            readiness_index,
            discrepancy_index,
            evidence_index,
            closeout_index,
            review_index,
            promotion_index,
            guidance_index,
        ):
            self._pack_loader.schema_store.validate_instance(document)

        readiness_by_initiative_id = {
            entry.initiative_id: entry for entry in readiness_entries
        }
        return {
            "initiative_index": initiative_index,
            "coordination_index": coordination_index,
            "task_index": task_index,
            "readiness_index": readiness_index,
            "discrepancy_index": discrepancy_index,
            "evidence_index": evidence_index,
            "closeout_index": closeout_index,
            "review_index": review_index,
            "promotion_index": promotion_index,
            "guidance_index": guidance_index,
            "plan_overview": self._renderer.render_plan_overview(coordination_index),
            "initiative_views": self._renderer.render_initiative_views(
                snapshots,
                readiness_by_initiative_id,
            ),
        }

    def build_task_index_document(
        self,
        snapshots: tuple[PlanInitiativeSnapshot, ...],
    ) -> dict[str, object]:
        task_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_task_entries(snapshot)
                ),
                key=lambda entry: entry.task_id,
            )
        )
        task_index: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:plan:task-summary-index:v1",
            "id": "index.plan_tasks",
            "title": "Plan Workspace Task Index",
            "status": "active",
            "entries": [self._serialize_task_entry(entry) for entry in task_entries],
        }
        self._pack_loader.schema_store.validate_instance(task_index)
        return task_index

    def build_rebuild_outputs(
        self,
        documents: dict[str, Any],
        artifact_document: dict[str, object],
    ) -> tuple[RebuildOutput, ...]:
        initiative_views = documents["initiative_views"]
        assert isinstance(initiative_views, dict)
        outputs = (
            RebuildOutput(
                relative_output_path=self._initiative_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["initiative_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._task_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["task_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._readiness_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["readiness_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._discrepancy_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["discrepancy_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._evidence_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["evidence_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._closeout_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["closeout_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._review_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["review_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._promotion_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["promotion_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._guidance_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["guidance_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._coordination_index_path,
                artifact_kind="index",
                output_format="json",
                content=self._json_doc(documents["coordination_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._artifact_index_path,
                artifact_kind="index",
                output_format="json",
                content=artifact_document,
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=self._overview_path,
                artifact_kind="rendered_view",
                output_format="markdown",
                content=markdown_content(documents["plan_overview"]),
            ),
        )
        return outputs + tuple(
            RebuildOutput(
                relative_output_path=relative_path,
                artifact_kind="rendered_view",
                output_format="markdown",
                content=markdown_content(content),
            )
            for relative_path, content in sorted(initiative_views.items())
        )

    def _build_initiative_entry(
        self, snapshot: PlanInitiativeSnapshot
    ) -> InitiativeIndexEntry:
        initiative = snapshot.initiative_document
        trace_id = str(initiative["trace_id"])
        traceability_entry = self._traceability_entry(trace_id)
        active_task_summaries = tuple(
            self._build_active_task_summary(snapshot, task_document)
            for task_document in snapshot.task_documents
            if str(task_document["task_status"]) not in TERMINAL_TASK_STATUSES
        )
        active_task_ids = tuple(task.task_id for task in active_task_summaries)
        blocked_by_task_ids = tuple(
            sorted(
                {
                    blocker
                    for task in active_task_summaries
                    for blocker in task.blocked_by
                }
            )
        )
        readiness = self._build_readiness_entry(snapshot)
        current_phase = current_phase_for_snapshot(
            initiative=initiative,
            active_task_summaries=active_task_summaries,
            vocabulary=self._vocabulary,
        )
        return InitiativeIndexEntry(
            trace_id=trace_id,
            title=str(initiative["title"]),
            summary=str(initiative["summary"]),
            artifact_status="active",
            initiative_status=initiative_status(initiative, self._vocabulary),
            current_phase=current_phase,
            updated_at=snapshot_updated_at(snapshot),
            open_task_count=len(active_task_summaries),
            blocked_task_count=sum(
                1 for task in active_task_summaries if task.task_status == "blocked"
            ),
            key_surface_path=f"{snapshot.initiative_root}/plan.md",
            next_action=next_action(snapshot, readiness, self._vocabulary),
            next_surface_path=next_surface_path(snapshot, readiness),
            initiative_id=str(initiative["initiative_id"]),
            slug=str(initiative["slug"]),
            scope_type=str(initiative["scope_type"]),
            project_id=(
                str(initiative["project_id"])
                if initiative.get("project_id") is not None
                else None
            ),
            primary_owner=str(initiative["owner"]),
            active_owners=(str(initiative["owner"]),),
            active_task_ids=active_task_ids,
            active_task_summaries=active_task_summaries,
            blocked_by_task_ids=blocked_by_task_ids,
            source_surface_paths=(
                traceability_entry.source_surface_paths
                if traceability_entry is not None
                else ()
            ),
            governing_document_paths=effective_initiative_governing_document_paths(
                initiative,
                repo_root=self._loader.repo_root,
            ),
            task_ids=tuple(initiative["task_ids"]),
            acceptance_ids=(
                traceability_entry.acceptance_ids
                if traceability_entry is not None
                else ()
            ),
            acceptance_contract_ids=snapshot.acceptance_contract_ids,
            evidence_ids=ordered_unique_strings(
                (
                    *initiative["evidence_ids"],
                    *snapshot.trace_evidence_ids,
                    *(
                        traceability_entry.evidence_ids
                        if traceability_entry is not None
                        else ()
                    ),
                )
            ),
            related_paths=ordered_unique_strings(
                (
                    *(
                        str(record["path"])
                        for record in initiative["authored_inputs"]
                        if isinstance(record, dict)
                        and isinstance(record.get("path"), str)
                    ),
                    *(
                        traceability_entry.related_paths
                        if traceability_entry is not None
                        else ()
                    ),
                )
            ),
            closed_at=(
                str(initiative["closed_at"])
                if initiative.get("closed_at") is not None
                else None
            ),
            closure_reason=(
                str(initiative["closure_reason"])
                if initiative.get("closure_reason") is not None
                else None
            ),
            superseded_by_trace_id=(
                str(initiative["superseded_by_trace_id"])
                if initiative.get("superseded_by_trace_id") is not None
                else None
            ),
            tags=traceability_entry.tags if traceability_entry is not None else (),
            notes=traceability_entry.notes if traceability_entry is not None else None,
        )

    def _traceability_entry(self, trace_id: str) -> TraceabilityEntry | None:
        if self._traceability_entries_by_trace is None:
            self._traceability_entries_by_trace = {
                entry.trace_id: entry
                for entry in self._loader.load_traceability_index().entries
            }
        return self._traceability_entries_by_trace.get(trace_id)

    def _build_task_entries(
        self,
        snapshot: PlanInitiativeSnapshot,
    ) -> tuple[PlanTaskIndexEntry, ...]:
        initiative = snapshot.initiative_document
        return tuple(
            PlanTaskIndexEntry(
                task_id=str(task["task_id"]),
                initiative_id=str(initiative["initiative_id"]),
                project_id=(
                    str(initiative["project_id"])
                    if initiative.get("project_id") is not None
                    else None
                ),
                trace_id=str(initiative["trace_id"]),
                initiative_title=str(initiative["title"]),
                title=str(task["title"]),
                summary=str(task["summary"]),
                status=str(task["status"]),
                task_status=str(task["task_status"]),
                task_kind=str(task.get("task_kind", "feature")),
                priority=str(task["priority"]),
                owner=str(task["owner"]),
                doc_path=f"{snapshot.initiative_root}/.wt/tasks/{task['slug']}/task.json",
                updated_at=str(task["updated_at"]),
                blocked_by=tuple(task.get("blocker_task_ids", ())),
                depends_on=tuple(task.get("dependency_task_ids", ())),
                related_ids=tuple(task.get("related_ids", ())),
                applies_to=tuple(task.get("applies_to", ())),
                governing_document_paths=effective_task_governing_document_paths(
                    task,
                    initiative_document=initiative,
                    repo_root=self._loader.repo_root,
                ),
                github_repository=(
                    str(task["github_repository"])
                    if task.get("github_repository") is not None
                    else None
                ),
                github_issue_number=(
                    int(task["github_issue_number"])
                    if task.get("github_issue_number") is not None
                    else None
                ),
                github_issue_node_id=(
                    str(task["github_issue_node_id"])
                    if task.get("github_issue_node_id") is not None
                    else None
                ),
                github_project_owner=(
                    str(task["github_project_owner"])
                    if task.get("github_project_owner") is not None
                    else None
                ),
                github_project_owner_type=(
                    str(task["github_project_owner_type"])
                    if task.get("github_project_owner_type") is not None
                    else None
                ),
                github_project_number=(
                    int(task["github_project_number"])
                    if task.get("github_project_number") is not None
                    else None
                ),
                github_project_item_id=(
                    str(task["github_project_item_id"])
                    if task.get("github_project_item_id") is not None
                    else None
                ),
                github_synced_at=(
                    str(task["github_synced_at"])
                    if task.get("github_synced_at") is not None
                    else None
                ),
            )
            for task in snapshot.task_documents
        )

    def _build_readiness_entry(
        self, snapshot: PlanInitiativeSnapshot
    ) -> PlanReadinessIndexEntry:
        initiative = snapshot.initiative_document
        gate_state = initiative["gate_state"]
        return PlanReadinessIndexEntry(
            initiative_id=str(initiative["initiative_id"]),
            project_id=(
                str(initiative["project_id"])
                if initiative.get("project_id") is not None
                else None
            ),
            trace_id=str(initiative["trace_id"]),
            title=str(initiative["title"]),
            initiative_root=snapshot.initiative_root,
            lifecycle_stage=str(initiative["lifecycle_stage"]),
            review_status=str(initiative["review_status"]),
            capture_complete=bool(gate_state["capture_complete"]),
            machine_valid=bool(gate_state["machine_valid"]),
            approval_status=str(gate_state["approval_status"]),
            ready_for_execution=bool(gate_state["ready_for_execution"]),
            blocking_reasons=tuple(gate_state.get("blocking_reasons", ())),
            updated_at=snapshot_updated_at(snapshot),
            scope_type=str(initiative["scope_type"]),
        )

    def _build_discrepancy_entries(
        self,
        snapshot: PlanInitiativeSnapshot,
    ) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        initiative = snapshot.initiative_document
        terminal_statuses = {"resolved", "closed", "completed", "cancelled"}
        return tuple(
            PlanDiscrepancyIndexEntry(
                discrepancy_id=str(document["discrepancy_id"]),
                initiative_id=str(initiative["initiative_id"]),
                project_id=(
                    str(initiative["project_id"])
                    if initiative.get("project_id") is not None
                    else None
                ),
                trace_id=str(initiative["trace_id"]),
                title=str(initiative["title"]),
                category=str(document["category"]),
                severity=str(document["severity"]),
                gate_effect=str(document["gate_effect"]),
                status=str(document["status"]),
                summary=str(document["summary"]),
                source_paths=tuple(document.get("source_paths", ())),
                updated_at=str(document["updated_at"]),
            )
            for document in snapshot.discrepancy_documents
            if str(document.get("status", "")) not in terminal_statuses
        )

    def _build_evidence_entries(
        self,
        snapshot: PlanInitiativeSnapshot,
    ) -> tuple[PlanEvidenceIndexEntry, ...]:
        initiative = snapshot.initiative_document
        return tuple(
            PlanEvidenceIndexEntry(
                evidence_id=artifact.evidence_id,
                initiative_id=str(initiative["initiative_id"]),
                project_id=(
                    str(initiative["project_id"])
                    if initiative.get("project_id") is not None
                    else None
                ),
                trace_id=str(initiative["trace_id"]),
                initiative_title=str(initiative["title"]),
                title=artifact.title,
                status=artifact.status,
                initiative_root=snapshot.initiative_root,
                entry_count=artifact.entry_count,
                acceptance_labels=artifact.acceptance_labels,
                validation_types=artifact.validation_types,
                owners=artifact.owners,
                target_phases=artifact.target_phases,
                expected_output_paths=artifact.expected_output_paths,
                updated_at=artifact.updated_at,
            )
            for artifact in (
                self._evidence_bundles.artifact_from_document(document)
                for document in snapshot.evidence_documents
            )
        )

    def _build_closeout_entries(
        self,
        snapshot: PlanInitiativeSnapshot,
    ) -> tuple[PlanCloseoutIndexEntry, ...]:
        initiative = snapshot.initiative_document
        return tuple(
            PlanCloseoutIndexEntry(
                closeout_id=str(document["id"]),
                initiative_id=str(initiative["initiative_id"]),
                project_id=(
                    str(initiative["project_id"])
                    if initiative.get("project_id") is not None
                    else None
                ),
                trace_id=str(initiative["trace_id"]),
                initiative_title=str(initiative["title"]),
                title=str(document["title"]),
                status=str(document["status"]),
                initiative_root=snapshot.initiative_root,
                expected_outcome=str(document["expected_outcome"]),
                acceptance_ids=tuple(document["acceptance_ids"]),
                evidence_ids=tuple(document["evidence_ids"]),
                follow_up_handling=str(document["follow_up_handling"]),
                promotion_review_required=bool(document["promotion_review_required"]),
                terminal_state_options=tuple(document["terminal_state_options"]),
                terminal_state=(
                    str(document["terminal_state"])
                    if document.get("terminal_state") is not None
                    else None
                ),
                updated_at=str(document["updated_at"]),
            )
            for document in snapshot.closeout_documents
        )

    def _build_review_entries(
        self,
        snapshot: PlanInitiativeSnapshot,
    ) -> tuple[PlanReviewIndexEntry, ...]:
        initiative = snapshot.initiative_document
        initiative_entry = PlanReviewIndexEntry(
            review_subject_id=str(initiative["initiative_id"]),
            subject_kind="initiative",
            initiative_id=str(initiative["initiative_id"]),
            project_id=(
                str(initiative["project_id"])
                if initiative.get("project_id") is not None
                else None
            ),
            trace_id=str(initiative["trace_id"]),
            initiative_title=str(initiative["title"]),
            title=str(initiative["title"]),
            review_state=str(initiative["review_status"]),
            review_refs=ordered_unique_strings(
                approval["actor_id"] for approval in initiative.get("approvals", ())
            ),
            evidence_refs=ordered_unique_strings(initiative.get("evidence_ids", ())),
            updated_at=str(initiative["updated_at"]),
            lifecycle_stage=str(initiative["lifecycle_stage"]),
            ready_for_execution=bool(initiative["gate_state"]["ready_for_execution"]),
        )
        promotion_entries = tuple(
            PlanReviewIndexEntry(
                review_subject_id=str(document["id"]),
                subject_kind="promotion",
                initiative_id=str(initiative["initiative_id"]),
                project_id=(
                    str(initiative["project_id"])
                    if initiative.get("project_id") is not None
                    else None
                ),
                trace_id=str(initiative["trace_id"]),
                initiative_title=str(initiative["title"]),
                title=str(document["title"]),
                review_state=str(document.get("approval_state", "pending")),
                review_refs=ordered_unique_strings(
                    str(value)
                    for value in (
                        document.get("review_refs")
                        or [
                            candidate["review_path"]
                            for candidate in document.get("candidates", ())
                            if isinstance(candidate, dict)
                            and candidate.get("review_path") is not None
                        ]
                    )
                ),
                evidence_refs=ordered_unique_strings(
                    str(value)
                    for value in (
                        document.get("evidence_refs")
                        or initiative.get("evidence_ids", ())
                    )
                ),
                updated_at=str(document["updated_at"]),
            )
            for document in snapshot.promotion_documents
        )
        return (initiative_entry, *promotion_entries)

    def _build_promotion_entries(
        self,
        snapshot: PlanInitiativeSnapshot,
    ) -> tuple[PlanPromotionIndexEntry, ...]:
        initiative = snapshot.initiative_document
        return tuple(
            PlanPromotionIndexEntry(
                promotion_id=str(document["id"]),
                initiative_id=str(initiative["initiative_id"]),
                project_id=(
                    str(initiative["project_id"])
                    if initiative.get("project_id") is not None
                    else None
                ),
                trace_id=str(initiative["trace_id"]),
                initiative_title=str(initiative["title"]),
                title=str(document["title"]),
                status=str(document["status"]),
                initiative_root=snapshot.initiative_root,
                candidate_count=len(document["candidates"]),
                candidate_paths=tuple(
                    str(candidate["candidate_path"])
                    for candidate in document["candidates"]
                ),
                target_paths=tuple(
                    sorted(
                        {
                            str(candidate["target_path"])
                            for candidate in document["candidates"]
                            if candidate.get("target_path") is not None
                        }
                    )
                ),
                target_families=tuple(
                    sorted(
                        {
                            str(candidate["target_family"])
                            for candidate in document["candidates"]
                        }
                    )
                ),
                review_paths=tuple(
                    sorted(
                        {
                            str(candidate["review_path"])
                            for candidate in document["candidates"]
                        }
                    )
                ),
                updated_at=str(document["updated_at"]),
                approval_state=(
                    str(document["approval_state"])
                    if document.get("approval_state") is not None
                    else None
                ),
                evidence_refs=tuple(
                    str(reference) for reference in document.get("evidence_refs", ())
                ),
                provenance_expectations=tuple(
                    sorted(
                        {
                            str(candidate["provenance_expectation"])
                            for candidate in document["candidates"]
                        }
                    )
                ),
            )
            for document in snapshot.promotion_documents
        )

    def _build_guidance_entries(self) -> tuple[PlanGuidanceIndexEntry, ...]:
        entries: list[PlanGuidanceIndexEntry] = []
        docs_root = self._loader.repo_root / self._workspace_paths.docs_root
        if not docs_root.exists():
            return ()
        for path in sorted(docs_root.rglob("*.md")):
            if path.name in {"README.md", "AGENTS.md"}:
                continue
            relative_path = path.relative_to(self._loader.repo_root).as_posix()
            if relative_path.startswith(f"{self._workspace_paths.docs_root}/commands/"):
                continue
            try:
                front_matter = load_front_matter(path)
            except FrontMatterParseError as exc:
                raise ValueError(
                    f"{relative_path} must carry governed front matter for guidance indexing: {exc.message}"
                ) from exc
            guidance_id = front_matter.get("id")
            title = front_matter.get("title")
            summary = front_matter.get("summary")
            guidance_family = front_matter.get("type")
            status = front_matter.get("status")
            owner = front_matter.get("owner")
            updated_at = front_matter.get("updated_at")
            required_fields = {
                "id": guidance_id,
                "title": title,
                "summary": summary,
                "type": guidance_family,
                "status": status,
                "owner": owner,
                "updated_at": updated_at,
            }
            missing_fields = [
                field_name
                for field_name, value in required_fields.items()
                if not isinstance(value, str) or not value
            ]
            if missing_fields:
                joined = ", ".join(missing_fields)
                raise ValueError(
                    f"{relative_path} is missing required guidance-index front matter fields: {joined}"
                )
            entries.append(
                PlanGuidanceIndexEntry(
                    guidance_id=str(guidance_id),
                    title=str(title),
                    summary=str(summary),
                    guidance_family=str(guidance_family),
                    status=str(status),
                    owner=str(owner),
                    doc_path=relative_path,
                    updated_at=str(updated_at),
                    trace_id=(
                        str(front_matter["trace_id"])
                        if isinstance(front_matter.get("trace_id"), str)
                        and front_matter.get("trace_id")
                        else None
                    ),
                    audience=(
                        str(front_matter["audience"])
                        if isinstance(front_matter.get("audience"), str)
                        and front_matter.get("audience")
                        else None
                    ),
                    authority=(
                        str(front_matter["authority"])
                        if isinstance(front_matter.get("authority"), str)
                        and front_matter.get("authority")
                        else None
                    ),
                    tags=tuple(
                        value
                        for value in front_matter.get("tags", ())
                        if isinstance(value, str) and value
                    ),
                    applies_to=tuple(
                        value
                        for value in front_matter.get("applies_to", ())
                        if isinstance(value, str) and value
                    ),
                )
            )
        return tuple(entries)

    def _build_active_task_summary(
        self,
        snapshot: PlanInitiativeSnapshot,
        task_document: dict[str, Any],
    ) -> InitiativeActiveTaskSummary:
        unresolved_dependencies = tuple(
            dependency
            for dependency in task_document.get("dependency_task_ids", ())
            if task_status_for_id(snapshot.task_documents, str(dependency))
            not in TERMINAL_TASK_STATUSES
        )
        unresolved_blockers = tuple(
            blocker
            for blocker in task_document.get("blocker_task_ids", ())
            if task_status_for_id(snapshot.task_documents, str(blocker))
            not in TERMINAL_TASK_STATUSES
        )
        local_status = str(task_document["task_status"])
        is_actionable = (
            local_status == "ready"
            and not unresolved_dependencies
            and not unresolved_blockers
        )
        return InitiativeActiveTaskSummary(
            task_id=str(task_document["task_id"]),
            title=str(task_document["title"]),
            task_status=self._vocabulary.surface_task_status(local_status),
            priority=str(task_document["priority"]),
            owner=str(task_document["owner"]),
            doc_path=f"{snapshot.initiative_root}/.wt/tasks/{task_document['slug']}/task.json",
            is_actionable=is_actionable,
            blocked_by=unresolved_blockers,
            depends_on=unresolved_dependencies,
        )

    def _build_coordination_document(
        self,
        entries: tuple[InitiativeIndexEntry, ...],
    ) -> dict[str, object]:
        active_entries = tuple(
            entry for entry in entries if entry.initiative_status == "active"
        )
        actionable_tasks = tuple(
            sorted(
                (
                    CoordinationTaskSummary(
                        trace_id=entry.trace_id,
                        initiative_title=entry.title,
                        task_id=task.task_id,
                        title=task.title,
                        task_status=task.task_status,
                        priority=task.priority,
                        owner=task.owner,
                        doc_path=task.doc_path,
                        is_actionable=task.is_actionable,
                        blocked_by=task.blocked_by,
                        depends_on=task.depends_on,
                    )
                    for entry in active_entries
                    for task in entry.active_task_summaries
                    if task.is_actionable
                ),
                key=lambda item: (
                    task_status_order(item.task_status),
                    PRIORITY_ORDER.get(item.priority, 99),
                    item.trace_id,
                    item.task_id,
                ),
            )
        )
        recent_closed = tuple(
            sorted(
                (
                    CoordinationRecentInitiativeSummary(
                        trace_id=entry.trace_id,
                        title=entry.title,
                        initiative_status=entry.initiative_status,
                        closed_at=entry.closed_at or entry.updated_at,
                        key_surface_path=entry.key_surface_path,
                        closure_reason=entry.closure_reason,
                    )
                    for entry in entries
                    if entry.initiative_status != "active"
                ),
                key=lambda entry: (
                    entry.closed_at,
                    entry.trace_id,
                ),
                reverse=True,
            )
        )[:10]
        if not active_entries:
            summary = "No active plan-workspace initiatives exist."
            next_action_value = (
                "Bootstrap a new initiative package before starting execution."
            )
            surface_path = self._overview_path
            coordination_mode = "ready_for_bootstrap"
        else:
            focus_entry = sorted(
                active_entries,
                key=lambda entry: (
                    0
                    if any(task.is_actionable for task in entry.active_task_summaries)
                    else 1,
                    PHASE_ORDER.get(entry.current_phase, 99),
                    entry.trace_id,
                ),
            )[0]
            coordination_mode = (
                "blocked_work"
                if not actionable_tasks
                and any(entry.blocked_task_count > 0 for entry in active_entries)
                else "active_work"
            )
            summary = "Active plan-workspace initiatives exist and the coordination surface points to the current pack-wide next work."
            next_action_value = focus_entry.next_action
            surface_path = focus_entry.next_surface_path
        return {
            "$schema": "urn:watchtower:schema:artifacts:indexes:coordination-index:v1",
            "id": "index.coordination",
            "title": "Plan Workspace Coordination Index",
            "status": "active",
            "updated_at": latest_timestamp(entry.updated_at for entry in entries),
            "coordination_mode": coordination_mode,
            "summary": summary,
            "recommended_next_action": next_action_value,
            "recommended_surface_path": surface_path,
            "active_initiative_count": len(active_entries),
            "blocked_task_count": sum(
                entry.blocked_task_count for entry in active_entries
            ),
            "actionable_task_count": len(actionable_tasks),
            "entries": [
                serialize_initiative_entry(entry, compact=True)
                for entry in active_entries
            ],
            "actionable_tasks": [
                {
                    "trace_id": task.trace_id,
                    "initiative_title": task.initiative_title,
                    "task_id": task.task_id,
                    "title": task.title,
                    "task_status": task.task_status,
                    "priority": task.priority,
                    "owner": task.owner,
                    "doc_path": task.doc_path,
                    "is_actionable": task.is_actionable,
                    **(
                        {"blocked_by": list(task.blocked_by)} if task.blocked_by else {}
                    ),
                    **(
                        {"depends_on": list(task.depends_on)} if task.depends_on else {}
                    ),
                }
                for task in actionable_tasks
            ],
            "recent_closed_initiatives": [
                {
                    "trace_id": entry.trace_id,
                    "title": entry.title,
                    "initiative_status": entry.initiative_status,
                    "closed_at": entry.closed_at,
                    "key_surface_path": entry.key_surface_path,
                    **(
                        {"closure_reason": entry.closure_reason}
                        if entry.closure_reason
                        else {}
                    ),
                }
                for entry in recent_closed
            ],
        }

    def _serialize_task_entry(self, entry: PlanTaskIndexEntry) -> dict[str, object]:
        payload: dict[str, object] = {
            "task_id": entry.task_id,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "initiative_title": entry.initiative_title,
            "title": entry.title,
            "summary": entry.summary,
            "status": entry.status,
            "task_status": entry.task_status,
            "task_kind": entry.task_kind,
            "priority": entry.priority,
            "owner": entry.owner,
            "doc_path": entry.doc_path,
            "updated_at": entry.updated_at,
        }
        if entry.project_id is not None:
            payload["project_id"] = entry.project_id
        if entry.blocked_by:
            payload["blocked_by"] = list(entry.blocked_by)
        if entry.depends_on:
            payload["depends_on"] = list(entry.depends_on)
        if entry.related_ids:
            payload["related_ids"] = list(entry.related_ids)
        if entry.applies_to:
            payload["applies_to"] = list(entry.applies_to)
        if entry.governing_document_paths:
            payload["governing_document_paths"] = list(entry.governing_document_paths)
        if entry.github_repository is not None:
            payload["github_repository"] = entry.github_repository
        if entry.github_issue_number is not None:
            payload["github_issue_number"] = entry.github_issue_number
        if entry.github_issue_node_id is not None:
            payload["github_issue_node_id"] = entry.github_issue_node_id
        if entry.github_project_owner is not None:
            payload["github_project_owner"] = entry.github_project_owner
        if entry.github_project_owner_type is not None:
            payload["github_project_owner_type"] = entry.github_project_owner_type
        if entry.github_project_number is not None:
            payload["github_project_number"] = entry.github_project_number
        if entry.github_project_item_id is not None:
            payload["github_project_item_id"] = entry.github_project_item_id
        if entry.github_synced_at is not None:
            payload["github_synced_at"] = entry.github_synced_at
        return payload

    def _serialize_readiness_entry(
        self, entry: PlanReadinessIndexEntry
    ) -> dict[str, object]:
        return {
            "initiative_id": entry.initiative_id,
            **(
                {"project_id": entry.project_id} if entry.project_id is not None else {}
            ),
            "trace_id": entry.trace_id,
            "title": entry.title,
            "initiative_root": entry.initiative_root,
            "scope_type": entry.scope_type,
            "lifecycle_stage": entry.lifecycle_stage,
            "review_status": entry.review_status,
            "capture_complete": entry.capture_complete,
            "machine_valid": entry.machine_valid,
            "approval_status": entry.approval_status,
            "ready_for_execution": entry.ready_for_execution,
            "blocking_reasons": list(entry.blocking_reasons),
            "updated_at": entry.updated_at,
        }

    def _serialize_discrepancy_entry(
        self, entry: PlanDiscrepancyIndexEntry
    ) -> dict[str, object]:
        return {
            "discrepancy_id": entry.discrepancy_id,
            "initiative_id": entry.initiative_id,
            **(
                {"project_id": entry.project_id} if entry.project_id is not None else {}
            ),
            "trace_id": entry.trace_id,
            "title": entry.title,
            "category": entry.category,
            "severity": entry.severity,
            "gate_effect": entry.gate_effect,
            "status": entry.status,
            "summary": entry.summary,
            "source_paths": list(entry.source_paths),
            "updated_at": entry.updated_at,
        }

    def _serialize_evidence_entry(
        self, entry: PlanEvidenceIndexEntry
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "evidence_id": entry.evidence_id,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "initiative_title": entry.initiative_title,
            "title": entry.title,
            "status": entry.status,
            "initiative_root": entry.initiative_root,
            "entry_count": entry.entry_count,
            "acceptance_labels": list(entry.acceptance_labels),
            "validation_types": list(entry.validation_types),
            "owners": list(entry.owners),
            "target_phases": list(entry.target_phases),
            "expected_output_paths": list(entry.expected_output_paths),
            "updated_at": entry.updated_at,
        }
        if entry.project_id is not None:
            payload["project_id"] = entry.project_id
        return payload

    def _serialize_closeout_entry(
        self, entry: PlanCloseoutIndexEntry
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "closeout_id": entry.closeout_id,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "initiative_title": entry.initiative_title,
            "title": entry.title,
            "status": entry.status,
            "initiative_root": entry.initiative_root,
            "expected_outcome": entry.expected_outcome,
            "acceptance_ids": list(entry.acceptance_ids),
            "evidence_ids": list(entry.evidence_ids),
            "follow_up_handling": entry.follow_up_handling,
            "promotion_review_required": entry.promotion_review_required,
            "terminal_state_options": list(entry.terminal_state_options),
            "updated_at": entry.updated_at,
        }
        if entry.project_id is not None:
            payload["project_id"] = entry.project_id
        if entry.terminal_state is not None:
            payload["terminal_state"] = entry.terminal_state
        return payload

    def _serialize_review_entry(self, entry: PlanReviewIndexEntry) -> dict[str, object]:
        payload: dict[str, object] = {
            "review_subject_id": entry.review_subject_id,
            "subject_kind": entry.subject_kind,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "initiative_title": entry.initiative_title,
            "title": entry.title,
            "review_state": entry.review_state,
            "review_refs": list(entry.review_refs),
            "evidence_refs": list(entry.evidence_refs),
            "updated_at": entry.updated_at,
        }
        if entry.project_id is not None:
            payload["project_id"] = entry.project_id
        if entry.lifecycle_stage is not None:
            payload["lifecycle_stage"] = entry.lifecycle_stage
        if entry.ready_for_execution is not None:
            payload["ready_for_execution"] = entry.ready_for_execution
        return payload

    def _serialize_promotion_entry(
        self, entry: PlanPromotionIndexEntry
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "promotion_id": entry.promotion_id,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "initiative_title": entry.initiative_title,
            "title": entry.title,
            "status": entry.status,
            "initiative_root": entry.initiative_root,
            "candidate_count": entry.candidate_count,
            "candidate_paths": list(entry.candidate_paths),
            "target_families": list(entry.target_families),
            "review_paths": list(entry.review_paths),
            "updated_at": entry.updated_at,
        }
        if entry.project_id is not None:
            payload["project_id"] = entry.project_id
        if entry.target_paths:
            payload["target_paths"] = list(entry.target_paths)
        if entry.approval_state is not None:
            payload["approval_state"] = entry.approval_state
        if entry.evidence_refs:
            payload["evidence_refs"] = list(entry.evidence_refs)
        if entry.provenance_expectations:
            payload["provenance_expectations"] = list(entry.provenance_expectations)
        return payload

    def _serialize_guidance_entry(
        self, entry: PlanGuidanceIndexEntry
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "guidance_id": entry.guidance_id,
            "title": entry.title,
            "summary": entry.summary,
            "guidance_family": entry.guidance_family,
            "status": entry.status,
            "owner": entry.owner,
            "doc_path": entry.doc_path,
            "updated_at": entry.updated_at,
        }
        if entry.trace_id is not None:
            payload["trace_id"] = entry.trace_id
        if entry.audience is not None:
            payload["audience"] = entry.audience
        if entry.authority is not None:
            payload["authority"] = entry.authority
        if entry.tags:
            payload["tags"] = list(entry.tags)
        if entry.applies_to:
            payload["applies_to"] = list(entry.applies_to)
        return payload

    @staticmethod
    def _json_doc(value: object) -> dict[str, object]:
        return json_document(value)


__all__ = ["PlanWorkspaceDocumentBuilder"]
