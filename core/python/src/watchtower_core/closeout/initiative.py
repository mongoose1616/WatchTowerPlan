"""Initiative closeout helpers built on the governed traceability index."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import (
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_core.control_plane.models import TaskIndexEntry
from watchtower_core.repo_ops.sync.decision_tracking import DecisionTrackingSyncService
from watchtower_core.repo_ops.sync.design_tracking import DesignTrackingSyncService
from watchtower_core.repo_ops.sync.initiative_index import InitiativeIndexSyncService
from watchtower_core.repo_ops.sync.initiative_tracking import InitiativeTrackingSyncService
from watchtower_core.repo_ops.sync.prd_tracking import PrdTrackingSyncService
from watchtower_core.utils import utc_timestamp_now

TERMINAL_INITIATIVE_STATUSES = {"completed", "superseded", "cancelled", "abandoned"}
TERMINAL_TASK_STATUSES = {"done", "cancelled"}


@dataclass(frozen=True, slots=True)
class InitiativeCloseoutResult:
    """Result summary for one initiative closeout command."""

    trace_id: str
    initiative_status: str
    closed_at: str
    closure_reason: str
    superseded_by_trace_id: str | None
    open_task_ids: tuple[str, ...]
    wrote: bool
    traceability_output_path: str | None
    initiative_index_output_path: str | None
    initiative_tracking_output_path: str | None
    prd_tracking_output_path: str | None
    decision_tracking_output_path: str | None
    design_tracking_output_path: str | None


class InitiativeCloseoutService:
    """Apply initiative closeout state to the traceability index and trackers."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def close(
        self,
        *,
        trace_id: str,
        initiative_status: str,
        closure_reason: str,
        superseded_by_trace_id: str | None = None,
        closed_at: str | None = None,
        write: bool,
        allow_open_tasks: bool = False,
    ) -> InitiativeCloseoutResult:
        if initiative_status not in TERMINAL_INITIATIVE_STATUSES:
            allowed = ", ".join(sorted(TERMINAL_INITIATIVE_STATUSES))
            raise ValueError(
                f"Initiative closeout requires one terminal initiative status: {allowed}"
            )
        if initiative_status == "superseded" and superseded_by_trace_id is None:
            raise ValueError("Superseded initiative closeout requires superseded_by_trace_id.")
        if initiative_status != "superseded" and superseded_by_trace_id is not None:
            raise ValueError(
                "superseded_by_trace_id is only valid when initiative_status is superseded."
            )

        document = self._load_current_document()
        target_entry = self._find_entry(document, trace_id)
        if initiative_status == "superseded":
            self._find_entry(document, superseded_by_trace_id or "")

        open_task_ids = self._open_task_ids(trace_id)
        if open_task_ids and not allow_open_tasks:
            joined = ", ".join(open_task_ids)
            raise ValueError(
                f"Trace {trace_id} still has open linked tasks: {joined}. "
                "Use --allow-open-tasks only when the initiative truly closes with open work."
            )

        resolved_closed_at = closed_at or utc_timestamp_now()
        target_entry["initiative_status"] = initiative_status
        target_entry["closed_at"] = resolved_closed_at
        target_entry["closure_reason"] = closure_reason
        if superseded_by_trace_id is not None:
            target_entry["superseded_by_trace_id"] = superseded_by_trace_id
        else:
            target_entry.pop("superseded_by_trace_id", None)

        self._loader.schema_store.validate_instance(document)

        traceability_output_path: str | None = None
        initiative_index_output_path: str | None = None
        initiative_tracking_output_path: str | None = None
        prd_tracking_output_path: str | None = None
        decision_tracking_output_path: str | None = None
        design_tracking_output_path: str | None = None
        if write:
            traceability_path = self._loader.artifact_store.write_json_object(
                TRACEABILITY_INDEX_PATH,
                document,
            )
            traceability_output_path = str(traceability_path)

            initiative_index_service = InitiativeIndexSyncService(self._loader)
            initiative_index_output_path = str(
                initiative_index_service.write_document(
                    initiative_index_service.build_document()
                )
            )
            initiative_tracking_service = InitiativeTrackingSyncService(self._loader)
            initiative_tracking_output_path = str(
                initiative_tracking_service.write_document(
                    initiative_tracking_service.build_document()
                )
            )
            prd_tracking_service = PrdTrackingSyncService(self._loader)
            prd_tracking_output_path = str(
                prd_tracking_service.write_document(prd_tracking_service.build_document())
            )
            decision_tracking_service = DecisionTrackingSyncService(self._loader)
            decision_tracking_output_path = str(
                decision_tracking_service.write_document(
                    decision_tracking_service.build_document()
                )
            )
            design_tracking_service = DesignTrackingSyncService(self._loader)
            design_tracking_output_path = str(
                design_tracking_service.write_document(
                    design_tracking_service.build_document()
                )
            )

        return InitiativeCloseoutResult(
            trace_id=trace_id,
            initiative_status=initiative_status,
            closed_at=resolved_closed_at,
            closure_reason=closure_reason,
            superseded_by_trace_id=superseded_by_trace_id,
            open_task_ids=open_task_ids,
            wrote=write,
            traceability_output_path=traceability_output_path,
            initiative_index_output_path=initiative_index_output_path,
            initiative_tracking_output_path=initiative_tracking_output_path,
            prd_tracking_output_path=prd_tracking_output_path,
            decision_tracking_output_path=decision_tracking_output_path,
            design_tracking_output_path=design_tracking_output_path,
        )

    def _load_current_document(self) -> dict[str, object]:
        loaded = self._loader.load_json_object(TRACEABILITY_INDEX_PATH)
        if not isinstance(loaded, dict):
            raise ValueError("Traceability index is not a JSON object.")
        return loaded

    @staticmethod
    def _find_entry(document: dict[str, object], trace_id: str) -> dict[str, object]:
        entries = document.get("entries")
        if not isinstance(entries, list):
            raise ValueError("Traceability index is missing its entries list.")
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("trace_id") == trace_id:
                return entry
        raise ValueError(f"Unknown trace ID: {trace_id}")

    def _open_task_ids(self, trace_id: str) -> tuple[str, ...]:
        try:
            trace_entry = self._loader.load_traceability_index().get(trace_id)
        except KeyError as exc:
            raise ValueError(f"Unknown trace ID: {trace_id}") from exc

        task_index = self._loader.load_task_index()
        task_entries_by_id = {entry.task_id: entry for entry in task_index.entries}
        candidate_entries: dict[str, TaskIndexEntry] = {}
        missing_task_ids: list[str] = []

        for task_id in trace_entry.task_ids:
            task_entry = task_entries_by_id.get(task_id)
            if task_entry is None:
                missing_task_ids.append(task_id)
                continue
            candidate_entries[task_id] = task_entry

        if missing_task_ids:
            joined = ", ".join(sorted(missing_task_ids))
            raise ValueError(
                f"Trace {trace_id} references missing linked tasks in the task index: {joined}. "
                "Rebuild traceability and task surfaces before closeout."
            )

        for task_entry in task_index.entries:
            if task_entry.trace_id == trace_id:
                candidate_entries[task_entry.task_id] = task_entry

        open_task_ids = sorted(
            task_id
            for task_id, task_entry in candidate_entries.items()
            if task_entry.task_status not in TERMINAL_TASK_STATUSES
        )
        return tuple(open_task_ids)
