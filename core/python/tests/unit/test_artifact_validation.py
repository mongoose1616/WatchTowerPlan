from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import ArtifactValidationService, ValidationSelectionError

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_artifact_validation_auto_selects_acceptance_contract_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json"
    )

    assert result.passed is True
    assert result.validator_id == "validator.control_plane.acceptance_contract"
    assert result.issue_count == 0


def test_artifact_validation_auto_selects_pack_work_item_note_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        "core/control_plane/examples/valid/interfaces/pack_work_item_note.v1.example.json"
    )

    assert result.passed is True
    assert result.validator_id == "validator.interface.pack_work_item_note"
    assert result.issue_count == 0


def test_artifact_validation_rejects_unsupported_path_without_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError):
        service.validate("docs/commands/core_python/watchtower_core.md")


def test_artifact_validation_reports_invalid_json(tmp_path: Path) -> None:
    document_path = tmp_path / "invalid.json"
    document_path.write_text("{ invalid json", encoding="utf-8")
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        document_path,
        validator_id="validator.control_plane.acceptance_contract",
    )

    assert result.passed is False
    assert result.issue_count == 1
    assert result.issues[0].code == "json_parse_invalid"


def test_artifact_validation_reports_invalid_pack_interface_example() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        "core/control_plane/examples/invalid/interfaces/pack_work_item_note_missing_work_item_id.v1.example.json",
        validator_id="validator.interface.pack_work_item_note",
    )

    assert result.passed is False
    assert result.validator_id == "validator.interface.pack_work_item_note"
    assert result.issue_count >= 1
    assert any("work_item_id" in issue.message for issue in result.issues)
