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


def _write_reference_fixture(path: Path, *, support_target: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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

            ## Canonical Upstream
            - [Example upstream](https://example.com/reference)

            ## Quick Reference or Distilled Reference
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
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    guidance_heading = "\n## Guidance" if blank_line_before_guidance else "## Guidance"
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
        - `Operational Surfaces`: `docs/standards/documentation/example_standard.md`

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
    applied_references_section = (
        """
        ## Applied References and Implications
        - docs/standards/governance/decision_capture_standard.md: keeps the
          decision aligned with the governed repository rule.

        """
        if include_applied_references
        else ""
    )
    path.write_text(
        dedent(
            f"""\
            ---
            trace_id: trace.example_decision_semantics
            id: decision.example_decision_semantics
            title: Example Decision Semantics
            summary: Exercises the decision semantic validator.
            type: decision_record
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T17:05:00Z'
            audience: shared
            authority: supporting
            ---

            # Example Decision Semantics

            ## Record Metadata
            - `Trace ID`: `trace.example_decision_semantics`
            - `Decision ID`: `decision.example_decision_semantics`
            - `Record Status`: `active`
            - `Decision Status`: `accepted`
            - `Linked PRDs`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-11T17:05:00Z`

            ## Summary
            Exercises the decision semantic validator.

            ## Decision Statement
            Keep the example small and deterministic.

            ## Trigger or Source Request
            - Added for semantic validation coverage.

            ## Current Context and Constraints
            - The example fixture must be valid apart from the targeted issue.

            {applied_references_section}## Affected Surfaces
            - `docs/planning/decisions/example_decision_semantics.md`

            ## Options Considered
            ### Option 1
            - Minimal fixture.
            - Strength.
            - Tradeoff.

            ### Option 2
            - Larger fixture.
            - Strength.
            - Tradeoff.

            ## Chosen Outcome
            Use the minimal fixture.

            ## Rationale and Tradeoffs
            - Small fixture: easier to keep deterministic.

            ## Consequences and Follow-Up Impacts
            - Tests will fail only for the intended issue.

            ## Risks, Dependencies, and Assumptions
            - The validator rules stay aligned with governed decision expectations.

            ## References
            - docs/standards/governance/decision_capture_standard.md
            """
        ),
        encoding="utf-8",
    )


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
