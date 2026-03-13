"""Shared fixture writers for focused document-semantics validation suites."""

from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[4]


def copy_control_plane_repo(tmp_path: Path) -> Path:
    """Copy the governed control-plane subtree into a temporary repo root."""

    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def write_repo_file(path: Path, content: str = "# Placeholder\n") -> None:
    """Write one placeholder repo-local file used by semantic fixtures."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_reference_fixture(
    path: Path,
    *,
    support_target: Path,
    include_canonical_upstream: bool = True,
    repository_status_line: str = (
        "Supporting authority for current repository docs, standards, commands, "
        "or control-plane surfaces."
    ),
    include_current_touchpoints: bool = True,
) -> None:
    """Write one governed reference fixture with configurable support sections."""

    path.parent.mkdir(parents=True, exist_ok=True)
    canonical_upstream = (
        "## Canonical Upstream\n"
        "- [Example upstream](https://example.com/reference)\n\n"
        if include_canonical_upstream
        else ""
    )
    current_touchpoints = (
        f"### Current Touchpoints\n- [support_target.md]({support_target})\n\n"
        if include_current_touchpoints
        else ""
    )
    path.write_text(
        dedent(
            """\
            ---
            id: "ref.example"
            title: "Example Reference"
            summary: "Provides governed local reference coverage for semantic tests."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:35:00Z"
            audience: "shared"
            authority: "supporting"
            ---

            # Example Reference

            __CANONICAL_UPSTREAM__## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## Local Mapping in This Repository
            ### Current Repository Status
            - __REPOSITORY_STATUS_LINE__

            __CURRENT_TOUCHPOINTS__### Why It Matters Here
            - Keep the fixture tied to one local repository surface.

            ## References
            - [support_target.md](__SUPPORT_TARGET__)

            ## Updated At
            - `2026-03-11T17:35:00Z`
            """
        )
        .replace("__CANONICAL_UPSTREAM__", canonical_upstream)
        .replace("__REPOSITORY_STATUS_LINE__", repository_status_line)
        .replace("__CURRENT_TOUCHPOINTS__", current_touchpoints)
        .replace("__SUPPORT_TARGET__", str(support_target)),
        encoding="utf-8",
    )


def write_standard_fixture(
    path: Path,
    *,
    related_target: Path,
    reference_target: Path,
    blank_line_before_guidance: bool = True,
    operationalization_surfaces: tuple[str, ...] = (
        "docs/standards/documentation/example_standard.md",
    ),
) -> None:
    """Write one standard fixture with configurable formatting and path coverage."""

    path.parent.mkdir(parents=True, exist_ok=True)
    guidance_heading = "\n## Guidance" if blank_line_before_guidance else "## Guidance"
    operationalization_surface_list = "; ".join(
        f"`{surface}`" for surface in operationalization_surfaces
    )
    content = dedent(
        f"""\
        ---
        id: "std.documentation.example"
        title: "Example Standard"
        summary: "Defines one example standard for semantic validation tests."
        type: "standard"
        status: "active"
        tags:
          - "standard"
          - "documentation"
          - "example"
        owner: "repository_maintainer"
        updated_at: "2026-03-10T20:33:00Z"
        audience: "shared"
        authority: "authoritative"
        ---

        # Example Standard

        ## Summary
        Defines one example standard for semantic validation tests.

        ## Purpose
        Keep the test fixture simple and valid apart from the targeted issue.

        ## Scope
        - Applies to one example fixture.

        ## Use When
        - Running semantic validation tests.

        ## Related Standards and Sources
        - [example_reference.md]({related_target}): defines a repo-local target for tests.
        __GUIDANCE_HEADING__
        - Keep fixtures small and deterministic.

        ## Operationalization
        - `Modes`: `documentation`
        - `Operational Surfaces`: {operationalization_surface_list}

        ## Validation
        - Semantic validation should fail only for the targeted issue.

        ## Change Control
        - Update the validator and template together if this rule changes.

        ## References
        - [supporting_template.md]({reference_target})

        ## Updated At
        - `2026-03-10T20:33:00Z`
        """
    ).replace("__GUIDANCE_HEADING__", guidance_heading)
    path.write_text(content, encoding="utf-8")


def write_standard_reference_rule_fixture(
    path: Path,
    *,
    related_lines: tuple[str, ...],
    reference_lines: tuple[str, ...],
) -> None:
    """Write one standard fixture that exercises related-source accounting rules."""

    path.parent.mkdir(parents=True, exist_ok=True)
    content = dedent(
        """\
        ---
        id: "std.documentation.example"
        title: "Example Standard"
        summary: "Exercises standard reference-accounting semantics."
        type: "standard"
        status: "active"
        tags:
          - "standard"
          - "documentation"
          - "example"
        owner: "repository_maintainer"
        updated_at: "2026-03-11T17:35:00Z"
        audience: "shared"
        authority: "authoritative"
        ---

        # Example Standard

        ## Summary
        Exercises standard reference-accounting semantics.

        ## Purpose
        Keep the fixture focused on governed external-authority rules.

        ## Scope
        - Applies to one standard-semantics fixture.

        ## Use When
        - Validating governed local-reference enforcement.

        ## Related Standards and Sources
        __RELATED_LINES__

        ## Guidance
        - Keep standard reference-accounting deterministic.

        ## Operationalization
        - `Modes`: `documentation`
        - `Operational Surfaces`: `docs/standards/documentation/example_standard.md`

        ## Validation
        - Standard semantic validation should stay aligned with standard-index sync.

        ## Change Control
        - Update validation and sync helpers together if this rule changes.

        ## References
        __REFERENCE_LINES__

        ## Updated At
        - `2026-03-11T17:35:00Z`
        """
    ).replace("__RELATED_LINES__", "\n".join(related_lines)).replace(
        "__REFERENCE_LINES__",
        "\n".join(reference_lines),
    )
    path.write_text(content, encoding="utf-8")


def write_decision_fixture(
    path: Path,
    *,
    include_applied_references: bool,
) -> None:
    """Write one decision-record fixture with optional applied-reference coverage."""

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "trace_id: trace.example_decision_semantics",
        "id: decision.example_decision_semantics",
        "title: Example Decision Semantics",
        "summary: Exercises the decision semantic validator.",
        "type: decision_record",
        "status: active",
        "owner: repository_maintainer",
        "updated_at: '2026-03-11T17:05:00Z'",
        "audience: shared",
        "authority: supporting",
        "---",
        "",
        "# Example Decision Semantics",
        "",
        "## Record Metadata",
        "- `Trace ID`: `trace.example_decision_semantics`",
        "- `Decision ID`: `decision.example_decision_semantics`",
        "- `Record Status`: `active`",
        "- `Decision Status`: `accepted`",
        "- `Linked PRDs`: `None`",
        "- `Linked Designs`: `None`",
        "- `Linked Implementation Plans`: `None`",
        "- `Updated At`: `2026-03-11T17:05:00Z`",
        "",
        "## Summary",
        "Exercises the decision semantic validator.",
        "",
        "## Decision Statement",
        "Keep the example small and deterministic.",
        "",
        "## Trigger or Source Request",
        "- Added for semantic validation coverage.",
        "",
        "## Current Context and Constraints",
        "- The example fixture must be valid apart from the targeted issue.",
        "",
    ]
    if include_applied_references:
        lines.extend(
            (
                "## Applied References and Implications",
                "- docs/standards/governance/decision_capture_standard.md: keeps the decision "
                "aligned with the governed repository rule.",
                "",
            )
        )
    lines.extend(
        (
            "## Affected Surfaces",
            "- `docs/planning/decisions/example_decision_semantics.md`",
            "",
            "## Options Considered",
            "### Option 1",
            "- Minimal fixture.",
            "- Strength.",
            "- Tradeoff.",
            "",
            "### Option 2",
            "- Larger fixture.",
            "- Strength.",
            "- Tradeoff.",
            "",
            "## Chosen Outcome",
            "Use the minimal fixture.",
            "",
            "## Rationale and Tradeoffs",
            "- Small fixture: easier to keep deterministic.",
            "",
            "## Consequences and Follow-Up Impacts",
            "- Tests will fail only for the intended issue.",
            "",
            "## Risks, Dependencies, and Assumptions",
            "- The validator rules stay aligned with governed decision expectations.",
            "",
            "## References",
            "- docs/standards/governance/decision_capture_standard.md",
            "",
        )
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_feature_design_fixture(path: Path) -> None:
    """Write one feature-design fixture that omits the applied-reference section."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.example_feature_semantics
            id: design.features.example_feature_semantics
            title: Example Feature Semantics
            summary: Exercises the feature-design semantic validator.
            type: feature_design
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T20:38:54Z'
            audience: shared
            authority: authoritative
            ---

            # Example Feature Semantics

            ## Record Metadata
            - `Trace ID`: `trace.example_feature_semantics`
            - `Design ID`: `design.features.example_feature_semantics`
            - `Design Status`: `active`
            - `Linked PRDs`: `None`
            - `Linked Decisions`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-11T20:38:54Z`

            ## Summary
            Exercises the feature-design semantic validator.

            ## Source Request
            - Added for semantic validation coverage.

            ## Scope and Feature Boundary
            - Covers one feature-design fixture.

            ## Current-State Context
            - The example is valid apart from the targeted missing sections.

            ## Design Goals and Constraints
            - Keep the fixture small and deterministic.

            ## Options Considered
            ### Option 1
            - Minimal fixture.
            - Strength.
            - Tradeoff.

            ### Option 2
            - Larger fixture.
            - Strength.
            - Tradeoff.

            ## Recommended Design
            ### Architecture
            - Use the minimal fixture.

            ### Data and Interface Impacts
            - None beyond the semantic validator.

            ### Execution Flow
            1. Write the fixture.
            2. Run validation.
            3. Confirm the missing-section failure.

            ### Invariants and Failure Cases
            - The validator should fail for the missing applied-reference sections.

            ## Affected Surfaces
            - docs/planning/design/features/example_feature_semantics.md

            ## Design Guardrails
            - Keep the fixture deterministic.

            ## Risks
            - The validator could drift from the authored contract.

            ## References
            - docs/standards/documentation/feature_design_md_standard.md
            """
        ),
        encoding="utf-8",
    )


def write_implementation_plan_fixture(path: Path) -> None:
    """Write one implementation-plan fixture that omits the applied-reference section."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.example_plan_semantics
            id: design.implementation.example_plan_semantics
            title: Example Implementation Plan Semantics
            summary: Exercises the implementation-plan semantic validator.
            type: implementation_plan
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T20:38:54Z'
            audience: shared
            authority: supporting
            ---

            # Example Implementation Plan Semantics

            ## Record Metadata
            - `Trace ID`: `trace.example_plan_semantics`
            - `Plan ID`: `design.implementation.example_plan_semantics`
            - `Plan Status`: `active`
            - `Linked PRDs`: `None`
            - `Linked Decisions`: `None`
            - `Source Designs`: `design.features.example_feature_semantics`
            - `Linked Acceptance Contracts`: `None`
            - `Updated At`: `2026-03-11T20:38:54Z`

            ## Summary
            Exercises the implementation-plan semantic validator.

            ## Source Request or Design
            - docs/planning/design/features/example_feature_semantics.md

            ## Scope Summary
            - Covers one implementation-plan fixture.

            ## Assumptions and Constraints
            - Keep the fixture small and deterministic.

            ## Proposed Technical Approach
            - Use the minimal fixture.

            ## Work Breakdown
            1. Write the fixture.
            2. Run validation.
            3. Confirm the missing-section failure.

            ## Risks
            - The validator could drift from the authored contract.

            ## Validation Plan
            - Run the semantic validator.

            ## References
            - docs/standards/documentation/implementation_plan_md_standard.md
            """
        ),
        encoding="utf-8",
    )
