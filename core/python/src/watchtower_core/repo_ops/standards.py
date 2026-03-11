"""Helpers for governed standard documents and their operationalization metadata."""

from __future__ import annotations

import re
from pathlib import Path

from watchtower_core.adapters import (
    extract_metadata_bullets,
    normalize_repo_path_reference,
    split_semicolon_list,
)
from watchtower_core.repo_ops.planning_documents import ordered_unique

STANDARD_OPERATIONALIZATION_SECTION = "Operationalization"
STANDARD_OPERATIONALIZATION_MODES_LABEL = "Modes"
STANDARD_OPERATIONALIZATION_PATHS_LABEL = "Operational Surfaces"
_STANDARD_MODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def parse_standard_operationalization(
    relative_path: str,
    section: str | None,
    repo_root: Path,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Parse the required operationalization metadata from one standard document."""
    if section is None:
        raise ValueError(
            f"{relative_path} is missing required section: {STANDARD_OPERATIONALIZATION_SECTION}"
        )

    metadata = extract_metadata_bullets(section)
    modes = _parse_standard_modes(relative_path, metadata)
    operationalization_paths = _parse_standard_paths(relative_path, metadata, repo_root)
    return modes, operationalization_paths


def _parse_standard_modes(
    relative_path: str,
    metadata: dict[str, str],
) -> tuple[str, ...]:
    values = _required_metadata_values(
        relative_path,
        metadata,
        STANDARD_OPERATIONALIZATION_MODES_LABEL,
    )
    modes = ordered_unique(values)
    invalid = [value for value in modes if _STANDARD_MODE_PATTERN.fullmatch(value) is None]
    if invalid:
        joined = ", ".join(invalid)
        raise ValueError(
            f"{relative_path} has unsupported operationalization mode values: {joined}"
        )
    return modes


def _parse_standard_paths(
    relative_path: str,
    metadata: dict[str, str],
    repo_root: Path,
) -> tuple[str, ...]:
    raw_values = _required_metadata_values(
        relative_path,
        metadata,
        STANDARD_OPERATIONALIZATION_PATHS_LABEL,
    )
    paths: list[str] = []
    for value in raw_values:
        normalized = normalize_repo_path_reference(value, repo_root)
        if normalized is None:
            raise ValueError(
                f"{relative_path} operationalization surface must be a valid repository path: "
                f"{value}"
            )
        paths.append(normalized)
    return ordered_unique(tuple(paths))


def _required_metadata_values(
    relative_path: str,
    metadata: dict[str, str],
    label: str,
) -> tuple[str, ...]:
    raw_value = metadata.get(label)
    if raw_value is None:
        raise ValueError(
            f"{relative_path} is missing required metadata label in "
            f"{STANDARD_OPERATIONALIZATION_SECTION}: {label}"
        )
    values = split_semicolon_list(raw_value)
    if not values:
        raise ValueError(
            f"{relative_path} metadata label {label!r} in "
            f"{STANDARD_OPERATIONALIZATION_SECTION} must include one or more values."
        )
    return values
