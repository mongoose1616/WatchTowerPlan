"""Typed models for coordination and execution-tracking artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class InitiativeActiveTaskSummary:
    """Compact active-task summary embedded in an initiative-index entry."""

    task_id: str
    title: str
    task_status: str
    priority: str
    owner: str
    doc_path: str
    is_actionable: bool
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> InitiativeActiveTaskSummary:
        return cls(
            task_id=document["task_id"],
            title=document["title"],
            task_status=document["task_status"],
            priority=document["priority"],
            owner=document["owner"],
            doc_path=document["doc_path"],
            is_actionable=document["is_actionable"],
            blocked_by=tuple(document.get("blocked_by", ())),
            depends_on=tuple(document.get("depends_on", ())),
        )


@dataclass(frozen=True, slots=True)
class InitiativeIndexEntry:
    """Initiative-index entry."""

    trace_id: str
    title: str
    summary: str
    status: str
    initiative_status: str
    current_phase: str
    updated_at: str
    open_task_count: int
    blocked_task_count: int
    key_surface_path: str
    next_action: str
    next_surface_path: str
    primary_owner: str | None = None
    active_owners: tuple[str, ...] = ()
    active_task_ids: tuple[str, ...] = ()
    active_task_summaries: tuple[InitiativeActiveTaskSummary, ...] = ()
    blocked_by_task_ids: tuple[str, ...] = ()
    prd_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    design_ids: tuple[str, ...] = ()
    plan_ids: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    acceptance_contract_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    closed_at: str | None = None
    closure_reason: str | None = None
    superseded_by_trace_id: str | None = None
    related_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> InitiativeIndexEntry:
        return cls(
            trace_id=document["trace_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            initiative_status=document["initiative_status"],
            current_phase=document["current_phase"],
            updated_at=document["updated_at"],
            open_task_count=document["open_task_count"],
            blocked_task_count=document["blocked_task_count"],
            key_surface_path=document["key_surface_path"],
            next_action=document["next_action"],
            next_surface_path=document["next_surface_path"],
            primary_owner=document.get("primary_owner"),
            active_owners=tuple(document.get("active_owners", ())),
            active_task_ids=tuple(document.get("active_task_ids", ())),
            active_task_summaries=tuple(
                InitiativeActiveTaskSummary.from_document(entry)
                for entry in document.get("active_task_summaries", ())
            ),
            blocked_by_task_ids=tuple(document.get("blocked_by_task_ids", ())),
            prd_ids=tuple(document.get("prd_ids", ())),
            decision_ids=tuple(document.get("decision_ids", ())),
            design_ids=tuple(document.get("design_ids", ())),
            plan_ids=tuple(document.get("plan_ids", ())),
            task_ids=tuple(document.get("task_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            acceptance_contract_ids=tuple(document.get("acceptance_contract_ids", ())),
            evidence_ids=tuple(document.get("evidence_ids", ())),
            closed_at=document.get("closed_at"),
            closure_reason=document.get("closure_reason"),
            superseded_by_trace_id=document.get("superseded_by_trace_id"),
            related_paths=tuple(document.get("related_paths", ())),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class InitiativeIndex:
    """Typed initiative-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[InitiativeIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> InitiativeIndex:
        entries = tuple(InitiativeIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, trace_id: str) -> InitiativeIndexEntry:
        """Return an initiative-index entry by trace identifier."""
        for entry in self.entries:
            if entry.trace_id == trace_id:
                return entry
        raise KeyError(trace_id)


@dataclass(frozen=True, slots=True)
class TaskIndexEntry:
    """Task-index entry."""

    task_id: str
    title: str
    summary: str
    status: str
    task_status: str
    task_kind: str
    priority: str
    owner: str
    doc_path: str
    updated_at: str
    trace_id: str | None = None
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    applies_to: tuple[str, ...] = ()
    github_repository: str | None = None
    github_issue_number: int | None = None
    github_issue_node_id: str | None = None
    github_project_owner: str | None = None
    github_project_owner_type: str | None = None
    github_project_number: int | None = None
    github_project_item_id: str | None = None
    github_synced_at: str | None = None
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TaskIndexEntry:
        return cls(
            task_id=document["task_id"],
            trace_id=document.get("trace_id"),
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            task_status=document["task_status"],
            task_kind=document["task_kind"],
            priority=document["priority"],
            owner=document["owner"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            blocked_by=tuple(document.get("blocked_by", ())),
            depends_on=tuple(document.get("depends_on", ())),
            related_ids=tuple(document.get("related_ids", ())),
            applies_to=tuple(document.get("applies_to", ())),
            github_repository=document.get("github_repository"),
            github_issue_number=document.get("github_issue_number"),
            github_issue_node_id=document.get("github_issue_node_id"),
            github_project_owner=document.get("github_project_owner"),
            github_project_owner_type=document.get("github_project_owner_type"),
            github_project_number=document.get("github_project_number"),
            github_project_item_id=document.get("github_project_item_id"),
            github_synced_at=document.get("github_synced_at"),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class TaskIndex:
    """Typed task-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[TaskIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TaskIndex:
        entries = tuple(TaskIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, task_id: str) -> TaskIndexEntry:
        """Return a task-index entry by identifier."""
        for entry in self.entries:
            if entry.task_id == task_id:
                return entry
        raise KeyError(task_id)


@dataclass(frozen=True, slots=True)
class TraceabilityEntry:
    """Traceability-index entry."""

    trace_id: str
    title: str
    summary: str
    status: str
    initiative_status: str
    updated_at: str
    closed_at: str | None = None
    closure_reason: str | None = None
    superseded_by_trace_id: str | None = None
    prd_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    design_ids: tuple[str, ...] = ()
    plan_ids: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    requirement_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    acceptance_contract_ids: tuple[str, ...] = ()
    validator_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TraceabilityEntry:
        return cls(
            trace_id=document["trace_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            initiative_status=document["initiative_status"],
            updated_at=document["updated_at"],
            closed_at=document.get("closed_at"),
            closure_reason=document.get("closure_reason"),
            superseded_by_trace_id=document.get("superseded_by_trace_id"),
            prd_ids=tuple(document.get("prd_ids", ())),
            decision_ids=tuple(document.get("decision_ids", ())),
            design_ids=tuple(document.get("design_ids", ())),
            plan_ids=tuple(document.get("plan_ids", ())),
            task_ids=tuple(document.get("task_ids", ())),
            requirement_ids=tuple(document.get("requirement_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            acceptance_contract_ids=tuple(document.get("acceptance_contract_ids", ())),
            validator_ids=tuple(document.get("validator_ids", ())),
            evidence_ids=tuple(document.get("evidence_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class TraceabilityIndex:
    """Typed traceability-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[TraceabilityEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TraceabilityIndex:
        entries = tuple(TraceabilityEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, trace_id: str) -> TraceabilityEntry:
        """Return a traceability entry by trace identifier."""
        for entry in self.entries:
            if entry.trace_id == trace_id:
                return entry
        raise KeyError(trace_id)
