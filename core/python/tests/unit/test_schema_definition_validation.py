from __future__ import annotations

import json
from pathlib import Path

from tests.pack_fixture_support import REPO_ROOT
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.schema_definition import (
    DRAFT202012_SCHEMA_ID,
    SCHEMA_DEFINITION_VALIDATOR_ID,
    SchemaDefinitionValidationService,
)


def test_schema_definition_validation_passes_for_repo_schema() -> None:
    service = SchemaDefinitionValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json"
    )

    assert result.passed is True
    assert result.validator_id == SCHEMA_DEFINITION_VALIDATOR_ID
    assert result.schema_ids == (DRAFT202012_SCHEMA_ID,)


def test_schema_definition_validation_reports_invalid_schema(tmp_path: Path) -> None:
    schema_path = tmp_path / "invalid.schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": DRAFT202012_SCHEMA_ID,
                "$id": "urn:watchtower:schema:test:invalid:v1",
                "type": 42,
            }
        ),
        encoding="utf-8",
    )
    service = SchemaDefinitionValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(schema_path)

    assert result.passed is False
    assert result.validator_id == SCHEMA_DEFINITION_VALIDATOR_ID
    assert result.issue_count >= 1
    assert any(issue.location == "type" for issue in result.issues)
