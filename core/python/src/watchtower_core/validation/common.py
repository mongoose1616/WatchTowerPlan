"""Shared helpers for registry-backed validation services."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import ValidationError

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.errors import ValidationExecutionError
from watchtower_core.validation.models import ValidationIssue


def format_error_location(error: ValidationError) -> str | None:
    """Return a stable dotted path for a schema validation error."""
    if not error.absolute_path:
        return None

    parts: list[str] = []
    for item in error.absolute_path:
        if isinstance(item, int):
            if not parts:
                parts.append(f"[{item}]")
            else:
                parts[-1] = f"{parts[-1]}[{item}]"
            continue
        parts.append(str(item))
    return ".".join(parts)


def matches_applies_to(relative_path: str, pattern: str) -> bool:
    """Return whether a repository-relative path matches a validator applies_to pattern."""
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return relative_path == prefix.rstrip("/") or relative_path.startswith(prefix)
    return PurePosixPath(relative_path).match(pattern)


def resolve_target_path(
    loader: ControlPlaneLoader,
    path: str | Path,
) -> tuple[Path, str, str | None]:
    """Resolve a user-supplied path to an existing file plus repo-relative metadata."""
    raw_path = Path(path)
    if raw_path.is_absolute():
        resolved_path = raw_path.resolve()
    else:
        resolved_path = (loader.repo_root / raw_path).resolve()

    if not resolved_path.exists() or not resolved_path.is_file():
        raise ValidationExecutionError(f"Target file does not exist: {path}")

    try:
        relative_path = resolved_path.relative_to(loader.repo_root).as_posix()
        return resolved_path, relative_path, relative_path
    except ValueError:
        return resolved_path, str(resolved_path), None


def iter_schema_validation_issues(
    loader: ControlPlaneLoader,
    instance: dict[str, Any],
    schema_ids: tuple[str, ...],
) -> list[ValidationIssue]:
    """Validate one object against one or more schema IDs and return structured issues."""
    issues: list[ValidationIssue] = []
    for schema_id in schema_ids:
        validator = loader.schema_store.build_validator(schema_id)
        errors = sorted(
            validator.iter_errors(instance),
            key=lambda error: (
                list(error.absolute_path),
                list(error.absolute_schema_path),
                error.message,
            ),
        )
        issues.extend(
            ValidationIssue(
                code="schema_validation_error",
                message=error.message,
                location=format_error_location(error),
                schema_id=schema_id,
            )
            for error in errors
        )
    return issues
