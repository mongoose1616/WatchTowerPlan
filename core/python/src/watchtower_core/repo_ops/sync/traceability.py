"""Deterministic rebuild helpers for the traceability index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.traceability_support import (
    TRACEABILITY_INDEX_ARTIFACT_PATH,
    TraceAccumulator,
    add_existing_paths,
    iter_validated_documents,
    load_entries,
    load_existing_trace_entries,
    merge_values,
    optional_string,
    tuple_of_strings,
)

PRD_INDEX_PATH = "core/control_plane/indexes/prds/prd_index.v1.json"
DECISION_INDEX_PATH = "core/control_plane/indexes/decisions/decision_index.v1.json"
DESIGN_DOCUMENT_INDEX_PATH = (
    "core/control_plane/indexes/design_documents/design_document_index.v1.json"
)
TASK_INDEX_PATH = "core/control_plane/indexes/tasks/task_index.v1.json"
ACCEPTANCE_CONTRACT_DIRECTORY = "core/control_plane/contracts/acceptance"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"


class TraceabilityIndexSyncService:
    """Build and write the traceability index from governed source artifacts."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> TraceabilityIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        accumulators: dict[str, TraceAccumulator] = {}
        existing_entries = load_existing_trace_entries(self._loader)

        self._merge_prd_index(accumulators)
        self._merge_decision_index(accumulators)
        self._merge_design_index(accumulators)
        self._merge_task_index(accumulators)
        self._merge_acceptance_contracts(accumulators)
        self._merge_validation_evidence(accumulators)
        self._merge_existing_state(accumulators, existing_entries)

        if not accumulators:
            raise ValueError("Traceability index rebuild produced no trace entries.")

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:traceability-index:v1",
            "id": "index.traceability",
            "title": "Traceability Index",
            "status": "active",
            "entries": [
                accumulators[trace_id].build_document()
                for trace_id in sorted(accumulators)
            ],
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated traceability index to disk."""

        target = destination or (self._repo_root / TRACEABILITY_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _accumulator(
        self,
        accumulators: dict[str, TraceAccumulator],
        trace_id: str,
    ) -> TraceAccumulator:
        accumulator = accumulators.get(trace_id)
        if accumulator is None:
            accumulator = TraceAccumulator(trace_id=trace_id)
            accumulators[trace_id] = accumulator
        return accumulator

    def _merge_existing_state(
        self,
        accumulators: dict[str, TraceAccumulator],
        existing_entries: dict[str, dict[str, Any]],
    ) -> None:
        for trace_id, accumulator in accumulators.items():
            existing = existing_entries.get(trace_id)
            if existing is None:
                continue
            accumulator.preserve_existing_state(existing)

    def _merge_prd_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(PRD_INDEX_PATH)
        for entry in load_entries(document, label=PRD_INDEX_PATH):
            trace_id = str(entry["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=1,
                title=str(entry["title"]),
                summary=str(entry["summary"]),
                status=str(entry["status"]),
                updated_at=str(entry["updated_at"]),
                note=optional_string(entry, "notes"),
            )
            merge_values(accumulator.prd_ids, tuple_of_strings(entry, "prd_id"))
            merge_values(accumulator.decision_ids, tuple_of_strings(entry, "linked_decision_ids"))
            merge_values(accumulator.design_ids, tuple_of_strings(entry, "linked_design_ids"))
            merge_values(accumulator.plan_ids, tuple_of_strings(entry, "linked_plan_ids"))
            merge_values(accumulator.requirement_ids, tuple_of_strings(entry, "requirement_ids"))
            merge_values(accumulator.acceptance_ids, tuple_of_strings(entry, "acceptance_ids"))
            merge_values(accumulator.tags, tuple_of_strings(entry, "tags"))
            add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                tuple_of_strings(entry, "doc_path", "related_paths"),
            )

    def _merge_decision_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(DECISION_INDEX_PATH)
        for entry in load_entries(document, label=DECISION_INDEX_PATH):
            trace_id = str(entry["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=3,
                title=str(entry["title"]),
                summary=str(entry["summary"]),
                status=str(entry["record_status"]),
                updated_at=str(entry["updated_at"]),
                note=optional_string(entry, "notes"),
            )
            merge_values(accumulator.prd_ids, tuple_of_strings(entry, "linked_prd_ids"))
            merge_values(accumulator.decision_ids, tuple_of_strings(entry, "decision_id"))
            merge_values(accumulator.design_ids, tuple_of_strings(entry, "linked_design_ids"))
            merge_values(accumulator.plan_ids, tuple_of_strings(entry, "linked_plan_ids"))
            merge_values(accumulator.tags, tuple_of_strings(entry, "tags"))
            add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                tuple_of_strings(entry, "doc_path", "related_paths"),
            )

    def _merge_design_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(DESIGN_DOCUMENT_INDEX_PATH)
        for entry in load_entries(document, label=DESIGN_DOCUMENT_INDEX_PATH):
            trace_id = str(entry["trace_id"])
            family = str(entry["family"])
            rank = 2 if family == "feature_design" else 4
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=rank,
                title=str(entry["title"]),
                summary=str(entry["summary"]),
                status=str(entry["status"]),
                updated_at=str(entry["updated_at"]),
                note=optional_string(entry, "notes"),
            )
            if family == "feature_design":
                merge_values(accumulator.design_ids, tuple_of_strings(entry, "document_id"))
            else:
                merge_values(accumulator.plan_ids, tuple_of_strings(entry, "document_id"))
            merge_values(accumulator.tags, tuple_of_strings(entry, "tags"))
            add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                tuple_of_strings(entry, "doc_path", "source_paths", "related_paths"),
            )

    def _merge_task_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(TASK_INDEX_PATH)
        for entry in load_entries(document, label=TASK_INDEX_PATH):
            trace_id_value = entry.get("trace_id")
            if not isinstance(trace_id_value, str) or not trace_id_value:
                continue
            accumulator = self._accumulator(accumulators, trace_id_value)
            task_status = entry.get("task_status")
            if isinstance(task_status, str):
                accumulator.mark_task_state(task_status=task_status)
            accumulator.merge_primary(
                rank=5,
                title=str(entry["title"]),
                summary=str(entry["summary"]),
                status=str(entry["status"]),
                updated_at=str(entry["updated_at"]),
                note=optional_string(entry, "notes"),
            )
            merge_values(accumulator.task_ids, tuple_of_strings(entry, "task_id"))
            merge_values(accumulator.tags, tuple_of_strings(entry, "tags"))
            add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                tuple_of_strings(entry, "doc_path", "applies_to"),
            )

    def _merge_acceptance_contracts(self, accumulators: dict[str, TraceAccumulator]) -> None:
        for relative_path, document in iter_validated_documents(
            self._loader,
            ACCEPTANCE_CONTRACT_DIRECTORY,
        ):
            trace_id = str(document["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=5,
                title=str(document["title"]),
                summary=f"Traceability join derived from acceptance contract {document['id']}.",
                status=str(document["status"]),
                updated_at=None,
            )
            merge_values(accumulator.acceptance_contract_ids, tuple_of_strings(document, "id"))
            merge_values(accumulator.prd_ids, tuple_of_strings(document, "source_prd_id"))
            add_existing_paths(self._repo_root, accumulator.related_paths, (relative_path,))
            entries = document.get("entries")
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                merge_values(accumulator.acceptance_ids, tuple_of_strings(entry, "acceptance_id"))
                merge_values(
                    accumulator.requirement_ids,
                    tuple_of_strings(entry, "source_requirement_ids"),
                )
                merge_values(
                    accumulator.validator_ids,
                    tuple_of_strings(entry, "required_validator_ids"),
                )
                add_existing_paths(
                    self._repo_root,
                    accumulator.related_paths,
                    tuple_of_strings(entry, "validation_targets", "related_paths"),
                )

    def _merge_validation_evidence(self, accumulators: dict[str, TraceAccumulator]) -> None:
        for relative_path, document in iter_validated_documents(
            self._loader,
            VALIDATION_EVIDENCE_DIRECTORY,
        ):
            trace_id = str(document["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=6,
                title=str(document["title"]),
                summary=f"Traceability join derived from validation evidence {document['id']}.",
                status=str(document["status"]),
                updated_at=str(document["recorded_at"]),
                note=optional_string(document, "notes"),
            )
            merge_values(accumulator.evidence_ids, tuple_of_strings(document, "id"))
            merge_values(accumulator.prd_ids, tuple_of_strings(document, "source_prd_ids"))
            merge_values(
                accumulator.decision_ids,
                tuple_of_strings(document, "source_decision_ids"),
            )
            merge_values(accumulator.design_ids, tuple_of_strings(document, "source_design_ids"))
            merge_values(accumulator.plan_ids, tuple_of_strings(document, "source_plan_ids"))
            merge_values(
                accumulator.acceptance_contract_ids,
                tuple_of_strings(document, "source_acceptance_contract_ids"),
            )
            add_existing_paths(self._repo_root, accumulator.related_paths, (relative_path,))
            add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                tuple_of_strings(document, "related_paths"),
            )
            checks = document.get("checks")
            if not isinstance(checks, list):
                continue
            for check in checks:
                if not isinstance(check, dict):
                    continue
                merge_values(accumulator.validator_ids, tuple_of_strings(check, "validator_id"))
                merge_values(accumulator.acceptance_ids, tuple_of_strings(check, "acceptance_ids"))
                add_existing_paths(
                    self._repo_root,
                    accumulator.related_paths,
                    tuple_of_strings(check, "subject_paths"),
                )
