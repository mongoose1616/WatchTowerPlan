"""Snapshot loading helpers for the plan workspace."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import (
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    VALIDATION_EVIDENCE_DIRECTORY,
    ControlPlaneLoader,
)
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_plan.workspace.support import ordered_unique_strings


@dataclass(frozen=True, slots=True)
class PlanInitiativeSnapshot:
    initiative_document: dict[str, Any]
    task_documents: tuple[dict[str, Any], ...]
    event_documents: tuple[dict[str, Any], ...]
    deferred_documents: tuple[dict[str, Any], ...]
    discrepancy_documents: tuple[dict[str, Any], ...]
    evidence_documents: tuple[dict[str, Any], ...]
    closeout_documents: tuple[dict[str, Any], ...]
    promotion_documents: tuple[dict[str, Any], ...]
    initiative_slug: str
    initiative_root: str
    project_slug: str | None
    project_root: str | None
    discrepancy_namespace: str
    acceptance_contract_ids: tuple[str, ...]
    trace_evidence_ids: tuple[str, ...]


class PlanWorkspaceSnapshotLoader:
    """Load initiative-local workspace snapshots from pack and project roots."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        workspace_paths: PackWorkspacePaths,
    ) -> None:
        self._loader = loader
        self._workspace_paths = workspace_paths

    def load_initiative_snapshots(self) -> tuple[PlanInitiativeSnapshot, ...]:
        snapshots: list[PlanInitiativeSnapshot] = []
        trace_artifact_refs = self._load_trace_artifact_refs()
        pack_initiatives_root = (
            self._loader.repo_root / self._workspace_paths.initiatives_root
        )
        if pack_initiatives_root.exists():
            for initiative_path in sorted(pack_initiatives_root.iterdir()):
                snapshot = self._snapshot_for_initiative_path(
                    initiative_path,
                    project_slug=None,
                    trace_artifact_refs=trace_artifact_refs,
                )
                if snapshot is not None:
                    snapshots.append(snapshot)

        projects_root = self._loader.repo_root / self._workspace_paths.projects_root
        if projects_root.exists():
            for project_path in sorted(projects_root.iterdir()):
                if not project_path.is_dir():
                    continue
                project_slug = project_path.name
                project_initiatives_root = project_path / "initiatives"
                if not project_initiatives_root.exists():
                    continue
                for initiative_path in sorted(project_initiatives_root.iterdir()):
                    snapshot = self._snapshot_for_initiative_path(
                        initiative_path,
                        project_slug=project_slug,
                        trace_artifact_refs=trace_artifact_refs,
                    )
                    if snapshot is not None:
                        snapshots.append(snapshot)
        return tuple(snapshots)

    def _snapshot_for_initiative_path(
        self,
        initiative_path: Path,
        *,
        project_slug: str | None,
        trace_artifact_refs: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
    ) -> PlanInitiativeSnapshot | None:
        if not initiative_path.is_dir():
            return None
        initiative_state_path = initiative_path / ".wt" / "initiative.json"
        if not initiative_state_path.exists():
            return None
        initiative_document = json.loads(
            initiative_state_path.read_text(encoding="utf-8")
        )
        acceptance_contract_ids, trace_evidence_ids = trace_artifact_refs.get(
            str(initiative_document["trace_id"]),
            ((), ()),
        )
        initiative_slug = initiative_path.name
        project_root = (
            self._workspace_paths.project_root_relative(project_slug)
            if project_slug is not None
            else None
        )
        discrepancy_namespace = (
            f"{project_slug}.{initiative_slug}"
            if project_slug is not None
            else initiative_slug
        )
        return PlanInitiativeSnapshot(
            initiative_document=initiative_document,
            task_documents=self._load_json_documents(
                initiative_path / ".wt" / "tasks", "task.json"
            ),
            event_documents=self._load_json_documents(
                initiative_path / ".wt" / "events", "*.json"
            ),
            deferred_documents=self._load_json_documents(
                initiative_path / ".wt" / "deferred", "*.json"
            ),
            discrepancy_documents=self._load_json_documents(
                initiative_path / ".wt" / "discrepancies",
                "*.json",
            ),
            evidence_documents=self._load_json_documents(
                initiative_path / ".wt" / "evidence", "*.json"
            ),
            closeout_documents=self._load_json_documents(
                initiative_path / ".wt" / "closeout", "*.json"
            ),
            promotion_documents=self._load_json_documents(
                initiative_path / ".wt" / "promotions", "*.json"
            ),
            initiative_slug=initiative_slug,
            initiative_root=str(initiative_path.relative_to(self._loader.repo_root)),
            project_slug=project_slug,
            project_root=project_root,
            discrepancy_namespace=discrepancy_namespace,
            acceptance_contract_ids=acceptance_contract_ids,
            trace_evidence_ids=trace_evidence_ids,
        )

    def _load_trace_artifact_refs(
        self,
    ) -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
        refs: dict[str, dict[str, list[str]]] = {}
        for (
            _relative_path,
            document,
        ) in self._loader.iter_validated_documents_with_paths_under(
            ACCEPTANCE_CONTRACTS_DIRECTORY
        ):
            trace_id = str(document.get("trace_id", "")).strip()
            artifact_id = str(document.get("id", "")).strip()
            if not trace_id or not artifact_id:
                continue
            refs.setdefault(
                trace_id, {"acceptance_contract_ids": [], "evidence_ids": []}
            )["acceptance_contract_ids"].append(artifact_id)
        for (
            _relative_path,
            document,
        ) in self._loader.iter_validated_documents_with_paths_under(
            VALIDATION_EVIDENCE_DIRECTORY
        ):
            trace_id = str(document.get("trace_id", "")).strip()
            artifact_id = str(document.get("id", "")).strip()
            if not trace_id or not artifact_id:
                continue
            refs.setdefault(
                trace_id, {"acceptance_contract_ids": [], "evidence_ids": []}
            )["evidence_ids"].append(artifact_id)
        return {
            trace_id: (
                ordered_unique_strings(values["acceptance_contract_ids"]),
                ordered_unique_strings(values["evidence_ids"]),
            )
            for trace_id, values in refs.items()
        }

    def _load_json_documents(
        self, root: Path, pattern: str
    ) -> tuple[dict[str, Any], ...]:
        if not root.exists():
            return ()
        if pattern == "task.json":
            paths = sorted(root.glob("*/task.json"))
        else:
            paths = sorted(root.glob(pattern))
        return tuple(json.loads(path.read_text(encoding="utf-8")) for path in paths)


def snapshot_updated_at(snapshot: PlanInitiativeSnapshot) -> str:
    documents = (
        snapshot.initiative_document,
        *snapshot.task_documents,
        *snapshot.deferred_documents,
        *snapshot.discrepancy_documents,
        *snapshot.evidence_documents,
        *snapshot.closeout_documents,
        *snapshot.promotion_documents,
    )
    return latest_timestamp(document_updated_at(document) for document in documents)


def document_updated_at(document: dict[str, Any]) -> str:
    updated_at = document.get("updated_at")
    if isinstance(updated_at, str) and updated_at:
        return updated_at
    created_at = document.get("created_at")
    if isinstance(created_at, str) and created_at:
        return created_at
    return ""


def existing_document_updated_at(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    if not isinstance(document, dict):
        return ""
    return document_updated_at(document)


def latest_timestamp(values: Iterable[object], *, fallback: str = "") -> str:
    normalized = [value for value in values if isinstance(value, str) and value]
    if normalized:
        return max(normalized)
    if fallback:
        return fallback
    return utc_timestamp_now()
