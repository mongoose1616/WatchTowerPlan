"""Support helpers for planning scaffold rendering and validation."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, Protocol

from watchtower_core.adapters import extract_first_paragraph, extract_metadata_bullets
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_documents import (
    validate_explained_bullet_section,
)

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
        "Applied References and Implications",
        "Affected Surfaces",
        "Options Considered",
        "Chosen Outcome",
        "Rationale and Tradeoffs",
        "Consequences and Follow-Up Impacts",
        "Risks, Dependencies, and Assumptions",
        "References",
    ),
}


class PlanScaffoldLike(Protocol):
    """Protocol for section-rendering inputs."""

    @property
    def linked_prd_ids(self) -> tuple[str, ...]: ...

    @property
    def linked_decision_ids(self) -> tuple[str, ...]: ...

    @property
    def linked_design_ids(self) -> tuple[str, ...]: ...

    @property
    def linked_plan_ids(self) -> tuple[str, ...]: ...

    @property
    def linked_acceptance_ids(self) -> tuple[str, ...]: ...

    @property
    def source_requests(self) -> tuple[str, ...]: ...

    @property
    def references(self) -> tuple[str, ...]: ...

    @property
    def applies_to(self) -> tuple[str, ...]: ...


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


def trace_suffix(trace_id: str) -> str:
    """Return the trace suffix used for derived IDs."""

    return normalize_required_string(trace_id, label="trace_id").removeprefix("trace.")


def slugify_file_stem(value: str) -> str:
    """Normalize a title or stem into a repo-safe file stem."""

    normalized = _FILE_STEM_PATTERN.sub("_", value.casefold()).strip("_")
    if not normalized:
        raise ValueError("Document file stem resolved to an empty value.")
    return normalized


def scaffold_type_for_kind(kind: PlanKind) -> str:
    """Return the front-matter type for a scaffold kind."""

    return _PLAN_KIND_TO_DOC_TYPE[kind]


def scaffold_schema_for_kind(kind: PlanKind) -> str:
    """Return the schema ID for a scaffold kind."""

    return _PLAN_KIND_TO_SCHEMA[kind]


def scaffold_directory_for_kind(kind: PlanKind) -> str:
    """Return the canonical directory for a scaffold kind."""

    return _PLAN_KIND_TO_DIRECTORY[kind]


def default_status_for_kind(kind: PlanKind) -> str:
    """Return the default authored status for a scaffold kind."""

    return _PLAN_KIND_TO_DEFAULT_STATUS[kind]


def default_authority_for_kind(kind: PlanKind) -> str:
    """Return the default authority for a scaffold kind."""

    return _PLAN_KIND_TO_DEFAULT_AUTHORITY[kind]


def id_label_for_kind(kind: PlanKind) -> str:
    """Return the Record Metadata label for the document ID."""

    return _PLAN_KIND_TO_ID_LABEL[kind]


def status_label_for_kind(kind: PlanKind) -> str:
    """Return the Record Metadata label for the document status."""

    return _PLAN_KIND_TO_STATUS_LABEL[kind]


def render_sections(
    kind: PlanKind,
    front_matter: dict[str, object],
    params: PlanScaffoldLike,
) -> dict[str, str]:
    """Render the default section set for a scaffold kind."""

    trace_id = str(front_matter["trace_id"])
    trace_id_suffix = trace_suffix(trace_id)
    updated_at = str(front_matter["updated_at"])
    status = str(front_matter["status"])
    document_id = str(front_matter["id"])
    summary = str(front_matter["summary"])

    if kind == "prd":
        return {
            "Record Metadata": "\n".join(
                (
                    render_metadata("Trace ID", (trace_id,)),
                    render_metadata("PRD ID", (document_id,)),
                    render_metadata("Status", (status,)),
                    render_metadata("Linked Decisions", params.linked_decision_ids),
                    render_metadata("Linked Designs", params.linked_design_ids),
                    render_metadata("Linked Implementation Plans", params.linked_plan_ids),
                    render_metadata("Updated At", (updated_at,)),
                )
            ),
            "Summary": summary,
            "Problem Statement": "<Describe the problem this PRD exists to solve.>",
            "Goals": render_bullets((), placeholder="<Primary goal>"),
            "Non-Goals": render_bullets((), placeholder="<Non-goal>"),
            "Requirements": f"- `req.{trace_id_suffix}.001`: <Requirement>",
            "Acceptance Criteria": f"- `ac.{trace_id_suffix}.001`: <Acceptance criterion>",
            "Risks and Dependencies": render_bullets(
                (), placeholder="<Risk or dependency>"
            ),
            "References": render_references(params.references),
        }

    if kind == "feature-design":
        return {
            "Record Metadata": "\n".join(
                (
                    render_metadata("Trace ID", (trace_id,)),
                    render_metadata("Design ID", (document_id,)),
                    render_metadata("Design Status", (status,)),
                    render_metadata("Linked PRDs", params.linked_prd_ids),
                    render_metadata("Linked Decisions", params.linked_decision_ids),
                    render_metadata("Linked Implementation Plans", params.linked_plan_ids),
                    render_metadata("Updated At", (updated_at,)),
                )
            ),
            "Summary": summary,
            "Source Request": render_bullets(
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
            "Foundations References Applied": render_bullets(
                (),
                placeholder="<Foundations source>: <Why it changes this design.>",
            ),
            "Internal Standards and Canonical References Applied": render_bullets(
                (),
                placeholder="<Internal authority>: <Why it constrains this design.>",
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
            "Affected Surfaces": render_bullets(
                params.applies_to,
                placeholder="<Docs, code paths, or governed artifacts affected.>",
            ),
            "Design Guardrails": "\n".join(
                (
                    "- <Implementation rule that must hold.>",
                    "- <Boundary the implementation must not cross.>",
                )
            ),
            "Risks": render_bullets((), placeholder="<Concrete risk or uncertainty.>"),
            "References": render_references(params.references),
        }

    if kind == "implementation-plan":
        return {
            "Record Metadata": "\n".join(
                (
                    render_metadata("Trace ID", (trace_id,)),
                    render_metadata("Plan ID", (document_id,)),
                    render_metadata("Plan Status", (status,)),
                    render_metadata("Linked PRDs", params.linked_prd_ids),
                    render_metadata("Linked Decisions", params.linked_decision_ids),
                    render_metadata("Source Designs", params.linked_design_ids),
                    render_metadata(
                        "Linked Acceptance Contracts", params.linked_acceptance_ids
                    ),
                    render_metadata("Updated At", (updated_at,)),
                )
            ),
            "Summary": summary,
            "Source Request or Design": render_bullets(
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
            "Internal Standards and Canonical References Applied": render_bullets(
                (),
                placeholder="<Internal authority>: <Why it constrains this implementation.>",
            ),
            "Proposed Technical Approach": "\n".join(
                (
                    "- <High-level implementation structure and boundaries.>",
                    "- <How the work composes with existing repository surfaces.>",
                )
            ),
            "Work Breakdown": render_numbered(
                (),
                placeholders=(
                    "<Concrete work slice or step.>",
                    "<Concrete work slice or step.>",
                    "<Concrete work slice or step.>",
                ),
            ),
            "Risks": render_bullets((), placeholder="<Concrete risk or uncertainty.>"),
            "Validation Plan": "\n".join(
                (
                    "- <How the implementation will be verified.>",
                    "- <Tests, checks, or review evidence expected.>",
                )
            ),
            "References": render_references(params.references),
        }

    return {
        "Record Metadata": "\n".join(
            (
                render_metadata("Trace ID", (trace_id,)),
                render_metadata("Decision ID", (document_id,)),
                render_metadata("Record Status", (status,)),
                render_metadata("Decision Status", ("proposed",)),
                render_metadata("Linked PRDs", params.linked_prd_ids),
                render_metadata("Linked Designs", params.linked_design_ids),
                render_metadata("Linked Implementation Plans", params.linked_plan_ids),
                render_metadata("Updated At", (updated_at,)),
            )
        ),
        "Summary": summary,
        "Decision Statement": "<State the decision in one clear sentence.>",
        "Trigger or Source Request": render_bullets(
            params.source_requests,
            placeholder="<Describe what prompted the decision.>",
        ),
        "Current Context and Constraints": render_bullets(
            (),
            placeholder="<Constraint or current-state fact.>",
        ),
        "Applied References and Implications": render_bullets(
            (),
            placeholder="<Reference or authority>: <Why it affects this decision.>",
        ),
        "Affected Surfaces": render_bullets(
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
        "Rationale and Tradeoffs": render_bullets(
            (),
            placeholder="<Why this outcome was chosen.>",
        ),
        "Consequences and Follow-Up Impacts": render_bullets(
            (),
            placeholder="<What changes next.>",
        ),
        "Risks, Dependencies, and Assumptions": render_bullets(
            (),
            placeholder="<Risk, dependency, or assumption.>",
        ),
        "References": render_references(params.references),
    }


def render_document_content(title: object, sections: dict[str, str]) -> str:
    """Render a document body from ordered sections."""

    lines = [f"# {title}", ""]
    for section_title, section_body in sections.items():
        lines.extend((f"## {section_title}", section_body.strip(), ""))
    return "\n".join(lines).rstrip() + "\n"


def validate_rendered_document(loader: ControlPlaneLoader, rendered: RenderedDocument) -> None:
    """Validate a rendered scaffold against schema and section expectations."""

    loader.schema_store.validate_instance(rendered.front_matter, schema_id=rendered.schema_id)

    required_sections = set(_PLAN_KIND_TO_REQUIRED_SECTIONS[rendered.kind])
    missing_sections = sorted(required_sections.difference(rendered.sections))
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
    if rendered.kind == "decision":
        validate_metadata_scalar(
            metadata, "Decision Status", "proposed", path=rendered.doc_path
        )
        validate_explained_bullet_section(
            rendered.doc_path,
            "Applied References and Implications",
            rendered.sections.get("Applied References and Implications"),
        )
    if rendered.kind == "feature-design":
        validate_explained_bullet_section(
            rendered.doc_path,
            "Foundations References Applied",
            rendered.sections.get("Foundations References Applied"),
        )
        validate_explained_bullet_section(
            rendered.doc_path,
            "Internal Standards and Canonical References Applied",
            rendered.sections.get("Internal Standards and Canonical References Applied"),
        )
    if rendered.kind == "implementation-plan":
        validate_explained_bullet_section(
            rendered.doc_path,
            "Internal Standards and Canonical References Applied",
            rendered.sections.get("Internal Standards and Canonical References Applied"),
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


def split_metadata_values(raw_value: str) -> tuple[str, ...]:
    """Split metadata values rendered with code formatting back into scalars."""

    cleaned = raw_value.replace("`", "")
    values = tuple(value.strip() for value in cleaned.split(";") if value.strip())
    if values == ("None",):
        return ()
    return values


def ensure_available_path(loader: ControlPlaneLoader, relative_path: str) -> None:
    """Reject scaffold writes that would overwrite an existing document."""

    if (loader.repo_root / relative_path).exists():
        raise ValueError(f"Planning scaffold path already exists: {relative_path}")


def format_code_values(values: tuple[str, ...]) -> str:
    """Render metadata values using the planning-document code style."""

    if not values:
        return "`None`"
    return "; ".join(f"`{value}`" for value in values)


def render_metadata(label: str, values: tuple[str, ...]) -> str:
    """Render one Record Metadata bullet."""

    return f"- `{label}`: {format_code_values(values)}"


def render_bullets(values: tuple[str, ...], *, placeholder: str) -> str:
    """Render a bullet list or one placeholder bullet."""

    if values:
        return "\n".join(f"- {value}" for value in values)
    return f"- {placeholder}"


def render_numbered(values: tuple[str, ...], *, placeholders: tuple[str, ...]) -> str:
    """Render a numbered list or placeholder steps."""

    if values:
        return "\n".join(f"{index}. {value}" for index, value in enumerate(values, start=1))
    return "\n".join(
        f"{index}. {value}" for index, value in enumerate(placeholders, start=1)
    )


def render_references(values: tuple[str, ...]) -> str:
    """Render references for a scaffolded planning document."""

    if values:
        return "\n".join(f"- {value}" for value in values)
    return "- <Companion document or source>"
