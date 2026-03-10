"""Coordinated rebuild helpers for all local derived sync surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypeVar

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.command_index import (
    COMMAND_INDEX_ARTIFACT_PATH,
    CommandIndexSyncService,
)
from watchtower_core.sync.decision_index import (
    DECISION_INDEX_ARTIFACT_PATH,
    DecisionIndexSyncService,
)
from watchtower_core.sync.decision_tracking import (
    DECISION_TRACKING_DOCUMENT_PATH,
    DecisionTrackingSyncService,
)
from watchtower_core.sync.design_document_index import (
    DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH,
    DesignDocumentIndexSyncService,
)
from watchtower_core.sync.design_tracking import (
    DESIGN_TRACKING_DOCUMENT_PATH,
    DesignTrackingSyncService,
)
from watchtower_core.sync.foundation_index import (
    FOUNDATION_INDEX_ARTIFACT_PATH,
    FoundationIndexSyncService,
)
from watchtower_core.sync.initiative_index import (
    INITIATIVE_INDEX_ARTIFACT_PATH,
    InitiativeIndexSyncService,
)
from watchtower_core.sync.initiative_tracking import (
    INITIATIVE_TRACKING_DOCUMENT_PATH,
    InitiativeTrackingSyncService,
)
from watchtower_core.sync.prd_index import PRD_INDEX_ARTIFACT_PATH, PrdIndexSyncService
from watchtower_core.sync.prd_tracking import PRD_TRACKING_DOCUMENT_PATH, PrdTrackingSyncService
from watchtower_core.sync.reference_index import (
    REFERENCE_INDEX_ARTIFACT_PATH,
    ReferenceIndexSyncService,
)
from watchtower_core.sync.repository_paths import (
    REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
    RepositoryPathIndexSyncService,
)
from watchtower_core.sync.standard_index import (
    STANDARD_INDEX_ARTIFACT_PATH,
    StandardIndexSyncService,
)
from watchtower_core.sync.task_index import TASK_INDEX_ARTIFACT_PATH, TaskIndexSyncService
from watchtower_core.sync.task_tracking import TASK_TRACKING_DOCUMENT_PATH, TaskTrackingSyncService
from watchtower_core.sync.traceability import (
    TRACEABILITY_INDEX_ARTIFACT_PATH,
    TraceabilityIndexSyncService,
)
from watchtower_core.sync.workflow_index import (
    WORKFLOW_INDEX_ARTIFACT_PATH,
    WorkflowIndexSyncService,
)


@dataclass(frozen=True, slots=True)
class AllSyncRecord:
    """One sync target executed by the all-sync coordinator."""

    target: str
    artifact_kind: str
    relative_output_path: str
    output_path: str | None
    wrote: bool
    record_count: int
    details: dict[str, int]


@dataclass(frozen=True, slots=True)
class AllSyncResult:
    """Aggregated output for one all-sync run."""

    records: tuple[AllSyncRecord, ...]
    wrote: bool
    output_dir: str | None


class DocumentSyncService(Protocol):
    """Protocol for sync services that build JSON index documents."""

    def build_document(self) -> dict[str, object]:
        """Build one JSON document."""

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write one JSON document."""


TrackingResultT = TypeVar("TrackingResultT")


class TrackingSyncService(Protocol[TrackingResultT]):
    """Protocol for sync services that build Markdown tracking outputs."""

    def build_document(self) -> TrackingResultT:
        """Build one tracker result object."""

    def write_document(
        self,
        result: TrackingResultT,
        destination: Path | None = None,
    ) -> Path:
        """Write one tracker result object."""


