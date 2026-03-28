"""Shared helpers for governed reference-document maturity semantics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import extract_repo_path_references, extract_subsections
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.reference_status import (
    REFERENCE_REPOSITORY_STATUS_PREFIXES,
)
from watchtower_core.documentation.governed_documents import validate_required_section_order
from watchtower_core.pack_integration.roots import pack_reference_doc_roots

REFERENCE_LOCAL_MAPPING_SECTION = "Local Mapping in This Repository"
REFERENCE_CURRENT_REPOSITORY_STATUS_SUBSECTION = "Current Repository Status"
REFERENCE_CURRENT_TOUCHPOINTS_SUBSECTION = "Current Touchpoints"
CORE_REFERENCE_DOC_ROOT = "core/docs/references"


@dataclass(frozen=True, slots=True)
class ReferenceLocalMapping:
    """Structured current-state metadata derived from one reference document."""

    repository_status: str
    current_touchpoints_present: bool
    related_paths: tuple[str, ...]


def governed_reference_doc_roots(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[str, ...]:
    """Return shared and pack-owned governed reference roots visible in one repo."""

    return (
        CORE_REFERENCE_DOC_ROOT,
        *pack_reference_doc_roots(repo_root, loader=loader),
    )


def is_governed_reference_doc_path(
    relative_path: str,
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> bool:
    """Return whether one repo-relative path names a governed reference document."""

    return any(
        _path_is_or_descends_from_root(relative_path, root)
        for root in governed_reference_doc_roots(repo_root, loader=loader)
    )


def parse_reference_local_mapping(
    relative_path: str,
    local_mapping_section: str,
    *,
    repo_root: Path,
    source_path: Path,
) -> ReferenceLocalMapping:
    """Return deterministic maturity and touchpoint metadata for one reference doc."""
    subsections = extract_subsections(local_mapping_section)
    required_subsections: tuple[str, ...] = (REFERENCE_CURRENT_REPOSITORY_STATUS_SUBSECTION,)
    if REFERENCE_CURRENT_TOUCHPOINTS_SUBSECTION in subsections:
        required_subsections = required_subsections + (REFERENCE_CURRENT_TOUCHPOINTS_SUBSECTION,)
    validate_required_section_order(
        relative_path,
        subsections,
        required_subsections,
    )
    status_body = subsections[REFERENCE_CURRENT_REPOSITORY_STATUS_SUBSECTION]
    repository_status = parse_reference_repository_status(relative_path, status_body)
    touchpoints_body = subsections.get(REFERENCE_CURRENT_TOUCHPOINTS_SUBSECTION)
    related_paths = (
        extract_repo_path_references(
            touchpoints_body,
            repo_root,
            source_path=source_path,
        )
        if touchpoints_body
        else ()
    )
    return ReferenceLocalMapping(
        repository_status=repository_status,
        current_touchpoints_present=touchpoints_body is not None,
        related_paths=related_paths,
    )


def parse_reference_repository_status(relative_path: str, status_body: str) -> str:
    """Return the normalized repository-status enum for one status subsection body."""
    status_line = _first_meaningful_line(status_body)
    for repository_status, prefix in REFERENCE_REPOSITORY_STATUS_PREFIXES.items():
        if status_line.startswith(prefix):
            return repository_status
    allowed = ", ".join(f"`{prefix}`" for prefix in REFERENCE_REPOSITORY_STATUS_PREFIXES.values())
    raise ValueError(
        f"{relative_path} Current Repository Status must begin with one of: {allowed}."
    )


def _first_meaningful_line(section_body: str) -> str:
    for line in section_body.splitlines():
        candidate = line.strip()
        if not candidate:
            continue
        if candidate.startswith("- "):
            return candidate[2:].strip()
        return candidate
    raise ValueError("Current Repository Status is missing its expected status line.")


def _path_is_or_descends_from_root(relative_path: str, root: str) -> bool:
    normalized_path = relative_path.rstrip("/")
    normalized_root = root.rstrip("/")
    return normalized_path == normalized_root or normalized_path.startswith(
        f"{normalized_root}/"
    )
