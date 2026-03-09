from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import FrontMatterValidationService, ValidationSelectionError

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_front_matter_validation_auto_selects_standard_validator() -> None:
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("docs/standards/metadata/front_matter_standard.md")

    assert result.passed is True
    assert result.validator_id == "validator.documentation.standard_front_matter"
    assert result.issue_count == 0


def test_front_matter_validation_auto_selects_feature_design_validator() -> None:
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("docs/planning/design/features/python_validator_execution.md")

    assert result.passed is True
    assert result.validator_id == "validator.documentation.feature_design_front_matter"
    assert result.issue_count == 0


def test_front_matter_validation_rejects_unsupported_path_without_validator() -> None:
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError):
        service.validate("docs/commands/core_python/watchtower_core.md")


def test_front_matter_validation_reports_missing_front_matter(tmp_path: Path) -> None:
    document_path = tmp_path / "missing_front_matter.md"
    document_path.write_text("# Missing front matter\n", encoding="utf-8")
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        document_path,
        validator_id="validator.documentation.standard_front_matter",
    )

    assert result.passed is False
    assert result.issue_count == 1
    assert result.issues[0].code == "front_matter_missing"
