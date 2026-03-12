"""Structured lifecycle helpers for governed local task documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.front_matter_paths import normalize_governed_applies_to_values
from watchtower_core.repo_ops.sync.coordination import CoordinationSyncService
from watchtower_core.repo_ops.task_documents import iter_task_documents, write_task_document
from watchtower_core.repo_ops.task_lifecycle_support import (
    TASK_KIND_CHOICES,
    TASK_PRIORITY_CHOICES,
    TASK_STATUS_CHOICES,
    apply_optional_list_field,
    closeout_recommended,
    compact_front_matter,
    ensure_available_path,
    load_existing_task,
    normalize_choice,
    normalize_required_string,
    optional_front_matter_value,
    ordered_sections,
    pick_choice,
    pick_string,
    render_bullets,
    task_documents_by_id,
    task_relative_path,
    validate_references,
    validate_rendered_task,
)
from watchtower_core.utils import utc_timestamp_now


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
    task_status: str = "backlog"
    trace_id: str | None = None
    applies_to: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
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


class TaskLifecycleService:
    """Create, update, and transition governed local task records."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def create(self, params: TaskCreateParams, *, write: bool) -> TaskMutationResult:
        existing_documents = task_documents_by_id(iter_task_documents(self._loader))
        task_id = normalize_required_string(params.task_id, label="task_id")
        if task_id in existing_documents:
            raise ValueError(f"Task ID already exists: {task_id}")

        updated_at = params.updated_at or utc_timestamp_now()
        task_status = normalize_choice(
            params.task_status,
            TASK_STATUS_CHOICES,
            label="task_status",
        )
        task_kind = normalize_choice(params.task_kind, TASK_KIND_CHOICES, label="task_kind")
        priority = normalize_choice(params.priority, TASK_PRIORITY_CHOICES, label="priority")
        title = normalize_required_string(params.title, label="title")
        summary = normalize_required_string(params.summary, label="summary")
        owner = normalize_required_string(params.owner, label="owner")
        trace_id = (
            None
            if params.trace_id is None
            else normalize_required_string(params.trace_id, label="trace_id")
        )
        front_matter, sections, relative_path = self._create_document_parts(
            params,
            task_id=task_id,
            title=title,
            summary=summary,
            owner=owner,
            trace_id=trace_id,
            task_status=task_status,
            task_kind=task_kind,
            priority=priority,
            updated_at=updated_at,
        )
        ensure_available_path(
            relative_path,
            existing_relative_paths={
                document.relative_path for document in existing_documents.values()
            },
        )
        validate_references(
            front_matter,
            existing_task_ids=set(existing_documents),
            current_task_id=task_id,
        )
        validate_rendered_task(
            self._loader,
            front_matter,
            sections,
            relative_path=relative_path,
        )

        if write:
            write_task_document(
                self._loader,
                relative_path,
                front_matter=front_matter,
                sections=sections,
            )
            CoordinationSyncService(self._loader).run(write=True)

        return TaskMutationResult(
            task_id=task_id,
            title=title,
            summary=summary,
            trace_id=trace_id,
            task_status=task_status,
            task_kind=task_kind,
            priority=priority,
            owner=owner,
            updated_at=updated_at,
            doc_path=relative_path,
            previous_doc_path=None,
            moved=False,
            changed=True,
            wrote=write,
            coordination_refreshed=write,
            closeout_recommended=closeout_recommended(
                existing_documents,
                task_id=task_id,
                trace_id=trace_id,
                task_status=task_status,
            ),
        )

    def update(self, params: TaskUpdateParams, *, write: bool) -> TaskMutationResult:
        _validate_update_flags(params)
        documents = task_documents_by_id(iter_task_documents(self._loader))
        document = load_existing_task(
            documents,
            normalize_required_string(params.task_id, label="task_id"),
        )

        front_matter = dict(document.front_matter)
        sections = dict(document.sections)
        changed = False

        title = pick_string(params.title, current=document.title, label="title")
        if title != document.title:
            front_matter["title"] = title
            changed = True

        summary = pick_string(params.summary, current=document.summary, label="summary")
        if summary != document.summary:
            front_matter["summary"] = summary
            sections["Summary"] = summary
            changed = True

        task_kind = pick_choice(
            params.task_kind,
            current=document.task_kind,
            allowed=TASK_KIND_CHOICES,
            label="task_kind",
        )
        if task_kind != document.task_kind:
            front_matter["task_kind"] = task_kind
            changed = True

        priority = pick_choice(
            params.priority,
            current=document.priority,
            allowed=TASK_PRIORITY_CHOICES,
            label="priority",
        )
        if priority != document.priority:
            front_matter["priority"] = priority
            changed = True

        owner = pick_string(params.owner, current=document.owner, label="owner")
        if owner != document.owner:
            front_matter["owner"] = owner
            changed = True

        task_status = pick_choice(
            params.task_status,
            current=document.task_status,
            allowed=TASK_STATUS_CHOICES,
            label="task_status",
        )
        if task_status != document.task_status:
            front_matter["task_status"] = task_status
            changed = True

        trace_id = document.trace_id
        if params.clear_trace_id:
            if trace_id is not None:
                front_matter.pop("trace_id", None)
                trace_id = None
                changed = True
        elif params.trace_id is not None:
            resolved_trace_id = normalize_required_string(params.trace_id, label="trace_id")
            if resolved_trace_id != trace_id:
                front_matter["trace_id"] = resolved_trace_id
                trace_id = resolved_trace_id
                changed = True

        applies_to = (
            normalize_governed_applies_to_values(
                params.applies_to,
                origin=f"task update {document.task_id} applies_to",
                repo_root=self._loader.repo_root,
            )
            if params.applies_to is not None
            else None
        )
        changed |= apply_optional_list_field(
            front_matter,
            "applies_to",
            values=applies_to,
            clear=params.clear_applies_to,
        )
        changed |= apply_optional_list_field(
            front_matter,
            "related_ids",
            values=params.related_ids,
            clear=params.clear_related_ids,
        )
        changed |= apply_optional_list_field(
            front_matter,
            "depends_on",
            values=params.depends_on,
            clear=params.clear_depends_on,
        )
        changed |= apply_optional_list_field(
            front_matter,
            "blocked_by",
            values=params.blocked_by,
            clear=params.clear_blocked_by,
        )

        if params.scope_items is not None:
            sections["Scope"] = render_bullets(params.scope_items, label="scope")
            changed = True
        if params.done_when_items is not None:
            sections["Done When"] = render_bullets(params.done_when_items, label="done-when")
            changed = True

        file_stem = params.file_stem or Path(document.relative_path).stem
        relative_path = task_relative_path(file_stem, task_status=task_status)
        moved = relative_path != document.relative_path
        if moved:
            changed = True

        updated_at = params.updated_at or (utc_timestamp_now() if changed else document.updated_at)
        if updated_at != document.updated_at:
            front_matter["updated_at"] = updated_at
            changed = True
            if "Updated At" in sections:
                sections["Updated At"] = f"- `{updated_at}`"

        ensure_available_path(
            relative_path,
            existing_relative_paths={item.relative_path for item in documents.values()},
            current_relative_path=document.relative_path,
        )
        validate_references(
            front_matter,
            existing_task_ids=set(documents),
            current_task_id=document.task_id,
        )
        validate_rendered_task(
            self._loader,
            front_matter,
            sections,
            relative_path=relative_path,
        )

        if write and changed:
            write_task_document(
                self._loader,
                relative_path,
                front_matter=front_matter,
                sections=ordered_sections(sections),
            )
            if moved:
                (self._loader.repo_root / document.relative_path).unlink()
            CoordinationSyncService(self._loader).run(write=True)

        return TaskMutationResult(
            task_id=document.task_id,
            title=str(front_matter["title"]),
            summary=str(front_matter["summary"]),
            trace_id=optional_front_matter_value(front_matter, "trace_id"),
            task_status=str(front_matter["task_status"]),
            task_kind=str(front_matter["task_kind"]),
            priority=str(front_matter["priority"]),
            owner=str(front_matter["owner"]),
            updated_at=str(front_matter["updated_at"]),
            doc_path=relative_path,
            previous_doc_path=document.relative_path if moved else None,
            moved=moved,
            changed=changed,
            wrote=bool(write and changed),
            coordination_refreshed=bool(write and changed),
            closeout_recommended=closeout_recommended(
                documents,
                task_id=document.task_id,
                trace_id=optional_front_matter_value(front_matter, "trace_id"),
                task_status=str(front_matter["task_status"]),
            ),
        )

    def transition(self, params: TaskTransitionParams, *, write: bool) -> TaskMutationResult:
        return self.update(
            TaskUpdateParams(
                task_id=params.task_id,
                task_status=params.task_status,
                owner=params.next_owner,
                depends_on=params.depends_on,
                clear_depends_on=params.clear_depends_on,
                blocked_by=params.blocked_by,
                clear_blocked_by=params.clear_blocked_by,
                file_stem=params.file_stem,
                updated_at=params.updated_at,
            ),
            write=write,
        )

    def _create_document_parts(
        self,
        params: TaskCreateParams,
        *,
        task_id: str,
        title: str,
        summary: str,
        owner: str,
        trace_id: str | None,
        task_status: str,
        task_kind: str,
        priority: str,
        updated_at: str,
    ) -> tuple[dict[str, object], dict[str, str], str]:
        applies_to = normalize_governed_applies_to_values(
            params.applies_to,
            origin=f"task create {task_id} applies_to",
            repo_root=self._loader.repo_root,
        )
        front_matter = compact_front_matter(
            {
                "id": task_id,
                "trace_id": trace_id,
                "title": title,
                "summary": summary,
                "type": "task",
                "status": "active",
                "task_status": task_status,
                "task_kind": task_kind,
                "priority": priority,
                "owner": owner,
                "updated_at": updated_at,
                "audience": "shared",
                "authority": "authoritative",
                "applies_to": applies_to,
                "related_ids": params.related_ids,
                "depends_on": params.depends_on,
                "blocked_by": params.blocked_by,
            }
        )
        sections = {
            "Summary": summary,
            "Scope": render_bullets(params.scope_items, label="scope"),
            "Done When": render_bullets(params.done_when_items, label="done-when"),
        }
        relative_path = task_relative_path(
            params.file_stem or title,
            task_status=task_status,
        )
        return front_matter, sections, relative_path


def _validate_update_flags(params: TaskUpdateParams) -> None:
    _reject_conflicting_clear(params.trace_id is not None, params.clear_trace_id, key="trace_id")
    _reject_conflicting_clear(
        params.applies_to is not None,
        params.clear_applies_to,
        key="applies_to",
    )
    _reject_conflicting_clear(
        params.related_ids is not None,
        params.clear_related_ids,
        key="related_ids",
    )
    _reject_conflicting_clear(
        params.depends_on is not None,
        params.clear_depends_on,
        key="depends_on",
    )
    _reject_conflicting_clear(
        params.blocked_by is not None,
        params.clear_blocked_by,
        key="blocked_by",
    )


def _reject_conflicting_clear(has_values: bool, clear: bool, *, key: str) -> None:
    if has_values and clear:
        raise ValueError(f"Cannot provide replacement values and clear {key} in the same call.")
