from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from tests.unit.document_semantics_fixtures import (
    REPO_ROOT,
    copy_control_plane_repo,
    write_repo_file,
    write_standard_fixture,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import (
    DocumentSemanticsValidationService,
    ValidationSelectionError,
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
    repo_root = copy_control_plane_repo(tmp_path)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    related_target = repo_root / "docs/references/example_reference.md"
    reference_target = repo_root / "docs/templates/supporting_template.md"
    write_repo_file(related_target)
    write_repo_file(reference_target)
    write_standard_fixture(
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


def test_document_semantics_validation_rejects_heading_after_list_without_blank_line_in_workflow(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
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


def test_document_semantics_validation_rejects_missing_repo_local_markdown_link_in_workflow(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
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
