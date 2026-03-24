"""Helpers for normalized governing-document references in plan artifacts."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path

from watchtower_core.adapters import normalize_repo_path_reference


def normalize_governing_document_paths(
    values: Iterable[str],
    *,
    origin: str,
    repo_root: Path,
    allowed_missing_paths: Iterable[str] = (),
) -> tuple[str, ...]:
    """Return canonical repo-relative Markdown paths for governing documents."""

    allowed_missing = {
        value.strip().lstrip("/") for value in allowed_missing_paths if value.strip()
    }
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        candidate = value.strip()
        if not candidate:
            raise ValueError(
                f"{origin} governing_document_paths entries must be non-empty strings."
            )

        normalized = _normalize_governing_document_path(
            candidate,
            repo_root=repo_root,
            allowed_missing_paths=allowed_missing,
        )
        if normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return tuple(ordered)


def authored_input_document_paths(
    initiative_document: Mapping[str, object],
) -> tuple[str, ...]:
    """Return unique authored-input Markdown paths from one initiative document."""

    authored_inputs = initiative_document.get("authored_inputs")
    if not isinstance(authored_inputs, (list, tuple)):
        return ()
    return _ordered_string_values(
        record.get("path") for record in authored_inputs if isinstance(record, Mapping)
    )


def effective_initiative_governing_document_paths(
    initiative_document: Mapping[str, object],
    *,
    repo_root: Path | None = None,
) -> tuple[str, ...]:
    """Return the effective initiative-level governing-document set."""

    explicit_paths = _document_path_values(
        initiative_document.get("governing_document_paths"),
        repo_root=repo_root,
    )
    authored_paths = _document_path_values(
        authored_input_document_paths(initiative_document),
        repo_root=repo_root,
    )
    return _ordered_unique((*explicit_paths, *authored_paths))


def effective_task_governing_document_paths(
    task_document: Mapping[str, object],
    *,
    initiative_document: Mapping[str, object],
    repo_root: Path | None = None,
) -> tuple[str, ...]:
    """Return the effective task-level governing-document set."""

    explicit_paths = _document_path_values(
        task_document.get("governing_document_paths"),
        repo_root=repo_root,
    )
    if explicit_paths:
        return explicit_paths
    return effective_initiative_governing_document_paths(
        initiative_document,
        repo_root=repo_root,
    )


def _document_path_values(
    value: object,
    *,
    repo_root: Path | None,
) -> tuple[str, ...]:
    values = _ordered_string_values(
        value if isinstance(value, (list, tuple)) else (value,)
    )
    if repo_root is None:
        return values

    ordered: list[str] = []
    seen: set[str] = set()
    for item in values:
        normalized = normalize_repo_path_reference(item, repo_root)
        if normalized is None:
            continue
        resolved = repo_root / normalized
        if not resolved.exists() or not resolved.is_file() or resolved.suffix != ".md":
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return tuple(ordered)


def _normalize_governing_document_path(
    value: str,
    *,
    repo_root: Path,
    allowed_missing_paths: set[str],
) -> str:
    direct_candidate = value.lstrip("/")
    if direct_candidate in allowed_missing_paths:
        normalized = direct_candidate
    else:
        maybe_normalized = normalize_repo_path_reference(value, repo_root)
        if maybe_normalized is None:
            raise ValueError(
                "governing_document_paths entries must use canonical repo-relative Markdown paths: "
                f"{value}"
            )
        normalized = maybe_normalized
        resolved = repo_root / normalized
        if not resolved.exists() or not resolved.is_file():
            raise ValueError(f"governing_document_paths entry does not exist: {value}")
    if Path(normalized).suffix != ".md":
        raise ValueError(
            f"governing_document_paths entries must point to Markdown documents: {value}"
        )
    return normalized


def _ordered_string_values(values: Iterable[object]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        candidate = value.strip()
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        ordered.append(candidate)
    return tuple(ordered)


def _ordered_unique(values: Iterable[str]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


__all__ = [
    "authored_input_document_paths",
    "effective_initiative_governing_document_paths",
    "effective_task_governing_document_paths",
    "normalize_governing_document_paths",
]
