from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import (
    DocumentSemanticsValidationService,
    ValidationSelectionError,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _write_repo_file(path: Path, content: str = "# Placeholder\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_reference_fixture(
    path: Path,
    *,
    support_target: Path,
    include_canonical_upstream: bool = True,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    canonical_upstream = (
        "## Canonical Upstream\n"
        "- [Example upstream](https://example.com/reference)\n\n"
        if include_canonical_upstream
        else ""
    )
    path.write_text(
        dedent(
            f"""\
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

            {canonical_upstream}## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## References
            - [support_target.md]({support_target})

            ## Updated At
            - `2026-03-11T17:35:00Z`
            """
        ),
        encoding="utf-8",
    )


def _write_standard_fixture(
    path: Path,
    *,
    related_target: Path,
    reference_target: Path,
    blank_line_before_guidance: bool = True,
    operationalization_surfaces: tuple[str, ...] = (
        "docs/standards/documentation/example_standard.md",
    ),
) -> None:
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
    path.write_text(
        content,
        encoding="utf-8",
    )


def _write_standard_reference_rule_fixture(
    path: Path,
    *,
    related_lines: tuple[str, ...],
    reference_lines: tuple[str, ...],
) -> None:
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


def _write_decision_fixture(
    path: Path,
    *,
    include_applied_references: bool,
) -> None:
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


def test_document_semantics_validation_auto_selects_workflow_validator() -> None:
    service = DocumentSemanticsValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("workflows/modules/code_validation.md")

    assert result.passed is True
    assert result.validator_id == "validator.documentation.workflow_semantics"
    assert result.issue_count == 0


def test_document_semantics_validation_auto_selects_standard_validator() -> None:
    service = DocumentSemanticsValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("docs/standards/documentation/workflow_md_standard.md")

    assert result.passed is True
    assert result.validator_id == "validator.documentation.standard_semantics"
    assert result.issue_count == 0


def test_document_semantics_validation_rejects_unsupported_path_without_validator() -> None:
    service = DocumentSemanticsValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError):
        service.validate("docs/commands/core_python/watchtower_core.md")


def test_document_semantics_validation_rejects_heading_after_list_without_blank_line(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    related_target = repo_root / "docs/references/example_reference.md"
    reference_target = repo_root / "docs/templates/supporting_template.md"
    _write_repo_file(related_target)
    _write_repo_file(reference_target)
    _write_standard_fixture(
        standard_path,
        related_target=related_target,
        reference_target=reference_target,
        blank_line_before_guidance=False,
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "separated from the preceding list by a blank line" in result.issues[0].message


def test_document_semantics_validation_rejects_heading_after_list_without_blank_line_in_decision(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    decision_path = repo_root / "docs/planning/decisions/example_decision_semantics.md"
    _write_decision_fixture(decision_path, include_applied_references=True)
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            "coverage.\n\n## Current Context and Constraints",
            "coverage.\n## Current Context and Constraints",
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/planning/decisions/example_decision_semantics.md")

    assert result.passed is False
    assert result.validator_id == "validator.documentation.decision_record_semantics"
    assert result.issue_count == 1
    assert "separated from the preceding list by a blank line" in result.issues[0].message


def test_document_semantics_validation_rejects_heading_after_list_without_blank_line_in_workflow(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    workflow_path = repo_root / "workflows/modules/code_validation.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(
        dedent(
            """\
            # Code Validation Workflow

            ## Purpose
            Use this workflow to test blank-line heading separation for workflows.

            ## Use When
            - Validating workflow semantics.

            ## Inputs
            - One example request.
            ## Workflow
            1. Run the workflow semantic check.

            ## Data Structure
            - One workflow fixture.

            ## Outputs
            - One validation result.

            ## Done When
            - The workflow fails for the expected heading-separation reason.
            """
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("workflows/modules/code_validation.md")

    assert result.passed is False
    assert result.validator_id == "validator.documentation.workflow_semantics"
    assert result.issue_count == 1
    assert "separated from the preceding list by a blank line" in result.issues[0].message


def test_document_semantics_validation_accepts_existing_repo_local_markdown_link(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    related_target = repo_root / "docs/references/example_reference.md"
    reference_target = repo_root / "docs/templates/supporting_template.md"
    _write_repo_file(related_target)
    _write_repo_file(reference_target)
    _write_standard_fixture(
        standard_path,
        related_target=related_target,
        reference_target=reference_target,
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_accepts_repo_relative_operationalization_glob_patterns(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    _write_repo_file(repo_root / "README.md")
    _write_repo_file(repo_root / "docs/README.md")
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    related_target = repo_root / "docs/references/example_reference.md"
    reference_target = repo_root / "docs/templates/supporting_template.md"
    _write_repo_file(related_target)
    _write_repo_file(reference_target)
    _write_standard_fixture(
        standard_path,
        related_target=related_target,
        reference_target=reference_target,
        operationalization_surfaces=("README.md", "**/README.md"),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_rejects_reference_without_canonical_upstream(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    _write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(
        reference_path,
        support_target=support_target,
        include_canonical_upstream=False,
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/references/example_reference.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "missing required sections: Canonical Upstream" in result.issues[0].message


def test_document_semantics_validation_rejects_missing_repo_local_markdown_link_in_workflow(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    workflow_path = repo_root / "workflows/modules/example_workflow.md"
    missing_target = repo_root / "docs/references/missing_reference.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(
        dedent(
            f"""\
            # Example Workflow

            ## Purpose
            Use this workflow to test repo-local Markdown link validation.

            ## Use When
            - Running semantic validation tests for workflow modules.

            ## Inputs
            - One test request.

            ## Additional Files to Load
            - [missing_reference.md]({missing_target}): should fail because the target is absent.

            ## Workflow
            1. Validate the workflow fixture.

            ## Data Structure
            - One workflow fixture.

            ## Outputs
            - One semantic-validation result.

            ## Done When
            - The workflow passes or fails for the expected reason.
            """
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("workflows/modules/example_workflow.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "repo-local Markdown link" in result.issues[0].message
    assert "missing_reference.md" in result.issues[0].message


def test_document_semantics_validation_accepts_local_reference_doc_in_related_sources(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    _write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(reference_path, support_target=support_target)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    _write_standard_reference_rule_fixture(
        standard_path,
        related_lines=(
            (
                "- [Example upstream](https://example.com/reference): external authority "
                "drives the rule."
            ),
            (
                f"- [example_reference.md]({reference_path}): governed local reference doc "
                "captures the applied implication."
            ),
        ),
        reference_lines=(
            f"- [README.md]({support_target})",
        ),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_rejects_noncanonical_directory_operationalization_path(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    _write_repo_file(support_target)
    related_target = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(related_target, support_target=support_target)
    (repo_root / "docs/commands").mkdir(parents=True, exist_ok=True)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    _write_standard_fixture(
        standard_path,
        related_target=related_target,
        reference_target=support_target,
        operationalization_surfaces=("docs/commands",),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is False
    assert result.issue_count == 1
    expected = (
        "directory operationalization surfaces must use repo-relative "
        "directory paths ending in '/'"
    )
    assert expected in result.issues[0].message


def test_document_semantics_validation_rejects_noncanonical_directory_applies_to_path(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    _write_repo_file(support_target)
    related_target = repo_root / "docs/references/example_reference.md"
    _write_reference_fixture(related_target, support_target=support_target)
    (repo_root / "docs/commands").mkdir(parents=True, exist_ok=True)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        dedent(
            f"""\
            ---
            id: "std.documentation.example"
            title: "Example Standard"
            summary: "Exercises canonical applies_to directory validation."
            type: "standard"
            status: "active"
            tags:
              - "standard"
              - "documentation"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-12T02:46:38Z"
            audience: "shared"
            authority: "authoritative"
            applies_to:
              - "docs/commands"
            ---

            # Example Standard

            ## Summary
            Exercises canonical applies_to directory validation.

            ## Purpose
            Keep the fixture focused on applies_to path semantics.

            ## Scope
            - Applies to one fixture.

            ## Use When
            - Running semantic validation tests.

            ## Related Standards and Sources
            - [example_reference.md]({related_target}): provides one governed local reference.

            ## Guidance
            - Keep applies_to directory paths canonical.

            ## Operationalization
            - `Modes`: `documentation`
            - `Operational Surfaces`: `docs/standards/documentation/example_standard.md`

            ## Validation
            - Semantic validation should reject non-canonical directory applies_to values.

            ## Change Control
            - Update validation and sync together if the rule changes.

            ## References
            - [README.md]({support_target})

            ## Updated At
            - `2026-03-12T02:46:38Z`
            """
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "directory applies_to paths must use repo-relative directory paths ending in '/'" in (
        result.issues[0].message
    )


def test_document_semantics_validation_rejects_external_authority_without_local_reference_doc(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    _write_repo_file(support_target)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    _write_standard_reference_rule_fixture(
        standard_path,
        related_lines=(
            (
                f"- [README.md]({support_target}): local repository context for the fixture."
            ),
        ),
        reference_lines=(
            "- [Example upstream](https://example.com/reference)",
        ),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "governed local reference doc under docs/references/" in result.issues[0].message


def test_document_semantics_validation_rejects_missing_decision_applied_references(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    decision_path = repo_root / "docs/planning/decisions/example_decision_semantics.md"
    _write_decision_fixture(decision_path, include_applied_references=False)

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/planning/decisions/example_decision_semantics.md")

    assert result.passed is False
    assert result.validator_id == "validator.documentation.decision_record_semantics"
    assert result.issue_count == 1
    assert "missing required sections: Applied References and Implications" in (
        result.issues[0].message
    )


def test_document_semantics_validation_rejects_missing_feature_design_applied_references(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    feature_path = repo_root / "docs/planning/design/features/example_feature_semantics.md"
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text(
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

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/planning/design/features/example_feature_semantics.md")

    assert result.passed is False
    assert result.validator_id == "validator.documentation.feature_design_semantics"
    assert result.issue_count == 1
    assert "missing required section: Foundations References Applied" in (
        result.issues[0].message
    )


def test_document_semantics_validation_rejects_missing_implementation_plan_applied_references(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    plan_path = repo_root / "docs/planning/design/implementation/example_plan_semantics.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
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

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/planning/design/implementation/example_plan_semantics.md")

    assert result.passed is False
    assert result.validator_id == "validator.documentation.implementation_plan_semantics"
    assert result.issue_count == 1
    assert "missing required section: Internal Standards and Canonical References Applied" in (
        result.issues[0].message
    )
