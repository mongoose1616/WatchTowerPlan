"""Deterministic rebuild helpers for the initiative index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    InitiativeIndexEntry,
)
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.planning_projection_snapshot import (
    TracePlanningProjectionSnapshot,
    _build_active_task_summaries,
    _determine_current_phase,
    _select_coordination_task,
    _task_is_blocked,
    build_trace_planning_coordination_snapshot,
    build_trace_planning_projection_snapshots,
)
from watchtower_core.repo_ops.planning_projection_serialization import (
    serialize_initiative_entry,
)
from watchtower_core.repo_ops.sync.tracking_common import effective_updated_at

INITIATIVE_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/initiatives/initiative_index.v1.json"
PHASE_ORDER = {
    "prd": 1,
    "design": 2,
    "implementation_planning": 3,
    "execution": 4,
    "validation": 5,
    "closeout": 6,
    "closed": 7,
}


class InitiativeIndexSyncService:
    """Build and write the initiative index from current planning and task surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> InitiativeIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        entries = [
            self._build_entry(snapshot)
            for snapshot in build_trace_planning_projection_snapshots(self._loader)
        ]

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:initiative-index:v1",
            "id": "index.initiatives",
            "title": "Initiative Index",
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
        """Write the generated initiative index to disk."""
        target = destination or (self._repo_root / INITIATIVE_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _build_entry(
        self,
        snapshot: TracePlanningProjectionSnapshot,
    ) -> dict[str, object]:
        trace_entry = snapshot.trace_entry
        coordination = build_trace_planning_coordination_snapshot(snapshot)
        entry_updated_at = effective_updated_at(trace_entry.updated_at, trace_entry.closed_at)

        initiative_entry = InitiativeIndexEntry(
            trace_id=trace_entry.trace_id,
            title=trace_entry.title,
            summary=trace_entry.summary,
            artifact_status=trace_entry.status,
            initiative_status=trace_entry.initiative_status,
            current_phase=coordination.current_phase,
            updated_at=entry_updated_at,
            open_task_count=coordination.open_task_count,
            blocked_task_count=coordination.blocked_task_count,
            key_surface_path=coordination.key_surface_path,
            next_action=coordination.next_action,
            next_surface_path=coordination.next_surface_path,
            primary_owner=coordination.primary_owner,
            active_owners=coordination.active_owners,
            active_task_ids=coordination.active_task_ids,
            active_task_summaries=coordination.active_task_summaries,
            blocked_by_task_ids=coordination.blocked_by_task_ids,
            prd_ids=trace_entry.prd_ids,
            decision_ids=trace_entry.decision_ids,
            design_ids=trace_entry.design_ids,
            plan_ids=trace_entry.plan_ids,
            task_ids=trace_entry.task_ids,
            acceptance_ids=trace_entry.acceptance_ids,
            acceptance_contract_ids=trace_entry.acceptance_contract_ids,
            evidence_ids=trace_entry.evidence_ids,
            closed_at=(
                trace_entry.closed_at
                if trace_entry.initiative_status != "active"
                else None
            ),
            closure_reason=(
                trace_entry.closure_reason
                if trace_entry.initiative_status != "active"
                else None
            ),
            superseded_by_trace_id=(
                trace_entry.superseded_by_trace_id
                if trace_entry.initiative_status != "active"
                else None
            ),
            related_paths=trace_entry.related_paths,
            tags=trace_entry.tags,
            notes=trace_entry.notes,
        )
        return serialize_initiative_entry(initiative_entry, compact=True)
