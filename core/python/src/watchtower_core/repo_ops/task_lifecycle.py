"""Structured lifecycle helpers for governed local task documents."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import extract_first_paragraph, extract_updated_at_from_section
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.coordination import CoordinationSyncService
from watchtower_core.repo_ops.task_documents import (
    TASK_CLOSED_ROOT,
    TASK_FRONT_MATTER_SCHEMA_ID,
    TASK_OPEN_ROOT,
    TASK_REQUIRED_SECTIONS,
    TERMINAL_TASK_STATUSES,
    TaskDocument,
    iter_task_documents,
    write_task_document,
)
from watchtower_core.utils import utc_timestamp_now

TASK_STATUS_CHOICES = (
    "backlog",
    "ready",
    "in_progress",
    "blocked",
    "in_review",
    "done",
    "cancelled",
)
TASK_KIND_CHOICES = ("feature", "bug", "chore", "documentation", "governance", "research")
TASK_PRIORITY_CHOICES = ("critical", "high", "medium", "low")
_TASK_SECTION_ORDER = ("Summary", "Scope", "Done When")
_FILE_STEM_PATTERN = re.compile(r"[^a-z0-9]+")


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
        existing_documents = _task_documents_by_id(iter_task_documents(self._loader))
        task_id = _normalize_required_string(params.task_id, label="task_id")
        if task_id in existing_documents:
            raise ValueError(f"Task ID already exists: {task_id}")

        updated_at = params.updated_at or utc_timestamp_now()
        task_status = _normalize_choice(
            params.task_status,
            TASK_STATUS_CHOICES,
            label="task_status",
        )
        task_kind = _normalize_choice(params.task_kind, TASK_KIND_CHOICES, label="task_kind")
        priority = _normalize_choice(params.priority, TASK_PRIORITY_CHOICES, label="priority")
        title = _normalize_required_string(params.title, label="title")
        summary = _normalize_required_string(params.summary, label="summary")
        owner = _normalize_required_string(params.owner, label="owner")
        trace_id = (
            None
            if params.trace_id is None
            else _normalize_required_string(params.trace_id, label="trace_id")
        )

        front_matter = _compact_front_matter(
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
                "applies_to": _normalize_list(params.applies_to),
                "related_ids": _normalize_list(params.related_ids),
                "depends_on": _normalize_list(params.depends_on),
                "blocked_by": _normalize_list(params.blocked_by),
            }
        )
        sections = {
            "Summary": summary,
            "Scope": _render_bullets(params.scope_items, label="scope"),
            "Done When": _render_bullets(params.done_when_items, label="done-when"),
        }
        relative_path = _task_relative_path(
            params.file_stem or title,
            task_status=task_status,
        )
        _ensure_available_path(
            relative_path,
            existing_relative_paths={
                document.relative_path for document in existing_documents.values()
            },
        )
        _validate_references(
            front_matter,
            existing_task_ids=set(existing_documents),
            current_task_id=task_id,
        )
        _validate_rendered_task(
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
            closeout_recommended=_closeout_recommended(
                existing_documents,
                task_id=task_id,
                trace_id=trace_id,
                task_status=task_status,
            ),
        )

    def update(self, params: TaskUpdateParams, *, write: bool) -> TaskMutationResult:
        _validate_update_flags(params)
        documents = _task_documents_by_id(iter_task_documents(self._loader))
        document = _load_existing_task(
            documents,
            _normalize_required_string(params.task_id, label="task_id"),
        )

        front_matter = dict(document.front_matter)
        sections = dict(document.sections)
        changed = False

        title = _pick_string(params.title, current=document.title, label="title")
        if title != document.title:
            front_matter["title"] = title
            changed = True

        summary = _pick_string(params.summary, current=document.summary, label="summary")
        if summary != document.summary:
            front_matter["summary"] = summary
            sections["Summary"] = summary
            changed = True

        task_kind = _pick_choice(
            params.task_kind,
            current=document.task_kind,
            allowed=TASK_KIND_CHOICES,
            label="task_kind",
        )
        if task_kind != document.task_kind:
            front_matter["task_kind"] = task_kind
            changed = True

        priority = _pick_choice(
            params.priority,
            current=document.priority,
            allowed=TASK_PRIORITY_CHOICES,
            label="priority",
        )
        if priority != document.priority:
            front_matter["priority"] = priority
            changed = True

        owner = _pick_string(params.owner, current=document.owner, label="owner")
        if owner != document.owner:
            front_matter["owner"] = owner
            changed = True

        task_status = _pick_choice(
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
            resolved_trace_id = _normalize_required_string(params.trace_id, label="trace_id")
            if resolved_trace_id != trace_id:
                front_matter["trace_id"] = resolved_trace_id
                trace_id = resolved_trace_id
                changed = True

        changed |= _apply_optional_list_field(
            front_matter,
            "applies_to",
            values=params.applies_to,
            clear=params.clear_applies_to,
        )
        changed |= _apply_optional_list_field(
            front_matter,
            "related_ids",
            values=params.related_ids,
            clear=params.clear_related_ids,
        )
        changed |= _apply_optional_list_field(
            front_matter,
            "depends_on",
            values=params.depends_on,
            clear=params.clear_depends_on,
        )
        changed |= _apply_optional_list_field(
            front_matter,
            "blocked_by",
            values=params.blocked_by,
            clear=params.clear_blocked_by,
        )

        if params.scope_items is not None:
            sections["Scope"] = _render_bullets(params.scope_items, label="scope")
            changed = True
        if params.done_when_items is not None:
            sections["Done When"] = _render_bullets(params.done_when_items, label="done-when")
            changed = True

        file_stem = params.file_stem or Path(document.relative_path).stem
        relative_path = _task_relative_path(file_stem, task_status=task_status)
        moved = relative_path != document.relative_path
        if moved:
            changed = True

        updated_at = params.updated_at or (utc_timestamp_now() if changed else document.updated_at)
        if updated_at != document.updated_at:
            front_matter["updated_at"] = updated_at
            changed = True
            if "Updated At" in sections:
                sections["Updated At"] = f"- `{updated_at}`"

        _ensure_available_path(
            relative_path,
            existing_relative_paths={item.relative_path for item in documents.values()},
            current_relative_path=document.relative_path,
        )
        _validate_references(
            front_matter,
            existing_task_ids=set(documents),
            current_task_id=document.task_id,
        )
        _validate_rendered_task(
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
                sections=_ordered_sections(sections),
            )
            if moved:
                (self._loader.repo_root / document.relative_path).unlink()
            CoordinationSyncService(self._loader).run(write=True)

        return TaskMutationResult(
            task_id=document.task_id,
            title=str(front_matter["title"]),
            summary=str(front_matter["summary"]),
            trace_id=_optional_front_matter_value(front_matter, "trace_id"),
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
            closeout_recommended=_closeout_recommended(
                documents,
                task_id=document.task_id,
                trace_id=_optional_front_matter_value(front_matter, "trace_id"),
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


def _task_documents_by_id(documents: Iterable[TaskDocument]) -> dict[str, TaskDocument]:
    by_id: dict[str, TaskDocument] = {}
    for document in documents:
        existing = by_id.get(document.task_id)
        if existing is not None:
            raise ValueError(
                "Duplicate task ID in current task corpus: "
                f"{document.task_id} in {existing.relative_path} and {document.relative_path}"
            )
        by_id[document.task_id] = document
    return by_id


def _load_existing_task(
    documents: dict[str, TaskDocument],
    task_id: str,
) -> TaskDocument:
    try:
        return documents[task_id]
    except KeyError as exc:
        raise ValueError(f"Unknown task ID: {task_id}") from exc


def _normalize_choice(value: str, allowed: tuple[str, ...], *, label: str) -> str:
    normalized = _normalize_required_string(value, label=label)
    if normalized not in allowed:
        joined = ", ".join(allowed)
        raise ValueError(f"{label} must be one of: {joined}")
    return normalized


def _pick_choice(
    value: str | None,
    *,
    current: str,
    allowed: tuple[str, ...],
    label: str,
) -> str:
    if value is None:
        return current
    return _normalize_choice(value, allowed, label=label)


def _pick_string(value: str | None, *, current: str, label: str) -> str:
    if value is None:
        return current
    return _normalize_required_string(value, label=label)


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


def _render_bullets(items: Iterable[str], *, label: str) -> str:
    normalized = _normalize_list(items)
    if not normalized:
        raise ValueError(f"{label} requires at least one non-empty item.")
    return "\n".join(f"- {item}" for item in normalized)


def _apply_optional_list_field(
    front_matter: dict[str, object],
    key: str,
    *,
    values: tuple[str, ...] | None,
    clear: bool,
) -> bool:
    if clear:
        if key in front_matter:
            del front_matter[key]
            return True
        return False
    if values is None:
        return False
    normalized = _normalize_list(values)
    if not normalized:
        if key in front_matter:
            del front_matter[key]
            return True
        return False
    existing_values = front_matter.get(key)
    current_values = tuple(existing_values) if isinstance(existing_values, list) else ()
    if current_values != normalized:
        front_matter[key] = list(normalized)
        return True
    return False


def _task_relative_path(file_stem_source: str, *, task_status: str) -> str:
    root = TASK_CLOSED_ROOT if task_status in TERMINAL_TASK_STATUSES else TASK_OPEN_ROOT
    file_stem = _slugify_file_stem(file_stem_source)
    return f"{root}/{file_stem}.md"


def _slugify_file_stem(value: str) -> str:
    normalized = _FILE_STEM_PATTERN.sub("_", value.casefold()).strip("_")
    if not normalized:
        raise ValueError("Task file stem resolved to an empty value.")
    return normalized


def _ensure_available_path(
    relative_path: str,
    *,
    existing_relative_paths: set[str],
    current_relative_path: str | None = None,
) -> None:
    if relative_path == current_relative_path:
        return
    if relative_path in existing_relative_paths:
        raise ValueError(f"Task document path already exists: {relative_path}")


def _ordered_sections(sections: dict[str, str]) -> dict[str, str]:
    ordered: dict[str, str] = {}
    for section_title in _TASK_SECTION_ORDER:
        body = sections.get(section_title)
        if body is None:
            continue
        ordered[section_title] = body
    for section_title, body in sections.items():
        if section_title not in ordered:
            ordered[section_title] = body
    return ordered


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


def _validate_references(
    front_matter: dict[str, object],
    *,
    existing_task_ids: set[str],
    current_task_id: str,
) -> None:
    for key in ("blocked_by", "depends_on"):
        values = front_matter.get(key)
        if values is None:
            continue
        if not isinstance(values, list):
            raise ValueError(f"{key} must be a list of task IDs.")
        for value in values:
            if value == current_task_id:
                raise ValueError(f"{key} cannot reference the current task: {current_task_id}")
            if value not in existing_task_ids:
                raise ValueError(f"{key} references unknown task ID: {value}")


def _validate_rendered_task(
    loader: ControlPlaneLoader,
    front_matter: dict[str, object],
    sections: dict[str, str],
    *,
    relative_path: str,
) -> None:
    required_sections = set(TASK_REQUIRED_SECTIONS)
    missing_sections = sorted(required_sections.difference(sections))
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{relative_path} is missing required task sections: {joined}")

    summary = front_matter.get("summary")
    if not isinstance(summary, str) or extract_first_paragraph(sections["Summary"]) != summary:
        raise ValueError(f"{relative_path} Summary section does not match front matter summary.")

    updated_at = front_matter.get("updated_at")
    if "Updated At" in sections:
        if not isinstance(updated_at, str):
            raise ValueError(f"{relative_path} front matter updated_at must be a string.")
        if extract_updated_at_from_section(sections["Updated At"]) != updated_at:
            raise ValueError(f"{relative_path} Updated At section does not match front matter.")

    task_status = front_matter.get("task_status")
    if not isinstance(task_status, str):
        raise ValueError(f"{relative_path} front matter task_status must be a string.")

    if relative_path.startswith(f"{TASK_OPEN_ROOT}/") and task_status in TERMINAL_TASK_STATUSES:
        raise ValueError(
            f"{relative_path} is under open/ but uses terminal task status {task_status}."
        )
    if (
        relative_path.startswith(f"{TASK_CLOSED_ROOT}/")
        and task_status not in TERMINAL_TASK_STATUSES
    ):
        raise ValueError(
            f"{relative_path} is under closed/ but uses non-terminal task status {task_status}."
        )

    if not isinstance(front_matter.get("title"), str):
        raise ValueError(f"{relative_path} front matter title must be present.")
    loader.schema_store.validate_instance(front_matter, schema_id=TASK_FRONT_MATTER_SCHEMA_ID)


def _closeout_recommended(
    documents: dict[str, TaskDocument],
    *,
    task_id: str,
    trace_id: str | None,
    task_status: str,
) -> bool:
    if trace_id is None:
        return False
    for existing_task_id, document in documents.items():
        candidate_trace_id: str | None
        if existing_task_id == task_id:
            candidate_trace_id = trace_id
            candidate_task_status = task_status
        else:
            candidate_trace_id = document.trace_id
            candidate_task_status = document.task_status
        if candidate_trace_id != trace_id:
            continue
        if candidate_task_status not in TERMINAL_TASK_STATUSES:
            return False
    return task_status in TERMINAL_TASK_STATUSES


def _optional_front_matter_value(front_matter: dict[str, object], key: str) -> str | None:
    value = front_matter.get(key)
    if not isinstance(value, str) or not value:
        return None
    return value


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
