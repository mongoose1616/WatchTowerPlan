"""Schema-backed validation services for machine-readable governed artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ValidatorDefinition
from watchtower_core.validation.common import (
    iter_schema_validation_issues,
    matches_applies_to,
    resolve_target_path,
)
from watchtower_core.validation.errors import ValidationExecutionError, ValidationSelectionError
from watchtower_core.validation.models import ValidationIssue, ValidationResult


class ArtifactValidationService:
    """Validate JSON governed artifacts through registry-backed schema validators."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, path: str | Path, validator_id: str | None = None) -> ValidationResult:
        """Validate one JSON artifact through an explicit or auto-selected validator."""
        resolved_path, target_path, relative_target_path = resolve_target_path(self._loader, path)
        validator = self._resolve_validator(relative_target_path, validator_id)

        try:
            payload = self._load_json_object(resolved_path)
        except ValueError as exc:
            return ValidationResult(
                validator_id=validator.validator_id,
                target_path=target_path,
                engine=validator.engine,
                schema_ids=validator.schema_ids,
                passed=False,
                issues=(
                    ValidationIssue(
                        code="json_parse_invalid",
                        message=str(exc),
                    ),
                ),
            )

        issues = iter_schema_validation_issues(self._loader, payload, validator.schema_ids)
        return ValidationResult(
            validator_id=validator.validator_id,
            target_path=target_path,
            engine=validator.engine,
            schema_ids=validator.schema_ids,
            passed=not issues,
            issues=tuple(issues),
        )

    def _resolve_validator(
        self,
        relative_target_path: str | None,
        validator_id: str | None,
    ) -> ValidatorDefinition:
        registry = self._loader.load_validator_registry()
        if validator_id is not None:
            try:
                validator = registry.get(validator_id)
            except KeyError as exc:
                raise ValidationSelectionError(f"Unknown validator ID: {validator_id}") from exc
            return self._validate_registry_record(validator)

        if relative_target_path is None:
            raise ValidationSelectionError(
                "Auto-selection requires a repository-local path. Use --validator-id "
                "for external files."
            )

        candidates = [
            validator
            for validator in registry.validators
            if validator.artifact_kind != "documentation_front_matter"
            and validator.status == "active"
            and any(
                matches_applies_to(relative_target_path, pattern)
                for pattern in validator.applies_to
            )
        ]
        if not candidates:
            raise ValidationSelectionError(
                f"No active schema-backed artifact validator applies to {relative_target_path}."
            )
        if len(candidates) > 1:
            candidate_ids = ", ".join(sorted(candidate.validator_id for candidate in candidates))
            raise ValidationSelectionError(
                f"Multiple artifact validators apply to {relative_target_path}: {candidate_ids}"
            )
        return self._validate_registry_record(candidates[0])

    def _validate_registry_record(self, validator: ValidatorDefinition) -> ValidatorDefinition:
        if validator.status != "active":
            raise ValidationSelectionError(
                f"Validator is not active and cannot be selected: {validator.validator_id}"
            )
        if validator.artifact_kind == "documentation_front_matter":
            raise ValidationSelectionError(
                "Requested validator targets documentation front matter rather than a JSON "
                f"artifact: {validator.validator_id}"
            )
        if validator.engine != "json_schema":
            raise ValidationExecutionError(
                f"Unsupported validator engine for artifact validation: {validator.engine}"
            )
        if not validator.schema_ids:
            raise ValidationExecutionError(
                f"Validator does not declare schema IDs: {validator.validator_id}"
            )
        return validator

    def _load_json_object(self, path: Path) -> dict[str, Any]:
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON document: {exc}") from exc

        if not isinstance(loaded, dict):
            raise ValueError("JSON artifact must be a top-level object.")
        return loaded
