"""Plan-workspace aggregate builders, rendered views, and query helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    CoordinationIndex,
    CoordinationRecentInitiativeSummary,
    CoordinationTaskSummary,
    InitiativeActiveTaskSummary,
    InitiativeIndex,
    InitiativeIndexEntry,
)
from watchtower_core.repo_ops.planning_rendered_serialization import serialize_initiative_entry
from watchtower_core.repo_ops.query.common import (
    RenderedSearchFilters,
    initiative_rendered_query_terms,
    normalize_optional_text,
    normalize_text,
    query_score,
    search_rendered_entries,
)
from watchtower_core.utils.timestamps import utc_timestamp_now

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"
PLAN_INITIATIVE_INDEX_PATH = "plan/.wt/indexes/initiative_index.json"
PLAN_TASK_INDEX_PATH = "plan/.wt/indexes/task_index.json"
PLAN_READINESS_INDEX_PATH = "plan/.wt/indexes/readiness_index.json"
PLAN_DISCREPANCY_INDEX_PATH = "plan/.wt/indexes/discrepancy_index.json"
PLAN_COORDINATION_INDEX_PATH = "plan/.wt/indexes/coordination_index.json"
PLAN_OVERVIEW_PATH = "plan/plan_overview.md"

_TASK_STATUS_MAP = {
    "planned": "backlog",
    "ready": "ready",
    "in_progress": "in_progress",
    "in_review": "in_review",
    "blocked": "blocked",
    "completed": "done",
    "cancelled": "cancelled",
}
_ACTIVE_LIFECYCLE_STAGES = frozenset(
    {
        "capture_incomplete",
        "ready_for_review",
        "ready_for_execution",
        "in_progress",
        "blocked",
        "closing",
    }
)
_TERMINAL_LIFECYCLE_STAGES = frozenset({"completed", "superseded", "cancelled"})
_TERMINAL_TASK_STATUSES = frozenset({"completed", "cancelled"})
_PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
_PHASE_ORDER = {
    "implementation_planning": 0,
    "execution": 1,
    "closeout": 2,
    "closed": 3,
}
_TASK_STATUS_ORDER = {
    "ready": 0,
    "in_progress": 1,
    "in_review": 2,
    "backlog": 3,
    "blocked": 4,
    "done": 5,
    "cancelled": 6,
}


@dataclass(frozen=True, slots=True)
class PlanTaskIndexEntry:
    """Machine-readable task-summary entry for the plan workspace."""

    task_id: str
    initiative_id: str
    trace_id: str
    initiative_title: str
    title: str
    summary: str
    status: str
    priority: str
    owner: str
    doc_path: str
    updated_at: str
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanTaskIndexEntry:
        return cls(
            task_id=str(document["task_id"]),
            initiative_id=str(document["initiative_id"]),
            trace_id=str(document["trace_id"]),
            initiative_title=str(document["initiative_title"]),
            title=str(document["title"]),
            summary=str(document["summary"]),
            status=str(document["status"]),
            priority=str(document["priority"]),
            owner=str(document["owner"]),
            doc_path=str(document["doc_path"]),
            updated_at=str(document["updated_at"]),
            blocked_by=tuple(document.get("blocked_by", ())),
            depends_on=tuple(document.get("depends_on", ())),
            related_ids=tuple(document.get("related_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanReadinessIndexEntry:
    """Machine-readable readiness-gate summary for one initiative package."""

    initiative_id: str
    trace_id: str
    title: str
    initiative_root: str
    lifecycle_stage: str
    review_status: str
    capture_complete: bool
    machine_valid: bool
    approval_status: str
    ready_for_execution: bool
    blocking_reasons: tuple[str, ...]
    updated_at: str
    scope_type: str = "pack_wide"

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanReadinessIndexEntry:
        return cls(
            initiative_id=str(document["initiative_id"]),
            trace_id=str(document["trace_id"]),
            title=str(document["title"]),
            initiative_root=str(document["initiative_root"]),
            lifecycle_stage=str(document["lifecycle_stage"]),
            review_status=str(document["review_status"]),
            capture_complete=bool(document["capture_complete"]),
            machine_valid=bool(document["machine_valid"]),
            approval_status=str(document["approval_status"]),
            ready_for_execution=bool(document["ready_for_execution"]),
            blocking_reasons=tuple(document.get("blocking_reasons", ())),
            updated_at=str(document["updated_at"]),
            scope_type=str(document.get("scope_type", "pack_wide")),
        )


@dataclass(frozen=True, slots=True)
class PlanDiscrepancyIndexEntry:
    """Machine-readable discrepancy summary for one initiative-local discrepancy."""

    discrepancy_id: str
    initiative_id: str
    trace_id: str
    title: str
    category: str
    severity: str
    gate_effect: str
    status: str
    summary: str
    source_paths: tuple[str, ...]
    updated_at: str

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanDiscrepancyIndexEntry:
        return cls(
            discrepancy_id=str(document["discrepancy_id"]),
            initiative_id=str(document["initiative_id"]),
            trace_id=str(document["trace_id"]),
            title=str(document["title"]),
            category=str(document["category"]),
            severity=str(document["severity"]),
            gate_effect=str(document["gate_effect"]),
            status=str(document["status"]),
            summary=str(document["summary"]),
            source_paths=tuple(document.get("source_paths", ())),
            updated_at=str(document["updated_at"]),
        )


@dataclass(frozen=True, slots=True)
class PlanTaskSearchParams:
    """Structured task lookup filters for plan-workspace task summaries."""

    query: str | None = None
    initiative_id: str | None = None
    trace_id: str | None = None
    status: str | None = None
    priority: str | None = None
    owner: str | None = None
    blocked_only: bool = False
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanReadinessSearchParams:
    """Structured readiness lookup filters for initiative packages."""

    query: str | None = None
    initiative_id: str | None = None
    trace_id: str | None = None
    lifecycle_stage: str | None = None
    review_status: str | None = None
    ready_for_execution: bool | None = None
    blocked_only: bool = False
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanDiscrepancySearchParams:
    """Structured discrepancy lookup filters for plan-workspace discrepancies."""

    query: str | None = None
    initiative_id: str | None = None
    trace_id: str | None = None
    category: str | None = None
    severity: str | None = None
    status: str | None = None
    blocking_only: bool = False
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class DerivedSurfaceIssue:
    """One stale or missing rendered/index surface discovered during validation."""

    category: str
    relative_path: str
    message: str
    discrepancy_id: str


@dataclass(frozen=True, slots=True)
class PlanWorkspaceSyncResult:
    """Summary of one plan-workspace rebuild run."""

    initiative_count: int
    task_count: int
    discrepancy_count: int
    wrote: bool


@dataclass(frozen=True, slots=True)
class _PlanInitiativeSnapshot:
    initiative_document: dict[str, object]
    task_documents: tuple[dict[str, object], ...]
    deferred_documents: tuple[dict[str, object], ...]
    discrepancy_documents: tuple[dict[str, object], ...]
    evidence_documents: tuple[dict[str, object], ...]
    closeout_documents: tuple[dict[str, object], ...]
    promotion_documents: tuple[dict[str, object], ...]
    initiative_root: str


class PlanWorkspaceService:
    """Build plan-local indexes, rendered views, and query surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def sync(self, *, write: bool) -> PlanWorkspaceSyncResult:
        snapshots = self._load_initiative_snapshots()
        documents = self._build_documents(snapshots)
        if write:
            self._write_json(PLAN_INITIATIVE_INDEX_PATH, documents["initiative_index"])
            self._write_json(PLAN_TASK_INDEX_PATH, documents["task_index"])
            self._write_json(PLAN_READINESS_INDEX_PATH, documents["readiness_index"])
            self._write_json(PLAN_DISCREPANCY_INDEX_PATH, documents["discrepancy_index"])
            self._write_json(PLAN_COORDINATION_INDEX_PATH, documents["coordination_index"])
            self._write_markdown(PLAN_OVERVIEW_PATH, str(documents["plan_overview"]))
            for relative_path, content in documents["initiative_views"].items():
                self._write_markdown(relative_path, content)
        return PlanWorkspaceSyncResult(
            initiative_count=len(snapshots),
            task_count=len(documents["task_index"]["entries"]),
            discrepancy_count=len(documents["discrepancy_index"]["entries"]),
            wrote=write,
        )

    def expected_surface_issues(self, initiative_slug: str) -> tuple[DerivedSurfaceIssue, ...]:
        snapshots = self._load_initiative_snapshots()
        documents = self._build_documents(snapshots)
        initiative_root = f"plan/initiatives/{initiative_slug}"
        expected_markdown = {
            PLAN_OVERVIEW_PATH: str(documents["plan_overview"]),
            f"{initiative_root}/plan.md": documents["initiative_views"].get(
                f"{initiative_root}/plan.md",
                "",
            ),
            f"{initiative_root}/progress.md": documents["initiative_views"].get(
                f"{initiative_root}/progress.md",
                "",
            ),
            f"{initiative_root}/summary.md": documents["initiative_views"].get(
                f"{initiative_root}/summary.md",
                "",
            ),
        }
        expected_json = {
            PLAN_INITIATIVE_INDEX_PATH: documents["initiative_index"],
            PLAN_TASK_INDEX_PATH: documents["task_index"],
            PLAN_READINESS_INDEX_PATH: documents["readiness_index"],
            PLAN_DISCREPANCY_INDEX_PATH: documents["discrepancy_index"],
            PLAN_COORDINATION_INDEX_PATH: documents["coordination_index"],
        }

        issues: list[DerivedSurfaceIssue] = []
        for relative_path, expected in expected_markdown.items():
            if not expected:
                issues.append(
                    DerivedSurfaceIssue(
                        category="stale_rendered_surface",
                        relative_path=relative_path,
                        message=f"Required rendered surface is missing from the expected build: {relative_path}.",
                        discrepancy_id=f"discrepancy.{initiative_slug}.{Path(relative_path).stem}_surface_drift",
                    )
                )
                continue
            candidate = self._loader.repo_root / relative_path
            if not candidate.exists():
                issues.append(
                    DerivedSurfaceIssue(
                        category="stale_rendered_surface",
                        relative_path=relative_path,
                        message=f"Required rendered surface is missing: {relative_path}.",
                        discrepancy_id=f"discrepancy.{initiative_slug}.{Path(relative_path).stem}_surface_drift",
                    )
                )
                continue
            if candidate.read_text(encoding="utf-8") != expected:
                issues.append(
                    DerivedSurfaceIssue(
                        category="stale_rendered_surface",
                        relative_path=relative_path,
                        message=f"Rendered surface drift detected for {relative_path}.",
                        discrepancy_id=f"discrepancy.{initiative_slug}.{Path(relative_path).stem}_surface_drift",
                    )
                )

        for relative_path, expected in expected_json.items():
            candidate = self._loader.repo_root / relative_path
            if not candidate.exists():
                issues.append(
                    DerivedSurfaceIssue(
                        category="stale_aggregate_index",
                        relative_path=relative_path,
                        message=f"Required aggregate index is missing: {relative_path}.",
                        discrepancy_id=f"discrepancy.{initiative_slug}.{Path(relative_path).stem}_index_drift",
                    )
                )
                continue
            try:
                current = json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                issues.append(
                    DerivedSurfaceIssue(
                        category="stale_aggregate_index",
                        relative_path=relative_path,
                        message=f"Aggregate index is not valid JSON: {relative_path}.",
                        discrepancy_id=f"discrepancy.{initiative_slug}.{Path(relative_path).stem}_index_drift",
                    )
                )
                continue
            if current != expected:
                issues.append(
                    DerivedSurfaceIssue(
                        category="stale_aggregate_index",
                        relative_path=relative_path,
                        message=f"Aggregate index drift detected for {relative_path}.",
                        discrepancy_id=f"discrepancy.{initiative_slug}.{Path(relative_path).stem}_index_drift",
                    )
                )
        return tuple(sorted(issues, key=lambda issue: (issue.category, issue.relative_path)))

    def load_initiative_index(self) -> InitiativeIndex:
        return InitiativeIndex.from_document(self._load_plan_json(PLAN_INITIATIVE_INDEX_PATH))

    def load_coordination_index(self) -> CoordinationIndex:
        return CoordinationIndex.from_document(self._load_plan_json(PLAN_COORDINATION_INDEX_PATH))

    def load_task_entries(self) -> tuple[PlanTaskIndexEntry, ...]:
        document = self._load_plan_json(PLAN_TASK_INDEX_PATH)
        return tuple(PlanTaskIndexEntry.from_document(entry) for entry in document["entries"])

    def load_readiness_entries(self) -> tuple[PlanReadinessIndexEntry, ...]:
        document = self._load_plan_json(PLAN_READINESS_INDEX_PATH)
        return tuple(PlanReadinessIndexEntry.from_document(entry) for entry in document["entries"])

    def load_discrepancy_entries(self) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        document = self._load_plan_json(PLAN_DISCREPANCY_INDEX_PATH)
        return tuple(PlanDiscrepancyIndexEntry.from_document(entry) for entry in document["entries"])

    def search_initiatives(
        self,
        filters: RenderedSearchFilters,
    ) -> tuple[InitiativeIndexEntry, ...]:
        return search_rendered_entries(
            self.load_initiative_index().entries,
            filters,
            query_fields=initiative_rendered_query_terms,
            sort_key=lambda entry: (_PHASE_ORDER.get(entry.current_phase, 99), entry.trace_id),
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
            blocked_task_count=lambda entry: entry.blocked_task_count,
        )

    def search_coordination(
        self,
        filters: RenderedSearchFilters,
    ) -> tuple[InitiativeIndexEntry, ...]:
        coordination_index = self.load_coordination_index()
        entry_rank = {entry.trace_id: idx for idx, entry in enumerate(coordination_index.entries)}
        return search_rendered_entries(
            coordination_index.entries,
            filters,
            query_fields=initiative_rendered_query_terms,
            sort_key=lambda entry: (entry_rank.get(entry.trace_id, 9999), entry.trace_id),
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
            blocked_task_count=lambda entry: entry.blocked_task_count,
        )

    def search_tasks(self, params: PlanTaskSearchParams) -> tuple[PlanTaskIndexEntry, ...]:
        return _search_task_entries(self.load_task_entries(), params)

    def search_readiness(
        self,
        params: PlanReadinessSearchParams,
    ) -> tuple[PlanReadinessIndexEntry, ...]:
        return _search_readiness_entries(self.load_readiness_entries(), params)

    def search_discrepancies(
        self,
        params: PlanDiscrepancySearchParams,
    ) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        return _search_discrepancy_entries(self.load_discrepancy_entries(), params)

    def _build_documents(
        self,
        snapshots: tuple[_PlanInitiativeSnapshot, ...],
    ) -> dict[str, object]:
        workspace_updated_at = _latest_timestamp(
            str(snapshot.initiative_document["updated_at"]) for snapshot in snapshots
        )
        initiative_entries = tuple(
            sorted(
                (self._build_initiative_entry(snapshot) for snapshot in snapshots),
                key=lambda entry: entry.trace_id,
            )
        )
        task_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_task_entries(snapshot)
                ),
                key=lambda entry: entry.task_id,
            )
        )
        readiness_entries = tuple(
            sorted(
                (self._build_readiness_entry(snapshot) for snapshot in snapshots),
                key=lambda entry: entry.initiative_id,
            )
        )
        discrepancy_entries = tuple(
            sorted(
                (
                    entry
                    for snapshot in snapshots
                    for entry in self._build_discrepancy_entries(snapshot)
                ),
                key=lambda entry: entry.discrepancy_id,
            )
        )
        initiative_index = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:initiative-index:v1",
            "id": "index.initiatives",
            "title": "Plan Workspace Initiative Index",
            "status": "active",
            "entries": [serialize_initiative_entry(entry, compact=True) for entry in initiative_entries],
        }
        coordination_index = self._build_coordination_document(initiative_entries)
        task_index = {
            "$schema": "urn:watchtower:schema:artifacts:plan:task-summary-index:v1",
            "id": "index.plan_tasks",
            "title": "Plan Workspace Task Index",
            "status": "active",
            "entries": [self._serialize_task_entry(entry) for entry in task_entries],
        }
        readiness_index = {
            "$schema": "urn:watchtower:schema:artifacts:plan:readiness-index:v1",
            "id": "index.readiness",
            "title": "Plan Workspace Readiness Index",
            "status": "active",
            "updated_at": _latest_timestamp(
                [*(entry.updated_at for entry in readiness_entries), workspace_updated_at]
            ),
            "entries": [self._serialize_readiness_entry(entry) for entry in readiness_entries],
        }
        discrepancy_index = {
            "$schema": "urn:watchtower:schema:artifacts:plan:discrepancy-index:v1",
            "id": "index.plan_discrepancies",
            "title": "Plan Workspace Discrepancy Index",
            "status": "active",
            "updated_at": _latest_timestamp(
                [*(entry.updated_at for entry in discrepancy_entries), workspace_updated_at]
            ),
            "entries": [self._serialize_discrepancy_entry(entry) for entry in discrepancy_entries],
        }

        pack_loader = self._pack_loader()
        for document in (
            initiative_index,
            coordination_index,
            task_index,
            readiness_index,
            discrepancy_index,
        ):
            pack_loader.schema_store.validate_instance(document)

        return {
            "initiative_index": initiative_index,
            "coordination_index": coordination_index,
            "task_index": task_index,
            "readiness_index": readiness_index,
            "discrepancy_index": discrepancy_index,
            "plan_overview": self._render_plan_overview(coordination_index),
            "initiative_views": self._render_initiative_views(snapshots),
        }

    def _build_initiative_entry(self, snapshot: _PlanInitiativeSnapshot) -> InitiativeIndexEntry:
        initiative = snapshot.initiative_document
        active_task_summaries = tuple(
            self._build_active_task_summary(snapshot, task_document)
            for task_document in snapshot.task_documents
            if str(task_document["status"]) not in _TERMINAL_TASK_STATUSES
        )
        active_task_ids = tuple(task.task_id for task in active_task_summaries)
        blocked_by_task_ids = tuple(
            sorted(
                {
                    blocker
                    for task in active_task_summaries
                    for blocker in task.blocked_by
                }
            )
        )
        lifecycle_stage = str(initiative["lifecycle_stage"])
        readiness = self._build_readiness_entry(snapshot)
        return InitiativeIndexEntry(
            trace_id=str(initiative["trace_id"]),
            title=str(initiative["title"]),
            summary=str(initiative["summary"]),
            artifact_status="active",
            initiative_status=_initiative_status(initiative),
            current_phase=_current_phase_for_lifecycle(lifecycle_stage),
            updated_at=str(initiative["updated_at"]),
            open_task_count=len(active_task_summaries),
            blocked_task_count=sum(
                1 for task in active_task_summaries if task.task_status == "blocked"
            ),
            key_surface_path=f"{snapshot.initiative_root}/plan.md",
            next_action=_next_action(snapshot, readiness),
            next_surface_path=_next_surface_path(snapshot, readiness),
            primary_owner=str(initiative["owner"]),
            active_owners=(str(initiative["owner"]),),
            active_task_ids=active_task_ids,
            active_task_summaries=active_task_summaries,
            blocked_by_task_ids=blocked_by_task_ids,
            task_ids=tuple(initiative["task_ids"]),
            evidence_ids=tuple(initiative["evidence_ids"]),
            related_paths=tuple(record["path"] for record in initiative["authored_inputs"]),
        )

    def _build_task_entries(
        self,
        snapshot: _PlanInitiativeSnapshot,
    ) -> tuple[PlanTaskIndexEntry, ...]:
        initiative = snapshot.initiative_document
        return tuple(
            PlanTaskIndexEntry(
                task_id=str(task["task_id"]),
                initiative_id=str(initiative["initiative_id"]),
                trace_id=str(initiative["trace_id"]),
                initiative_title=str(initiative["title"]),
                title=str(task["title"]),
                summary=str(task["summary"]),
                status=str(task["status"]),
                priority=str(task["priority"]),
                owner=str(task["owner"]),
                doc_path=f"{snapshot.initiative_root}/.wt/tasks/{task['slug']}/task.json",
                updated_at=str(task["updated_at"]),
                blocked_by=tuple(task.get("blocker_task_ids", ())),
                depends_on=tuple(task.get("dependency_task_ids", ())),
                related_ids=tuple(task.get("related_ids", ())),
            )
            for task in snapshot.task_documents
        )

    def _build_readiness_entry(self, snapshot: _PlanInitiativeSnapshot) -> PlanReadinessIndexEntry:
        initiative = snapshot.initiative_document
        gate_state = initiative["gate_state"]
        return PlanReadinessIndexEntry(
            initiative_id=str(initiative["initiative_id"]),
            trace_id=str(initiative["trace_id"]),
            title=str(initiative["title"]),
            initiative_root=snapshot.initiative_root,
            lifecycle_stage=str(initiative["lifecycle_stage"]),
            review_status=str(initiative["review_status"]),
            capture_complete=bool(gate_state["capture_complete"]),
            machine_valid=bool(gate_state["machine_valid"]),
            approval_status=str(gate_state["approval_status"]),
            ready_for_execution=bool(gate_state["ready_for_execution"]),
            blocking_reasons=tuple(gate_state.get("blocking_reasons", ())),
            updated_at=str(initiative["updated_at"]),
            scope_type=str(initiative["scope_type"]),
        )

    def _build_discrepancy_entries(
        self,
        snapshot: _PlanInitiativeSnapshot,
    ) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        initiative = snapshot.initiative_document
        return tuple(
            PlanDiscrepancyIndexEntry(
                discrepancy_id=str(document["discrepancy_id"]),
                initiative_id=str(initiative["initiative_id"]),
                trace_id=str(initiative["trace_id"]),
                title=str(initiative["title"]),
                category=str(document["category"]),
                severity=str(document["severity"]),
                gate_effect=str(document["gate_effect"]),
                status=str(document["status"]),
                summary=str(document["summary"]),
                source_paths=tuple(document.get("source_paths", ())),
                updated_at=str(document["updated_at"]),
            )
            for document in snapshot.discrepancy_documents
        )

    def _build_active_task_summary(
        self,
        snapshot: _PlanInitiativeSnapshot,
        task_document: dict[str, object],
    ) -> InitiativeActiveTaskSummary:
        unresolved_dependencies = tuple(
            dependency
            for dependency in task_document.get("dependency_task_ids", ())
            if _task_status_for_id(snapshot.task_documents, str(dependency))
            not in _TERMINAL_TASK_STATUSES
        )
        unresolved_blockers = tuple(
            blocker
            for blocker in task_document.get("blocker_task_ids", ())
            if _task_status_for_id(snapshot.task_documents, str(blocker))
            not in _TERMINAL_TASK_STATUSES
        )
        local_status = str(task_document["status"])
        is_actionable = (
            local_status == "ready"
            and not unresolved_dependencies
            and not unresolved_blockers
        )
        return InitiativeActiveTaskSummary(
            task_id=str(task_document["task_id"]),
            title=str(task_document["title"]),
            task_status=_TASK_STATUS_MAP[local_status],
            priority=str(task_document["priority"]),
            owner=str(task_document["owner"]),
            doc_path=f"{snapshot.initiative_root}/.wt/tasks/{task_document['slug']}/task.json",
            is_actionable=is_actionable,
            blocked_by=unresolved_blockers,
            depends_on=unresolved_dependencies,
        )

    def _build_coordination_document(
        self,
        entries: tuple[InitiativeIndexEntry, ...],
    ) -> dict[str, object]:
        active_entries = tuple(
            entry for entry in entries if entry.initiative_status == "active"
        )
        actionable_tasks = tuple(
            sorted(
                (
                    CoordinationTaskSummary(
                        trace_id=entry.trace_id,
                        initiative_title=entry.title,
                        task_id=task.task_id,
                        title=task.title,
                        task_status=task.task_status,
                        priority=task.priority,
                        owner=task.owner,
                        doc_path=task.doc_path,
                        is_actionable=task.is_actionable,
                        blocked_by=task.blocked_by,
                        depends_on=task.depends_on,
                    )
                    for entry in active_entries
                    for task in entry.active_task_summaries
                    if task.is_actionable
                ),
                key=lambda item: (
                    _TASK_STATUS_ORDER.get(item.task_status, 99),
                    _PRIORITY_ORDER.get(item.priority, 99),
                    item.trace_id,
                    item.task_id,
                ),
            )
        )
        recent_closed = tuple(
            CoordinationRecentInitiativeSummary(
                trace_id=entry.trace_id,
                title=entry.title,
                initiative_status=entry.initiative_status,
                closed_at=entry.closed_at or entry.updated_at,
                key_surface_path=entry.key_surface_path,
                closure_reason=entry.closure_reason,
            )
            for entry in entries
            if entry.initiative_status != "active"
        )[:10]
        if not active_entries:
            summary = "No active plan-workspace initiatives exist."
            next_action = "Bootstrap a new initiative package before starting execution."
            surface_path = PLAN_OVERVIEW_PATH
            coordination_mode = "ready_for_bootstrap"
        else:
            focus_entry = sorted(
                active_entries,
                key=lambda entry: (
                    0 if any(task.is_actionable for task in entry.active_task_summaries) else 1,
                    _PHASE_ORDER.get(entry.current_phase, 99),
                    entry.trace_id,
                ),
            )[0]
            coordination_mode = (
                "blocked_work"
                if not actionable_tasks and any(entry.blocked_task_count > 0 for entry in active_entries)
                else "active_work"
            )
            summary = (
                "Active plan-workspace initiatives exist and the coordination surface points to the current pack-wide next work."
            )
            next_action = focus_entry.next_action
            surface_path = focus_entry.next_surface_path
        document = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:coordination-index:v1",
            "id": "index.coordination",
            "title": "Plan Workspace Coordination Index",
            "status": "active",
            "updated_at": _latest_timestamp(entry.updated_at for entry in entries),
            "coordination_mode": coordination_mode,
            "summary": summary,
            "recommended_next_action": next_action,
            "recommended_surface_path": surface_path,
            "active_initiative_count": len(active_entries),
            "blocked_task_count": sum(entry.blocked_task_count for entry in active_entries),
            "actionable_task_count": len(actionable_tasks),
            "entries": [serialize_initiative_entry(entry, compact=True) for entry in active_entries],
            "actionable_tasks": [
                {
                    "trace_id": task.trace_id,
                    "initiative_title": task.initiative_title,
                    "task_id": task.task_id,
                    "title": task.title,
                    "task_status": task.task_status,
                    "priority": task.priority,
                    "owner": task.owner,
                    "doc_path": task.doc_path,
                    "is_actionable": task.is_actionable,
                    **({"blocked_by": list(task.blocked_by)} if task.blocked_by else {}),
                    **({"depends_on": list(task.depends_on)} if task.depends_on else {}),
                }
                for task in actionable_tasks
            ],
            "recent_closed_initiatives": [
                {
                    "trace_id": entry.trace_id,
                    "title": entry.title,
                    "initiative_status": entry.initiative_status,
                    "closed_at": entry.closed_at,
                    "key_surface_path": entry.key_surface_path,
                    **({"closure_reason": entry.closure_reason} if entry.closure_reason else {}),
                }
                for entry in recent_closed
            ],
        }
        return document

    def _render_plan_overview(self, coordination_document: dict[str, object]) -> str:
        actionable_task_lines = "\n".join(
            f"- `{entry['task_id']}` ({entry['priority']}) in `{entry['trace_id']}` -> `{entry['doc_path']}`"
            for entry in coordination_document["actionable_tasks"]
        ) or "- None."
        initiative_lines = "\n".join(
            f"- `{entry['trace_id']}`: {entry['title']} (`{entry['current_phase']}`)"
            for entry in coordination_document["entries"]
        ) or "- None."
        return "\n".join(
            (
                "# Plan Overview",
                "",
                "## Current State",
                f"- `coordination_mode`: `{coordination_document['coordination_mode']}`",
                f"- `summary`: {coordination_document['summary']}",
                f"- `recommended_next_action`: {coordination_document['recommended_next_action']}",
                f"- `recommended_surface_path`: `{coordination_document['recommended_surface_path']}`",
                "",
                "## Active Initiatives",
                initiative_lines,
                "",
                "## Actionable Tasks",
                actionable_task_lines,
                "",
            )
        )

    def _render_initiative_views(
        self,
        snapshots: tuple[_PlanInitiativeSnapshot, ...],
    ) -> dict[str, str]:
        documents: dict[str, str] = {}
        for snapshot in snapshots:
            initiative = snapshot.initiative_document
            readiness = self._build_readiness_entry(snapshot)
            task_lines = "\n".join(
                f"- `{task['task_id']}`: `{task['status']}` ({task['priority']})"
                for task in snapshot.task_documents
            )
            deferred_lines = "\n".join(
                f"- `{document['deferred_item_id']}`: `{document['status']}`"
                for document in snapshot.deferred_documents
            ) or "- None."
            discrepancy_lines = "\n".join(
                f"- `{document['discrepancy_id']}`: `{document['status']}` / `{document['category']}`"
                for document in snapshot.discrepancy_documents
            ) or "- None."
            root = snapshot.initiative_root
            documents[f"{root}/plan.md"] = "\n".join(
                (
                    f"# {initiative['title']} Plan",
                    "",
                    "## Summary",
                    str(initiative["summary"]),
                    "",
                    "## Identity",
                    f"- `initiative_id`: `{initiative['initiative_id']}`",
                    f"- `trace_id`: `{initiative['trace_id']}`",
                    f"- `lifecycle_stage`: `{initiative['lifecycle_stage']}`",
                    f"- `review_status`: `{initiative['review_status']}`",
                    "",
                    "## Task Plan",
                    task_lines or "- None.",
                    "",
                    "## Deferred Items",
                    deferred_lines,
                    "",
                )
            )
            documents[f"{root}/progress.md"] = "\n".join(
                (
                    f"# {initiative['title']} Progress",
                    "",
                    "## Gate State",
                    f"- `capture_complete`: `{readiness.capture_complete}`",
                    f"- `machine_valid`: `{readiness.machine_valid}`",
                    f"- `approval_status`: `{readiness.approval_status}`",
                    f"- `ready_for_execution`: `{readiness.ready_for_execution}`",
                    f"- `blocking_reasons`: `{', '.join(readiness.blocking_reasons) if readiness.blocking_reasons else 'none'}`",
                    "",
                    "## Task Status",
                    task_lines or "- None.",
                    "",
                    "## Discrepancies",
                    discrepancy_lines,
                    "",
                )
            )
            documents[f"{root}/summary.md"] = "\n".join(
                (
                    f"# {initiative['title']} Summary",
                    "",
                    "## Lifecycle",
                    f"- `lifecycle_stage`: `{initiative['lifecycle_stage']}`",
                    f"- `owner`: `{initiative['owner']}`",
                    f"- `updated_at`: `{initiative['updated_at']}`",
                    "",
                    "## Evidence",
                    "\n".join(
                        f"- `{document['id']}`: `{document['status']}`"
                        for document in snapshot.evidence_documents
                    ) or "- None.",
                    "",
                    "## Closeout",
                    "\n".join(
                        f"- `{document['id']}`: `{document['status']}`"
                        for document in snapshot.closeout_documents
                    ) or "- None.",
                    "",
                    "## Promotion",
                    "\n".join(
                        f"- `{document['id']}`: `{document['status']}`"
                        for document in snapshot.promotion_documents
                    ) or "- None.",
                    "",
                )
            )
        return documents

    def _load_initiative_snapshots(self) -> tuple[_PlanInitiativeSnapshot, ...]:
        initiatives_root = self._loader.repo_root / "plan" / "initiatives"
        if not initiatives_root.exists():
            return ()
        snapshots: list[_PlanInitiativeSnapshot] = []
        for initiative_path in sorted(initiatives_root.iterdir()):
            if not initiative_path.is_dir():
                continue
            initiative_state_path = initiative_path / ".wt" / "initiative.json"
            if not initiative_state_path.exists():
                continue
            initiative_document = json.loads(initiative_state_path.read_text(encoding="utf-8"))
            snapshots.append(
                _PlanInitiativeSnapshot(
                    initiative_document=initiative_document,
                    task_documents=self._load_json_documents(initiative_path / ".wt" / "tasks", "task.json"),
                    deferred_documents=self._load_json_documents(initiative_path / ".wt" / "deferred", "*.json"),
                    discrepancy_documents=self._load_json_documents(
                        initiative_path / ".wt" / "discrepancies",
                        "*.json",
                    ),
                    evidence_documents=self._load_json_documents(initiative_path / ".wt" / "evidence", "*.json"),
                    closeout_documents=self._load_json_documents(initiative_path / ".wt" / "closeout", "*.json"),
                    promotion_documents=self._load_json_documents(initiative_path / ".wt" / "promotions", "*.json"),
                    initiative_root=str(initiative_path.relative_to(self._loader.repo_root)),
                )
            )
        return tuple(snapshots)

    def _load_json_documents(self, root: Path, pattern: str) -> tuple[dict[str, object], ...]:
        if not root.exists():
            return ()
        if pattern == "task.json":
            paths = sorted(root.glob("*/task.json"))
        else:
            paths = sorted(root.glob(pattern))
        return tuple(json.loads(path.read_text(encoding="utf-8")) for path in paths)

    def _pack_loader(self) -> ControlPlaneLoader:
        return ControlPlaneLoader(
            self._loader.repo_root,
            active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def _load_plan_json(self, relative_path: str) -> dict[str, object]:
        document = self._pack_loader().load_validated_document(relative_path)
        assert isinstance(document, dict)
        return document

    def _write_json(self, relative_path: str, document: dict[str, object]) -> None:
        self._loader.artifact_store.write_json_object(relative_path, document)

    def _write_markdown(self, relative_path: str, content: str) -> None:
        path = self._loader.repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{content.rstrip()}\n", encoding="utf-8")

    def _serialize_task_entry(self, entry: PlanTaskIndexEntry) -> dict[str, object]:
        payload: dict[str, object] = {
            "task_id": entry.task_id,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "initiative_title": entry.initiative_title,
            "title": entry.title,
            "summary": entry.summary,
            "status": entry.status,
            "priority": entry.priority,
            "owner": entry.owner,
            "doc_path": entry.doc_path,
            "updated_at": entry.updated_at,
        }
        if entry.blocked_by:
            payload["blocked_by"] = list(entry.blocked_by)
        if entry.depends_on:
            payload["depends_on"] = list(entry.depends_on)
        if entry.related_ids:
            payload["related_ids"] = list(entry.related_ids)
        return payload

    def _serialize_readiness_entry(self, entry: PlanReadinessIndexEntry) -> dict[str, object]:
        return {
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "title": entry.title,
            "initiative_root": entry.initiative_root,
            "scope_type": entry.scope_type,
            "lifecycle_stage": entry.lifecycle_stage,
            "review_status": entry.review_status,
            "capture_complete": entry.capture_complete,
            "machine_valid": entry.machine_valid,
            "approval_status": entry.approval_status,
            "ready_for_execution": entry.ready_for_execution,
            "blocking_reasons": list(entry.blocking_reasons),
            "updated_at": entry.updated_at,
        }

    def _serialize_discrepancy_entry(self, entry: PlanDiscrepancyIndexEntry) -> dict[str, object]:
        return {
            "discrepancy_id": entry.discrepancy_id,
            "initiative_id": entry.initiative_id,
            "trace_id": entry.trace_id,
            "title": entry.title,
            "category": entry.category,
            "severity": entry.severity,
            "gate_effect": entry.gate_effect,
            "status": entry.status,
            "summary": entry.summary,
            "source_paths": list(entry.source_paths),
            "updated_at": entry.updated_at,
        }


def _task_status_for_id(
    task_documents: tuple[dict[str, object], ...],
    task_id: str,
) -> str | None:
    for task_document in task_documents:
        if task_document["task_id"] == task_id:
            return str(task_document["status"])
    return None


def _initiative_status(document: dict[str, object]) -> str:
    lifecycle_stage = str(document["lifecycle_stage"])
    if lifecycle_stage in _TERMINAL_LIFECYCLE_STAGES:
        return lifecycle_stage
    return "active"


def _current_phase_for_lifecycle(lifecycle_stage: str) -> str:
    if lifecycle_stage in {"capture_incomplete", "ready_for_review", "ready_for_execution"}:
        return "implementation_planning"
    if lifecycle_stage in {"in_progress", "blocked"}:
        return "execution"
    if lifecycle_stage == "closing":
        return "closeout"
    return "closed"


def _next_action(
    snapshot: _PlanInitiativeSnapshot,
    readiness: PlanReadinessIndexEntry,
) -> str:
    if readiness.blocking_reasons:
        return "Resolve blocking reasons and rebuild derived surfaces before execution."
    if readiness.review_status != "approved" and not readiness.ready_for_execution:
        return "Review and approve the initiative package for execution."
    if readiness.ready_for_execution:
        return "Start the highest-priority ready task from the initiative package."
    if snapshot.initiative_document["lifecycle_stage"] == "closing":
        return "Finalize closeout, evidence, and promotion decisions."
    return "Keep initiative-local task state current before opening follow-up work."


def _next_surface_path(
    snapshot: _PlanInitiativeSnapshot,
    readiness: PlanReadinessIndexEntry,
) -> str:
    if readiness.blocking_reasons:
        return f"{snapshot.initiative_root}/progress.md"
    if readiness.ready_for_execution:
        return f"{snapshot.initiative_root}/plan.md"
    return f"{snapshot.initiative_root}/progress.md"


def _latest_timestamp(values: object) -> str:
    normalized = [value for value in values if isinstance(value, str) and value]
    return max(normalized, default=utc_timestamp_now())


def _search_task_entries(
    entries: tuple[PlanTaskIndexEntry, ...],
    params: PlanTaskSearchParams,
) -> tuple[PlanTaskIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    trace_id = normalize_optional_text(params.trace_id)
    status = normalize_optional_text(params.status)
    priority = normalize_optional_text(params.priority)
    owner = normalize_optional_text(params.owner)
    matches: list[tuple[int, PlanTaskIndexEntry]] = []
    for entry in entries:
        if initiative_id is not None and normalize_text(entry.initiative_id) != initiative_id:
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if status is not None and normalize_text(entry.status) != status:
            continue
        if priority is not None and normalize_text(entry.priority) != priority:
            continue
        if owner is not None and normalize_text(entry.owner) != owner:
            continue
        if params.blocked_only and not entry.blocked_by:
            continue
        score = query_score(
            params.query,
            (
                entry.task_id,
                entry.initiative_id,
                entry.trace_id,
                entry.initiative_title,
                entry.title,
                entry.summary,
                entry.status,
                entry.priority,
                entry.owner,
                entry.doc_path,
                *entry.blocked_by,
                *entry.depends_on,
                *entry.related_ids,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(
        key=lambda item: (
            -item[0],
            _TASK_STATUS_ORDER.get(item[1].status, 99),
            _PRIORITY_ORDER.get(item[1].priority, 99),
            item[1].task_id,
        )
    )
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def _search_readiness_entries(
    entries: tuple[PlanReadinessIndexEntry, ...],
    params: PlanReadinessSearchParams,
) -> tuple[PlanReadinessIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    trace_id = normalize_optional_text(params.trace_id)
    lifecycle_stage = normalize_optional_text(params.lifecycle_stage)
    review_status = normalize_optional_text(params.review_status)
    matches: list[tuple[int, PlanReadinessIndexEntry]] = []
    for entry in entries:
        if initiative_id is not None and normalize_text(entry.initiative_id) != initiative_id:
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if lifecycle_stage is not None and normalize_text(entry.lifecycle_stage) != lifecycle_stage:
            continue
        if review_status is not None and normalize_text(entry.review_status) != review_status:
            continue
        if (
            params.ready_for_execution is not None
            and entry.ready_for_execution != params.ready_for_execution
        ):
            continue
        if params.blocked_only and not entry.blocking_reasons:
            continue
        score = query_score(
            params.query,
            (
                entry.initiative_id,
                entry.trace_id,
                entry.title,
                entry.initiative_root,
                entry.lifecycle_stage,
                entry.review_status,
                entry.approval_status,
                *entry.blocking_reasons,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].initiative_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def _search_discrepancy_entries(
    entries: tuple[PlanDiscrepancyIndexEntry, ...],
    params: PlanDiscrepancySearchParams,
) -> tuple[PlanDiscrepancyIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    trace_id = normalize_optional_text(params.trace_id)
    category = normalize_optional_text(params.category)
    severity = normalize_optional_text(params.severity)
    status = normalize_optional_text(params.status)
    matches: list[tuple[int, PlanDiscrepancyIndexEntry]] = []
    for entry in entries:
        if initiative_id is not None and normalize_text(entry.initiative_id) != initiative_id:
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if category is not None and normalize_text(entry.category) != category:
            continue
        if severity is not None and normalize_text(entry.severity) != severity:
            continue
        if status is not None and normalize_text(entry.status) != status:
            continue
        if params.blocking_only and entry.gate_effect == "none":
            continue
        score = query_score(
            params.query,
            (
                entry.discrepancy_id,
                entry.initiative_id,
                entry.trace_id,
                entry.title,
                entry.category,
                entry.severity,
                entry.gate_effect,
                entry.status,
                entry.summary,
                *entry.source_paths,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].discrepancy_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)
