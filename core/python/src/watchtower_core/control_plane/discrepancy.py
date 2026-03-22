"""Helpers for governed discrepancy records and reconciliation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, cast

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader

DISCREPANCY_RECORD_SCHEMA_ID = "urn:watchtower:schema:artifacts:plan:discrepancy-record:v1"


@dataclass(frozen=True, slots=True)
class DiscrepancyDescriptor:
    """One discrepancy-record root plus the owning initiative identity."""

    relative_dir: str
    initiative_id: str


@dataclass(frozen=True, slots=True)
class DiscrepancyIssue:
    """One discrepancy to write or reconcile against governed records."""

    discrepancy_id: str
    record_slug: str
    category: str
    summary: str
    source_paths: tuple[str, ...]
    severity: str = "high"
    gate_effect: str = "readiness"
    resolution_owner: str = "repository_maintainer"


class DiscrepancyHelper:
    """Build, reconcile, and load governed discrepancy records."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> DiscrepancyHelper:
        """Build one helper from a loader and effective pack settings path."""

        effective_pack_settings_path = loader.effective_pack_settings_path(pack_settings_path)
        effective_loader = (
            loader
            if loader.active_pack_settings_path == effective_pack_settings_path
            else loader.derive(active_pack_settings_path=effective_pack_settings_path)
        )
        return cls(effective_loader)

    def build_record(
        self,
        descriptor: DiscrepancyDescriptor,
        issue: DiscrepancyIssue,
        *,
        detected_at: str,
        status: str = "open",
        updated_at: str | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Build one validated discrepancy record for an issue."""

        relative_path = (
            f"{_normalize_relative_dir(descriptor.relative_dir)}/"
            f"{_normalize_record_slug(issue.record_slug)}.json"
        )
        document: dict[str, Any] = {
            "$schema": DISCREPANCY_RECORD_SCHEMA_ID,
            "discrepancy_id": issue.discrepancy_id,
            "initiative_id": descriptor.initiative_id,
            "category": issue.category,
            "severity": issue.severity,
            "gate_effect": issue.gate_effect,
            "status": status,
            "summary": issue.summary,
            "source_paths": list(issue.source_paths),
            "resolution_owner": issue.resolution_owner,
            "detected_at": detected_at,
            "updated_at": updated_at or detected_at,
        }
        self._loader.schema_store.validate_instance(
            document,
            schema_id=DISCREPANCY_RECORD_SCHEMA_ID,
        )
        return relative_path, document

    def open_records(
        self,
        descriptor: DiscrepancyDescriptor,
    ) -> tuple[tuple[str, dict[str, Any]], ...]:
        """Return the open validated discrepancy records for one descriptor."""

        discrepancy_dir = self._loader.repo_root / _normalize_relative_dir(descriptor.relative_dir)
        if not discrepancy_dir.exists():
            return ()

        documents: list[tuple[str, dict[str, Any]]] = []
        for path in sorted(discrepancy_dir.glob("*.json")):
            relative_path = str(path.relative_to(self._loader.repo_root))
            document = self._load_record(relative_path)
            if document["status"] == "open":
                documents.append((relative_path, document))
        return tuple(documents)

    def sync_records(
        self,
        descriptor: DiscrepancyDescriptor,
        *,
        issues: tuple[DiscrepancyIssue, ...],
        updated_at: str,
        managed_categories: tuple[str, ...] = (),
    ) -> None:
        """Write current issues and resolve obsolete managed open records."""

        normalized_dir = _normalize_relative_dir(descriptor.relative_dir)
        discrepancy_dir = self._loader.repo_root / normalized_dir
        discrepancy_dir.mkdir(parents=True, exist_ok=True)

        issue_map = {issue.discrepancy_id: issue for issue in issues}
        if len(issue_map) != len(issues):
            raise ValueError("Discrepancy issues must use unique discrepancy_id values.")

        record_slug_map = {issue.record_slug: issue for issue in issues}
        if len(record_slug_map) != len(issues):
            raise ValueError("Discrepancy issues must use unique record_slug values.")

        managed_category_set = frozenset(
            managed_categories or tuple(issue.category for issue in issues)
        )

        for path in sorted(discrepancy_dir.glob("*.json")):
            relative_path = str(path.relative_to(self._loader.repo_root))
            document = self._load_record(relative_path)
            discrepancy_id = str(document["discrepancy_id"])
            if discrepancy_id in issue_map:
                issue = issue_map.pop(discrepancy_id)
                refreshed_path, refreshed_document = self.build_record(
                    descriptor,
                    issue,
                    detected_at=str(document["detected_at"]),
                    status="open",
                    updated_at=updated_at,
                )
                self._loader.artifact_store.write_json_object(
                    refreshed_path,
                    refreshed_document,
                )
            elif (
                str(document["category"]) in managed_category_set
                and str(document["status"]) == "open"
            ):
                document["status"] = "resolved"
                document["updated_at"] = updated_at
                self._loader.schema_store.validate_instance(
                    document,
                    schema_id=DISCREPANCY_RECORD_SCHEMA_ID,
                )
                self._loader.artifact_store.write_json_object(relative_path, document)

        for issue in issue_map.values():
            relative_path, document = self.build_record(
                descriptor,
                issue,
                detected_at=updated_at,
                status="open",
                updated_at=updated_at,
            )
            self._loader.artifact_store.write_json_object(relative_path, document)

    def _load_record(self, relative_path: str) -> dict[str, Any]:
        path = self._loader.repo_root / relative_path
        document = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
        self._loader.schema_store.validate_instance(
            document,
            schema_id=DISCREPANCY_RECORD_SCHEMA_ID,
        )
        return document


def _normalize_relative_dir(relative_dir: str) -> str:
    return relative_dir.strip().strip("/")


def _normalize_record_slug(record_slug: str) -> str:
    cleaned = record_slug.strip().strip("/")
    if not cleaned or "/" in cleaned:
        raise ValueError("Discrepancy record_slug must be one filename stem.")
    return cleaned


__all__ = [
    "DISCREPANCY_RECORD_SCHEMA_ID",
    "DiscrepancyDescriptor",
    "DiscrepancyHelper",
    "DiscrepancyIssue",
]
