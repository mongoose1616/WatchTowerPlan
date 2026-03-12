"""Repo-specific helpers for governed local task documents."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from watchtower_core.adapters import (
    extract_first_paragraph,
    extract_sections,
    extract_title,
    extract_updated_at_from_section,
    load_front_matter,
    load_markdown_body,
    render_front_matter,
    replace_front_matter,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.front_matter_paths import normalize_front_matter_applies_to

TASK_FRONT_MATTER_SCHEMA_ID = "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1"
TASK_OPEN_ROOT = "docs/planning/tasks/open"
TASK_CLOSED_ROOT = "docs/planning/tasks/closed"
TASK_EXCLUDED_NAMES = {"README.md"}
TERMINAL_TASK_STATUSES = {"done", "cancelled"}
TASK_REQUIRED_SECTIONS = ("Summary", "Scope", "Done When")
TASK_FRONT_MATTER_KEY_ORDER = (
    "id",
    "trace_id",
    "title",
    "summary",
    "type",
    "status",
    "task_status",
    "task_kind",
    "priority",
    "owner",
    "updated_at",
    "github_synced_at",
    "audience",
    "authority",
    "applies_to",
    "related_ids",
    "depends_on",
    "blocked_by",
    "github_repository",
    "github_issue_number",
    "github_issue_node_id",
    "github_project_owner",
    "github_project_owner_type",
    "github_project_number",
    "github_project_item_id",
    "aliases",
    "tags",
)


@dataclass(frozen=True, slots=True)
class TaskDocument:
    """Parsed and validated local task document."""

    relative_path: str
    front_matter: dict[str, Any]
    sections: dict[str, str]

    @property
    def task_id(self) -> str:
        return _required_string(self.front_matter, "id", path=self.relative_path)

    @property
    def trace_id(self) -> str | None:
        value = self.front_matter.get("trace_id")
        if value is None:
            return None
        return _required_string(self.front_matter, "trace_id", path=self.relative_path)

    @property
    def title(self) -> str:
        return _required_string(self.front_matter, "title", path=self.relative_path)

    @property
    def summary(self) -> str:
        return _required_string(self.front_matter, "summary", path=self.relative_path)

    @property
    def status(self) -> str:
        return _required_string(self.front_matter, "status", path=self.relative_path)

    @property
    def task_status(self) -> str:
        return _required_string(self.front_matter, "task_status", path=self.relative_path)

    @property
    def task_kind(self) -> str:
        return _required_string(self.front_matter, "task_kind", path=self.relative_path)

    @property
    def priority(self) -> str:
        return _required_string(self.front_matter, "priority", path=self.relative_path)

    @property
    def owner(self) -> str:
        return _required_string(self.front_matter, "owner", path=self.relative_path)

    @property
    def updated_at(self) -> str:
        return _required_string(self.front_matter, "updated_at", path=self.relative_path)

    def list_values(self, key: str) -> tuple[str, ...]:
        value = self.front_matter.get(key)
        if value is None:
            return ()
        if not isinstance(value, list):
            raise ValueError(f"{self.relative_path} front matter key {key} must be a YAML list.")
        values: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(
                    f"{self.relative_path} front matter key {key} must contain only strings."
                )
            values.append(item.strip())
        return tuple(values)

    def optional_string(self, key: str) -> str | None:
        value = self.front_matter.get(key)
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{self.relative_path} front matter key {key} must be a string.")
        return value.strip()

    def optional_int(self, key: str) -> int | None:
        value = self.front_matter.get(key)
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError(f"{self.relative_path} front matter key {key} must be an integer.")
        return value

    @property
    def github_repository(self) -> str | None:
        return self.optional_string("github_repository")

    @property
    def github_issue_number(self) -> int | None:
        return self.optional_int("github_issue_number")

    @property
    def github_issue_node_id(self) -> str | None:
        return self.optional_string("github_issue_node_id")

    @property
    def github_project_owner(self) -> str | None:
        return self.optional_string("github_project_owner")

    @property
    def github_project_owner_type(self) -> str | None:
        return self.optional_string("github_project_owner_type")

    @property
    def github_project_number(self) -> int | None:
        return self.optional_int("github_project_number")

    @property
    def github_project_item_id(self) -> str | None:
        return self.optional_string("github_project_item_id")

    @property
    def github_synced_at(self) -> str | None:
        return self.optional_string("github_synced_at")


def iter_task_documents(
    loader: ControlPlaneLoader,
) -> tuple[TaskDocument, ...]:
    """Return all governed task documents in deterministic path order."""
    documents: list[TaskDocument] = []
    for root in (TASK_OPEN_ROOT, TASK_CLOSED_ROOT):
        directory = loader.repo_root / root
        for path in sorted(directory.glob("*.md")):
            if path.name in TASK_EXCLUDED_NAMES:
                continue
            relative_path = path.relative_to(loader.repo_root).as_posix()
            try:
                documents.append(load_task_document(loader, relative_path))
            except FileNotFoundError:
                # Task lifecycle moves can relocate a task between discovery and load.
                continue
    return tuple(documents)


def load_task_document(loader: ControlPlaneLoader, relative_path: str) -> TaskDocument:
    path = loader.repo_root / relative_path
    front_matter = load_front_matter(path)
    loader.schema_store.validate_instance(front_matter, schema_id=TASK_FRONT_MATTER_SCHEMA_ID)
    applies_to = normalize_front_matter_applies_to(
        front_matter,
        relative_path=relative_path,
        repo_root=loader.repo_root,
    )
    if applies_to:
        front_matter["applies_to"] = list(applies_to)

    markdown = load_markdown_body(path)
    visible_title = extract_title(markdown)
    sections = extract_sections(markdown)
    document = TaskDocument(
        relative_path=relative_path,
        front_matter=front_matter,
        sections=sections,
    )

    required_sections = set(TASK_REQUIRED_SECTIONS)
    missing_sections = sorted(required_sections.difference(sections))
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{relative_path} is missing required task sections: {joined}")

    if visible_title != document.title:
        raise ValueError(
            f"{relative_path} H1 title does not match front matter title: "
            f"{visible_title!r} != {document.title!r}"
        )
    summary_section = extract_first_paragraph(sections["Summary"])
    if summary_section != document.summary:
        raise ValueError(
            f"{relative_path} Summary section does not match front matter summary."
        )
    if "Updated At" in sections and (
        extract_updated_at_from_section(sections["Updated At"]) != document.updated_at
    ):
        raise ValueError(f"{relative_path} Updated At section does not match front matter.")

    is_open = relative_path.startswith(f"{TASK_OPEN_ROOT}/")
    is_closed = relative_path.startswith(f"{TASK_CLOSED_ROOT}/")
    if is_open and document.task_status in TERMINAL_TASK_STATUSES:
        raise ValueError(
            f"{relative_path} is under open/ but uses terminal task status {document.task_status}."
        )
    if is_closed and document.task_status not in TERMINAL_TASK_STATUSES:
        raise ValueError(
            f"{relative_path} is under closed/ but uses non-terminal task status "
            f"{document.task_status}."
        )

    return document


def update_task_document_front_matter(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    updates: Mapping[str, Any],
) -> bool:
    """Apply a front-matter update to one task document if any values changed."""
    path = loader.repo_root / relative_path
    current = load_front_matter(path)
    new_front_matter = dict(current)
    changed = False

    for key, value in updates.items():
        if value is None:
            if key in new_front_matter:
                del new_front_matter[key]
                changed = True
            continue
        if new_front_matter.get(key) != value:
            new_front_matter[key] = value
            changed = True

    if not changed:
        return False

    ordered_front_matter = _ordered_front_matter(new_front_matter)
    replace_front_matter(path, ordered_front_matter)
    return True


def write_task_document(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    front_matter: Mapping[str, Any],
    sections: Mapping[str, str],
) -> None:
    """Write one governed task document from front matter and rendered sections."""
    title = _required_string(dict(front_matter), "title", path=relative_path)
    ordered_front_matter = _ordered_front_matter(front_matter)
    path = loader.repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered_front_matter = render_front_matter(ordered_front_matter)
    path.write_text(
        f"---\n{rendered_front_matter}\n---\n\n{_render_task_body(title, sections)}",
        encoding="utf-8",
    )


def _ordered_front_matter(front_matter: Mapping[str, Any]) -> dict[str, Any]:
    ordered: dict[str, Any] = {}
    for key in TASK_FRONT_MATTER_KEY_ORDER:
        if key in front_matter:
            ordered[key] = front_matter[key]
    for key, value in front_matter.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def _required_string(front_matter: dict[str, Any], key: str, *, path: str) -> str:
    value = front_matter.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} front matter key {key} is missing or empty.")
    return value.strip()


def _render_task_body(title: str, sections: Mapping[str, str]) -> str:
    lines = [f"# {title}", ""]
    for section_title, section_body in sections.items():
        lines.extend((f"## {section_title}", section_body.strip(), ""))
    return "\n".join(lines).rstrip() + "\n"
