from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import (
    DocumentSemanticsValidationService,
    ValidationSelectionError,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


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
