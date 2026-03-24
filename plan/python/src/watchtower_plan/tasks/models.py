"""Public task lifecycle request and result models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TaskCreateParams:
    """Inputs for one task creation operation."""

    task_id: str
    title: str
    summary: str
    task_kind: str
    priority: str
    owner: str
    scope_items: tuple[str, ...]
    done_when_items: tuple[str, ...]
    task_status: str = "planned"
    trace_id: str | None = None
    applies_to: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    governing_document_paths: tuple[str, ...] = ()
    file_stem: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskUpdateParams:
    """Inputs for one task update operation."""

    task_id: str
    title: str | None = None
    summary: str | None = None
    task_kind: str | None = None
    priority: str | None = None
    owner: str | None = None
    task_status: str | None = None
    trace_id: str | None = None
    clear_trace_id: bool = False
    scope_items: tuple[str, ...] | None = None
    done_when_items: tuple[str, ...] | None = None
    applies_to: tuple[str, ...] | None = None
    clear_applies_to: bool = False
    governing_document_paths: tuple[str, ...] | None = None
    clear_governing_document_paths: bool = False
    related_ids: tuple[str, ...] | None = None
    clear_related_ids: bool = False
    depends_on: tuple[str, ...] | None = None
    clear_depends_on: bool = False
    blocked_by: tuple[str, ...] | None = None
    clear_blocked_by: bool = False
    file_stem: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskTransitionParams:
    """Inputs for one task handoff or phase-transition operation."""

    task_id: str
    task_status: str
    next_owner: str | None = None
    depends_on: tuple[str, ...] | None = None
    clear_depends_on: bool = False
    blocked_by: tuple[str, ...] | None = None
    clear_blocked_by: bool = False
    file_stem: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskMutationResult:
    """Result summary for one task lifecycle command."""

    task_id: str
    title: str
    summary: str
    trace_id: str | None
    task_status: str
    task_kind: str
    priority: str
    owner: str
    updated_at: str
    doc_path: str
    previous_doc_path: str | None
    moved: bool
    changed: bool
    wrote: bool
    coordination_refreshed: bool
    closeout_recommended: bool
