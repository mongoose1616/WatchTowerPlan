"""Shared models for planning scaffold authoring and bootstrap results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from watchtower_core.repo_ops.planning_scaffold_specs import PlanKind

if TYPE_CHECKING:
    from watchtower_core.repo_ops.task_lifecycle import TaskMutationResult


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
