from __future__ import annotations

from pathlib import Path

from tests.unit.document_semantics_fixtures import (
    copy_control_plane_repo,
    write_reference_fixture,
    write_repo_file,
    write_standard_fixture,
    write_standard_reference_rule_fixture,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import DocumentSemanticsValidationService


def test_document_semantics_validation_accepts_existing_repo_local_markdown_link(
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
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_accepts_repo_relative_operationalization_glob_patterns(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    write_repo_file(repo_root / "README.md")
    write_repo_file(repo_root / "docs/README.md")
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    related_target = repo_root / "docs/references/example_reference.md"
    reference_target = repo_root / "docs/templates/supporting_template.md"
    write_repo_file(related_target)
    write_repo_file(reference_target)
    write_standard_fixture(
        standard_path,
        related_target=related_target,
        reference_target=reference_target,
        operationalization_surfaces=("README.md", "**/README.md"),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_accepts_local_reference_doc_in_related_sources(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    reference_path = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(reference_path, support_target=support_target)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    write_standard_reference_rule_fixture(
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
        reference_lines=(f"- [README.md]({support_target})",),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is True
    assert result.issue_count == 0


def test_document_semantics_validation_rejects_noncanonical_directory_operationalization_path(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    related_target = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(related_target, support_target=support_target)
    (repo_root / "docs/commands").mkdir(parents=True, exist_ok=True)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    write_standard_fixture(
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
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    related_target = repo_root / "docs/references/example_reference.md"
    write_reference_fixture(related_target, support_target=support_target)
    (repo_root / "docs/commands").mkdir(parents=True, exist_ok=True)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    standard_path.parent.mkdir(parents=True, exist_ok=True)
    standard_path.write_text(
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
""",
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
    repo_root = copy_control_plane_repo(tmp_path)
    support_target = repo_root / "docs" / "README.md"
    write_repo_file(support_target)
    standard_path = repo_root / "docs/standards/documentation/example_standard.md"
    write_standard_reference_rule_fixture(
        standard_path,
        related_lines=(
            f"- [README.md]({support_target}): local repository context for the fixture.",
        ),
        reference_lines=("- [Example upstream](https://example.com/reference)",),
    )

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/standards/documentation/example_standard.md")

    assert result.passed is False
    assert result.issue_count == 1
    assert "governed local reference doc under docs/references/" in result.issues[0].message
