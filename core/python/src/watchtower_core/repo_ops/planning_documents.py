"""Repo-specific helpers for governed planning-document services."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.adapters import (
    extract_external_urls,
    extract_metadata_bullets,
    extract_repo_path_references,
    extract_sections,
    extract_title,
    extract_updated_at_from_section,
    load_front_matter,
    load_markdown_body,
    split_semicolon_list,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader


def ordered_unique(*groups: tuple[str, ...]) -> tuple[str, ...]:
    """Return values in first-seen order with duplicates removed."""
    seen: set[str] = set()
    ordered: list[str] = []
    for group in groups:
        for value in group:
            if not value or value in seen:
                continue
            seen.add(value)
            ordered.append(value)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class PlanningDocument:
    """Parsed and validated governed planning document."""

    relative_path: str
    front_matter: dict[str, Any]
    sections: dict[str, str]
    metadata: dict[str, str]

    @property
    def trace_id(self) -> str:
        return required_front_matter_value(self.front_matter, "trace_id")

    @property
    def document_id(self) -> str:
        return required_front_matter_value(self.front_matter, "id")

    @property
    def title(self) -> str:
        return required_front_matter_value(self.front_matter, "title")

    @property
    def summary(self) -> str:
        return required_front_matter_value(self.front_matter, "summary")

    @property
    def document_type(self) -> str:
        return required_front_matter_value(self.front_matter, "type")

    @property
    def status(self) -> str:
        return required_front_matter_value(self.front_matter, "status")

    @property
    def updated_at(self) -> str:
        return required_front_matter_value(self.front_matter, "updated_at")

    def metadata_scalar(self, label: str) -> str:
        raw_value = self.metadata.get(label)
        if raw_value is None:
            raise ValueError(
                f"{self.relative_path} is missing required Record Metadata label: {label}"
            )
        values = _parse_metadata_values(raw_value, path=self.relative_path, label=label)
        if len(values) != 1:
            raise ValueError(
                f"{self.relative_path} expected one value for Record Metadata label {label}, "
                f"found {len(values)}"
            )
        return values[0]

    def metadata_ids(self, label: str, *, allowed_prefixes: tuple[str, ...]) -> tuple[str, ...]:
        raw_value = self.metadata.get(label)
        if raw_value is None:
            return ()
        values = _parse_metadata_values(raw_value, path=self.relative_path, label=label)
        for value in values:
            if not value.startswith(allowed_prefixes):
                allowed = ", ".join(allowed_prefixes)
                raise ValueError(
                    f"{self.relative_path} has unsupported ID in Record Metadata label "
                    f"{label}: {value} (expected prefixes: {allowed})"
                )
        return values

    def front_matter_list(self, key: str) -> tuple[str, ...]:
        value = self.front_matter.get(key)
        if value is None:
            return ()
        if not isinstance(value, list):
            raise ValueError(f"{self.relative_path} front matter key {key} must be a YAML list.")
        items: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(
                    f"{self.relative_path} front matter key {key} must contain only strings."
                )
            items.append(item.strip())
        return tuple(items)

    def front_matter_path_values(self) -> tuple[str, ...]:
        values = self.front_matter_list("applies_to")
        return tuple(
            value
            for value in values
            if "/" in value and value != self.relative_path
        )

    def section(self, title: str) -> str | None:
        """Return one section body when it exists."""
        return self.sections.get(title)


def required_front_matter_value(front_matter: dict[str, Any], key: str) -> str:
    """Return one required string front-matter value."""
    value = front_matter.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Front matter key {key} is missing or empty.")
    return value.strip()


def load_governed_document(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    schema_id: str,
    id_label: str,
    status_label: str,
    required_sections: tuple[str, ...] = (),
    required_explained_sections: tuple[str, ...] = (),
    require_updated_at_section: bool = False,
) -> PlanningDocument:
    """Load one governed planning document and validate its metadata alignment."""
    path = loader.repo_root / relative_path
    front_matter = load_front_matter(path)
    loader.schema_store.validate_instance(front_matter, schema_id=schema_id)

    markdown = load_markdown_body(path)
    visible_title = extract_title(markdown)
    sections = extract_sections(markdown)
    if "Record Metadata" not in sections:
        raise ValueError(f"{relative_path} is missing its required Record Metadata section.")
    if require_updated_at_section and "Updated At" not in sections:
        raise ValueError(f"{relative_path} is missing its required Updated At section.")
    missing_sections = [title for title in required_sections if title not in sections]
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{relative_path} is missing required sections: {joined}")
    validate_required_section_order(relative_path, sections, required_sections)
    for title in required_explained_sections:
        validate_explained_bullet_section(relative_path, title, sections.get(title))

    document = PlanningDocument(
        relative_path=relative_path,
        front_matter=front_matter,
        sections=sections,
        metadata=extract_metadata_bullets(sections["Record Metadata"]),
    )

    if visible_title != document.title:
        raise ValueError(
            f"{relative_path} H1 title does not match front matter title: "
            f"{visible_title!r} != {document.title!r}"
        )
    if document.metadata_scalar("Trace ID") != document.trace_id:
        raise ValueError(f"{relative_path} Record Metadata Trace ID does not match front matter.")
    if document.metadata_scalar(id_label) != document.document_id:
        raise ValueError(
            f"{relative_path} Record Metadata {id_label} does not match front matter."
        )
    if document.metadata_scalar(status_label) != document.status:
        raise ValueError(
            f"{relative_path} Record Metadata {status_label} does not match front matter."
        )
    if document.metadata_scalar("Updated At") != document.updated_at:
        raise ValueError(
            f"{relative_path} Record Metadata Updated At does not match front matter."
        )
    if "Updated At" in sections and (
        extract_updated_at_from_section(sections["Updated At"]) != document.updated_at
    ):
        raise ValueError(f"{relative_path} Updated At section does not match front matter.")

    return document


def collect_reference_indicators(
    document: PlanningDocument,
    repo_root: Path,
    *,
    internal_sections: tuple[str, ...],
    external_sections: tuple[str, ...],
) -> tuple[bool, bool, tuple[str, ...], tuple[str, ...]]:
    """Collect reference indicators from the nominated sections of one planning document."""
    internal_paths = ordered_unique(
        *(
            extract_repo_path_references(section, repo_root)
            for title in internal_sections
            if (section := document.section(title)) is not None
        )
    )
    external_urls = ordered_unique(
        *(
            extract_external_urls(section)
            for title in external_sections
            if (section := document.section(title)) is not None
        )
    )
    return (
        bool(internal_paths),
        bool(external_urls),
        internal_paths,
        external_urls,
    )


def iter_markdown_documents(
    repo_root: Path,
    relative_directory: str,
    *,
    excluded_names: set[str],
) -> tuple[str, ...]:
    """Return sorted repository-relative Markdown document paths for one directory."""
    directory = repo_root / relative_directory
    return tuple(
        path.relative_to(repo_root).as_posix()
        for path in sorted(directory.glob("*.md"))
        if path.name not in excluded_names
    )


def parse_optional_metadata_list(
    metadata: dict[str, str],
    label: str,
    *,
    path: str,
) -> tuple[str, ...]:
    """Return an optional Record Metadata list, treating `None` as empty."""
    raw_value = metadata.get(label)
    if raw_value is None:
        return ()
    return _parse_metadata_values(raw_value, path=path, label=label)


def _parse_metadata_values(raw_value: str, *, path: str, label: str) -> tuple[str, ...]:
    values = split_semicolon_list(raw_value)
    if not values:
        return ()
    if "None" in values:
        if len(values) > 1:
            raise ValueError(
                f"{path} Record Metadata label {label} mixes None with concrete values."
            )
        return ()
    return values


def validate_explained_bullet_section(
    relative_path: str,
    title: str,
    section: str | None,
) -> None:
    if section is None:
        raise ValueError(f"{relative_path} is missing required section: {title}")

    bullets = [
        line.strip()
        for line in section.splitlines()
        if line.strip().startswith("- ")
    ]
    if not bullets:
        raise ValueError(
            f"{relative_path} section {title!r} must contain one or more bullet entries."
        )
    if any(": " not in bullet for bullet in bullets):
        raise ValueError(
            f"{relative_path} section {title!r} must explain the implication of each cited "
            "source using bullet text that includes ': '."
        )


def validate_explained_bullet_section_if_present(
    relative_path: str,
    title: str,
    section: str | None,
) -> None:
    """Validate an explained-bullet section only when the section exists."""
    if section is None:
        return
    validate_explained_bullet_section(relative_path, title, section)


def validate_required_section_order(
    relative_path: str,
    sections: dict[str, str],
    required_sections: tuple[str, ...],
) -> None:
    """Ensure the required sections appear in the documented order."""
    section_order = list(sections.keys())
    previous_index = -1
    for title in required_sections:
        try:
            current_index = section_order.index(title)
        except ValueError as exc:
            raise ValueError(f"{relative_path} is missing required section: {title}") from exc
        if current_index < previous_index:
            raise ValueError(
                f"{relative_path} places required section {title!r} out of order."
            )
        previous_index = current_index
