"""Guarded trace-package purge helpers and minimal surviving ledger writes."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import (
    TRACE_PURGE_LEDGER_DIRECTORY,
    ControlPlaneLoader,
)
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    PrdIndexEntry,
    TaskIndexEntry,
    TraceabilityEntry,
    ValidationEvidenceArtifact,
)
from watchtower_core.repo_ops.sync.all import AllSyncService
from watchtower_core.utils import utc_timestamp_now
from watchtower_core.validation import AcceptanceReconciliationService

TRACE_PURGE_RECORD_SCHEMA_ID = "urn:watchtower:schema:artifacts:ledgers:trace-purge-record:v1"
TERMINAL_INITIATIVE_STATUSES = frozenset(
    {"completed", "superseded", "cancelled", "abandoned"}
)
TERMINAL_TASK_STATUSES = frozenset({"done", "cancelled"})
TRACE_LOCAL_ROOTS = (
    "docs/planning/prds/",
    "docs/planning/decisions/",
    "docs/planning/design/features/",
    "docs/planning/design/implementation/",
    "docs/planning/tasks/open/",
    "docs/planning/tasks/closed/archive/",
    "core/control_plane/contracts/acceptance/",
    "core/control_plane/ledgers/validation_evidence/",
)
DERIVED_REFERENCE_CARRIER_ROOTS = ("core/control_plane/indexes/",)
DERIVED_REFERENCE_CARRIER_PATHS = frozenset(
    {
        "docs/planning/coordination_tracking.md",
        "docs/planning/initiatives/initiative_tracking.md",
        "docs/planning/prds/prd_tracking.md",
        "docs/planning/design/design_tracking.md",
        "docs/planning/decisions/decision_tracking.md",
        "docs/planning/tasks/task_tracking.md",
    }
)
DEFAULT_REFERENCE_SCAN_ROOTS = (".github", "core", "docs", "workflows")
SCANNABLE_TEXT_EXTENSIONS = frozenset(
    {".json", ".md", ".py", ".toml", ".yaml", ".yml", ".txt", ".sh", ".lock"}
)


@dataclass(frozen=True, slots=True)
class TracePurgeResult:
    """Result summary for one guarded trace purge."""

    trace_id: str
    title: str
    initiative_status: str
    closed_at: str
    closure_reason: str
    purged_at: str
    wrote: bool
    removed_paths: tuple[str, ...]
    retained_authority_paths: tuple[str, ...]
    purge_ledger_relative_path: str
    purge_ledger_output_path: str | None
    refreshed_targets: tuple[str, ...]


class TracePurgeService:
    """Delete one closed trace package after validating purge preconditions."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        all_sync_factory: Callable[[ControlPlaneLoader], AllSyncService] | None = None,
    ) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root
        self._all_sync_factory = all_sync_factory or AllSyncService

    def purge(
        self,
        *,
        trace_id: str,
        retained_authority_paths: tuple[str, ...] = (),
        purged_at: str | None = None,
        write: bool,
    ) -> TracePurgeResult:
        trace_entry = self._load_trace_entry(trace_id)
        if trace_entry.initiative_status not in TERMINAL_INITIATIVE_STATUSES:
            allowed = ", ".join(sorted(TERMINAL_INITIATIVE_STATUSES))
            raise ValueError(
                f"Trace purge requires a terminal initiative status ({allowed}); "
                f"{trace_id} is {trace_entry.initiative_status}."
            )
        if trace_entry.closed_at is None:
            raise ValueError(
                f"Trace {trace_id} is missing closed_at and cannot be purged safely."
            )
        if trace_entry.closure_reason is None:
            raise ValueError(
                f"Trace {trace_id} is missing closure_reason and cannot be purged safely."
            )

        open_task_ids = self._open_task_ids(trace_id)
        if open_task_ids:
            joined = ", ".join(open_task_ids)
            raise ValueError(
                f"Trace {trace_id} still has open linked tasks: {joined}. "
                "Close or cancel every linked task before purging the trace package."
            )

        acceptance_service = AcceptanceReconciliationService(self._loader)
        if trace_id in acceptance_service.acceptance_trace_ids():
            acceptance_result = acceptance_service.validate(trace_id)
            if acceptance_result.issue_count:
                raise ValueError(
                    f"Trace {trace_id} has {acceptance_result.issue_count} acceptance "
                    "reconciliation issue(s). Reconcile the trace before purging it."
                )

        existing_record = next(
            (
                record
                for record in self._loader.load_trace_purge_records()
                if record.trace_id == trace_id
            ),
            None,
        )
        if existing_record is not None:
            raise ValueError(
                f"Trace {trace_id} already has a purge ledger entry at {existing_record.doc_path}."
            )

        package_paths = self._package_paths(trace_id)
        if not package_paths:
            raise ValueError(
                f"Trace {trace_id} does not resolve to a purgeable planning package."
            )

        missing_paths = tuple(
            relative_path
            for relative_path in package_paths
            if not self._loader.resolve_path(relative_path).exists()
        )
        if missing_paths:
            missing = ", ".join(missing_paths)
            raise ValueError(
                f"Trace {trace_id} has already-drifted package paths: {missing}. "
                "Repair the retained planning surfaces before purging the trace."
            )

        resolved_authority_paths = self._resolve_retained_authority_paths(
            trace_entry=trace_entry,
            package_paths=package_paths,
            explicit_paths=retained_authority_paths,
        )
        if not resolved_authority_paths:
            raise ValueError(
                f"Trace {trace_id} does not resolve to surviving canonical authority paths. "
                "Pass --retained-authority-path explicitly after promoting the durable rule."
            )

        surviving_reference_paths = self._find_surviving_reference_paths(
            trace_entry=trace_entry,
            package_paths=package_paths,
        )
        if surviving_reference_paths:
            joined = ", ".join(surviving_reference_paths)
            raise ValueError(
                "Surviving canonical surfaces still reference purgeable trace material: "
                f"{joined}. Repair those references before purging {trace_id}."
            )

        resolved_purged_at = purged_at or utc_timestamp_now()
        ledger_relative_path = _ledger_relative_path(trace_id)
        ledger_document = self._build_ledger_document(
            trace_entry=trace_entry,
            package_paths=package_paths,
            retained_authority_paths=resolved_authority_paths,
            purged_at=resolved_purged_at,
        )

        ledger_path = self._loader.resolve_path(ledger_relative_path)
        if ledger_path.exists():
            raise ValueError(
                f"Trace purge ledger path already exists for {trace_id}: {ledger_relative_path}."
            )

        purge_ledger_output_path: str | None = None
        refreshed_targets: tuple[str, ...] = ()
        if write:
            self._delete_package_paths(package_paths)
            purge_ledger_output_path = str(
                self._loader.artifact_store.write_json_object(
                    ledger_relative_path,
                    ledger_document,
                )
            )
            runtime_loader = ControlPlaneLoader(self._repo_root)
            sync_result = self._all_sync_factory(runtime_loader).run(write=True)
            refreshed_targets = tuple(record.target for record in sync_result.records)

        return TracePurgeResult(
            trace_id=trace_id,
            title=trace_entry.title,
            initiative_status=trace_entry.initiative_status,
            closed_at=trace_entry.closed_at,
            closure_reason=trace_entry.closure_reason,
            purged_at=resolved_purged_at,
            wrote=write,
            removed_paths=package_paths,
            retained_authority_paths=resolved_authority_paths,
            purge_ledger_relative_path=ledger_relative_path,
            purge_ledger_output_path=purge_ledger_output_path,
            refreshed_targets=refreshed_targets,
        )

    def _load_trace_entry(self, trace_id: str) -> TraceabilityEntry:
        try:
            return self._loader.load_traceability_index().get(trace_id)
        except KeyError as exc:
            raise ValueError(f"Unknown trace ID: {trace_id}") from exc

    def _open_task_ids(self, trace_id: str) -> tuple[str, ...]:
        task_index = self._loader.load_task_index()
        candidate_entries = {
            entry.task_id: entry
            for entry in task_index.entries
            if entry.trace_id == trace_id
        }
        if not candidate_entries:
            return ()
        return tuple(
            sorted(
                task_id
                for task_id, entry in candidate_entries.items()
                if entry.task_status not in TERMINAL_TASK_STATUSES
            )
        )

    def _package_paths(self, trace_id: str) -> tuple[str, ...]:
        package_paths: set[str] = set()

        package_paths.update(
            entry.doc_path
            for entry in self._entries_for_trace(self._loader.load_prd_index().entries, trace_id)
        )
        package_paths.update(
            entry.doc_path
            for entry in self._entries_for_trace(
                self._loader.load_decision_index().entries,
                trace_id,
            )
        )
        package_paths.update(
            entry.doc_path
            for entry in self._entries_for_trace(
                self._loader.load_design_document_index().entries,
                trace_id,
            )
        )
        package_paths.update(
            entry.doc_path
            for entry in self._entries_for_trace(self._loader.load_task_index().entries, trace_id)
        )
        package_paths.update(
            artifact.doc_path
            for artifact in self._entries_for_trace(
                self._loader.load_acceptance_contracts(),
                trace_id,
            )
        )
        package_paths.update(
            artifact.doc_path
            for artifact in self._entries_for_trace(
                self._loader.load_validation_evidence_artifacts(),
                trace_id,
            )
        )

        return tuple(sorted(package_paths))

    def _resolve_retained_authority_paths(
        self,
        *,
        trace_entry: TraceabilityEntry,
        package_paths: tuple[str, ...],
        explicit_paths: tuple[str, ...],
    ) -> tuple[str, ...]:
        resolved: list[str] = []
        seen: set[str] = set()

        def add(relative_path: str) -> None:
            normalized = _normalize_repo_relative_path(relative_path)
            if normalized in seen:
                return
            if normalized in package_paths:
                raise ValueError(
                    "Retained authority path cannot point back into the purge package: "
                    f"{normalized}"
                )
            if _is_derived_reference_carrier(normalized):
                return
            if normalized in {
                "docs/planning/",
                "docs/planning",
                "core/control_plane/",
                "core/control_plane",
            }:
                return
            if not self._loader.resolve_path(normalized).exists():
                raise ValueError(
                    f"Retained authority path does not exist for purge: {normalized}"
                )
            seen.add(normalized)
            resolved.append(normalized)

        if explicit_paths:
            for relative_path in explicit_paths:
                add(relative_path)
        else:
            for relative_path in trace_entry.related_paths:
                if _is_trace_local_path(relative_path):
                    continue
                add(relative_path)

        return tuple(sorted(resolved))

    def _build_ledger_document(
        self,
        *,
        trace_entry: TraceabilityEntry,
        package_paths: tuple[str, ...],
        retained_authority_paths: tuple[str, ...],
        purged_at: str,
    ) -> dict[str, object]:
        document: dict[str, object] = {
            "$schema": TRACE_PURGE_RECORD_SCHEMA_ID,
            "id": _ledger_record_id(trace_entry.trace_id),
            "title": f"Trace Purge Record for {trace_entry.title}",
            "status": "active",
            "trace_id": trace_entry.trace_id,
            "initiative_status": trace_entry.initiative_status,
            "closed_at": trace_entry.closed_at,
            "purged_at": purged_at,
            "closure_reason": trace_entry.closure_reason,
            "summary": (
                "Removed the closed trace-local planning package after validating terminal "
                "state, acceptance reconciliation, and surviving canonical authority."
            ),
            "surviving_authority_paths": list(retained_authority_paths),
            "purged_paths": list(package_paths),
        }
        self._loader.schema_store.validate_instance(
            document,
            schema_id=TRACE_PURGE_RECORD_SCHEMA_ID,
        )
        return document

    def _find_surviving_reference_paths(
        self,
        *,
        trace_entry: TraceabilityEntry,
        package_paths: tuple[str, ...],
    ) -> tuple[str, ...]:
        search_tokens = {
            trace_entry.trace_id,
            *trace_entry.prd_ids,
            *trace_entry.decision_ids,
            *trace_entry.design_ids,
            *trace_entry.plan_ids,
            *trace_entry.task_ids,
            *trace_entry.requirement_ids,
            *trace_entry.acceptance_ids,
            *trace_entry.acceptance_contract_ids,
            *trace_entry.evidence_ids,
            *package_paths,
        }
        conflicts: list[str] = []
        for path in _iter_reference_scan_files(self._repo_root):
            relative_path = path.relative_to(self._repo_root).as_posix()
            if relative_path in package_paths or _is_derived_reference_carrier(relative_path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(token and token in text for token in search_tokens):
                conflicts.append(relative_path)
        return tuple(sorted(conflicts))

    def _delete_package_paths(self, package_paths: tuple[str, ...]) -> None:
        deleted_paths = sorted(package_paths, reverse=True)
        for relative_path in deleted_paths:
            path = self._loader.resolve_path(relative_path)
            if not path.exists():
                raise ValueError(f"Package path disappeared before purge: {relative_path}")
            path.unlink()
            self._prune_empty_ancestors(path)

    def _prune_empty_ancestors(self, path: Path) -> None:
        prune_roots = tuple(
            self._loader.resolve_path(root.rstrip("/")) for root in TRACE_LOCAL_ROOTS
        )
        current = path.parent
        while any(current != root and _is_within(current, root) for root in prune_roots):
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent

    @staticmethod
    def _entries_for_trace[
        TEntry: PrdIndexEntry
        | DecisionIndexEntry
        | DesignDocumentIndexEntry
        | TaskIndexEntry
        | AcceptanceContract
        | ValidationEvidenceArtifact
    ](
        entries: Iterable[TEntry],
        trace_id: str,
    ) -> tuple[TEntry, ...]:
        return tuple(entry for entry in entries if entry.trace_id == trace_id)


def _ledger_record_id(trace_id: str) -> str:
    if trace_id.startswith("trace."):
        return f"purge.{trace_id.removeprefix('trace.')}"
    return f"purge.{trace_id}"


def _ledger_relative_path(trace_id: str) -> str:
    slug_source = trace_id.removeprefix("trace.")
    slug = re.sub(r"[^a-z0-9]+", "_", slug_source.casefold()).strip("_") or "trace"
    return f"{TRACE_PURGE_LEDGER_DIRECTORY}/{slug}_purge_record.json"


def _is_trace_local_path(relative_path: str) -> bool:
    normalized = relative_path.rstrip("/")
    return any(
        normalized == root.rstrip("/") or normalized.startswith(root)
        for root in TRACE_LOCAL_ROOTS
    )


def _is_derived_reference_carrier(relative_path: str) -> bool:
    normalized = relative_path.rstrip("/")
    return normalized in DERIVED_REFERENCE_CARRIER_PATHS or any(
        normalized == root.rstrip("/") or normalized.startswith(root)
        for root in DERIVED_REFERENCE_CARRIER_ROOTS
    )


def _normalize_repo_relative_path(relative_path: str) -> str:
    normalized = PurePosixPath(relative_path.rstrip("/"))
    if normalized.is_absolute() or not normalized.parts or ".." in normalized.parts:
        raise ValueError(f"Expected a repository-relative path, received: {relative_path}")
    return normalized.as_posix()


def _iter_reference_scan_files(repo_root: Path) -> tuple[Path, ...]:
    files: list[Path] = []

    for top_level in DEFAULT_REFERENCE_SCAN_ROOTS:
        root = repo_root / top_level
        if not root.exists():
            continue
        files.extend(_iter_text_files_under(root))

    for top_level_file in ("AGENTS.md", "README.md"):
        path = repo_root / top_level_file
        if path.exists():
            files.append(path)

    return tuple(sorted(set(files)))


def _iter_text_files_under(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix and path.suffix not in SCANNABLE_TEXT_EXTENSIONS:
            continue
        yield path


def _is_within(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True
