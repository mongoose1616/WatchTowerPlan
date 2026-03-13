from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from tests.unit.document_semantics_fixtures import (
    copy_control_plane_repo,
    write_reference_fixture,
    write_repo_file,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import DocumentSemanticsValidationService


def test_document_semantics_validation_rejects_reference_without_canonical_upstream(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(
        reference_path,
        support_target=support_target,
        include_canonical_upstream=False,
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/references/example_reference.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "missing required sections: Canonical Upstream" in result.issues[0].message


def test_document_semantics_validation_rejects_reference_without_repository_status(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.write_text(
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

            ## Local Mapping in This Repository
            ### Why It Matters Here
            - Keep the fixture tied to one local repository surface.

            ## References
            - [support_target.md]({support_target})

            ## Updated At
            - `2026-03-11T17:35:00Z`
            """
        ),
        encoding="utf-8",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/references/example_reference.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "missing required section: Current Repository Status" in result.issues[0].message


def test_document_semantics_validation_rejects_supporting_reference_without_current_touchpoints(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(
        reference_path,
        support_target=support_target,
        include_current_touchpoints=False,
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/references/example_reference.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "Current Touchpoints is required" in result.issues[0].message


def test_document_semantics_validation_accepts_candidate_reference_without_current_touchpoints(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(
        reference_path,
        support_target=support_target,
        repository_status_line=(
            "Candidate reference. No active standard or workflow in this repository "
            "links this file directly yet."
        ),
        include_current_touchpoints=False,
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/references/example_reference.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_rejects_unapproved_reference_status_vocabulary(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(
        reference_path,
        support_target=support_target,
        repository_status_line="Experimental local use. This wording is not approved.",
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/references/example_reference.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "Current Repository Status must begin with one of" in result.issues[0].message
