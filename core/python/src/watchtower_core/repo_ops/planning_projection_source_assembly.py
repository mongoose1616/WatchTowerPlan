"""Private helpers for assembling trace-scoped planning projection sources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    PrdIndexEntry,
    TaskIndexEntry,
    ValidationEvidenceArtifact,
)


class _TraceLinkedEntry(Protocol):
    """Protocol for index entries that carry a shared trace identifier."""

    @property
    def trace_id(self) -> str | None: ...


@dataclass(frozen=True, slots=True)
class TracePlanningProjectionSourceAssembly:
    """Trace-linked planning sources grouped once for downstream projections."""

    prd_entries_by_trace: dict[str, tuple[PrdIndexEntry, ...]]
    decision_entries_by_trace: dict[str, tuple[DecisionIndexEntry, ...]]
    design_entries_by_trace: dict[str, tuple[DesignDocumentIndexEntry, ...]]
    task_entries_by_trace: dict[str, tuple[TaskIndexEntry, ...]]
    acceptance_contracts_by_trace: dict[str, tuple[AcceptanceContract, ...]]
    validation_evidence_by_trace: dict[str, tuple[ValidationEvidenceArtifact, ...]]

    def prd_entries_for(self, trace_id: str) -> tuple[PrdIndexEntry, ...]:
        return self.prd_entries_by_trace.get(trace_id, ())

    def decision_entries_for(self, trace_id: str) -> tuple[DecisionIndexEntry, ...]:
        return self.decision_entries_by_trace.get(trace_id, ())

    def design_entries_for(self, trace_id: str) -> tuple[DesignDocumentIndexEntry, ...]:
        return self.design_entries_by_trace.get(trace_id, ())

    def task_entries_for(self, trace_id: str) -> tuple[TaskIndexEntry, ...]:
        return self.task_entries_by_trace.get(trace_id, ())

    def acceptance_contracts_for(self, trace_id: str) -> tuple[AcceptanceContract, ...]:
        return self.acceptance_contracts_by_trace.get(trace_id, ())

    def validation_evidence_for(
        self,
        trace_id: str,
    ) -> tuple[ValidationEvidenceArtifact, ...]:
        return self.validation_evidence_by_trace.get(trace_id, ())


def build_trace_planning_projection_source_assembly(
    loader: ControlPlaneLoader,
) -> TracePlanningProjectionSourceAssembly:
    """Load and group planning sources once per sync or query pass."""

    return TracePlanningProjectionSourceAssembly(
        prd_entries_by_trace=_group_by_trace(loader.load_prd_index().entries),
        decision_entries_by_trace=_group_by_trace(loader.load_decision_index().entries),
        design_entries_by_trace=_group_by_trace(
            loader.load_design_document_index().entries
        ),
        task_entries_by_trace=_group_by_trace(loader.load_task_index().entries),
        acceptance_contracts_by_trace=_group_by_trace(
            loader.load_acceptance_contracts()
        ),
        validation_evidence_by_trace=_group_by_trace(
            loader.load_validation_evidence_artifacts()
        ),
    )


def _group_by_trace[TTraceLinkedEntry: _TraceLinkedEntry](
    entries: tuple[TTraceLinkedEntry, ...],
) -> dict[str, tuple[TTraceLinkedEntry, ...]]:
    grouped: dict[str, list[TTraceLinkedEntry]] = {}
    for entry in entries:
        trace_id = entry.trace_id
        if not trace_id:
            continue
        grouped.setdefault(trace_id, []).append(entry)
    return {trace_id: tuple(values) for trace_id, values in grouped.items()}
