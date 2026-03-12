"""Index-backed query helpers for governed standards."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import StandardIndexEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class StandardSearchParams:
    """Filter and ranking inputs for standards lookup."""

    query: str | None = None
    standard_id: str | None = None
    category: str | None = None
    owner: str | None = None
    tag: str | None = None
    applies_to: str | None = None
    related_path: str | None = None
    reference_path: str | None = None
    operationalization_mode: str | None = None
    operationalization_path: str | None = None
    limit: int | None = None


class StandardQueryService:
    """Search the standard index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: StandardSearchParams) -> tuple[StandardIndexEntry, ...]:
        """Return standard entries matching the requested filters."""
        index = self._loader.load_standard_index()
        standard_id = params.standard_id.casefold() if params.standard_id is not None else None
        category = params.category.casefold() if params.category is not None else None
        owner = params.owner.casefold() if params.owner is not None else None
        tag = params.tag.casefold() if params.tag is not None else None
        applies_to = params.applies_to.casefold() if params.applies_to is not None else None
        related_path = params.related_path.casefold() if params.related_path is not None else None
        reference_path = (
            params.reference_path.casefold() if params.reference_path is not None else None
        )
        operationalization_mode = (
            params.operationalization_mode.casefold()
            if params.operationalization_mode is not None
            else None
        )
        operationalization_path = (
            params.operationalization_path.casefold()
            if params.operationalization_path is not None
            else None
        )

        matches: list[tuple[int, StandardIndexEntry]] = []
        for entry in index.entries:
            if standard_id is not None and entry.standard_id.casefold() != standard_id:
                continue
            if category is not None and entry.category.casefold() != category:
                continue
            if owner is not None and entry.owner.casefold() != owner:
                continue
            if tag is not None and tag not in {value.casefold() for value in entry.tags}:
                continue
            if applies_to is not None and applies_to not in {
                value.casefold() for value in entry.applies_to
            }:
                continue
            if related_path is not None and related_path not in {
                value.casefold() for value in entry.related_paths
            }:
                continue
            if reference_path is not None and reference_path not in {
                value.casefold() for value in entry.reference_doc_paths
            }:
                continue
            if operationalization_mode is not None and operationalization_mode not in {
                value.casefold() for value in entry.operationalization_modes
            }:
                continue
            if operationalization_path is not None and not self._matches_operationalization_path(
                operationalization_path,
                entry.operationalization_paths,
            ):
                continue

            score = query_score(
                params.query,
                (
                    entry.standard_id,
                    entry.category,
                    entry.owner,
                    entry.title,
                    entry.summary,
                    *entry.applies_to,
                    *entry.related_paths,
                    *entry.reference_doc_paths,
                    *entry.internal_reference_paths,
                    *entry.applied_reference_paths,
                    *entry.external_reference_urls,
                    *entry.applied_external_reference_urls,
                    *entry.operationalization_modes,
                    *entry.operationalization_paths,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].standard_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)

    def _matches_operationalization_path(
        self,
        requested_path: str,
        indexed_paths: tuple[str, ...],
    ) -> bool:
        """Match exact operationalization paths and descendants of indexed directories."""
        for indexed_path in indexed_paths:
            normalized_indexed = indexed_path.casefold()
            if requested_path == normalized_indexed:
                return True
            if self._indexed_path_is_directory(indexed_path):
                directory_prefix = (
                    normalized_indexed
                    if normalized_indexed.endswith("/")
                    else f"{normalized_indexed}/"
                )
                if requested_path.startswith(directory_prefix):
                    return True
        return False

    def _indexed_path_is_directory(self, indexed_path: str) -> bool:
        """Return whether an indexed operationalization path resolves to a directory."""
        candidate = indexed_path[:-1] if indexed_path.endswith("/") else indexed_path
        resolved = self._loader.repo_root / Path(candidate)
        return indexed_path.endswith("/") or resolved.is_dir()