class AllSyncService:
    """Run all local deterministic sync operations in dependency order."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> AllSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def run(
        self,
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> AllSyncResult:
        records = [
            self._run_document_sync(
                target="command-index",
                artifact_kind="index",
                relative_output_path=COMMAND_INDEX_ARTIFACT_PATH,
                service=CommandIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="foundation-index",
                artifact_kind="index",
                relative_output_path=FOUNDATION_INDEX_ARTIFACT_PATH,
                service=FoundationIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="reference-index",
                artifact_kind="index",
                relative_output_path=REFERENCE_INDEX_ARTIFACT_PATH,
                service=ReferenceIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="standard-index",
                artifact_kind="index",
                relative_output_path=STANDARD_INDEX_ARTIFACT_PATH,
                service=StandardIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="workflow-index",
                artifact_kind="index",
                relative_output_path=WORKFLOW_INDEX_ARTIFACT_PATH,
                service=WorkflowIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="prd-index",
                artifact_kind="index",
                relative_output_path=PRD_INDEX_ARTIFACT_PATH,
                service=PrdIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="decision-index",
                artifact_kind="index",
                relative_output_path=DECISION_INDEX_ARTIFACT_PATH,
                service=DecisionIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="design-document-index",
                artifact_kind="index",
                relative_output_path=DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH,
                service=DesignDocumentIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="task-index",
                artifact_kind="index",
                relative_output_path=TASK_INDEX_ARTIFACT_PATH,
                service=TaskIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="traceability-index",
                artifact_kind="index",
                relative_output_path=TRACEABILITY_INDEX_ARTIFACT_PATH,
                service=TraceabilityIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="initiative-index",
                artifact_kind="index",
                relative_output_path=INITIATIVE_INDEX_ARTIFACT_PATH,
                service=InitiativeIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
            self._run_tracking_sync(
                target="prd-tracking",
                artifact_kind="tracker",
                relative_output_path=PRD_TRACKING_DOCUMENT_PATH,
                service=PrdTrackingSyncService(self._loader),
                record_count_attr="prd_count",
                write=write,
                output_dir=output_dir,
            ),
            self._run_tracking_sync(
                target="decision-tracking",
                artifact_kind="tracker",
                relative_output_path=DECISION_TRACKING_DOCUMENT_PATH,
                service=DecisionTrackingSyncService(self._loader),
                record_count_attr="decision_count",
                write=write,
                output_dir=output_dir,
            ),
            self._run_tracking_sync(
                target="design-tracking",
                artifact_kind="tracker",
                relative_output_path=DESIGN_TRACKING_DOCUMENT_PATH,
                service=DesignTrackingSyncService(self._loader),
                record_count_attr=None,
                write=write,
                output_dir=output_dir,
            ),
            self._run_tracking_sync(
                target="task-tracking",
                artifact_kind="tracker",
                relative_output_path=TASK_TRACKING_DOCUMENT_PATH,
                service=TaskTrackingSyncService(self._loader),
                record_count_attr="task_count",
                write=write,
                output_dir=output_dir,
            ),
            self._run_tracking_sync(
                target="initiative-tracking",
                artifact_kind="tracker",
                relative_output_path=INITIATIVE_TRACKING_DOCUMENT_PATH,
                service=InitiativeTrackingSyncService(self._loader),
                record_count_attr="initiative_count",
                write=write,
                output_dir=output_dir,
            ),
            self._run_document_sync(
                target="repository-paths",
                artifact_kind="index",
                relative_output_path=REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
                service=RepositoryPathIndexSyncService(self._loader),
                write=write,
                output_dir=output_dir,
            ),
        ]
        return AllSyncResult(
            records=tuple(records),
            wrote=(write or output_dir is not None),
            output_dir=str(output_dir.resolve()) if output_dir is not None else None,
        )

    def _run_document_sync(
        self,
        *,
        target: str,
        artifact_kind: str,
        relative_output_path: str,
        service: DocumentSyncService,
        write: bool,
        output_dir: Path | None,
    ) -> AllSyncRecord:
        document = service.build_document()
        entries = document.get("entries")
        if not isinstance(entries, list):
            raise RuntimeError(f"{target} document is missing its entries list.")
        destination = self._resolve_destination(relative_output_path, write, output_dir)
        wrote = destination is not None
        if destination is not None:
            service.write_document(document, destination)
        return AllSyncRecord(
            target=target,
            artifact_kind=artifact_kind,
            relative_output_path=relative_output_path,
            output_path=str(destination.resolve()) if destination is not None else None,
            wrote=wrote,
            record_count=len(entries),
            details={},
        )

    def _run_tracking_sync(
        self,
        *,
        target: str,
        artifact_kind: str,
        relative_output_path: str,
        service: TrackingSyncService[TrackingResultT],
        record_count_attr: str | None,
        write: bool,
        output_dir: Path | None,
    ) -> AllSyncRecord:
        result = service.build_document()
        destination = self._resolve_destination(relative_output_path, write, output_dir)
        wrote = destination is not None
        if destination is not None:
            service.write_document(result, destination)

        details = self._tracking_details(result)
        if record_count_attr is not None:
            record_count = int(getattr(result, record_count_attr))
        else:
            record_count = sum(details.values())

        return AllSyncRecord(
            target=target,
            artifact_kind=artifact_kind,
            relative_output_path=relative_output_path,
            output_path=str(destination.resolve()) if destination is not None else None,
            wrote=wrote,
            record_count=record_count,
            details=details,
        )

    def _resolve_destination(
        self,
        relative_output_path: str,
        write: bool,
        output_dir: Path | None,
    ) -> Path | None:
        if output_dir is not None:
            destination = output_dir / relative_output_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            return destination
        if not write:
            return None
        destination = self._repo_root / relative_output_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        return destination

    def _tracking_details(self, result: object) -> dict[str, int]:
        details: dict[str, int] = {}
        for attr in (
            "prd_count",
            "decision_count",
            "task_count",
            "open_count",
            "closed_count",
            "feature_design_count",
            "implementation_plan_count",
        ):
            value = getattr(result, attr, None)
            if isinstance(value, int):
                details[attr] = value
        return details
