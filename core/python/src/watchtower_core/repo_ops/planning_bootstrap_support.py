"""Helper seams for planning bootstrap artifacts and surface refresh."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.evidence.validation_evidence import (
    VALIDATION_EVIDENCE_DIRECTORY,
    VALIDATION_EVIDENCE_SCHEMA_ID,
)
from watchtower_core.repo_ops.planning_scaffold_models import (
    AcceptanceContractResult,
    PlanBootstrapParams,
    PlanScaffoldParams,
    ValidationEvidenceResult,
)
from watchtower_core.repo_ops.planning_scaffold_specs import PlanKind, trace_suffix
from watchtower_core.repo_ops.planning_scaffold_support import (
    RenderedDocument,
    ensure_available_path,
    normalize_choice,
    slugify_file_stem,
)
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
)

ACCEPTANCE_CONTRACT_SCHEMA_ID = "urn:watchtower:schema:artifacts:contracts:acceptance-contract:v1"
ACCEPTANCE_CONTRACT_DIRECTORY = "core/control_plane/contracts/acceptance"
BOOTSTRAP_VALIDATION_EVIDENCE_VALIDATOR_ID = "validator.control_plane.validation_evidence"


@dataclass(frozen=True, slots=True)
class PlanBootstrapIdentifiers:
    """Derived IDs and stems used by one bootstrap flow."""

    trace_id_suffix: str
    base_stem: str
    prd_id: str
    design_id: str
    implementation_id: str
    decision_id: str
    task_id: str
    contract_id: str
    evidence_id: str


def build_bootstrap_identifiers(params: PlanBootstrapParams) -> PlanBootstrapIdentifiers:
    """Derive the canonical IDs and file stem for one bootstrap request."""

    trace_id_suffix = trace_suffix(params.trace_id)
    return PlanBootstrapIdentifiers(
        trace_id_suffix=trace_id_suffix,
        base_stem=params.file_stem or params.title,
        prd_id=f"prd.{trace_id_suffix}",
        design_id=f"design.features.{trace_id_suffix}",
        implementation_id=f"design.implementation.{trace_id_suffix}",
        decision_id=params.decision_id or f"decision.{trace_id_suffix}_direction",
        task_id=params.task_id or f"task.{trace_id_suffix}.bootstrap.001",
        contract_id=f"contract.acceptance.{trace_id_suffix}",
        evidence_id=f"evidence.{trace_id_suffix}.planning_baseline",
    )


def build_bootstrap_scaffold_params(
    params: PlanBootstrapParams,
    identifiers: PlanBootstrapIdentifiers,
    *,
    updated_at: str,
) -> tuple[PlanScaffoldParams, ...]:
    """Build the planning-document scaffold params for one bootstrap request."""

    scaffold_params: list[PlanScaffoldParams] = [
        PlanScaffoldParams(
            kind="prd",
            trace_id=params.trace_id,
            document_id=identifiers.prd_id,
            title=f"{params.title} PRD",
            summary=params.summary,
            owner=params.owner,
            applies_to=params.applies_to,
            aliases=params.aliases,
            file_stem=identifiers.base_stem,
            linked_decision_ids=((identifiers.decision_id,) if params.include_decision else ()),
            linked_design_ids=(identifiers.design_id,),
            linked_plan_ids=(identifiers.implementation_id,),
            references=params.references,
            updated_at=updated_at,
        ),
        PlanScaffoldParams(
            kind="feature-design",
            trace_id=params.trace_id,
            document_id=identifiers.design_id,
            title=f"{params.title} Feature Design",
            summary=f"Defines the technical design boundary for {params.title}.",
            owner=params.owner,
            applies_to=params.applies_to,
            aliases=params.aliases,
            file_stem=identifiers.base_stem,
            linked_prd_ids=(identifiers.prd_id,),
            linked_decision_ids=((identifiers.decision_id,) if params.include_decision else ()),
            linked_plan_ids=(identifiers.implementation_id,),
            source_requests=params.source_requests,
            references=params.references,
            updated_at=updated_at,
        ),
        PlanScaffoldParams(
            kind="implementation-plan",
            trace_id=params.trace_id,
            document_id=identifiers.implementation_id,
            title=f"{params.title} Implementation Plan",
            summary=f"Breaks {params.title} into a bounded implementation slice.",
            owner=params.owner,
            applies_to=params.applies_to,
            aliases=params.aliases,
            file_stem=identifiers.base_stem,
            linked_prd_ids=(identifiers.prd_id,),
            linked_decision_ids=((identifiers.decision_id,) if params.include_decision else ()),
            linked_design_ids=(identifiers.design_id,),
            source_requests=params.source_requests,
            references=params.references,
            updated_at=updated_at,
        ),
    ]
    if params.include_decision:
        scaffold_params.append(
            PlanScaffoldParams(
                kind="decision",
                trace_id=params.trace_id,
                document_id=identifiers.decision_id,
                title=f"{params.title} Direction Decision",
                summary=f"Records the initial direction decision for {params.title}.",
                owner=params.owner,
                applies_to=params.applies_to,
                aliases=params.aliases,
                file_stem=f"{identifiers.base_stem}_direction",
                linked_prd_ids=(identifiers.prd_id,),
                linked_design_ids=(identifiers.design_id,),
                linked_plan_ids=(identifiers.implementation_id,),
                source_requests=params.source_requests,
                references=params.references,
                updated_at=updated_at,
            )
        )
    return tuple(scaffold_params)


def build_bootstrap_task_create_params(
    params: PlanBootstrapParams,
    identifiers: PlanBootstrapIdentifiers,
    *,
    updated_at: str,
    related_ids: tuple[str, ...],
) -> TaskCreateParams:
    """Build the bootstrap task create params for one trace."""

    return TaskCreateParams(
        task_id=identifiers.task_id,
        trace_id=params.trace_id,
        title=f"Bootstrap {params.title} planning chain",
        summary=f"Bootstraps the initial planning chain for {params.title}.",
        task_kind=normalize_choice(params.task_kind, TASK_KIND_CHOICES, label="task_kind"),
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
        file_stem=f"{slugify_file_stem(identifiers.base_stem)}_bootstrap",
        updated_at=updated_at,
    )


def build_acceptance_contract_artifact(
    loader: ControlPlaneLoader,
    params: PlanBootstrapParams,
    identifiers: PlanBootstrapIdentifiers,
    *,
    updated_at: str,
    rendered_documents: tuple[RenderedDocument, ...],
    task_doc_path: str,
) -> tuple[dict[str, object], AcceptanceContractResult]:
    """Build the bootstrap acceptance contract artifact and preview."""

    doc_path = f"{ACCEPTANCE_CONTRACT_DIRECTORY}/{identifiers.trace_id_suffix}_acceptance.v1.json"
    ensure_available_path(loader, doc_path)
    document: dict[str, object] = {
        "$schema": ACCEPTANCE_CONTRACT_SCHEMA_ID,
        "id": identifiers.contract_id,
        "title": f"{params.title} Acceptance Contract",
        "status": "active",
        "trace_id": params.trace_id,
        "source_prd_id": identifiers.prd_id,
        "entries": [
            {
                "acceptance_id": f"ac.{identifiers.trace_id_suffix}.001",
                "summary": (
                    "The bootstrap flow publishes the initial PRD, feature design, "
                    "implementation plan, acceptance contract, planning-baseline "
                    "evidence, and bootstrap task for the trace."
                ),
                "source_requirement_ids": [f"req.{identifiers.trace_id_suffix}.001"],
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
                    f"Bootstrap baseline contract prepared at {updated_at} for {params.trace_id}."
                ),
            }
        ],
    }
    loader.schema_store.validate_instance(document, schema_id=ACCEPTANCE_CONTRACT_SCHEMA_ID)
    return document, AcceptanceContractResult(
        contract_id=identifiers.contract_id,
        trace_id=params.trace_id,
        source_prd_id=identifiers.prd_id,
        title=str(document["title"]),
        doc_path=doc_path,
        content=f"{json.dumps(document, indent=2)}\n",
        wrote=False,
    )


def build_validation_evidence_artifact(
    loader: ControlPlaneLoader,
    params: PlanBootstrapParams,
    identifiers: PlanBootstrapIdentifiers,
    *,
    updated_at: str,
    rendered_documents: tuple[RenderedDocument, ...],
    task_doc_path: str,
    contract_doc_path: str,
) -> tuple[dict[str, object], ValidationEvidenceResult]:
    """Build the bootstrap validation-evidence artifact and preview."""

    doc_path = (
        f"{VALIDATION_EVIDENCE_DIRECTORY}/{identifiers.trace_id_suffix}_planning_baseline.v1.json"
    )
    ensure_available_path(loader, doc_path)
    subject_paths = [
        *(document.doc_path for document in rendered_documents),
        contract_doc_path,
    ]
    if task_doc_path not in subject_paths:
        subject_paths.append(task_doc_path)
    subject_ids = [
        identifiers.prd_id,
        identifiers.design_id,
        identifiers.implementation_id,
        identifiers.task_id,
        identifiers.contract_id,
    ]
    if params.include_decision:
        subject_ids.append(identifiers.decision_id)
    document: dict[str, object] = {
        "$schema": VALIDATION_EVIDENCE_SCHEMA_ID,
        "id": identifiers.evidence_id,
        "title": f"{params.title} Planning Baseline Evidence",
        "status": "active",
        "trace_id": params.trace_id,
        "overall_result": "passed",
        "recorded_at": updated_at,
        "source_prd_ids": [identifiers.prd_id],
        "source_design_ids": [identifiers.design_id],
        "source_plan_ids": [identifiers.implementation_id],
        "source_acceptance_contract_ids": [identifiers.contract_id],
        "checks": [
            {
                "check_id": f"check.{identifiers.trace_id_suffix}.planning_baseline",
                "title": "Bootstrap planning baseline is aligned",
                "result": "passed",
                "subject_paths": subject_paths,
                "subject_ids": subject_ids,
                "validator_id": BOOTSTRAP_VALIDATION_EVIDENCE_VALIDATOR_ID,
                "acceptance_ids": [f"ac.{identifiers.trace_id_suffix}.001"],
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
        "notes": (f"Planning baseline evidence prepared at {updated_at} for {params.trace_id}."),
    }
    if params.include_decision:
        document["source_decision_ids"] = [identifiers.decision_id]
    loader.schema_store.validate_instance(
        document,
        schema_id=VALIDATION_EVIDENCE_SCHEMA_ID,
    )
    return document, ValidationEvidenceResult(
        evidence_id=identifiers.evidence_id,
        trace_id=params.trace_id,
        title=str(document["title"]),
        overall_result=str(document["overall_result"]),
        doc_path=doc_path,
        content=f"{json.dumps(document, indent=2)}\n",
        wrote=False,
    )


def refresh_planning_surfaces(loader: ControlPlaneLoader, *, kind: PlanKind) -> None:
    """Refresh the index and tracking surfaces touched by one scaffold kind."""

    if kind == "prd":
        _write_index_and_tracker(
            index_service=PrdIndexSyncService(loader),
            tracking_service=PrdTrackingSyncService(loader),
        )
    elif kind in {"feature-design", "implementation-plan"}:
        _write_index_and_tracker(
            index_service=DesignDocumentIndexSyncService(loader),
            tracking_service=DesignTrackingSyncService(loader),
        )
    else:
        _write_index_and_tracker(
            index_service=DecisionIndexSyncService(loader),
            tracking_service=DecisionTrackingSyncService(loader),
        )


def refresh_bootstrap_document_surfaces(
    loader: ControlPlaneLoader,
    *,
    include_decision: bool,
) -> None:
    """Refresh all planning-document surfaces touched by bootstrap mode."""

    _write_index_and_tracker(
        index_service=PrdIndexSyncService(loader),
        tracking_service=PrdTrackingSyncService(loader),
    )
    _write_index_and_tracker(
        index_service=DesignDocumentIndexSyncService(loader),
        tracking_service=DesignTrackingSyncService(loader),
    )
    if include_decision:
        _write_index_and_tracker(
            index_service=DecisionIndexSyncService(loader),
            tracking_service=DecisionTrackingSyncService(loader),
        )


def _write_index_and_tracker(
    *,
    index_service: Any,
    tracking_service: Any,
) -> None:
    index_document = index_service.build_document()
    index_service.write_document(index_document)
    tracker_result = tracking_service.build_document()
    tracking_service.write_document(tracker_result)
