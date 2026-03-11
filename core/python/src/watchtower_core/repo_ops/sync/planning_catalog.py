"""Deterministic rebuild helpers for the canonical planning catalog."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    InitiativeIndexEntry,
    PrdIndexEntry,
    TaskIndexEntry,
    TraceabilityEntry,
    ValidationEvidenceArtifact,
)
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import latest_timestamp

PLANNING_CATALOG_ARTIFACT_PATH = (
    "core/control_plane/indexes/planning/planning_catalog.v1.json"
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
        traceability_index = self._loader.load_traceability_index()
        initiative_lookup = {
            entry.trace_id: entry for entry in self._loader.load_initiative_index().entries
        }
        prd_entries = _group_by_trace(self._loader.load_prd_index().entries)
        decision_entries = _group_by_trace(self._loader.load_decision_index().entries)
        design_entries = _group_by_trace(self._loader.load_design_document_index().entries)
        task_entries = _group_by_trace(self._loader.load_task_index().entries)
        acceptance_contracts = _group_by_trace(self._loader.load_acceptance_contracts())
        validation_evidence = _group_by_trace(
            self._loader.load_validation_evidence_artifacts()
        )

        entries = [
            self._build_entry(
                trace_entry=trace_entry,
                initiative_entry=initiative_lookup.get(trace_entry.trace_id),
                prd_entries=prd_entries.get(trace_entry.trace_id, ()),
                decision_entries=decision_entries.get(trace_entry.trace_id, ()),
                design_entries=design_entries.get(trace_entry.trace_id, ()),
                task_entries=task_entries.get(trace_entry.trace_id, ()),
                acceptance_contracts=acceptance_contracts.get(trace_entry.trace_id, ()),
                validation_evidence=validation_evidence.get(trace_entry.trace_id, ()),
            )
            for trace_entry in traceability_index.entries
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
        *,
        trace_entry: TraceabilityEntry,
        initiative_entry: InitiativeIndexEntry | None,
        prd_entries: tuple[PrdIndexEntry, ...],
        decision_entries: tuple[DecisionIndexEntry, ...],
        design_entries: tuple[DesignDocumentIndexEntry, ...],
        task_entries: tuple[TaskIndexEntry, ...],
        acceptance_contracts: tuple[AcceptanceContract, ...],
        validation_evidence: tuple[ValidationEvidenceArtifact, ...],
    ) -> dict[str, object]:
        if initiative_entry is None:
            raise ValueError(
                "Planning catalog could not resolve an initiative entry for "
                f"{trace_entry.trace_id}."
            )

        validator_ids = tuple(
            sorted(
                {
                    *trace_entry.validator_ids,
                    *(
                        validator_id
                        for contract in acceptance_contracts
                        for validator_id in _contract_validator_ids(contract)
                    ),
                    *(
                        validator_id
                        for evidence in validation_evidence
                        for validator_id in _evidence_validator_ids(evidence)
                    ),
                }
            )
        )
        related_paths = tuple(
            sorted(
                {
                    *trace_entry.related_paths,
                    initiative_entry.key_surface_path,
                    initiative_entry.next_surface_path,
                    *(entry.doc_path for entry in prd_entries),
                    *(entry.doc_path for entry in decision_entries),
                    *(entry.doc_path for entry in design_entries),
                    *(entry.doc_path for entry in task_entries),
                    *(entry.doc_path for entry in acceptance_contracts),
                    *(entry.doc_path for entry in validation_evidence),
                    *(
                        path
                        for contract in acceptance_contracts
                        for path in _contract_related_paths(contract)
                    ),
                    *(
                        path
                        for evidence in validation_evidence
                        for path in evidence.related_paths
                    ),
                    *(
                        path
                        for task_entry in task_entries
                        for path in task_entry.applies_to
                    ),
                }
            )
        )
        tags = tuple(
            sorted(
                {
                    *trace_entry.tags,
                    *(entry.family for entry in design_entries),
                    *(
                        task_entry.task_kind
                        for task_entry in task_entries
                    ),
                }
            )
        )
        updated_at = latest_timestamp(
            (
                trace_entry.updated_at,
                initiative_entry.updated_at,
                *(entry.updated_at for entry in prd_entries),
                *(entry.updated_at for entry in decision_entries),
                *(entry.updated_at for entry in design_entries),
                *(entry.updated_at for entry in task_entries),
                *(entry.recorded_at for entry in validation_evidence),
            )
        )

        entry: dict[str, object] = {
            "trace_id": trace_entry.trace_id,
            "title": trace_entry.title,
            "summary": trace_entry.summary,
            "artifact_status": trace_entry.status,
            "initiative_status": trace_entry.initiative_status,
            "updated_at": updated_at,
            "coordination": _coordination_section(initiative_entry),
        }
        if prd_entries:
            entry["prds"] = [_prd_summary(item) for item in prd_entries]
        if decision_entries:
            entry["decisions"] = [_decision_summary(item) for item in decision_entries]
        if design_entries:
            entry["design_documents"] = [
                _design_summary(item) for item in design_entries
            ]
        if task_entries:
            entry["tasks"] = [_task_summary(item) for item in task_entries]
        if acceptance_contracts:
            entry["acceptance_contracts"] = [
                _acceptance_contract_summary(item) for item in acceptance_contracts
            ]
        if validation_evidence:
            entry["validation_evidence"] = [
                _validation_evidence_summary(item) for item in validation_evidence
            ]
        if trace_entry.prd_ids:
            entry["prd_ids"] = list(trace_entry.prd_ids)
        if trace_entry.decision_ids:
            entry["decision_ids"] = list(trace_entry.decision_ids)
        if trace_entry.design_ids:
            entry["design_ids"] = list(trace_entry.design_ids)
        if trace_entry.plan_ids:
            entry["plan_ids"] = list(trace_entry.plan_ids)
        if trace_entry.task_ids:
            entry["task_ids"] = list(trace_entry.task_ids)
        if trace_entry.requirement_ids:
            entry["requirement_ids"] = list(trace_entry.requirement_ids)
        if trace_entry.acceptance_ids:
            entry["acceptance_ids"] = list(trace_entry.acceptance_ids)
        if trace_entry.acceptance_contract_ids:
            entry["acceptance_contract_ids"] = list(
                trace_entry.acceptance_contract_ids
            )
        if trace_entry.evidence_ids:
            entry["evidence_ids"] = list(trace_entry.evidence_ids)
        if validator_ids:
            entry["validator_ids"] = list(validator_ids)
        if related_paths:
            entry["related_paths"] = list(related_paths)
        if tags:
            entry["tags"] = list(tags)
        if trace_entry.notes is not None:
            entry["notes"] = trace_entry.notes
        if trace_entry.closed_at is not None:
            entry["closed_at"] = trace_entry.closed_at
        if trace_entry.closure_reason is not None:
            entry["closure_reason"] = trace_entry.closure_reason
        if trace_entry.superseded_by_trace_id is not None:
            entry["superseded_by_trace_id"] = trace_entry.superseded_by_trace_id
        return entry


def _group_by_trace[T: object](
    entries: tuple[T, ...],
) -> dict[str, tuple[T, ...]]:
    grouped: dict[str, list[T]] = {}
    for entry in entries:
        trace_id = getattr(entry, "trace_id", None)
        if not isinstance(trace_id, str) or not trace_id:
            continue
        grouped.setdefault(trace_id, []).append(entry)
    return {trace_id: tuple(values) for trace_id, values in grouped.items()}


def _coordination_section(entry: InitiativeIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "current_phase": entry.current_phase,
        "key_surface_path": entry.key_surface_path,
        "next_action": entry.next_action,
        "next_surface_path": entry.next_surface_path,
        "open_task_count": entry.open_task_count,
        "blocked_task_count": entry.blocked_task_count,
    }
    if entry.primary_owner is not None:
        document["primary_owner"] = entry.primary_owner
    if entry.active_owners:
        document["active_owners"] = list(entry.active_owners)
    if entry.active_task_ids:
        document["active_task_ids"] = list(entry.active_task_ids)
    if entry.active_task_summaries:
        document["active_task_summaries"] = [
            _active_task_summary(task) for task in entry.active_task_summaries
        ]
    if entry.blocked_by_task_ids:
        document["blocked_by_task_ids"] = list(entry.blocked_by_task_ids)
    return document


def _active_task_summary(task: object) -> dict[str, object]:
    document: dict[str, object] = {
        "task_id": task.task_id,
        "title": task.title,
        "task_status": task.task_status,
        "priority": task.priority,
        "owner": task.owner,
        "doc_path": task.doc_path,
        "is_actionable": task.is_actionable,
    }
    blocked_by = tuple(task.blocked_by)
    depends_on = tuple(task.depends_on)
    if blocked_by:
        document["blocked_by"] = list(blocked_by)
    if depends_on:
        document["depends_on"] = list(depends_on)
    return document


def _prd_summary(entry: PrdIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "prd_id": entry.prd_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    if entry.requirement_ids:
        document["requirement_ids"] = list(entry.requirement_ids)
    if entry.acceptance_ids:
        document["acceptance_ids"] = list(entry.acceptance_ids)
    if entry.linked_decision_ids:
        document["linked_decision_ids"] = list(entry.linked_decision_ids)
    if entry.linked_design_ids:
        document["linked_design_ids"] = list(entry.linked_design_ids)
    if entry.linked_plan_ids:
        document["linked_plan_ids"] = list(entry.linked_plan_ids)
    return document


def _decision_summary(entry: DecisionIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "decision_id": entry.decision_id,
        "title": entry.title,
        "summary": entry.summary,
        "record_status": entry.record_status,
        "decision_status": entry.decision_status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    if entry.linked_prd_ids:
        document["linked_prd_ids"] = list(entry.linked_prd_ids)
    if entry.linked_design_ids:
        document["linked_design_ids"] = list(entry.linked_design_ids)
    if entry.linked_plan_ids:
        document["linked_plan_ids"] = list(entry.linked_plan_ids)
    return document


def _design_summary(entry: DesignDocumentIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "document_id": entry.document_id,
        "family": entry.family,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    if entry.source_paths:
        document["source_paths"] = list(entry.source_paths)
    return document


def _task_summary(entry: TaskIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "task_id": entry.task_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.status,
        "task_status": entry.task_status,
        "task_kind": entry.task_kind,
        "priority": entry.priority,
        "owner": entry.owner,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    if entry.blocked_by:
        document["blocked_by"] = list(entry.blocked_by)
    if entry.depends_on:
        document["depends_on"] = list(entry.depends_on)
    if entry.related_ids:
        document["related_ids"] = list(entry.related_ids)
    if entry.applies_to:
        document["applies_to"] = list(entry.applies_to)
    return document


def _acceptance_contract_summary(entry: AcceptanceContract) -> dict[str, object]:
    document: dict[str, object] = {
        "contract_id": entry.contract_id,
        "title": entry.title,
        "artifact_status": entry.status,
        "source_prd_id": entry.source_prd_id,
        "doc_path": entry.doc_path,
        "acceptance_ids": [item.acceptance_id for item in entry.entries],
    }
    validator_ids = _contract_validator_ids(entry)
    validation_targets = tuple(
        sorted(
            {
                target
                for item in entry.entries
                for target in item.validation_targets
            }
        )
    )
    related_paths = tuple(
        sorted(
            {
                *(
                    path
                    for item in entry.entries
                    for path in item.related_paths
                )
            }
        )
    )
    if validator_ids:
        document["required_validator_ids"] = list(validator_ids)
    if validation_targets:
        document["validation_targets"] = list(validation_targets)
    if related_paths:
        document["related_paths"] = list(related_paths)
    return document


def _contract_related_paths(entry: AcceptanceContract) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                path
                for item in entry.entries
                for path in item.related_paths
            }
        )
    )


def _contract_validator_ids(entry: AcceptanceContract) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                validator_id
                for item in entry.entries
                for validator_id in item.required_validator_ids
            }
        )
    )


def _validation_evidence_summary(entry: ValidationEvidenceArtifact) -> dict[str, object]:
    document: dict[str, object] = {
        "evidence_id": entry.evidence_id,
        "title": entry.title,
        "artifact_status": entry.status,
        "overall_result": entry.overall_result,
        "recorded_at": entry.recorded_at,
        "doc_path": entry.doc_path,
        "check_ids": [check.check_id for check in entry.checks],
    }
    acceptance_ids = tuple(
        sorted(
            {
                acceptance_id
                for check in entry.checks
                for acceptance_id in check.acceptance_ids
            }
        )
    )
    validator_ids = _evidence_validator_ids(entry)
    if acceptance_ids:
        document["acceptance_ids"] = list(acceptance_ids)
    if validator_ids:
        document["validator_ids"] = list(validator_ids)
    if entry.related_paths:
        document["related_paths"] = list(entry.related_paths)
    return document


def _evidence_validator_ids(entry: ValidationEvidenceArtifact) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                check.validator_id
                for check in entry.checks
                if check.validator_id is not None
            }
        )
    )
