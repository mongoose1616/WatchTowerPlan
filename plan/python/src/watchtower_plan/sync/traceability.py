"""Deterministic rebuild helpers for the traceability index."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.path_support import add_existing_paths
from watchtower_plan.workspace.service import PLAN_PACK_SETTINGS_PATH
from watchtower_plan.sync.traceability_support import (
    TRACEABILITY_INDEX_ARTIFACT_PATH,
    TraceAccumulator,
    iter_validated_documents,
    load_entries,
    load_existing_trace_entries,
    merge_values,
    optional_string,
    tuple_of_strings,
)

ACCEPTANCE_CONTRACT_DIRECTORY = "core/control_plane/contracts/acceptance"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/records/validation_evidence"


class TraceabilityIndexSyncService:
    """Build and write the traceability index from governed source artifacts."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._plan_loader = loader.derive(
            active_pack_settings_path=PLAN_PACK_SETTINGS_PATH
        )
        self._repo_root = loader.repo_root
        self._workspace_paths = PackWorkspacePaths.from_loader(
            self._plan_loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._task_index_path = self._workspace_paths.index_path("task_index.json")

    @classmethod
    def from_repo_root(
        cls, repo_root: Path | None = None
    ) -> TraceabilityIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        accumulators: dict[str, TraceAccumulator] = {}
        existing_entries = load_existing_trace_entries(self._loader)

        self._merge_live_initiatives(accumulators)
        self._merge_task_index(accumulators)
        self._merge_acceptance_contracts(accumulators)
        self._merge_validation_evidence(accumulators)
        self._merge_existing_state(accumulators, existing_entries)

        if not accumulators:
            raise ValueError("Traceability index rebuild produced no trace entries.")

        published_entries = [
            accumulators[trace_id].build_document()
            for trace_id in sorted(accumulators)
            if accumulators[trace_id].should_publish()
        ]
        if not published_entries:
            raise ValueError(
                "Traceability index rebuild produced no publishable trace entries."
            )

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:traceability-index:v1",
            "id": "index.traceability",
            "title": "Traceability Index",
            "status": "active",
            "entries": published_entries,
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(
        self, document: dict[str, object], destination: Path | None = None
    ) -> Path:
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

    def _merge_live_initiatives(
        self, accumulators: dict[str, TraceAccumulator]
    ) -> None:
        for relative_path in self._initiative_state_paths():
            document = json.loads(
                (self._repo_root / PurePosixPath(relative_path)).read_text(
                    encoding="utf-8"
                )
            )
            trace_id = str(document["trace_id"])
            accumulator = self._accumulator(accumulators, trace_id)
            accumulator.has_live_initiative_state = True
            accumulator.merge_primary(
                rank=1,
                title=str(document["title"]),
                summary=str(document["summary"]),
                status="active",
                updated_at=str(document["updated_at"]),
            )
            merge_values(accumulator.task_ids, tuple_of_strings(document, "task_ids"))
            merge_values(
                accumulator.source_surface_paths,
                tuple(
                    str(record["path"])
                    for record in document.get("authored_inputs", ())
                    if isinstance(record, dict) and isinstance(record.get("path"), str)
                ),
            )
            add_existing_paths(
                self._repo_root,
                accumulator.related_paths,
                (
                    relative_path,
                    *tuple_of_strings(document, "closeout_ids", "promotion_ids"),
                    *tuple(
                        str(record["path"])
                        for record in document.get("authored_inputs", ())
                        if isinstance(record, dict)
                        and isinstance(record.get("path"), str)
                    ),
                ),
            )
            if self._initiative_is_closed(document):
                accumulator.initiative_status = str(document["status"])
                accumulator.closed_at = optional_string(document, "closed_at")
                accumulator.closure_reason = optional_string(document, "closure_reason")
                accumulator.superseded_by_trace_id = optional_string(
                    document,
                    "superseded_by_trace_id",
                )
                if accumulator.closed_at is not None:
                    accumulator._timestamps.add(accumulator.closed_at)

    def _initiative_state_paths(self) -> tuple[str, ...]:
        paths: list[str] = []
        for root in (
            self._repo_root / self._workspace_paths.initiatives_root,
            self._repo_root / self._workspace_paths.projects_root,
        ):
            if not root.exists():
                continue
            for path in sorted(root.glob("**/.wt/initiative.json")):
                paths.append(path.relative_to(self._repo_root).as_posix())
        return tuple(paths)

    @staticmethod
    def _initiative_is_closed(document: dict[str, Any]) -> bool:
        status = document.get("status")
        return isinstance(status, str) and status in {
            "completed",
            "superseded",
            "cancelled",
            "abandoned",
        }

    def _merge_task_index(self, accumulators: dict[str, TraceAccumulator]) -> None:
        document = self._plan_loader.load_validated_document(self._task_index_path)
        for entry in load_entries(document, label=self._task_index_path):
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

    def _merge_acceptance_contracts(
        self, accumulators: dict[str, TraceAccumulator]
    ) -> None:
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
            merge_values(
                accumulator.acceptance_contract_ids, tuple_of_strings(document, "id")
            )
            merge_values(
                accumulator.source_surface_paths,
                tuple_of_strings(document, "source_surface_path"),
            )
            add_existing_paths(
                self._repo_root, accumulator.related_paths, (relative_path,)
            )
            entries = document.get("entries")
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                merge_values(
                    accumulator.acceptance_ids, tuple_of_strings(entry, "acceptance_id")
                )
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

    def _merge_validation_evidence(
        self, accumulators: dict[str, TraceAccumulator]
    ) -> None:
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
            add_existing_paths(
                self._repo_root,
                accumulator.source_surface_paths,
                tuple_of_strings(document, "source_surface_paths"),
            )
            merge_values(
                accumulator.acceptance_contract_ids,
                tuple_of_strings(document, "source_acceptance_contract_ids"),
            )
            add_existing_paths(
                self._repo_root, accumulator.related_paths, (relative_path,)
            )
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
                merge_values(
                    accumulator.validator_ids, tuple_of_strings(check, "validator_id")
                )
                merge_values(
                    accumulator.acceptance_ids,
                    tuple_of_strings(check, "acceptance_ids"),
                )
                add_existing_paths(
                    self._repo_root,
                    accumulator.related_paths,
                    tuple_of_strings(check, "subject_paths"),
                )
