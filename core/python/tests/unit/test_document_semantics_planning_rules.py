from __future__ import annotations

from pathlib import Path

from tests.unit.document_semantics_fixtures import (
    copy_control_plane_repo,
    write_decision_fixture,
    write_feature_design_fixture,
    write_implementation_plan_fixture,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import DocumentSemanticsValidationService


def test_document_semantics_validation_rejects_heading_after_list_without_blank_line_in_decision(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    decision_path = repo_root / "docs/planning/decisions/example_decision_semantics.md"
    write_decision_fixture(decision_path, include_applied_references=True)
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


def test_document_semantics_validation_rejects_missing_decision_applied_references(
    tmp_path: Path,
) -> None:
    repo_root = copy_control_plane_repo(tmp_path)
    decision_path = repo_root / "docs/planning/decisions/example_decision_semantics.md"
    write_decision_fixture(decision_path, include_applied_references=False)

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
    repo_root = copy_control_plane_repo(tmp_path)
    feature_path = repo_root / "docs/planning/design/features/example_feature_semantics.md"
    write_feature_design_fixture(feature_path)

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
    repo_root = copy_control_plane_repo(tmp_path)
    plan_path = repo_root / "docs/planning/design/implementation/example_plan_semantics.md"
    write_implementation_plan_fixture(plan_path)

    service = DocumentSemanticsValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("docs/planning/design/implementation/example_plan_semantics.md")

    assert result.passed is False
    assert result.validator_id == "validator.documentation.implementation_plan_semantics"
    assert result.issue_count == 1
    assert "missing required section: Internal Standards and Canonical References Applied" in (
        result.issues[0].message
    )
