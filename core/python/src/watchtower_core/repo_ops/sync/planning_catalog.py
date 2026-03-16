"""Deterministic rebuild helpers for the canonical planning catalog."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.planning_rendered_catalog_composition import (
    build_trace_planning_catalog_entry,
)
from watchtower_core.repo_ops.planning_rendered_serialization import (
    serialize_planning_catalog_entry,
)
from watchtower_core.repo_ops.planning_rendered_snapshot import (
    TracePlanningRenderedSnapshot,
    build_trace_planning_coordination_snapshot,
    build_trace_planning_rendered_snapshots,
)

PLANNING_CATALOG_ARTIFACT_PATH = (
    "core/control_plane/indexes/planning/planning_catalog.json"
)


class PlanningCatalogSyncService:
    """Build and write the canonical planning catalog from trace-linked sources."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> PlanningCatalogSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        entries = [
            self._build_entry(snapshot)
            for snapshot in build_trace_planning_rendered_snapshots(self._loader)
        ]

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:planning-catalog:v1",
            "id": "index.planning_catalog",
            "title": "Planning Catalog",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write the generated planning catalog to disk."""
        target = destination or (self._repo_root / PLANNING_CATALOG_ARTIFACT_PATH)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _build_entry(
        self,
        snapshot: TracePlanningRenderedSnapshot,
    ) -> dict[str, object]:
        coordination = build_trace_planning_coordination_snapshot(snapshot)
        planning_entry = build_trace_planning_catalog_entry(snapshot, coordination)
        return serialize_planning_catalog_entry(planning_entry, compact=True)
