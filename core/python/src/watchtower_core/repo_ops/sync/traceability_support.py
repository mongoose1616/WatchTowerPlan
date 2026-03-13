"""Support helpers for rebuilding the traceability index."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader

TRACEABILITY_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/traceability/traceability_index.v1.json"
)


def path_exists(repo_root: Path, relative_path: str) -> bool:
    """Return whether one repo-relative path currently exists."""

    candidate = relative_path.rstrip("/")
    if not candidate:
        return False
    normalized = PurePosixPath(candidate)
    if normalized.is_absolute() or ".." in normalized.parts:
        return False
    resolved = repo_root / normalized
    return resolved.exists()


def add_existing_paths(repo_root: Path, destination: set[str], values: tuple[str, ...]) -> None:
    """Add existing repo-relative paths to a destination set."""

    for value in values:
        if path_exists(repo_root, value):
            destination.add(value)


def existing_paths(repo_root: Path, values: tuple[str, ...]) -> tuple[str, ...]:
    """Return the existing repo-relative paths from one ordered value set."""

    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen or not path_exists(repo_root, value):
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def merge_values(destination: set[str], values: tuple[str, ...]) -> None:
    """Merge non-empty string values into a destination set."""

    destination.update(value for value in values if value)


def resolve_status(statuses: set[str]) -> str:
    """Resolve one derived traceability status from source statuses."""

    if "active" in statuses:
        return "active"
    if "draft" in statuses:
        return "draft"
    if "deprecated" in statuses:
        return "deprecated"
    return "active"


def trace_title(trace_id: str) -> str:
    """Derive a human-readable title from a trace ID."""

    trace_name = trace_id.removeprefix("trace.")
    words: list[str] = []
    for token in trace_name.split("."):
        words.extend(part for part in token.split("_") if part)
    return " ".join(word.capitalize() for word in words) or trace_id


def load_entries(document: dict[str, Any], *, label: str) -> list[dict[str, Any]]:
    """Load and validate the `entries` list from a governed document."""

    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{label} is missing its entries list.")
    return [entry for entry in entries if isinstance(entry, dict)]


def load_existing_trace_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    """Load the existing traceability entries for closed-state preservation."""

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


def iter_validated_documents(
    loader: ControlPlaneLoader,
    relative_directory: str,
) -> list[tuple[str, dict[str, Any]]]:
    """Load every validated document in one repo-relative directory."""

    directory = loader.repo_root / relative_directory
    documents: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(directory.glob("*.json")):
        relative_path = path.relative_to(loader.repo_root).as_posix()
        document = loader.load_validated_document(relative_path)
        documents.append((relative_path, document))
    return documents


def optional_string(document: dict[str, Any], key: str) -> str | None:
    """Return one optional non-empty string from a document."""

    value = document.get(key)
    return value if isinstance(value, str) and value else None


def tuple_of_strings(document: dict[str, Any], *keys: str) -> tuple[str, ...]:
    """Collect one or more scalar or list string fields into one tuple."""

    values: list[str] = []
    for key in keys:
        value = document.get(key)
        if isinstance(value, str) and value:
            values.append(value)
            continue
        if isinstance(value, list):
            values.extend(item for item in value if isinstance(item, str) and item)
    return tuple(values)


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
            self.title = trace_title(self.trace_id)
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
            "status": resolve_status(self._statuses),
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
        existing_updated_at = entry.get("updated_at")
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
        self.reopen_completed_initiative_if_needed()
        if isinstance(existing_updated_at, str) and existing_updated_at:
            self._timestamps.add(existing_updated_at)
        if self.initiative_status != "active" and isinstance(closed_at, str) and closed_at:
            self._timestamps.add(closed_at)

    def mark_task_state(self, *, task_status: str) -> None:
        if task_status not in {"done", "cancelled"}:
            self._has_active_tasks = True

    def reopen_completed_initiative_if_needed(self) -> None:
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
