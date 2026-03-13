"""Support helpers for planning scaffold normalization and validation."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from watchtower_core.adapters import extract_first_paragraph, extract_metadata_bullets
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_documents import (
    validate_explained_bullet_section,
)
from watchtower_core.repo_ops.planning_scaffold_rendering import (
    split_metadata_values,
)
from watchtower_core.repo_ops.planning_scaffold_specs import (
    PLAN_KIND_CHOICES,
    PlanKind,
    scaffold_spec_for_kind,
)

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


@dataclass(frozen=True, slots=True)
class RenderedDocument:
    """Rendered planning document with validation metadata."""

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


def normalize_plan_kind(value: str) -> PlanKind:
    """Validate and normalize a scaffold kind."""

    normalized = value.strip()
    if normalized not in PLAN_KIND_CHOICES:
        joined = ", ".join(PLAN_KIND_CHOICES)
        raise ValueError(f"kind must be one of: {joined}")
    return normalized  # type: ignore[return-value]


def normalize_choice(value: str, allowed: tuple[str, ...], *, label: str) -> str:
    """Validate and normalize one required enum value."""

    normalized = normalize_required_string(value, label=label)
    if normalized not in allowed:
        joined = ", ".join(allowed)
        raise ValueError(f"{label} must be one of: {joined}")
    return normalized


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


def compact_front_matter(front_matter: dict[str, object]) -> dict[str, object]:
    """Drop empty fields and normalize tuple values to lists."""

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


def ordered_front_matter(front_matter: dict[str, object]) -> dict[str, object]:
    """Order front matter using the planning-document convention."""

    ordered: dict[str, object] = {}
    for key in _PLANNING_FRONT_MATTER_KEY_ORDER:
        if key in front_matter:
            ordered[key] = front_matter[key]
    for key, value in front_matter.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def slugify_file_stem(value: str) -> str:
    """Normalize a title or stem into a repo-safe file stem."""

    normalized = _FILE_STEM_PATTERN.sub("_", value.casefold()).strip("_")
    if not normalized:
        raise ValueError("Document file stem resolved to an empty value.")
    return normalized


def scaffold_type_for_kind(kind: PlanKind) -> str:
    """Return the front-matter type for a scaffold kind."""

    return scaffold_spec_for_kind(kind).doc_type


def scaffold_schema_for_kind(kind: PlanKind) -> str:
    """Return the schema ID for a scaffold kind."""

    return scaffold_spec_for_kind(kind).schema_id


def scaffold_directory_for_kind(kind: PlanKind) -> str:
    """Return the canonical directory for a scaffold kind."""

    return scaffold_spec_for_kind(kind).directory


def default_status_for_kind(kind: PlanKind) -> str:
    """Return the default authored status for a scaffold kind."""

    return scaffold_spec_for_kind(kind).default_status


def default_authority_for_kind(kind: PlanKind) -> str:
    """Return the default authority for a scaffold kind."""

    return scaffold_spec_for_kind(kind).default_authority


def id_label_for_kind(kind: PlanKind) -> str:
    """Return the Record Metadata label for the document ID."""

    return scaffold_spec_for_kind(kind).id_label


def status_label_for_kind(kind: PlanKind) -> str:
    """Return the Record Metadata label for the document status."""

    return scaffold_spec_for_kind(kind).status_label


def validate_rendered_document(loader: ControlPlaneLoader, rendered: RenderedDocument) -> None:
    """Validate a rendered scaffold against schema and section expectations."""

    loader.schema_store.validate_instance(rendered.front_matter, schema_id=rendered.schema_id)
    spec = scaffold_spec_for_kind(rendered.kind)

    missing_sections = sorted(set(spec.required_sections).difference(rendered.sections))
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{rendered.doc_path} is missing required sections: {joined}")

    if extract_first_paragraph(rendered.sections["Summary"]) != rendered.summary:
        raise ValueError(f"{rendered.doc_path} Summary section does not match front matter.")

    metadata = extract_metadata_bullets(rendered.sections["Record Metadata"])
    validate_metadata_scalar(metadata, "Trace ID", rendered.trace_id, path=rendered.doc_path)
    validate_metadata_scalar(
        metadata,
        rendered.id_label,
        rendered.document_id,
        path=rendered.doc_path,
    )
    validate_metadata_scalar(
        metadata,
        rendered.status_label,
        rendered.status,
        path=rendered.doc_path,
    )
    validate_metadata_scalar(
        metadata,
        "Updated At",
        str(rendered.front_matter["updated_at"]),
        path=rendered.doc_path,
    )
    for label, expected in spec.constant_metadata_values:
        validate_metadata_scalar(metadata, label, expected, path=rendered.doc_path)
    for section_title in spec.required_explained_sections:
        validate_explained_bullet_section(
            rendered.doc_path,
            section_title,
            rendered.sections.get(section_title),
        )


def validate_metadata_scalar(
    metadata: dict[str, str],
    label: str,
    expected: str,
    *,
    path: str,
) -> None:
    """Validate one Record Metadata scalar value."""

    raw_value = metadata.get(label)
    if raw_value is None:
        raise ValueError(f"{path} is missing Record Metadata label: {label}")
    values = tuple(value for value in split_metadata_values(raw_value))
    if values != (expected,):
        raise ValueError(
            f"{path} Record Metadata label {label} does not match expected value {expected!r}."
        )


def ensure_available_path(loader: ControlPlaneLoader, relative_path: str) -> None:
    """Reject scaffold writes that would overwrite an existing document."""

    if (loader.repo_root / relative_path).exists():
        raise ValueError(f"Planning scaffold path already exists: {relative_path}")
