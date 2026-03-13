"""Declarative planning scaffold kind metadata and section renderers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal, Protocol

from watchtower_core.repo_ops.planning_documents import (
    DECISION_REQUIRED_EXPLAINED_SECTIONS,
    DECISION_REQUIRED_SECTIONS,
    FEATURE_DESIGN_REQUIRED_EXPLAINED_SECTIONS,
    FEATURE_DESIGN_REQUIRED_SECTIONS,
    IMPLEMENTATION_PLAN_REQUIRED_EXPLAINED_SECTIONS,
    IMPLEMENTATION_PLAN_REQUIRED_SECTIONS,
    PRD_REQUIRED_SECTIONS,
)
from watchtower_core.repo_ops.planning_scaffold_rendering import (
    render_bullets,
    render_metadata,
    render_numbered,
    render_references,
)

PlanKind = Literal["prd", "feature-design", "implementation-plan", "decision"]


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


SectionRenderer = Callable[[dict[str, object], PlanScaffoldLike], dict[str, str]]


@dataclass(frozen=True, slots=True)
class PlanningScaffoldSpec:
    """One planning scaffold kind definition."""

    kind: PlanKind
    doc_type: str
    schema_id: str
    directory: str
    default_status: str
    default_authority: str
    id_label: str
    status_label: str
    required_sections: tuple[str, ...]
    required_explained_sections: tuple[str, ...]
    constant_metadata_values: tuple[tuple[str, str], ...]
    render_sections: SectionRenderer


def trace_suffix(trace_id: str) -> str:
    """Return the trace suffix used for derived IDs."""

    normalized = trace_id.strip()
    if not normalized:
        raise ValueError("trace_id must be a non-empty string.")
    return normalized.removeprefix("trace.")


def scaffold_spec_for_kind(kind: PlanKind) -> PlanningScaffoldSpec:
    """Return the declarative spec for one scaffold kind."""

    return _PLAN_SCAFFOLD_SPECS[kind]


def render_sections(
    kind: PlanKind,
    front_matter: dict[str, object],
    params: PlanScaffoldLike,
) -> dict[str, str]:
    """Render the default section set for a scaffold kind."""

    return scaffold_spec_for_kind(kind).render_sections(front_matter, params)


def _metadata_section(*items: tuple[str, tuple[str, ...]]) -> str:
    return "\n".join(render_metadata(label, values) for label, values in items)


def _render_prd_sections(
    front_matter: dict[str, object],
    params: PlanScaffoldLike,
) -> dict[str, str]:
    trace_id = str(front_matter["trace_id"])
    trace_id_suffix = trace_suffix(trace_id)
    updated_at = str(front_matter["updated_at"])
    status = str(front_matter["status"])
    document_id = str(front_matter["id"])
    summary = str(front_matter["summary"])
    return {
        "Record Metadata": _metadata_section(
            ("Trace ID", (trace_id,)),
            ("PRD ID", (document_id,)),
            ("Status", (status,)),
            ("Linked Decisions", params.linked_decision_ids),
            ("Linked Designs", params.linked_design_ids),
            ("Linked Implementation Plans", params.linked_plan_ids),
            ("Updated At", (updated_at,)),
        ),
        "Summary": summary,
        "Problem Statement": "<Describe the problem this PRD exists to solve.>",
        "Goals": render_bullets((), placeholder="<Primary goal>"),
        "Non-Goals": render_bullets((), placeholder="<Non-goal>"),
        "Requirements": f"- `req.{trace_id_suffix}.001`: <Requirement>",
        "Acceptance Criteria": f"- `ac.{trace_id_suffix}.001`: <Acceptance criterion>",
        "Risks and Dependencies": render_bullets((), placeholder="<Risk or dependency>"),
        "References": render_references(params.references),
    }


def _render_feature_design_sections(
    front_matter: dict[str, object],
    params: PlanScaffoldLike,
) -> dict[str, str]:
    trace_id = str(front_matter["trace_id"])
    updated_at = str(front_matter["updated_at"])
    status = str(front_matter["status"])
    document_id = str(front_matter["id"])
    summary = str(front_matter["summary"])
    return {
        "Record Metadata": _metadata_section(
            ("Trace ID", (trace_id,)),
            ("Design ID", (document_id,)),
            ("Design Status", (status,)),
            ("Linked PRDs", params.linked_prd_ids),
            ("Linked Decisions", params.linked_decision_ids),
            ("Linked Implementation Plans", params.linked_plan_ids),
            ("Updated At", (updated_at,)),
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


def _render_implementation_plan_sections(
    front_matter: dict[str, object],
    params: PlanScaffoldLike,
) -> dict[str, str]:
    trace_id = str(front_matter["trace_id"])
    updated_at = str(front_matter["updated_at"])
    status = str(front_matter["status"])
    document_id = str(front_matter["id"])
    summary = str(front_matter["summary"])
    return {
        "Record Metadata": _metadata_section(
            ("Trace ID", (trace_id,)),
            ("Plan ID", (document_id,)),
            ("Plan Status", (status,)),
            ("Linked PRDs", params.linked_prd_ids),
            ("Linked Decisions", params.linked_decision_ids),
            ("Source Designs", params.linked_design_ids),
            ("Linked Acceptance Contracts", params.linked_acceptance_ids),
            ("Updated At", (updated_at,)),
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


def _render_decision_sections(
    front_matter: dict[str, object],
    params: PlanScaffoldLike,
) -> dict[str, str]:
    trace_id = str(front_matter["trace_id"])
    updated_at = str(front_matter["updated_at"])
    status = str(front_matter["status"])
    document_id = str(front_matter["id"])
    summary = str(front_matter["summary"])
    return {
        "Record Metadata": _metadata_section(
            ("Trace ID", (trace_id,)),
            ("Decision ID", (document_id,)),
            ("Record Status", (status,)),
            ("Decision Status", ("proposed",)),
            ("Linked PRDs", params.linked_prd_ids),
            ("Linked Designs", params.linked_design_ids),
            ("Linked Implementation Plans", params.linked_plan_ids),
            ("Updated At", (updated_at,)),
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
            placeholder=(
                "<PRD, design, plan, standard, workflow, or implementation path affected.>"
            ),
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


_PLAN_SCAFFOLD_SPECS: dict[PlanKind, PlanningScaffoldSpec] = {
    "prd": PlanningScaffoldSpec(
        kind="prd",
        doc_type="prd",
        schema_id="urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        directory="docs/planning/prds",
        default_status="active",
        default_authority="authoritative",
        id_label="PRD ID",
        status_label="Status",
        required_sections=("Record Metadata", *PRD_REQUIRED_SECTIONS),
        required_explained_sections=(),
        constant_metadata_values=(),
        render_sections=_render_prd_sections,
    ),
    "feature-design": PlanningScaffoldSpec(
        kind="feature-design",
        doc_type="feature_design",
        schema_id=("urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1"),
        directory="docs/planning/design/features",
        default_status="draft",
        default_authority="authoritative",
        id_label="Design ID",
        status_label="Design Status",
        required_sections=("Record Metadata", *FEATURE_DESIGN_REQUIRED_SECTIONS),
        required_explained_sections=FEATURE_DESIGN_REQUIRED_EXPLAINED_SECTIONS,
        constant_metadata_values=(),
        render_sections=_render_feature_design_sections,
    ),
    "implementation-plan": PlanningScaffoldSpec(
        kind="implementation-plan",
        doc_type="implementation_plan",
        schema_id=(
            "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1"
        ),
        directory="docs/planning/design/implementation",
        default_status="draft",
        default_authority="supporting",
        id_label="Plan ID",
        status_label="Plan Status",
        required_sections=("Record Metadata", *IMPLEMENTATION_PLAN_REQUIRED_SECTIONS),
        required_explained_sections=IMPLEMENTATION_PLAN_REQUIRED_EXPLAINED_SECTIONS,
        constant_metadata_values=(),
        render_sections=_render_implementation_plan_sections,
    ),
    "decision": PlanningScaffoldSpec(
        kind="decision",
        doc_type="decision_record",
        schema_id="urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1",
        directory="docs/planning/decisions",
        default_status="active",
        default_authority="supporting",
        id_label="Decision ID",
        status_label="Record Status",
        required_sections=("Record Metadata", *DECISION_REQUIRED_SECTIONS),
        required_explained_sections=DECISION_REQUIRED_EXPLAINED_SECTIONS,
        constant_metadata_values=(("Decision Status", "proposed"),),
        render_sections=_render_decision_sections,
    ),
}

PLAN_KIND_CHOICES: tuple[PlanKind, ...] = tuple(_PLAN_SCAFFOLD_SPECS)
