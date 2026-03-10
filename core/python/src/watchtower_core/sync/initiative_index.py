"""Deterministic rebuild helpers for the initiative index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    PrdIndexEntry,
    TaskIndexEntry,
    TraceabilityEntry,
)
from watchtower_core.control_plane.paths import discover_repo_root

INITIATIVE_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/initiatives/initiative_index.v1.json"
VALIDATE_ACCEPTANCE_COMMAND_DOC = (
    "docs/commands/core_python/watchtower_core_validate_acceptance.md"
)
CLOSEOUT_INITIATIVE_COMMAND_DOC = (
    "docs/commands/core_python/watchtower_core_closeout_initiative.md"
)
DESIGN_DIRECTORY = "docs/planning/design/features/"
IMPLEMENTATION_PLAN_DIRECTORY = "docs/planning/design/implementation/"
TASK_OPEN_DIRECTORY = "docs/planning/tasks/open/"

TERMINAL_TASK_STATUSES = {"done", "cancelled"}
PHASE_ORDER = {
    "prd": 1,
    "design": 2,
    "implementation_planning": 3,
    "execution": 4,
    "validation": 5,
    "closeout": 6,
    "closed": 7,
}


class _TraceLinkedEntry(Protocol):
    """Protocol for index entries that carry a shared trace identifier."""

    @property
    def trace_id(self) -> str | None: ...


class InitiativeIndexSyncService:
    """Build and write the initiative index from current planning and task surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> InitiativeIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        traceability_index = self._loader.load_traceability_index()
        prd_entries = _group_by_trace(self._loader.load_prd_index().entries)
        decision_entries = _group_by_trace(self._loader.load_decision_index().entries)
        design_entries = _group_by_trace(self._loader.load_design_document_index().entries)
        task_entries = _group_by_trace(self._loader.load_task_index().entries)

        entries = [
            self._build_entry(
                trace_entry,
                prd_entries.get(trace_entry.trace_id, ()),
                decision_entries.get(trace_entry.trace_id, ()),
                design_entries.get(trace_entry.trace_id, ()),
                task_entries.get(trace_entry.trace_id, ()),
            )
            for trace_entry in traceability_index.entries
        ]

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:initiative-index:v1",
            "id": "index.initiatives",
            "title": "Initiative Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write the generated initiative index to disk."""
        target = destination or (self._repo_root / INITIATIVE_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _build_entry(
        self,
        trace_entry: TraceabilityEntry,
        prd_entries: tuple[PrdIndexEntry, ...],
        decision_entries: tuple[DecisionIndexEntry, ...],
        design_entries: tuple[DesignDocumentIndexEntry, ...],
        task_entries: tuple[TaskIndexEntry, ...],
    ) -> dict[str, object]:
        active_tasks = tuple(
            entry for entry in task_entries if entry.task_status not in TERMINAL_TASK_STATUSES
        )
        active_owners = tuple(sorted({entry.owner for entry in active_tasks}))
        primary_owner = active_owners[0] if len(active_owners) == 1 else None
        blocked_by_task_ids = tuple(
            sorted({task_id for entry in active_tasks for task_id in entry.blocked_by})
        )
        blocked_task_count = sum(
            1
            for entry in active_tasks
            if entry.task_status == "blocked" or len(entry.blocked_by) > 0
        )

        current_phase = _determine_current_phase(
            trace_entry=trace_entry,
            prd_entries=prd_entries,
            design_entries=design_entries,
            active_tasks=active_tasks,
        )
        key_surface_path = _key_surface_path(
            trace_entry=trace_entry,
            prd_entries=prd_entries,
            design_entries=design_entries,
            decision_entries=decision_entries,
            task_entries=task_entries,
        )
        next_action, next_surface_path = _next_step(
            current_phase=current_phase,
            initiative_status=trace_entry.initiative_status,
            active_tasks=active_tasks,
            blocked_task_count=blocked_task_count,
            key_surface_path=key_surface_path,
        )

        entry: dict[str, object] = {
            "trace_id": trace_entry.trace_id,
            "title": trace_entry.title,
            "summary": trace_entry.summary,
            "status": trace_entry.status,
            "initiative_status": trace_entry.initiative_status,
            "current_phase": current_phase,
            "updated_at": trace_entry.updated_at,
            "open_task_count": len(active_tasks),
            "blocked_task_count": blocked_task_count,
            "key_surface_path": key_surface_path,
            "next_action": next_action,
            "next_surface_path": next_surface_path,
        }
        if primary_owner is not None:
            entry["primary_owner"] = primary_owner
        if active_owners:
            entry["active_owners"] = list(active_owners)
        if active_tasks:
            entry["active_task_ids"] = [entry.task_id for entry in active_tasks]
        if blocked_by_task_ids:
            entry["blocked_by_task_ids"] = list(blocked_by_task_ids)
        if trace_entry.prd_ids:
            entry["prd_ids"] = list(trace_entry.prd_ids)
        if trace_entry.decision_ids:
            entry["decision_ids"] = list(trace_entry.decision_ids)
        if trace_entry.design_ids:
            entry["design_ids"] = list(trace_entry.design_ids)
        if trace_entry.plan_ids:
            entry["plan_ids"] = list(trace_entry.plan_ids)
        if trace_entry.task_ids:
            entry["task_ids"] = list(trace_entry.task_ids)
        if trace_entry.acceptance_ids:
            entry["acceptance_ids"] = list(trace_entry.acceptance_ids)
        if trace_entry.acceptance_contract_ids:
            entry["acceptance_contract_ids"] = list(trace_entry.acceptance_contract_ids)
        if trace_entry.evidence_ids:
            entry["evidence_ids"] = list(trace_entry.evidence_ids)
        if trace_entry.initiative_status != "active":
            if trace_entry.closed_at is not None:
                entry["closed_at"] = trace_entry.closed_at
            if trace_entry.closure_reason is not None:
                entry["closure_reason"] = trace_entry.closure_reason
            if trace_entry.superseded_by_trace_id is not None:
                entry["superseded_by_trace_id"] = trace_entry.superseded_by_trace_id
        if trace_entry.related_paths:
            entry["related_paths"] = list(trace_entry.related_paths)
        if trace_entry.tags:
            entry["tags"] = list(trace_entry.tags)
        if trace_entry.notes is not None:
            entry["notes"] = trace_entry.notes
        return entry


def _group_by_trace[T: _TraceLinkedEntry](entries: tuple[T, ...]) -> dict[str, tuple[T, ...]]:
    grouped: dict[str, list[T]] = {}
    for entry in entries:
        trace_id = entry.trace_id
        if trace_id is None:
            continue
        grouped.setdefault(trace_id, []).append(entry)
    return {trace_id: tuple(values) for trace_id, values in grouped.items()}


def _feature_designs(
    entries: tuple[DesignDocumentIndexEntry, ...],
) -> tuple[DesignDocumentIndexEntry, ...]:
    return tuple(entry for entry in entries if entry.family == "feature_design")


def _implementation_plans(
    entries: tuple[DesignDocumentIndexEntry, ...],
) -> tuple[DesignDocumentIndexEntry, ...]:
    return tuple(entry for entry in entries if entry.family == "implementation_plan")


def _determine_current_phase(
    *,
    trace_entry: TraceabilityEntry,
    prd_entries: tuple[PrdIndexEntry, ...],
    design_entries: tuple[DesignDocumentIndexEntry, ...],
    active_tasks: tuple[TaskIndexEntry, ...],
) -> str:
    if trace_entry.initiative_status != "active":
        return "closed"
    if active_tasks:
        return "execution"

    feature_designs = _feature_designs(design_entries)
    implementation_plans = _implementation_plans(design_entries)
    has_validation_inputs = bool(trace_entry.acceptance_ids or trace_entry.acceptance_contract_ids)
    has_evidence = bool(trace_entry.evidence_ids)

    if prd_entries and not feature_designs:
        return "prd"
    if feature_designs and not implementation_plans:
        return "design"
    if implementation_plans and not has_validation_inputs and not has_evidence:
        return "implementation_planning"
    if implementation_plans and has_validation_inputs and not has_evidence:
        return "validation"
    if has_evidence:
        return "closeout"
    if feature_designs:
        return "design"
    if prd_entries:
        return "prd"
    return "closeout"


def _key_surface_path(
    *,
    trace_entry: TraceabilityEntry,
    prd_entries: tuple[PrdIndexEntry, ...],
    design_entries: tuple[DesignDocumentIndexEntry, ...],
    decision_entries: tuple[DecisionIndexEntry, ...],
    task_entries: tuple[TaskIndexEntry, ...],
) -> str:
    if prd_entries:
        return sorted(entry.doc_path for entry in prd_entries)[0]
    feature_designs = _feature_designs(design_entries)
    if feature_designs:
        return sorted(entry.doc_path for entry in feature_designs)[0]
    implementation_plans = _implementation_plans(design_entries)
    if implementation_plans:
        return sorted(entry.doc_path for entry in implementation_plans)[0]
    if decision_entries:
        return sorted(entry.doc_path for entry in decision_entries)[0]
    if task_entries:
        return sorted(entry.doc_path for entry in task_entries)[0]
    if trace_entry.related_paths:
        return sorted(trace_entry.related_paths)[0]
    return "docs/planning/initiatives/initiative_tracking.md"


def _next_step(
    *,
    current_phase: str,
    initiative_status: str,
    active_tasks: tuple[TaskIndexEntry, ...],
    blocked_task_count: int,
    key_surface_path: str,
) -> tuple[str, str]:
    if initiative_status != "active":
        return (
            f"No further default action. Initiative is {initiative_status}.",
            key_surface_path,
        )
    if current_phase == "prd":
        return (
            (
                "Create or update a feature design so the initiative has a "
                "reviewed technical direction."
            ),
            DESIGN_DIRECTORY,
        )
    if current_phase == "design":
        return (
            (
                "Create or update an implementation plan so the approved "
                "design becomes executable work."
            ),
            IMPLEMENTATION_PLAN_DIRECTORY,
        )
    if current_phase == "implementation_planning":
        return (
            (
                "Create execution tasks and assign an owner so work can move "
                "from planning into execution."
            ),
            TASK_OPEN_DIRECTORY,
        )
    if current_phase == "execution":
        next_task_path = (
            sorted(entry.doc_path for entry in active_tasks)[0]
            if active_tasks
            else TASK_OPEN_DIRECTORY
        )
        if blocked_task_count > 0:
            return (
                (
                    "Resolve blockers on the active task set and keep task "
                    "state current before opening new follow-up work."
                ),
                next_task_path,
            )
        if any(entry.task_status in {"backlog", "ready"} for entry in active_tasks):
            return (
                (
                    "Start or continue the active task set and keep the "
                    "current task records aligned with execution progress."
                ),
                next_task_path,
            )
        if any(entry.task_status == "in_review" for entry in active_tasks):
            return (
                (
                    "Review the active task set, land any follow-up changes, "
                    "and close completed tasks explicitly."
                ),
                next_task_path,
            )
        return (
            (
                "Continue the active task set and keep planning, traceability, "
                "and derived surfaces aligned as work lands."
            ),
            next_task_path,
        )
    if current_phase == "validation":
        return (
            (
                "Run initiative validation and record durable evidence before "
                "moving the initiative into closeout."
            ),
            VALIDATE_ACCEPTANCE_COMMAND_DOC,
        )
    if current_phase == "closeout":
        return (
            (
                "Run initiative closeout or create explicit follow-up tasks "
                "before marking the initiative complete."
            ),
            CLOSEOUT_INITIATIVE_COMMAND_DOC,
        )
    return (
        "Inspect the initiative source surfaces and decide the next bounded planning step.",
        key_surface_path,
    )
