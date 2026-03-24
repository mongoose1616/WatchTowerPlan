"""Draft 2020-12 metaschema validation for JSON Schema definition files."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.common import format_error_location, resolve_target_path
from watchtower_core.validation.models import ValidationIssue, ValidationResult

DRAFT202012_SCHEMA_ID = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_DEFINITION_VALIDATOR_ID = "validator.schema_definition.draft2020_12"


class SchemaDefinitionValidationService:
    """Validate one JSON Schema document against the Draft 2020-12 metaschema."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, path: str | Path) -> ValidationResult:
        """Validate one repository-local or external schema definition file."""
        resolved_path, target_path, _ = resolve_target_path(self._loader, path)

        try:
            schema_document = self._load_json_object(resolved_path)
        except ValueError as exc:
            return ValidationResult(
                validator_id=SCHEMA_DEFINITION_VALIDATOR_ID,
                target_path=target_path,
                engine="json_schema",
                schema_ids=(DRAFT202012_SCHEMA_ID,),
                passed=False,
                issues=(
                    ValidationIssue(
                        code="json_parse_invalid",
                        message=str(exc),
                    ),
                ),
            )

        metaschema_validator = Draft202012Validator(Draft202012Validator.META_SCHEMA)
        errors = sorted(
            metaschema_validator.iter_errors(schema_document),
            key=lambda error: (
                list(error.absolute_path),
                list(error.absolute_schema_path),
                error.message,
            ),
        )
        issues = tuple(
            ValidationIssue(
                code="schema_definition_validation_error",
                message=error.message,
                location=format_error_location(error),
                schema_id=DRAFT202012_SCHEMA_ID,
            )
            for error in errors
        )
        return ValidationResult(
            validator_id=SCHEMA_DEFINITION_VALIDATOR_ID,
            target_path=target_path,
            engine="json_schema",
            schema_ids=(DRAFT202012_SCHEMA_ID,),
            passed=not issues,
            issues=issues,
        )

    def _load_json_object(self, path: Path) -> dict[str, object]:
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON document: {exc}") from exc

        if not isinstance(loaded, dict):
            raise ValueError("JSON schema definition must be a top-level object.")
        return loaded
