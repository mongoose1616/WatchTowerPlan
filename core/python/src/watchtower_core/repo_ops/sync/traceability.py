"""Deterministic rebuild helpers for the traceability index."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root

PRD_INDEX_PATH = "core/control_plane/indexes/prds/prd_index.v1.json"
DECISION_INDEX_PATH = "core/control_plane/indexes/decisions/decision_index.v1.json"
DESIGN_DOCUMENT_INDEX_PATH = (
    "core/control_plane/indexes/design_documents/design_document_index.v1.json"
)
TASK_INDEX_PATH = "core/control_plane/indexes/tasks/task_index.v1.json"
TRACEABILITY_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/traceability/traceability_index.v1.json"
)
ACCEPTANCE_CONTRACT_DIRECTORY = "core/control_plane/contracts/acceptance"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"


def _path_exists(repo_root: Path, relative_path: str) -> bool:
    resolved = repo_root / relative_path.rstrip("/")
    return resolved.exists()


def _add_existing_paths(repo_root: Path, destination: set[str], values: tuple[str, ...]) -> None:
    for value in values:
        if _path_exists(repo_root, value):
            destination.add(value)


def _merge_values(destination: set[str], values: tuple[str, ...]) -> None:
    destination.update(value for value in values if value)


def _resolve_status(statuses: set[str]) -> str:
    if "active" in statuses:
        return "active"
    if "draft" in statuses:
        return "draft"
    if "deprecated" in statuses:
        return "deprecated"
    return "active"


def _trace_title(trace_id: str) -> str:
    trace_name = trace_id.removeprefix("trace.")
    words: list[str] = []
    for token in trace_name.split("."):
        words.extend(part for part in token.split("_") if part)
    return " ".join(word.capitalize() for word in words) or trace_id


def _load_entries(document: dict[str, Any], *, label: str) -> list[dict[str, Any]]:
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{label} is missing its entries list.")
    return [entry for entry in entries if isinstance(entry, dict)]


def _load_existing_trace_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    path = loader.repo_root / TRACEABILITY_INDEX_ARTIFACT_PATH
    if not path.exists():
        return {}
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        return {}
    entries = loaded.get("entries")
    if not isinstance(entries, list):
        return {}

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        trace_id = entry.get("trace_id")
        if isinstance(trace_id, str):
            existing[trace_id] = entry
    return existing


def _iter_validated_documents(
    loader: ControlPlaneLoader,
    relative_directory: str,
) -> list[tuple[str, dict[str, Any]]]:
    directory = loader.repo_root / relative_directory
    documents: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(directory.glob("*.json")):
        relative_path = path.relative_to(loader.repo_root).as_posix()
        document = loader.load_validated_document(relative_path)
        documents.append((relative_path, document))
    return documents


@dataclass(slots=True)
class TraceAccumulator:
    """Mutable trace assembly state while rebuilding the traceability index."""

    trace_id: str
    title: str | None = None
    summary: str | None = None
    note: str | None = None
    initiative_status: str = "active"
    closed_at: str | None = None
    closure_reason: str | None = None
    superseded_by_trace_id: str | None = None
    _primary_rank: int = 999
    _note_rank: int = 999
    _statuses: set[str] = field(default_factory=set)
    _timestamps: set[str] = field(default_factory=set)
    _has_active_tasks: bool = False
    prd_ids: set[str] = field(default_factory=set)
    decision_ids: set[str] = field(default_factory=set)
    design_ids: set[str] = field(default_factory=set)
    plan_ids: set[str] = field(default_factory=set)
    task_ids: set[str] = field(default_factory=set)
    requirement_ids: set[str] = field(default_factory=set)
    acceptance_ids: set[str] = field(default_factory=set)
    acceptance_contract_ids: set[str] = field(default_factory=set)
    validator_ids: set[str] = field(default_factory=set)
    evidence_ids: set[str] = field(default_factory=set)
    related_paths: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=lambda: {"traceability"})

    def merge_primary(
        self,
        *,
        rank: int,
        title: str,
        summary: str,
        status: str,
        updated_at: str | None,
        note: str | None = None,
    ) -> None:
        if rank < self._primary_rank or self.title is None or self.summary is None:
            self.title = title
            self.summary = summary
            self._primary_rank = rank
        self._statuses.add(status)
        if updated_at is not None:
            self._timestamps.add(updated_at)
        self.merge_note(rank=rank, note=note)

    def merge_note(self, *, rank: int, note: str | None) -> None:
        if not note:
            return
        if rank < self._note_rank or self.note is None:
            self.note = note
            self._note_rank = rank

    def build_document(self) -> dict[str, object]:
        if self.title is None:
            self.title = _trace_title(self.trace_id)
        if self.summary is None:
            self.summary = "Joined traceability record derived from current governed sources."
        if not self._timestamps:
            raise ValueError(
                f"Traceability entry requires at least one timestamped source: {self.trace_id}"
            )

        document: dict[str, object] = {
            "trace_id": self.trace_id,
            "title": self.title,
            "summary": self.summary,
            "status": _resolve_status(self._statuses),
            "initiative_status": self.initiative_status,
            "updated_at": max(self._timestamps),
        }
        if self.initiative_status != "active":
            if self.closed_at is None or self.closure_reason is None:
                raise ValueError(
                    f"Closed trace {self.trace_id} is missing closeout metadata."
                )
            document["closed_at"] = self.closed_at
            document["closure_reason"] = self.closure_reason
            if self.initiative_status == "superseded":
                if self.superseded_by_trace_id is None:
                    raise ValueError(
                        f"Superseded trace {self.trace_id} is missing superseded_by_trace_id."
                    )
                document["superseded_by_trace_id"] = self.superseded_by_trace_id
        self._set_list_field(document, "prd_ids", self.prd_ids)
        self._set_list_field(document, "decision_ids", self.decision_ids)
        self._set_list_field(document, "design_ids", self.design_ids)
        self._set_list_field(document, "plan_ids", self.plan_ids)
        self._set_list_field(document, "task_ids", self.task_ids)
        self._set_list_field(document, "requirement_ids", self.requirement_ids)
        self._set_list_field(document, "acceptance_ids", self.acceptance_ids)
        self._set_list_field(
            document,
            "acceptance_contract_ids",
            self.acceptance_contract_ids,
        )
        self._set_list_field(document, "validator_ids", self.validator_ids)
        self._set_list_field(document, "evidence_ids", self.evidence_ids)
        self._set_list_field(document, "related_paths", self.related_paths)
        self._set_list_field(document, "tags", self.tags)
        if self.note is not None:
            document["notes"] = self.note
        return document

    def preserve_existing_state(self, entry: dict[str, Any]) -> None:
        initiative_status = entry.get("initiative_status")
        if isinstance(initiative_status, str) and initiative_status:
            self.initiative_status = initiative_status
        closed_at = entry.get("closed_at")
        if isinstance(closed_at, str) and closed_at:
            self.closed_at = closed_at
        closure_reason = entry.get("closure_reason")
        if isinstance(closure_reason, str) and closure_reason:
            self.closure_reason = closure_reason
        superseded_by_trace_id = entry.get("superseded_by_trace_id")
        if isinstance(superseded_by_trace_id, str) and superseded_by_trace_id:
            self.superseded_by_trace_id = superseded_by_trace_id
        note = entry.get("notes")
        if isinstance(note, str) and note:
            self.merge_note(rank=900, note=note)
        self._reopen_completed_initiative_if_needed()

    def mark_task_state(self, *, task_status: str) -> None:
        if task_status not in {"done", "cancelled"}:
            self._has_active_tasks = True

    def _reopen_completed_initiative_if_needed(self) -> None:
        if self.initiative_status != "completed" or not self._has_active_tasks:
            return
        self.initiative_status = "active"
        self.closed_at = None
        self.closure_reason = None
        self.superseded_by_trace_id = None

    @staticmethod
    def _set_list_field(document: dict[str, object], field_name: str, values: set[str]) -> None:
        if values:
            document[field_name] = sorted(values)


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
        existing_entries = _load_existing_trace_entries(self._loader)

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
        for entry in _load_entries(document, label=PRD_INDEX_PATH):
            trace_id = str(entry["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=1,
                title=str(entry["title"]),
                summary=str(entry["summary"]),
                status=str(entry["status"]),
                updated_at=str(entry["updated_at"]),
                note=_optional_string(entry, "notes"),
            )
            _merge_values(accumulator.prd_ids, _tuple_of_strings(entry, "prd_id"))
            _merge_values(accumulator.decision_ids, _tuple_of_strings(entry, "linked_decision_ids"))
            _merge_values(accumulator.design_ids, _tuple_of_strings(entry, "linked_design_ids"))
            _merge_values(accumulator.plan_ids, _tuple_of_strings(entry, "linked_plan_ids"))
            _merge_values(accumulator.requirement_ids, _tuple_of_strings(entry, "requirement_ids"))
            _merge_values(accumulator.acceptance_ids, _tuple_of_strings(entry, "acceptance_ids"))
            _merge_values(accumulator.tags, _tuple_of_strings(entry, "tags"))
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                _tuple_of_strings(entry, "doc_path", "related_paths"),
            )

    def _merge_decision_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(DECISION_INDEX_PATH)
        for entry in _load_entries(document, label=DECISION_INDEX_PATH):
            trace_id = str(entry["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.merge_primary(
                rank=3,
                title=str(entry["title"]),
                summary=str(entry["summary"]),
                status=str(entry["record_status"]),
                updated_at=str(entry["updated_at"]),
                note=_optional_string(entry, "notes"),
            )
            _merge_values(accumulator.prd_ids, _tuple_of_strings(entry, "linked_prd_ids"))
            _merge_values(accumulator.decision_ids, _tuple_of_strings(entry, "decision_id"))
            _merge_values(accumulator.design_ids, _tuple_of_strings(entry, "linked_design_ids"))
            _merge_values(accumulator.plan_ids, _tuple_of_strings(entry, "linked_plan_ids"))
            _merge_values(accumulator.tags, _tuple_of_strings(entry, "tags"))
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                _tuple_of_strings(entry, "doc_path", "related_paths"),
            )

    def _merge_design_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(DESIGN_DOCUMENT_INDEX_PATH)
        for entry in _load_entries(document, label=DESIGN_DOCUMENT_INDEX_PATH):
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
                note=_optional_string(entry, "notes"),
            )
            if family == "feature_design":
                _merge_values(accumulator.design_ids, _tuple_of_strings(entry, "document_id"))
            else:
                _merge_values(accumulator.plan_ids, _tuple_of_strings(entry, "document_id"))
            _merge_values(accumulator.tags, _tuple_of_strings(entry, "tags"))
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                _tuple_of_strings(entry, "doc_path", "source_paths", "related_paths"),
            )

    def _merge_task_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._loader.load_validated_document(TASK_INDEX_PATH)
        for entry in _load_entries(document, label=TASK_INDEX_PATH):
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
                note=_optional_string(entry, "notes"),
            )
            _merge_values(accumulator.task_ids, _tuple_of_strings(entry, "task_id"))
            _merge_values(accumulator.tags, _tuple_of_strings(entry, "tags"))
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                _tuple_of_strings(entry, "doc_path", "applies_to"),
            )

    def _merge_acceptance_contracts(self, accumulators: dict[str, TraceAccumulator]) -> None:
        for relative_path, document in _iter_validated_documents(
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
            _merge_values(
                accumulator.acceptance_contract_ids,
                _tuple_of_strings(document, "id"),
            )
            _merge_values(accumulator.prd_ids, _tuple_of_strings(document, "source_prd_id"))
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                (relative_path,),
            )
            entries = document.get("entries")
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                _merge_values(
                    accumulator.acceptance_ids,
                    _tuple_of_strings(entry, "acceptance_id"),
                )
                _merge_values(
                    accumulator.requirement_ids,
                    _tuple_of_strings(entry, "source_requirement_ids"),
                )
                _merge_values(
                    accumulator.validator_ids,
                    _tuple_of_strings(entry, "required_validator_ids"),
                )
                _add_existing_paths(
                    self._repo_root,
                    accumulator.related_paths,
                    _tuple_of_strings(entry, "validation_targets", "related_paths"),
                )

    def _merge_validation_evidence(self, accumulators: dict[str, TraceAccumulator]) -> None:
        for relative_path, document in _iter_validated_documents(
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
                note=_optional_string(document, "notes"),
            )
            _merge_values(accumulator.evidence_ids, _tuple_of_strings(document, "id"))
            _merge_values(accumulator.prd_ids, _tuple_of_strings(document, "source_prd_ids"))
            _merge_values(
                accumulator.decision_ids,
                _tuple_of_strings(document, "source_decision_ids"),
            )
            _merge_values(accumulator.design_ids, _tuple_of_strings(document, "source_design_ids"))
            _merge_values(accumulator.plan_ids, _tuple_of_strings(document, "source_plan_ids"))
            _merge_values(
                accumulator.acceptance_contract_ids,
                _tuple_of_strings(document, "source_acceptance_contract_ids"),
            )
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                (relative_path,),
            )
            _add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                _tuple_of_strings(document, "related_paths"),
            )
            checks = document.get("checks")
            if not isinstance(checks, list):
                continue
            for check in checks:
                if not isinstance(check, dict):
                    continue
                _merge_values(
                    accumulator.validator_ids,
                    _tuple_of_strings(check, "validator_id"),
                )
                _merge_values(
                    accumulator.acceptance_ids,
                    _tuple_of_strings(check, "acceptance_ids"),
                )
                _add_existing_paths(
                    self._repo_root,
                    accumulator.related_paths,
                    _tuple_of_strings(check, "subject_paths"),
                )


def _optional_string(document: dict[str, Any], key: str) -> str | None:
    value = document.get(key)
    return value if isinstance(value, str) and value else None


def _tuple_of_strings(document: dict[str, Any], *keys: str) -> tuple[str, ...]:
    values: list[str] = []
    for key in keys:
        value = document.get(key)
        if isinstance(value, str) and value:
            values.append(value)
            continue
        if isinstance(value, list):
            values.extend(item for item in value if isinstance(item, str) and item)
    return tuple(values)
