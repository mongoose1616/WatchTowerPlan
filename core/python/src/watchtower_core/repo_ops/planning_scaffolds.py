"""Template-aligned planning scaffold helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from watchtower_core.adapters import render_front_matter
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.evidence.validation_evidence import (
    VALIDATION_EVIDENCE_DIRECTORY,
    VALIDATION_EVIDENCE_SCHEMA_ID,
)
from watchtower_core.repo_ops.front_matter_paths import normalize_governed_applies_to_values
from watchtower_core.repo_ops.planning_scaffold_support import (
    PLAN_KIND_CHOICES as _PLAN_KIND_CHOICES,
)
from watchtower_core.repo_ops.planning_scaffold_support import (
    PlanKind,
    RenderedDocument,
    compact_front_matter,
    default_authority_for_kind,
    default_status_for_kind,
    ensure_available_path,
    id_label_for_kind,
    normalize_choice,
    normalize_list,
    normalize_plan_kind,
    normalize_required_string,
    ordered_front_matter,
    render_document_content,
    render_sections,
    scaffold_directory_for_kind,
    scaffold_schema_for_kind,
    scaffold_type_for_kind,
    slugify_file_stem,
    status_label_for_kind,
    trace_suffix,
    validate_rendered_document,
)
from watchtower_core.repo_ops.sync.coordination import CoordinationSyncService
from watchtower_core.repo_ops.sync.decision_index import DecisionIndexSyncService
from watchtower_core.repo_ops.sync.decision_tracking import DecisionTrackingSyncService
from watchtower_core.repo_ops.sync.design_document_index import DesignDocumentIndexSyncService
from watchtower_core.repo_ops.sync.design_tracking import DesignTrackingSyncService
from watchtower_core.repo_ops.sync.prd_index import PrdIndexSyncService
from watchtower_core.repo_ops.sync.prd_tracking import PrdTrackingSyncService
from watchtower_core.repo_ops.task_lifecycle import (
    TASK_KIND_CHOICES,
    TASK_PRIORITY_CHOICES,
    TaskCreateParams,
    TaskLifecycleService,
    TaskMutationResult,
)
from watchtower_core.utils import utc_timestamp_now

PLAN_KIND_CHOICES = _PLAN_KIND_CHOICES
ACCEPTANCE_CONTRACT_SCHEMA_ID = (
    "urn:watchtower:schema:artifacts:contracts:acceptance-contract:v1"
)
ACCEPTANCE_CONTRACT_DIRECTORY = "core/control_plane/contracts/acceptance"
BOOTSTRAP_VALIDATION_EVIDENCE_VALIDATOR_ID = "validator.control_plane.validation_evidence"


@dataclass(frozen=True, slots=True)
class PlanScaffoldParams:
    """Inputs for one planning-document scaffold."""

    kind: PlanKind
    trace_id: str
    document_id: str
    title: str
    summary: str
    owner: str = "repository_maintainer"
    status: str | None = None
    applies_to: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    file_stem: str | None = None
    linked_prd_ids: tuple[str, ...] = ()
    linked_decision_ids: tuple[str, ...] = ()
    linked_design_ids: tuple[str, ...] = ()
    linked_plan_ids: tuple[str, ...] = ()
    linked_acceptance_ids: tuple[str, ...] = ()
    source_requests: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class PlanBootstrapParams:
    """Inputs for one initiative bootstrap scaffold."""

    trace_id: str
    title: str
    summary: str
    owner: str = "repository_maintainer"
    applies_to: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    file_stem: str | None = None
    include_decision: bool = False
    decision_id: str | None = None
    source_requests: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    task_id: str | None = None
    task_owner: str | None = None
    task_kind: str = "governance"
    task_priority: str = "medium"
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class ScaffoldDocumentResult:
    """Rendered result for one planning-document scaffold."""

    kind: PlanKind
    document_id: str
    trace_id: str
    title: str
    summary: str
    status: str
    doc_path: str
    content: str
    wrote: bool


@dataclass(frozen=True, slots=True)
class AcceptanceContractResult:
    """Rendered result for one bootstrap acceptance contract artifact."""

    contract_id: str
    trace_id: str
    source_prd_id: str
    title: str
    doc_path: str
    content: str
    wrote: bool


@dataclass(frozen=True, slots=True)
class ValidationEvidenceResult:
    """Rendered result for one bootstrap validation-evidence artifact."""

    evidence_id: str
    trace_id: str
    title: str
    overall_result: str
    doc_path: str
    content: str
    wrote: bool


@dataclass(frozen=True, slots=True)
class PlanBootstrapResult:
    """Result summary for one initiative bootstrap scaffold."""

    documents: tuple[ScaffoldDocumentResult, ...]
    acceptance_contract: AcceptanceContractResult
    validation_evidence: ValidationEvidenceResult
    task_result: TaskMutationResult
    wrote: bool
    sync_refreshed: bool


class PlanningScaffoldService:
    """Render compact planning scaffolds aligned with current repository templates."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def scaffold(self, params: PlanScaffoldParams, *, write: bool) -> ScaffoldDocumentResult:
        rendered = self._render_scaffold(params)
        if write:
            self._write_rendered_document(rendered)
            self._refresh_planning_surfaces(kind=rendered.kind)
            if self._trace_participates_in_coordination(rendered.trace_id):
                CoordinationSyncService(self._loader).run(write=True)
        return _scaffold_result_from_rendered(rendered, wrote=write)

    def bootstrap(self, params: PlanBootstrapParams, *, write: bool) -> PlanBootstrapResult:
        updated_at = params.updated_at or utc_timestamp_now()
        trace_id_suffix = trace_suffix(params.trace_id)
        base_stem = params.file_stem or params.title
        prd_id = f"prd.{trace_id_suffix}"
        design_id = f"design.features.{trace_id_suffix}"
        implementation_id = f"design.implementation.{trace_id_suffix}"
        decision_id = params.decision_id or f"decision.{trace_id_suffix}_direction"
        task_id = params.task_id or f"task.{trace_id_suffix}.bootstrap.001"
        contract_id = f"contract.acceptance.{trace_id_suffix}"
        evidence_id = f"evidence.{trace_id_suffix}.planning_baseline"

        rendered_documents = self._bootstrap_documents(
            params,
            updated_at=updated_at,
            base_stem=base_stem,
            prd_id=prd_id,
            design_id=design_id,
            implementation_id=implementation_id,
            decision_id=decision_id,
        )
        preview_task_result = self._bootstrap_task_result(
            params,
            updated_at=updated_at,
            base_stem=base_stem,
            task_id=task_id,
            related_ids=tuple(document.document_id for document in rendered_documents)
            + (contract_id,),
            write=False,
        )
        acceptance_contract_document, acceptance_contract_preview = (
            self._bootstrap_acceptance_contract_artifact(
                params,
                updated_at=updated_at,
                trace_id_suffix=trace_id_suffix,
                prd_id=prd_id,
                rendered_documents=tuple(rendered_documents),
                task_doc_path=preview_task_result.doc_path,
                contract_id=contract_id,
            )
        )
        validation_evidence_document, validation_evidence_preview = (
            self._bootstrap_validation_evidence_artifact(
                params,
                updated_at=updated_at,
                trace_id_suffix=trace_id_suffix,
                prd_id=prd_id,
                design_id=design_id,
                implementation_id=implementation_id,
                decision_id=(decision_id if params.include_decision else None),
                task_id=task_id,
                task_doc_path=preview_task_result.doc_path,
                contract_id=contract_id,
                contract_doc_path=acceptance_contract_preview.doc_path,
                evidence_id=evidence_id,
                rendered_documents=tuple(rendered_documents),
            )
        )

        task_result = preview_task_result
        if write:
            for rendered in rendered_documents:
                self._write_rendered_document(rendered)
            self._refresh_bootstrap_document_surfaces(include_decision=params.include_decision)
            self._write_json_artifact(
                acceptance_contract_preview.doc_path,
                acceptance_contract_document,
            )
            task_result = self._bootstrap_task_result(
                params,
                updated_at=updated_at,
                base_stem=base_stem,
                task_id=task_id,
                related_ids=tuple(document.document_id for document in rendered_documents)
                + (contract_id,),
                write=True,
            )
            self._write_json_artifact(
                validation_evidence_preview.doc_path,
                validation_evidence_document,
            )
            CoordinationSyncService(self._loader).run(write=True)

        return PlanBootstrapResult(
            documents=tuple(
                _scaffold_result_from_rendered(rendered, wrote=write)
                for rendered in rendered_documents
            ),
            acceptance_contract=_acceptance_contract_result_from_preview(
                acceptance_contract_preview,
                wrote=write,
            ),
            validation_evidence=_validation_evidence_result_from_preview(
                validation_evidence_preview,
                wrote=write,
            ),
            task_result=TaskMutationResult(
                task_id=task_result.task_id,
                title=task_result.title,
                summary=task_result.summary,
                trace_id=task_result.trace_id,
                task_status=task_result.task_status,
                task_kind=task_result.task_kind,
                priority=task_result.priority,
                owner=task_result.owner,
                updated_at=task_result.updated_at,
                doc_path=task_result.doc_path,
                previous_doc_path=task_result.previous_doc_path,
                moved=task_result.moved,
                changed=task_result.changed,
                wrote=write,
                coordination_refreshed=write,
                closeout_recommended=task_result.closeout_recommended,
            ),
            wrote=write,
            sync_refreshed=write,
        )

    def _render_scaffold(self, params: PlanScaffoldParams) -> RenderedDocument:
        kind = normalize_plan_kind(params.kind)
        updated_at = params.updated_at or utc_timestamp_now()
        applies_to = normalize_governed_applies_to_values(
            params.applies_to,
            origin=f"{kind} scaffold applies_to",
            repo_root=self._loader.repo_root,
        )
        front_matter = compact_front_matter(
            {
                "trace_id": normalize_required_string(params.trace_id, label="trace_id"),
                "id": normalize_required_string(params.document_id, label="document_id"),
                "title": normalize_required_string(params.title, label="title"),
                "summary": normalize_required_string(params.summary, label="summary"),
                "type": scaffold_type_for_kind(kind),
                "status": normalize_required_string(
                    params.status or default_status_for_kind(kind),
                    label="status",
                ),
                "owner": normalize_required_string(params.owner, label="owner"),
                "updated_at": updated_at,
                "audience": "shared",
                "authority": default_authority_for_kind(kind),
                "applies_to": applies_to,
                "aliases": normalize_list(params.aliases),
            }
        )
        doc_path = (
            f"{scaffold_directory_for_kind(kind)}/"
            f"{slugify_file_stem(params.file_stem or params.title)}.md"
        )
        ensure_available_path(self._loader, doc_path)
        sections = render_sections(kind, front_matter, params)
        content = render_document_content(front_matter["title"], sections)
        rendered = RenderedDocument(
            kind=kind,
            document_id=str(front_matter["id"]),
            trace_id=str(front_matter["trace_id"]),
            title=str(front_matter["title"]),
            summary=str(front_matter["summary"]),
            status=str(front_matter["status"]),
            schema_id=scaffold_schema_for_kind(kind),
            id_label=id_label_for_kind(kind),
            status_label=status_label_for_kind(kind),
            doc_path=doc_path,
            front_matter=front_matter,
            sections=sections,
            content=content,
        )
        validate_rendered_document(self._loader, rendered)
        return rendered

    def _bootstrap_documents(
        self,
        params: PlanBootstrapParams,
        *,
        updated_at: str,
        base_stem: str,
        prd_id: str,
        design_id: str,
        implementation_id: str,
        decision_id: str,
    ) -> list[RenderedDocument]:
        rendered_documents = [
            self._render_scaffold(
                PlanScaffoldParams(
                    kind="prd",
                    trace_id=params.trace_id,
                    document_id=prd_id,
                    title=f"{params.title} PRD",
                    summary=params.summary,
                    owner=params.owner,
                    applies_to=params.applies_to,
                    aliases=params.aliases,
                    file_stem=base_stem,
                    linked_decision_ids=((decision_id,) if params.include_decision else ()),
                    linked_design_ids=(design_id,),
                    linked_plan_ids=(implementation_id,),
                    references=params.references,
                    updated_at=updated_at,
                )
            ),
            self._render_scaffold(
                PlanScaffoldParams(
                    kind="feature-design",
                    trace_id=params.trace_id,
                    document_id=design_id,
                    title=f"{params.title} Feature Design",
                    summary=f"Defines the technical design boundary for {params.title}.",
                    owner=params.owner,
                    applies_to=params.applies_to,
                    aliases=params.aliases,
                    file_stem=base_stem,
                    linked_prd_ids=(prd_id,),
                    linked_decision_ids=((decision_id,) if params.include_decision else ()),
                    linked_plan_ids=(implementation_id,),
                    source_requests=params.source_requests,
                    references=params.references,
                    updated_at=updated_at,
                )
            ),
            self._render_scaffold(
                PlanScaffoldParams(
                    kind="implementation-plan",
                    trace_id=params.trace_id,
                    document_id=implementation_id,
                    title=f"{params.title} Implementation Plan",
                    summary=f"Breaks {params.title} into a bounded implementation slice.",
                    owner=params.owner,
                    applies_to=params.applies_to,
                    aliases=params.aliases,
                    file_stem=base_stem,
                    linked_prd_ids=(prd_id,),
                    linked_decision_ids=((decision_id,) if params.include_decision else ()),
                    linked_design_ids=(design_id,),
                    source_requests=params.source_requests,
                    references=params.references,
                    updated_at=updated_at,
                )
            ),
        ]
        if params.include_decision:
            rendered_documents.append(
                self._render_scaffold(
                    PlanScaffoldParams(
                        kind="decision",
                        trace_id=params.trace_id,
                        document_id=decision_id,
                        title=f"{params.title} Direction Decision",
                        summary=f"Records the initial direction decision for {params.title}.",
                        owner=params.owner,
                        applies_to=params.applies_to,
                        aliases=params.aliases,
                        file_stem=f"{base_stem}_direction",
                        linked_prd_ids=(prd_id,),
                        linked_design_ids=(design_id,),
                        linked_plan_ids=(implementation_id,),
                        source_requests=params.source_requests,
                        references=params.references,
                        updated_at=updated_at,
                    )
                )
            )
        return rendered_documents

    def _bootstrap_task_result(
        self,
        params: PlanBootstrapParams,
        *,
        updated_at: str,
        base_stem: str,
        task_id: str,
        related_ids: tuple[str, ...],
        write: bool,
    ) -> TaskMutationResult:
        return TaskLifecycleService(self._loader).create(
            TaskCreateParams(
                task_id=task_id,
                trace_id=params.trace_id,
                title=f"Bootstrap {params.title} planning chain",
                summary=f"Bootstraps the initial planning chain for {params.title}.",
                task_kind=normalize_choice(
                    params.task_kind,
                    TASK_KIND_CHOICES,
                    label="task_kind",
                ),
                priority=normalize_choice(
                    params.task_priority,
                    TASK_PRIORITY_CHOICES,
                    label="task_priority",
                ),
                owner=params.task_owner or params.owner,
                scope_items=(
                    "Publish the initial PRD, feature design, and implementation plan chain.",
                    "Publish the matching acceptance contract and planning-baseline evidence.",
                    "Establish the first tracked task for the initiative.",
                ),
                done_when_items=(
                    "The planning chain exists under canonical planning paths.",
                    (
                        "The acceptance contract and planning-baseline evidence exist "
                        "under canonical control-plane paths."
                    ),
                    "The bootstrap task is visible through the derived coordination surfaces.",
                ),
                applies_to=params.applies_to,
                related_ids=related_ids,
                file_stem=f"{slugify_file_stem(base_stem)}_bootstrap",
                updated_at=updated_at,
            ),
            write=write,
        )

    def _write_rendered_document(self, rendered: RenderedDocument) -> None:
        path = self._loader.repo_root / rendered.doc_path
        path.parent.mkdir(parents=True, exist_ok=True)
        rendered_front_matter = render_front_matter(ordered_front_matter(rendered.front_matter))
        path.write_text(
            f"---\n{rendered_front_matter}\n---\n\n{rendered.content}",
            encoding="utf-8",
        )

    def _write_json_artifact(
        self,
        relative_path: str,
        document: dict[str, object],
    ) -> None:
        self._loader.artifact_store.write_json_object(relative_path, document)

    def _refresh_planning_surfaces(self, *, kind: PlanKind) -> None:
        if kind == "prd":
            self._write_index_and_tracker(
                index_service=PrdIndexSyncService(self._loader),
                tracking_service=PrdTrackingSyncService(self._loader),
            )
        elif kind in {"feature-design", "implementation-plan"}:
            self._write_index_and_tracker(
                index_service=DesignDocumentIndexSyncService(self._loader),
                tracking_service=DesignTrackingSyncService(self._loader),
            )
        else:
            self._write_index_and_tracker(
                index_service=DecisionIndexSyncService(self._loader),
                tracking_service=DecisionTrackingSyncService(self._loader),
            )

    def _refresh_bootstrap_document_surfaces(self, *, include_decision: bool) -> None:
        self._write_index_and_tracker(
            index_service=PrdIndexSyncService(self._loader),
            tracking_service=PrdTrackingSyncService(self._loader),
        )
        self._write_index_and_tracker(
            index_service=DesignDocumentIndexSyncService(self._loader),
            tracking_service=DesignTrackingSyncService(self._loader),
        )
        if include_decision:
            self._write_index_and_tracker(
                index_service=DecisionIndexSyncService(self._loader),
                tracking_service=DecisionTrackingSyncService(self._loader),
            )

    def _bootstrap_acceptance_contract_artifact(
        self,
        params: PlanBootstrapParams,
        *,
        updated_at: str,
        trace_id_suffix: str,
        prd_id: str,
        rendered_documents: tuple[RenderedDocument, ...],
        task_doc_path: str,
        contract_id: str,
    ) -> tuple[dict[str, object], AcceptanceContractResult]:
        doc_path = (
            f"{ACCEPTANCE_CONTRACT_DIRECTORY}/{trace_id_suffix}_acceptance.v1.json"
        )
        ensure_available_path(self._loader, doc_path)
        document: dict[str, object] = {
            "$schema": ACCEPTANCE_CONTRACT_SCHEMA_ID,
            "id": contract_id,
            "title": f"{params.title} Acceptance Contract",
            "status": "active",
            "trace_id": params.trace_id,
            "source_prd_id": prd_id,
            "entries": [
                {
                    "acceptance_id": f"ac.{trace_id_suffix}.001",
                    "summary": (
                        "The bootstrap flow publishes the initial PRD, feature design, "
                        "implementation plan, acceptance contract, planning-baseline "
                        "evidence, and bootstrap task for the trace."
                    ),
                    "source_requirement_ids": [f"req.{trace_id_suffix}.001"],
                    "validation_targets": [
                        *(document.doc_path for document in rendered_documents),
                        task_doc_path,
                    ],
                    "related_paths": [
                        "docs/planning/prds/prd_tracking.md",
                        "docs/planning/design/design_tracking.md",
                        "docs/planning/tasks/task_tracking.md",
                        "docs/planning/initiatives/initiative_tracking.md",
                        "docs/planning/coordination_tracking.md",
                    ],
                    "notes": (
                        f"Bootstrap baseline contract prepared at {updated_at} for "
                        f"{params.trace_id}."
                    ),
                }
            ],
        }
        self._loader.schema_store.validate_instance(
            document,
            schema_id=ACCEPTANCE_CONTRACT_SCHEMA_ID,
        )
        return document, AcceptanceContractResult(
            contract_id=contract_id,
            trace_id=params.trace_id,
            source_prd_id=prd_id,
            title=str(document["title"]),
            doc_path=doc_path,
            content=f"{json.dumps(document, indent=2)}\n",
            wrote=False,
        )

    def _bootstrap_validation_evidence_artifact(
        self,
        params: PlanBootstrapParams,
        *,
        updated_at: str,
        trace_id_suffix: str,
        prd_id: str,
        design_id: str,
        implementation_id: str,
        decision_id: str | None,
        task_id: str,
        task_doc_path: str,
        contract_id: str,
        contract_doc_path: str,
        evidence_id: str,
        rendered_documents: tuple[RenderedDocument, ...],
    ) -> tuple[dict[str, object], ValidationEvidenceResult]:
        doc_path = (
            f"{VALIDATION_EVIDENCE_DIRECTORY}/{trace_id_suffix}_planning_baseline.v1.json"
        )
        ensure_available_path(self._loader, doc_path)
        subject_paths = [
            *(document.doc_path for document in rendered_documents),
            contract_doc_path,
        ]
        if task_doc_path not in subject_paths:
            subject_paths.append(task_doc_path)
        subject_ids = [prd_id, design_id, implementation_id, task_id, contract_id]
        if decision_id is not None:
            subject_ids.append(decision_id)
        document: dict[str, object] = {
            "$schema": VALIDATION_EVIDENCE_SCHEMA_ID,
            "id": evidence_id,
            "title": f"{params.title} Planning Baseline Evidence",
            "status": "active",
            "trace_id": params.trace_id,
            "overall_result": "passed",
            "recorded_at": updated_at,
            "source_prd_ids": [prd_id],
            "source_design_ids": [design_id],
            "source_plan_ids": [implementation_id],
            "source_acceptance_contract_ids": [contract_id],
            "checks": [
                {
                    "check_id": f"check.{trace_id_suffix}.planning_baseline",
                    "title": "Bootstrap planning baseline is aligned",
                    "result": "passed",
                    "subject_paths": subject_paths,
                    "subject_ids": subject_ids,
                    "validator_id": BOOTSTRAP_VALIDATION_EVIDENCE_VALIDATOR_ID,
                    "acceptance_ids": [f"ac.{trace_id_suffix}.001"],
                    "notes": (
                        "Bootstrap write mode published the initial planning chain, "
                        "acceptance contract, evidence artifact, and bootstrap task "
                        "in canonical repository paths."
                    ),
                }
            ],
            "related_paths": [
                contract_doc_path,
                "docs/planning/coordination_tracking.md",
                "docs/planning/initiatives/initiative_tracking.md",
                "docs/planning/tasks/task_tracking.md",
            ],
            "notes": (
                f"Planning baseline evidence prepared at {updated_at} for "
                f"{params.trace_id}."
            ),
        }
        if decision_id is not None:
            document["source_decision_ids"] = [decision_id]
        self._loader.schema_store.validate_instance(
            document,
            schema_id=VALIDATION_EVIDENCE_SCHEMA_ID,
        )
        return document, ValidationEvidenceResult(
            evidence_id=evidence_id,
            trace_id=params.trace_id,
            title=str(document["title"]),
            overall_result=str(document["overall_result"]),
            doc_path=doc_path,
            content=f"{json.dumps(document, indent=2)}\n",
            wrote=False,
        )

    @staticmethod
    def _write_index_and_tracker(
        *,
        index_service: Any,
        tracking_service: Any,
    ) -> None:
        index_document = index_service.build_document()
        index_service.write_document(index_document)
        tracker_result = tracking_service.build_document()
        tracking_service.write_document(tracker_result)

    def _trace_participates_in_coordination(self, trace_id: str) -> bool:
        try:
            self._loader.load_traceability_index().get(trace_id)
            return True
        except KeyError:
            return any(
                entry.trace_id == trace_id
                for entry in self._loader.load_task_index().entries
            )


