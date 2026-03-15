"""Private shared helpers for trace-scoped planning projection snapshots."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    InitiativeActiveTaskSummary,
    PlanningCoordinationSection,
    PrdIndexEntry,
    TaskIndexEntry,
    TraceabilityEntry,
    ValidationEvidenceArtifact,
)
from watchtower_core.repo_ops.planning_projection_policy import (
    build_trace_planning_policy_snapshot,
)
from watchtower_core.repo_ops.planning_projection_source_assembly import (
    build_trace_planning_projection_source_assembly,
)
from watchtower_core.repo_ops.planning_projection_task_selection import (
    TERMINAL_TASK_STATUSES,
    build_trace_planning_task_selection,
)


@dataclass(frozen=True, slots=True)
class TracePlanningProjectionSnapshot:
    """Trace-scoped planning sources shared by initiative and catalog projections."""

    trace_entry: TraceabilityEntry
    prd_entries: tuple[PrdIndexEntry, ...] = ()
    decision_entries: tuple[DecisionIndexEntry, ...] = ()
    design_entries: tuple[DesignDocumentIndexEntry, ...] = ()
    task_entries: tuple[TaskIndexEntry, ...] = ()
    acceptance_contracts: tuple[AcceptanceContract, ...] = ()
    validation_evidence: tuple[ValidationEvidenceArtifact, ...] = ()


@dataclass(frozen=True, slots=True)
class TracePlanningCoordinationSnapshot:
    """Private coordination projection derived from one trace snapshot."""

    current_phase: str
    key_surface_path: str
    next_action: str
    next_surface_path: str
    open_task_count: int
    blocked_task_count: int
    primary_owner: str | None = None
    active_owners: tuple[str, ...] = ()
    active_task_ids: tuple[str, ...] = ()
    active_task_summaries: tuple[InitiativeActiveTaskSummary, ...] = ()
    blocked_by_task_ids: tuple[str, ...] = ()

    def to_planning_coordination_section(self) -> PlanningCoordinationSection:
        """Render the coordination snapshot into the public planning-catalog model."""

        return PlanningCoordinationSection(
            current_phase=self.current_phase,
            key_surface_path=self.key_surface_path,
            next_action=self.next_action,
            next_surface_path=self.next_surface_path,
            open_task_count=self.open_task_count,
            blocked_task_count=self.blocked_task_count,
            primary_owner=self.primary_owner,
            active_owners=self.active_owners,
            active_task_ids=self.active_task_ids,
            active_task_summaries=self.active_task_summaries,
            blocked_by_task_ids=self.blocked_by_task_ids,
        )


def build_trace_planning_projection_snapshots(
    loader: ControlPlaneLoader,
) -> tuple[TracePlanningProjectionSnapshot, ...]:
    """Load all trace-scoped planning snapshots in traceability index order."""

    traceability_index = loader.load_traceability_index()
    sources = build_trace_planning_projection_source_assembly(loader)

    return tuple(
        TracePlanningProjectionSnapshot(
            trace_entry=trace_entry,
            prd_entries=sources.prd_entries_for(trace_entry.trace_id),
            decision_entries=sources.decision_entries_for(trace_entry.trace_id),
            design_entries=sources.design_entries_for(trace_entry.trace_id),
            task_entries=sources.task_entries_for(trace_entry.trace_id),
            acceptance_contracts=sources.acceptance_contracts_for(trace_entry.trace_id),
            validation_evidence=sources.validation_evidence_for(trace_entry.trace_id),
        )
        for trace_entry in traceability_index.entries
    )


def build_trace_planning_coordination_snapshot(
    snapshot: TracePlanningProjectionSnapshot,
) -> TracePlanningCoordinationSnapshot:
    """Derive the shared coordination projection for one trace snapshot."""

    active_tasks = tuple(
        entry
        for entry in snapshot.task_entries
        if entry.task_status not in TERMINAL_TASK_STATUSES
    )
    task_lookup = {entry.task_id: entry for entry in snapshot.task_entries}
    task_selection = build_trace_planning_task_selection(active_tasks, task_lookup)
    policy = build_trace_planning_policy_snapshot(
        trace_entry=snapshot.trace_entry,
        prd_entries=snapshot.prd_entries,
        design_entries=snapshot.design_entries,
        decision_entries=snapshot.decision_entries,
        task_entries=snapshot.task_entries,
        active_tasks=active_tasks,
        task_lookup=task_lookup,
        task_selection=task_selection,
    )
    return TracePlanningCoordinationSnapshot(
        current_phase=policy.current_phase,
        key_surface_path=policy.key_surface_path,
        next_action=policy.next_action,
        next_surface_path=policy.next_surface_path,
        open_task_count=len(active_tasks),
        blocked_task_count=task_selection.blocked_task_count,
        primary_owner=task_selection.primary_owner,
        active_owners=task_selection.active_owners,
        active_task_ids=task_selection.active_task_ids,
        active_task_summaries=task_selection.active_task_summaries,
        blocked_by_task_ids=task_selection.blocked_by_task_ids,
    )
