from __future__ import annotations

import json
from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import ArtifactValidationService, ValidationSelectionError

REPO_ROOT = Path(__file__).resolve().parents[4]


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


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


def test_artifact_validation_supports_external_schema_id_with_supplemental_schema_path(
    tmp_path: Path,
) -> None:
    schema_path = tmp_path / "schemas" / "external_note.v1.schema.json"
    artifact_path = tmp_path / "artifacts" / "external_note.v1.json"
    schema_id = "urn:watchtower:schema:external:artifact-validation-note:v1"
    write_json(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "External Artifact Validation Note",
            "description": "Schema used to validate an external artifact without a registry entry.",
            "type": "object",
            "properties": {"kind": {"const": "external_validation_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        artifact_path,
        {
            "kind": "external_validation_note",
        },
    )

    service = ArtifactValidationService(
        ControlPlaneLoader(
            REPO_ROOT,
            supplemental_schema_paths=(schema_path,),
        )
    )

    result = service.validate(artifact_path, schema_id=schema_id)

    assert result.passed is True
    assert result.validator_id == f"schema:{schema_id}"
    assert result.schema_ids == (schema_id,)


def test_artifact_validation_supports_external_document_schema_with_supplemental_schema_path(
    tmp_path: Path,
) -> None:
    schema_dir = tmp_path / "schemas"
    artifact_path = tmp_path / "artifacts" / "external_note.v1.json"
    schema_id = "urn:watchtower:schema:external:artifact-validation-note-auto:v1"
    write_json(
        schema_dir / "external_note_auto.v1.schema.json",
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "External Artifact Validation Note Auto",
            "description": "Schema discovered through a document $schema field.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "external_validation_note_auto"},
            },
            "required": ["$schema", "kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        artifact_path,
        {
            "$schema": schema_id,
            "kind": "external_validation_note_auto",
        },
    )

    service = ArtifactValidationService(
        ControlPlaneLoader(
            REPO_ROOT,
            supplemental_schema_paths=(schema_dir,),
        )
    )

    result = service.validate(artifact_path)

    assert result.passed is True
    assert result.validator_id == f"schema:{schema_id}"
    assert result.schema_ids == (schema_id,)


def test_artifact_validation_rejects_external_file_without_validator_or_schema(
    tmp_path: Path,
) -> None:
    artifact_path = tmp_path / "artifacts" / "external_note.v1.json"
    write_json(
        artifact_path,
        {
            "kind": "external_validation_note",
        },
    )
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(
        ValidationSelectionError,
        match="External files require --validator-id, --schema-id, or a document \\$schema",
    ):
        service.validate(artifact_path)