def _scaffold_result_from_rendered(
    rendered: RenderedDocument,
    *,
    wrote: bool,
) -> ScaffoldDocumentResult:
    return ScaffoldDocumentResult(
        kind=rendered.kind,
        document_id=rendered.document_id,
        trace_id=rendered.trace_id,
        title=rendered.title,
        summary=rendered.summary,
        status=rendered.status,
        doc_path=rendered.doc_path,
        content=rendered.content,
        wrote=wrote,
    )


def _acceptance_contract_result_from_preview(
    preview: AcceptanceContractResult,
    *,
    wrote: bool,
) -> AcceptanceContractResult:
    return AcceptanceContractResult(
        contract_id=preview.contract_id,
        trace_id=preview.trace_id,
        source_prd_id=preview.source_prd_id,
        title=preview.title,
        doc_path=preview.doc_path,
        content=preview.content,
        wrote=wrote,
    )


def _validation_evidence_result_from_preview(
    preview: ValidationEvidenceResult,
    *,
    wrote: bool,
) -> ValidationEvidenceResult:
    return ValidationEvidenceResult(
        evidence_id=preview.evidence_id,
        trace_id=preview.trace_id,
        title=preview.title,
        overall_result=preview.overall_result,
        doc_path=preview.doc_path,
        content=preview.content,
        wrote=wrote,
    )
