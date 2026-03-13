"""Support helpers for governed local task lifecycle operations."""

from __future__ import annotations

import re
from collections.abc import Iterable

from watchtower_core.adapters import extract_first_paragraph, extract_updated_at_from_section
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.task_documents import (
    TASK_CLOSED_ROOT,
    TASK_FRONT_MATTER_SCHEMA_ID,
    TASK_OPEN_ROOT,
    TASK_REQUIRED_SECTIONS,
    TERMINAL_TASK_STATUSES,
    TaskDocument,
)

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


def task_documents_by_id(documents: Iterable[TaskDocument]) -> dict[str, TaskDocument]:
    """Index task documents by task ID while rejecting duplicates."""

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


def load_existing_task(
    documents: dict[str, TaskDocument],
    task_id: str,
) -> TaskDocument:
    """Load one existing task document or raise a stable error."""

    try:
        return documents[task_id]
    except KeyError as exc:
        raise ValueError(f"Unknown task ID: {task_id}") from exc


def normalize_choice(value: str, allowed: tuple[str, ...], *, label: str) -> str:
    """Validate and normalize one required enum value."""

    normalized = normalize_required_string(value, label=label)
    if normalized not in allowed:
        joined = ", ".join(allowed)
        raise ValueError(f"{label} must be one of: {joined}")
    return normalized


def pick_choice(
    value: str | None,
    *,
    current: str,
    allowed: tuple[str, ...],
    label: str,
) -> str:
    """Return the current enum value or a normalized replacement."""

    if value is None:
        return current
    return normalize_choice(value, allowed, label=label)


def pick_string(value: str | None, *, current: str, label: str) -> str:
    """Return the current string or a normalized replacement."""

    if value is None:
        return current
    return normalize_required_string(value, label=label)


def normalize_required_string(value: str, *, label: str) -> str:
    """Validate and normalize one required non-empty string."""

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} must be a non-empty string.")
    return normalized


def normalize_list(values: Iterable[str]) -> tuple[str, ...]:
    """Normalize a list of unique non-empty strings while preserving order."""

    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        candidate = normalize_required_string(value, label="list item")
        if candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)
    return tuple(normalized)


def render_bullets(items: Iterable[str], *, label: str) -> str:
    """Render one required bullet list."""

    normalized = normalize_list(items)
    if not normalized:
        raise ValueError(f"{label} requires at least one non-empty item.")
    return "\n".join(f"- {item}" for item in normalized)


def apply_optional_list_field(
    front_matter: dict[str, object],
    key: str,
    *,
    values: tuple[str, ...] | None,
    clear: bool,
) -> bool:
    """Update or clear one optional list-valued front-matter field."""

    if clear:
        if key in front_matter:
            del front_matter[key]
            return True
        return False
    if values is None:
        return False
    normalized = normalize_list(values)
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


def task_relative_path(file_stem_source: str, *, task_status: str) -> str:
    """Return the canonical task path for the current status."""

    root = TASK_CLOSED_ROOT if task_status in TERMINAL_TASK_STATUSES else TASK_OPEN_ROOT
    file_stem = slugify_file_stem(file_stem_source)
    return f"{root}/{file_stem}.md"


def ensure_available_path(
    relative_path: str,
    *,
    existing_relative_paths: set[str],
    current_relative_path: str | None = None,
) -> None:
    """Reject task writes that would collide with another task path."""

    if relative_path == current_relative_path:
        return
    if relative_path in existing_relative_paths:
        raise ValueError(f"Task document path already exists: {relative_path}")


def ordered_sections(sections: dict[str, str]) -> dict[str, str]:
    """Order task sections using the stable task-document convention."""

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


def compact_front_matter(front_matter: dict[str, object]) -> dict[str, object]:
    """Drop empty fields and normalize tuples to lists."""

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


def validate_references(
    front_matter: dict[str, object],
    *,
    existing_task_ids: set[str],
    current_task_id: str,
) -> None:
    """Validate `blocked_by` and `depends_on` task references."""

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


def validate_trace_linkage(front_matter: dict[str, object], *, relative_path: str) -> None:
    """Reject traced related IDs that would fall out of trace joins."""

    related_ids = front_matter.get("related_ids")
    if not isinstance(related_ids, list):
        return

    traced_related_ids = tuple(
        value
        for value in related_ids
        if isinstance(value, str) and value.startswith("trace.")
    )
    if not traced_related_ids:
        return

    trace_id = optional_front_matter_value(front_matter, "trace_id")
    if trace_id is None:
        raise ValueError(
            f"{relative_path} links to traced related_ids but is missing trace_id."
        )
    if trace_id not in traced_related_ids:
        joined = ", ".join(traced_related_ids)
        raise ValueError(
            f"{relative_path} trace_id {trace_id} must match one of its traced related_ids: "
            f"{joined}."
        )


def validate_rendered_task(
    loader: ControlPlaneLoader,
    front_matter: dict[str, object],
    sections: dict[str, str],
    *,
    relative_path: str,
) -> None:
    """Validate a task document against section and schema expectations."""

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
    validate_trace_linkage(front_matter, relative_path=relative_path)

    if not isinstance(front_matter.get("title"), str):
        raise ValueError(f"{relative_path} front matter title must be present.")
    loader.schema_store.validate_instance(front_matter, schema_id=TASK_FRONT_MATTER_SCHEMA_ID)


def closeout_recommended(
    documents: dict[str, TaskDocument],
    *,
    task_id: str,
    trace_id: str | None,
    task_status: str,
) -> bool:
    """Return whether all tasks for a trace are terminal after this mutation."""

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


def optional_front_matter_value(front_matter: dict[str, object], key: str) -> str | None:
    """Return one optional front-matter scalar string value."""

    value = front_matter.get(key)
    if not isinstance(value, str) or not value:
        return None
    return value


def slugify_file_stem(value: str) -> str:
    """Normalize one task title or file stem into a repo-safe filename."""

    normalized = _FILE_STEM_PATTERN.sub("_", value.casefold()).strip("_")
    if not normalized:
        raise ValueError("Task file stem resolved to an empty value.")
    return normalized
