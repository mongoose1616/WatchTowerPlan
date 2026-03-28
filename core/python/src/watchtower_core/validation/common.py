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
        prefix = pattern[:-3].rstrip("/")
        if any(token in prefix for token in "*?[]"):
            path = PurePosixPath(relative_path)
            candidates = (path, *path.parents)
            return any(
                str(candidate) != "." and PurePosixPath(candidate).match(prefix)
                for candidate in candidates
            )
        return relative_path == prefix or relative_path.startswith(f"{prefix}/")
    return PurePosixPath(relative_path).match(pattern)


def is_schema_definition_path(relative_path: str) -> bool:
    """Return whether a repository-relative path names a JSON Schema definition file."""

    return PurePosixPath(relative_path).name.endswith(".schema.json")


def artifact_pattern_match_score(
    relative_path: str,
    pattern: str,
) -> tuple[int, int, int, int, int] | None:
    """Return a specificity score for one matching artifact validator pattern."""

    if not matches_applies_to(relative_path, pattern):
        return None
    if is_schema_definition_path(relative_path) and ".schema.json" not in pattern:
        return None

    wildcard_count = sum(pattern.count(token) for token in "*?[")
    literal_length = len("".join(ch for ch in pattern if ch not in "*?[]"))
    path_depth = len(PurePosixPath(pattern).parts)
    exact_match = int(not any(token in pattern for token in "*?[]"))
    schema_explicit = int(".schema.json" in pattern)
    return (
        exact_match,
        schema_explicit,
        literal_length,
        path_depth,
        -wildcard_count,
    )


def resolve_target_path(
    loader: ControlPlaneLoader,
    path: str | Path,
) -> tuple[Path, str, str | None]:
    """Resolve a user-supplied path to an existing file plus repo-relative metadata."""
    raw_path = Path(path)
    if raw_path.is_absolute():
        resolved_path = raw_path.resolve()
    else:
        resolved_path = loader.resolve_path(raw_path.as_posix()).resolve()

    if not resolved_path.exists() or not resolved_path.is_file():
        raise ValidationExecutionError(f"Target file does not exist: {path}")

    try:
        relative_path = loader.workspace_config.logical_path_for(resolved_path)
    except ValueError:
        return resolved_path, str(resolved_path), None
    return resolved_path, relative_path, relative_path


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


def discover_repository_targets(
    loader: ControlPlaneLoader,
    patterns: tuple[str, ...],
    *,
    suffixes: tuple[str, ...],
) -> tuple[str, ...]:
    """Resolve repository-local validator patterns into stable target paths."""

    ordered_targets: list[str] = []
    seen_targets: set[str] = set()
    for pattern in patterns:
        if any(token in pattern for token in "*?[]"):
            candidate_paths = sorted(loader.repo_root.glob(pattern))
        else:
            resolved = loader.resolve_path(pattern)
            candidate_paths = [resolved] if resolved.exists() else []

        for candidate_path in candidate_paths:
            if not candidate_path.is_file():
                continue
            if suffixes and candidate_path.suffix not in suffixes:
                continue
            relative_path = loader.workspace_config.logical_path_for(candidate_path)
            if relative_path in seen_targets:
                continue
            seen_targets.add(relative_path)
            ordered_targets.append(relative_path)

    return tuple(ordered_targets)
