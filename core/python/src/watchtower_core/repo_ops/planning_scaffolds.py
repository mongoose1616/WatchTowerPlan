"""Template-aligned planning scaffold helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Literal

from watchtower_core.adapters import (
    extract_first_paragraph,
    extract_metadata_bullets,
    render_front_matter,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
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

PlanKind = Literal["prd", "feature-design", "implementation-plan", "decision"]

_PLANNING_FRONT_MATTER_KEY_ORDER = (
    "trace_id",
    "id",
    "title",
    "summary",
    "type",
    "status",
    "owner",
    "updated_at",
    "audience",
    "authority",
    "applies_to",
    "aliases",
)
_FILE_STEM_PATTERN = re.compile(r"[^a-z0-9]+")
PLAN_KIND_CHOICES: tuple[PlanKind, ...] = (
    "prd",
    "feature-design",
    "implementation-plan",
    "decision",
)
_PLAN_KIND_TO_DOC_TYPE = {
    "prd": "prd",
    "feature-design": "feature_design",
    "implementation-plan": "implementation_plan",
    "decision": "decision_record",
}
_PLAN_KIND_TO_SCHEMA = {
    "prd": "urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
    "feature-design": (
        "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1"
    ),
    "implementation-plan": (
        "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1"
    ),
    "decision": (
        "urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1"
    ),
}
_PLAN_KIND_TO_DIRECTORY = {
    "prd": "docs/planning/prds",
    "feature-design": "docs/planning/design/features",
    "implementation-plan": "docs/planning/design/implementation",
    "decision": "docs/planning/decisions",
}
_PLAN_KIND_TO_DEFAULT_STATUS = {
    "prd": "active",
    "feature-design": "draft",
    "implementation-plan": "draft",
    "decision": "active",
}
_PLAN_KIND_TO_DEFAULT_AUTHORITY = {
    "prd": "authoritative",
    "feature-design": "authoritative",
    "implementation-plan": "supporting",
    "decision": "supporting",
}
_PLAN_KIND_TO_ID_LABEL = {
    "prd": "PRD ID",
    "feature-design": "Design ID",
    "implementation-plan": "Plan ID",
    "decision": "Decision ID",
}
_PLAN_KIND_TO_STATUS_LABEL = {
    "prd": "Status",
    "feature-design": "Design Status",
    "implementation-plan": "Plan Status",
    "decision": "Record Status",
}
_PLAN_KIND_TO_REQUIRED_SECTIONS = {
    "prd": (
        "Record Metadata",
        "Summary",
        "Problem Statement",
        "Goals",
        "Non-Goals",
        "Requirements",
        "Acceptance Criteria",
        "Risks and Dependencies",
        "References",
    ),
    "feature-design": (
        "Record Metadata",
        "Summary",
        "Source Request",
        "Scope and Feature Boundary",
        "Current-State Context",
        "Design Goals and Constraints",
        "Options Considered",
        "Recommended Design",
        "Affected Surfaces",
        "Design Guardrails",
        "Risks",
        "References",
    ),
    "implementation-plan": (
        "Record Metadata",
        "Summary",
        "Source Request or Design",
        "Scope Summary",
        "Assumptions and Constraints",
        "Proposed Technical Approach",
        "Work Breakdown",
        "Risks",
        "Validation Plan",
        "References",
    ),
    "decision": (
        "Record Metadata",
        "Summary",
        "Decision Statement",
        "Trigger or Source Request",
        "Current Context and Constraints",
        "Affected Surfaces",
        "Options Considered",
        "Chosen Outcome",
        "Rationale and Tradeoffs",
        "Consequences and Follow-Up Impacts",
        "Risks, Dependencies, and Assumptions",
        "References",
    ),
}


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
class PlanBootstrapResult:
    """Result summary for one initiative bootstrap scaffold."""

    documents: tuple[ScaffoldDocumentResult, ...]
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
        return ScaffoldDocumentResult(
            kind=rendered.kind,
            document_id=rendered.document_id,
            trace_id=rendered.trace_id,
            title=rendered.title,
            summary=rendered.summary,
            status=rendered.status,
            doc_path=rendered.doc_path,
            content=rendered.content,
            wrote=write,
        )

    def bootstrap(self, params: PlanBootstrapParams, *, write: bool) -> PlanBootstrapResult:
        updated_at = params.updated_at or utc_timestamp_now()
        trace_suffix = _trace_suffix(params.trace_id)
        base_stem = params.file_stem or params.title
        prd_id = f"prd.{trace_suffix}"
        design_id = f"design.features.{trace_suffix}"
        implementation_id = f"design.implementation.{trace_suffix}"
        decision_id = params.decision_id or f"decision.{trace_suffix}_direction"
        task_id = params.task_id or f"task.{trace_suffix}.bootstrap.001"

        rendered_documents: list[_RenderedDocument] = [
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

        task_result = TaskLifecycleService(self._loader).create(
            TaskCreateParams(
                task_id=task_id,
                trace_id=params.trace_id,
                title=f"Bootstrap {params.title} planning chain",
                summary=f"Bootstraps the initial planning chain for {params.title}.",
                task_kind=_normalize_choice(
                    params.task_kind,
                    TASK_KIND_CHOICES,
                    label="task_kind",
                ),
                priority=_normalize_choice(
                    params.task_priority,
                    TASK_PRIORITY_CHOICES,
                    label="task_priority",
                ),
                owner=params.task_owner or params.owner,
                scope_items=(
                    "Publish the initial PRD, feature design, and implementation plan chain.",
                    "Establish the first tracked task for the initiative.",
                ),
                done_when_items=(
                    "The planning chain exists under canonical planning paths.",
                    "The bootstrap task is visible through the derived coordination surfaces.",
                ),
                applies_to=params.applies_to,
                related_ids=tuple(
                    document.document_id for document in rendered_documents
                ),
                file_stem=f"{_slugify_file_stem(base_stem)}_bootstrap",
                updated_at=updated_at,
            ),
            write=False,
        )

        if write:
            for rendered in rendered_documents:
                self._write_rendered_document(rendered)
            task_result = TaskLifecycleService(self._loader).create(
                TaskCreateParams(
                    task_id=task_id,
                    trace_id=params.trace_id,
                    title=f"Bootstrap {params.title} planning chain",
                    summary=f"Bootstraps the initial planning chain for {params.title}.",
                    task_kind=_normalize_choice(
                        params.task_kind,
                        TASK_KIND_CHOICES,
                        label="task_kind",
                    ),
                    priority=_normalize_choice(
                        params.task_priority,
                        TASK_PRIORITY_CHOICES,
                        label="task_priority",
                    ),
                    owner=params.task_owner or params.owner,
                    scope_items=(
                        "Publish the initial PRD, feature design, and implementation plan chain.",
                        "Establish the first tracked task for the initiative.",
                    ),
                    done_when_items=(
                        "The planning chain exists under canonical planning paths.",
                        "The bootstrap task is visible through the derived coordination surfaces.",
                    ),
                    applies_to=params.applies_to,
                    related_ids=tuple(
                        document.document_id for document in rendered_documents
                    ),
                    file_stem=f"{_slugify_file_stem(base_stem)}_bootstrap",
                    updated_at=updated_at,
                ),
                write=True,
            )
            self._refresh_bootstrap_surfaces(include_decision=params.include_decision)

        return PlanBootstrapResult(
            documents=tuple(
                ScaffoldDocumentResult(
                    kind=rendered.kind,
                    document_id=rendered.document_id,
                    trace_id=rendered.trace_id,
                    title=rendered.title,
                    summary=rendered.summary,
                    status=rendered.status,
                    doc_path=rendered.doc_path,
                    content=rendered.content,
                    wrote=write,
                )
                for rendered in rendered_documents
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

    def _render_scaffold(self, params: PlanScaffoldParams) -> _RenderedDocument:
        kind = _normalize_plan_kind(params.kind)
        updated_at = params.updated_at or utc_timestamp_now()
        front_matter = _compact_front_matter(
            {
                "trace_id": _normalize_required_string(params.trace_id, label="trace_id"),
                "id": _normalize_required_string(params.document_id, label="document_id"),
                "title": _normalize_required_string(params.title, label="title"),
                "summary": _normalize_required_string(params.summary, label="summary"),
                "type": _PLAN_KIND_TO_DOC_TYPE[kind],
                "status": _normalize_required_string(
                    params.status or _PLAN_KIND_TO_DEFAULT_STATUS[kind],
                    label="status",
                ),
                "owner": _normalize_required_string(params.owner, label="owner"),
                "updated_at": updated_at,
                "audience": "shared",
                "authority": _PLAN_KIND_TO_DEFAULT_AUTHORITY[kind],
                "applies_to": _normalize_list(params.applies_to),
                "aliases": _normalize_list(params.aliases),
            }
        )
        doc_path = (
            f"{_PLAN_KIND_TO_DIRECTORY[kind]}/"
            f"{_slugify_file_stem(params.file_stem or params.title)}.md"
        )
        _ensure_available_path(self._loader, doc_path)
        sections = _render_sections(kind, front_matter, params)
        content = _render_document_content(front_matter["title"], sections)
        rendered = _RenderedDocument(
            kind=kind,
            document_id=str(front_matter["id"]),
            trace_id=str(front_matter["trace_id"]),
            title=str(front_matter["title"]),
            summary=str(front_matter["summary"]),
            status=str(front_matter["status"]),
            schema_id=_PLAN_KIND_TO_SCHEMA[kind],
            id_label=_PLAN_KIND_TO_ID_LABEL[kind],
            status_label=_PLAN_KIND_TO_STATUS_LABEL[kind],
            doc_path=doc_path,
            front_matter=front_matter,
            sections=sections,
            content=content,
        )
        _validate_rendered_document(self._loader, rendered)
        return rendered

    def _write_rendered_document(self, rendered: _RenderedDocument) -> None:
        path = self._loader.repo_root / rendered.doc_path
        path.parent.mkdir(parents=True, exist_ok=True)
        rendered_front_matter = render_front_matter(_ordered_front_matter(rendered.front_matter))
        path.write_text(
            f"---\n{rendered_front_matter}\n---\n\n{rendered.content}",
            encoding="utf-8",
        )

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

    def _refresh_bootstrap_surfaces(self, *, include_decision: bool) -> None:
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
        CoordinationSyncService(self._loader).run(write=True)

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


@dataclass(frozen=True, slots=True)
class _RenderedDocument:
    kind: PlanKind
    document_id: str
    trace_id: str
    title: str
    summary: str
    status: str
    schema_id: str
    id_label: str
    status_label: str
    doc_path: str
    front_matter: dict[str, object]
    sections: dict[str, str]
    content: str


def _normalize_plan_kind(value: str) -> PlanKind:
    normalized = value.strip()
    if normalized not in PLAN_KIND_CHOICES:
        joined = ", ".join(PLAN_KIND_CHOICES)
        raise ValueError(f"kind must be one of: {joined}")
    return normalized  # type: ignore[return-value]


def _normalize_choice(value: str, allowed: tuple[str, ...], *, label: str) -> str:
    normalized = _normalize_required_string(value, label=label)
    if normalized not in allowed:
        joined = ", ".join(allowed)
        raise ValueError(f"{label} must be one of: {joined}")
    return normalized


def _normalize_required_string(value: str, *, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} must be a non-empty string.")
    return normalized


def _normalize_list(values: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        candidate = _normalize_required_string(value, label="list item")
        if candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)
    return tuple(normalized)


def _compact_front_matter(front_matter: dict[str, object]) -> dict[str, object]:
    compact: dict[str, object] = {}
    for key, value in front_matter.items():
        if value is None:
            continue
        if isinstance(value, tuple):
            if not value:
                continue
            compact[key] = list(value)
            continue
        compact[key] = value
    return compact


def _ordered_front_matter(front_matter: dict[str, object]) -> dict[str, object]:
    ordered: dict[str, object] = {}
    for key in _PLANNING_FRONT_MATTER_KEY_ORDER:
        if key in front_matter:
            ordered[key] = front_matter[key]
    for key, value in front_matter.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def _trace_suffix(trace_id: str) -> str:
    return _normalize_required_string(trace_id, label="trace_id").removeprefix("trace.")


def _slugify_file_stem(value: str) -> str:
    normalized = _FILE_STEM_PATTERN.sub("_", value.casefold()).strip("_")
    if not normalized:
        raise ValueError("Document file stem resolved to an empty value.")
    return normalized


def _format_code_values(values: tuple[str, ...]) -> str:
    if not values:
        return "`None`"
    return "; ".join(f"`{value}`" for value in values)


def _render_metadata(label: str, values: tuple[str, ...]) -> str:
    return f"- `{label}`: {_format_code_values(values)}"


def _render_bullets(values: tuple[str, ...], *, placeholder: str) -> str:
    if values:
        return "\n".join(f"- {value}" for value in values)
    return f"- {placeholder}"


def _render_numbered(values: tuple[str, ...], *, placeholders: tuple[str, ...]) -> str:
    if values:
        return "\n".join(f"{index}. {value}" for index, value in enumerate(values, start=1))
    return "\n".join(
        f"{index}. {value}" for index, value in enumerate(placeholders, start=1)
    )


def _render_references(values: tuple[str, ...]) -> str:
    if values:
        return "\n".join(f"- {value}" for value in values)
    return "- <Companion document or source>"


def _render_sections(
    kind: PlanKind,
    front_matter: dict[str, object],
    params: PlanScaffoldParams,
) -> dict[str, str]:
    trace_suffix = _trace_suffix(str(front_matter["trace_id"]))
    updated_at = str(front_matter["updated_at"])
    status = str(front_matter["status"])
    document_id = str(front_matter["id"])
    summary = str(front_matter["summary"])

    if kind == "prd":
        return {
            "Record Metadata": "\n".join(
                (
                    _render_metadata("Trace ID", (str(front_matter["trace_id"]),)),
                    _render_metadata("PRD ID", (document_id,)),
                    _render_metadata("Status", (status,)),
                    _render_metadata("Linked Decisions", params.linked_decision_ids),
                    _render_metadata("Linked Designs", params.linked_design_ids),
                    _render_metadata("Linked Implementation Plans", params.linked_plan_ids),
                    _render_metadata("Updated At", (updated_at,)),
                )
            ),
            "Summary": summary,
            "Problem Statement": "<Describe the problem this PRD exists to solve.>",
            "Goals": _render_bullets((), placeholder="<Primary goal>"),
            "Non-Goals": _render_bullets((), placeholder="<Non-goal>"),
            "Requirements": f"- `req.{trace_suffix}.001`: <Requirement>",
            "Acceptance Criteria": f"- `ac.{trace_suffix}.001`: <Acceptance criterion>",
            "Risks and Dependencies": _render_bullets((), placeholder="<Risk or dependency>"),
            "References": _render_references(params.references),
        }
    if kind == "feature-design":
        return {
            "Record Metadata": "\n".join(
                (
                    _render_metadata("Trace ID", (str(front_matter["trace_id"]),)),
                    _render_metadata("Design ID", (document_id,)),
                    _render_metadata("Design Status", (status,)),
                    _render_metadata("Linked PRDs", params.linked_prd_ids),
                    _render_metadata("Linked Decisions", params.linked_decision_ids),
                    _render_metadata("Linked Implementation Plans", params.linked_plan_ids),
                    _render_metadata("Updated At", (updated_at,)),
                )
            ),
            "Summary": summary,
            "Source Request": _render_bullets(
                params.source_requests,
                placeholder="<Request, issue, or planning input that triggered this design.>",
            ),
            "Scope and Feature Boundary": "\n".join(
                (
                    "- <What the design covers.>",
                    "- <What the design intentionally excludes.>",
                )
            ),
            "Current-State Context": "\n".join(
                (
                    "- <Relevant repository or workflow context.>",
                    "- <Current constraint or gap that shapes the design.>",
                )
            ),
            "Design Goals and Constraints": "\n".join(
                (
                    "- <Primary design goal.>",
                    "- <Key constraint or non-goal.>",
                    "- <Invariant the implementation must preserve.>",
                )
            ),
            "Options Considered": "\n".join(
                (
                    "### Option 1",
                    "- <Short description.>",
                    "- <Strength.>",
                    "- <Tradeoff.>",
                    "",
                    "### Option 2",
                    "- <Short description.>",
                    "- <Strength.>",
                    "- <Tradeoff.>",
                )
            ),
            "Recommended Design": "\n".join(
                (
                    "### Architecture",
                    "- <Core components and responsibilities.>",
                    "",
                    "### Data and Interface Impacts",
                    "- <Artifacts, schemas, or interfaces affected.>",
                    "",
                    "### Execution Flow",
                    "1. <Step in the recommended flow.>",
                    "2. <Step in the recommended flow.>",
                    "3. <Step in the recommended flow.>",
                    "",
                    "### Invariants and Failure Cases",
                    "- <Invariant or fail-closed behavior.>",
                    "- <Failure case the implementation must handle explicitly.>",
                )
            ),
            "Affected Surfaces": _render_bullets(
                params.applies_to,
                placeholder="<Docs, code paths, or governed artifacts affected.>",
            ),
            "Design Guardrails": "\n".join(
                (
                    "- <Implementation rule that must hold.>",
                    "- <Boundary the implementation must not cross.>",
                )
            ),
            "Risks": _render_bullets((), placeholder="<Concrete risk or uncertainty.>"),
            "References": _render_references(params.references),
        }
    if kind == "implementation-plan":
        return {
            "Record Metadata": "\n".join(
                (
                    _render_metadata("Trace ID", (str(front_matter["trace_id"]),)),
                    _render_metadata("Plan ID", (document_id,)),
                    _render_metadata("Plan Status", (status,)),
                    _render_metadata("Linked PRDs", params.linked_prd_ids),
                    _render_metadata("Linked Decisions", params.linked_decision_ids),
                    _render_metadata("Source Designs", params.linked_design_ids),
                    _render_metadata("Linked Acceptance Contracts", params.linked_acceptance_ids),
                    _render_metadata("Updated At", (updated_at,)),
                )
            ),
            "Summary": summary,
            "Source Request or Design": _render_bullets(
                params.source_requests or params.linked_design_ids,
                placeholder="<Driving feature design, PRD, or user request.>",
            ),
            "Scope Summary": "\n".join(
                (
                    "- <What this plan covers.>",
                    "- <What this plan intentionally excludes.>",
                )
            ),
            "Assumptions and Constraints": "\n".join(
                (
                    "- <Hard constraint the implementation must preserve.>",
                    "- <Assumption that shapes the work breakdown.>",
                )
            ),
            "Proposed Technical Approach": "\n".join(
                (
                    "- <High-level implementation structure and boundaries.>",
                    "- <How the work composes with existing repository surfaces.>",
                )
            ),
            "Work Breakdown": _render_numbered(
                (),
                placeholders=(
                    "<Concrete work slice or step.>",
                    "<Concrete work slice or step.>",
                    "<Concrete work slice or step.>",
                ),
            ),
            "Risks": _render_bullets((), placeholder="<Concrete risk or uncertainty.>"),
            "Validation Plan": "\n".join(
                (
                    "- <How the implementation will be verified.>",
                    "- <Tests, checks, or review evidence expected.>",
                )
            ),
            "References": _render_references(params.references),
        }
    return {
        "Record Metadata": "\n".join(
            (
                _render_metadata("Trace ID", (str(front_matter["trace_id"]),)),
                _render_metadata("Decision ID", (document_id,)),
                _render_metadata("Record Status", (status,)),
                _render_metadata("Decision Status", ("proposed",)),
                _render_metadata("Linked PRDs", params.linked_prd_ids),
                _render_metadata("Linked Designs", params.linked_design_ids),
                _render_metadata("Linked Implementation Plans", params.linked_plan_ids),
                _render_metadata("Updated At", (updated_at,)),
            )
        ),
        "Summary": summary,
        "Decision Statement": "<State the decision in one clear sentence.>",
        "Trigger or Source Request": _render_bullets(
            params.source_requests,
            placeholder="<Describe what prompted the decision.>",
        ),
        "Current Context and Constraints": _render_bullets(
            (),
            placeholder="<Constraint or current-state fact.>",
        ),
        "Affected Surfaces": _render_bullets(
            params.applies_to,
            placeholder="<PRD, design, plan, standard, workflow, or implementation path affected.>",
        ),
        "Options Considered": "\n".join(
            (
                "### Option 1",
                "- <Description.>",
                "- <Strength.>",
                "- <Tradeoff.>",
                "",
                "### Option 2",
                "- <Description.>",
                "- <Strength.>",
                "- <Tradeoff.>",
            )
        ),
        "Chosen Outcome": "<Describe the recommended or accepted outcome.>",
        "Rationale and Tradeoffs": _render_bullets(
            (),
            placeholder="<Why this outcome was chosen.>",
        ),
        "Consequences and Follow-Up Impacts": _render_bullets(
            (),
            placeholder="<What changes next.>",
        ),
        "Risks, Dependencies, and Assumptions": _render_bullets(
            (),
            placeholder="<Risk, dependency, or assumption.>",
        ),
        "References": _render_references(params.references),
    }


def _render_document_content(title: object, sections: dict[str, str]) -> str:
    lines = [f"# {title}", ""]
    for section_title, section_body in sections.items():
        lines.extend((f"## {section_title}", section_body.strip(), ""))
    return "\n".join(lines).rstrip() + "\n"


def _validate_rendered_document(loader: ControlPlaneLoader, rendered: _RenderedDocument) -> None:
    loader.schema_store.validate_instance(rendered.front_matter, schema_id=rendered.schema_id)

    required_sections = set(_PLAN_KIND_TO_REQUIRED_SECTIONS[rendered.kind])
    missing_sections = sorted(required_sections.difference(rendered.sections))
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{rendered.doc_path} is missing required sections: {joined}")

    if extract_first_paragraph(rendered.sections["Summary"]) != rendered.summary:
        raise ValueError(f"{rendered.doc_path} Summary section does not match front matter.")

    metadata = extract_metadata_bullets(rendered.sections["Record Metadata"])
    _validate_metadata_scalar(
        metadata,
        "Trace ID",
        rendered.trace_id,
        path=rendered.doc_path,
    )
    _validate_metadata_scalar(
        metadata,
        rendered.id_label,
        rendered.document_id,
        path=rendered.doc_path,
    )
    _validate_metadata_scalar(
        metadata,
        rendered.status_label,
        rendered.status,
        path=rendered.doc_path,
    )
    _validate_metadata_scalar(
        metadata,
        "Updated At",
        str(rendered.front_matter["updated_at"]),
        path=rendered.doc_path,
    )
    if rendered.kind == "decision":
        _validate_metadata_scalar(metadata, "Decision Status", "proposed", path=rendered.doc_path)


def _validate_metadata_scalar(
    metadata: dict[str, str],
    label: str,
    expected: str,
    *,
    path: str,
) -> None:
    raw_value = metadata.get(label)
    if raw_value is None:
        raise ValueError(f"{path} is missing Record Metadata label: {label}")
    values = tuple(split for split in _split_metadata_values(raw_value))
    if values != (expected,):
        raise ValueError(
            f"{path} Record Metadata label {label} does not match expected value {expected!r}."
        )


def _split_metadata_values(raw_value: str) -> tuple[str, ...]:
    cleaned = raw_value.replace("`", "")
    values = tuple(value.strip() for value in cleaned.split(";") if value.strip())
    if values == ("None",):
        return ()
    return values


def _ensure_available_path(loader: ControlPlaneLoader, relative_path: str) -> None:
    if (loader.repo_root / relative_path).exists():
        raise ValueError(f"Planning scaffold path already exists: {relative_path}")
