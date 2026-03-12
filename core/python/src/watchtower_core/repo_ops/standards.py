"""Helpers for governed standard documents and their operationalization metadata."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from glob import has_magic
from pathlib import Path, PurePosixPath

from watchtower_core.adapters import (
    extract_external_urls,
    extract_metadata_bullets,
    extract_repo_path_references,
    normalize_repo_path_reference,
    split_semicolon_list,
)
from watchtower_core.repo_ops.planning_documents import ordered_unique

STANDARD_OPERATIONALIZATION_SECTION = "Operationalization"
STANDARD_OPERATIONALIZATION_MODES_LABEL = "Modes"
STANDARD_OPERATIONALIZATION_PATHS_LABEL = "Operational Surfaces"
_STANDARD_MODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_STANDARD_GLOB_PATTERN_ERROR = (
    "operationalization surface glob patterns must be repo-relative and match at least "
    "one live repository surface"
)


@dataclass(frozen=True, slots=True)
class StandardReferenceMetadata:
    """Reference and authority metadata derived from one standard document."""

    internal_reference_paths: tuple[str, ...]
    applied_reference_paths: tuple[str, ...]
    reference_doc_paths: tuple[str, ...]
    applied_reference_doc_paths: tuple[str, ...]
    external_reference_urls: tuple[str, ...]
    applied_external_reference_urls: tuple[str, ...]
    direct_external_urls: tuple[str, ...]
    applied_direct_external_urls: tuple[str, ...]


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


def collect_standard_reference_metadata(
    *,
    relative_path: str,
    repo_root: Path,
    source_path: Path,
    related_section: str,
    references_section: str,
    reference_urls_by_path: Mapping[str, tuple[str, ...]] | None = None,
) -> StandardReferenceMetadata:
    """Collect reference-accounting metadata for one standard document."""
    applied_reference_paths = ordered_unique(
        extract_repo_path_references(
            related_section,
            repo_root,
            source_path=source_path,
        )
    )
    internal_reference_paths = ordered_unique(
        applied_reference_paths,
        extract_repo_path_references(
            references_section,
            repo_root,
            source_path=source_path,
        ),
    )
    reference_doc_paths = tuple(
        value for value in internal_reference_paths if value.startswith("docs/references/")
    )
    applied_reference_doc_paths = tuple(
        value for value in applied_reference_paths if value.startswith("docs/references/")
    )

    direct_external_urls = ordered_unique(
        extract_external_urls(related_section),
        extract_external_urls(references_section),
    )
    applied_direct_external_urls = ordered_unique(extract_external_urls(related_section))
    reference_urls_by_path = reference_urls_by_path or {}
    transitive_external_urls = ordered_unique(
        *(
            reference_urls_by_path.get(reference_path, ())
            for reference_path in reference_doc_paths
        )
    )
    applied_transitive_external_urls = ordered_unique(
        *(
            reference_urls_by_path.get(reference_path, ())
            for reference_path in applied_reference_doc_paths
        )
    )
    external_reference_urls = ordered_unique(
        direct_external_urls,
        transitive_external_urls,
    )
    applied_external_reference_urls = ordered_unique(
        applied_direct_external_urls,
        applied_transitive_external_urls,
    )
    if direct_external_urls and not reference_doc_paths:
        raise ValueError(
            f"{relative_path} cites external authority directly but does not cite a "
            "governed local reference doc under docs/references/."
        )
    return StandardReferenceMetadata(
        internal_reference_paths=internal_reference_paths,
        applied_reference_paths=applied_reference_paths,
        reference_doc_paths=reference_doc_paths,
        applied_reference_doc_paths=applied_reference_doc_paths,
        external_reference_urls=external_reference_urls,
        applied_external_reference_urls=applied_external_reference_urls,
        direct_external_urls=direct_external_urls,
        applied_direct_external_urls=applied_direct_external_urls,
    )


def operationalization_path_matches(
    requested_path: str,
    indexed_path: str,
    repo_root: Path,
) -> bool:
    """Return whether one concrete path matches one indexed operationalization entry."""
    normalized_requested = requested_path.casefold()
    normalized_indexed = indexed_path.casefold()
    if normalized_requested == normalized_indexed:
        return True
    if operationalization_path_is_glob(indexed_path):
        return PurePosixPath(normalized_requested).match(normalized_indexed)
    if operationalization_path_is_directory(indexed_path, repo_root):
        directory_prefix = (
            normalized_indexed if normalized_indexed.endswith("/") else f"{normalized_indexed}/"
        )
        return normalized_requested.startswith(directory_prefix)
    return False


def operationalization_path_is_glob(indexed_path: str) -> bool:
    """Return whether one indexed operationalization entry is a glob pattern."""
    return has_magic(indexed_path)


def operationalization_path_is_directory(indexed_path: str, repo_root: Path) -> bool:
    """Return whether one indexed operationalization entry resolves to a directory."""
    if operationalization_path_is_glob(indexed_path):
        return False
    candidate = indexed_path[:-1] if indexed_path.endswith("/") else indexed_path
    resolved = repo_root / Path(candidate)
    return indexed_path.endswith("/") or resolved.is_dir()


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
        normalized = _normalize_standard_operationalization_path(
            relative_path,
            value,
            repo_root,
        )
        paths.append(normalized)
    return ordered_unique(tuple(paths))


def _normalize_standard_operationalization_path(
    relative_path: str,
    value: str,
    repo_root: Path,
) -> str:
    stripped = value.strip()
    without_fragment = stripped.split("#", 1)[0].split("?", 1)[0].strip()
    if not without_fragment:
        raise ValueError(
            f"{relative_path} operationalization surface must be a valid repository path: "
            f"{value}"
        )
    if operationalization_path_is_glob(without_fragment):
        normalized_pattern = _normalize_repo_relative_glob_pattern(
            relative_path,
            without_fragment,
            repo_root,
        )
        if normalized_pattern is None:
            raise ValueError(f"{relative_path} {_STANDARD_GLOB_PATTERN_ERROR}: {value}")
        return normalized_pattern
    normalized = normalize_repo_path_reference(without_fragment, repo_root)
    if normalized is None:
        raise ValueError(
            f"{relative_path} operationalization surface must be a valid repository path: "
            f"{value}"
        )
    return normalized


def _normalize_repo_relative_glob_pattern(
    relative_path: str,
    value: str,
    repo_root: Path,
) -> str | None:
    normalized = value.replace("\\", "/").lstrip("/")
    if (
        not normalized
        or value.startswith(("http://", "https://", "mailto:"))
        or value.startswith("/")
        or any(part == ".." for part in PurePosixPath(normalized).parts)
    ):
        return None
    try:
        matches = tuple(repo_root.glob(normalized))
    except ValueError as exc:
        raise ValueError(
            f"{relative_path} {_STANDARD_GLOB_PATTERN_ERROR}: {value}"
        ) from exc
    if not matches:
        return None
    return normalized


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
