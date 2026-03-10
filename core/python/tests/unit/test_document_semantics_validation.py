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
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
        dedent(
            """\
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
            updated_at: "2026-03-10T16:45:00Z"
            audience: "shared"
            authority: "authoritative"
            ---

            # Example Standard

            ## Summary
            Defines one example standard for semantic validation tests.

            ## Purpose
            Keep the test fixture simple and valid apart from the spacing issue.

            ## Scope
            - Applies to one example fixture.

            ## Use When
            - Running semantic validation tests.

            ## Related Standards and Sources
            - [standard_md_standard.md](docs/standards/documentation/standard_md_standard.md):
              defines the expected standard-document shape.
            ## Guidance
            - Keep a blank line between a list and the next heading.

            ## Validation
            - Semantic validation should fail when the blank line is missing.

            ## Change Control
            - Update the validator and template together if this rule changes.

            ## References
            - [standard_document_template.md](docs/templates/standard_document_template.md)

            ## Updated At
            - `2026-03-10T16:45:00Z`
            """
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "separated from the preceding list by a blank line" in result.issues[0].message
