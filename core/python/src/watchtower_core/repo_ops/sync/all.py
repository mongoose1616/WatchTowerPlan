"""Coordinated rebuild helpers for all local derived sync surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.control_plane.workspace import (
    FileSystemArtifactIO,
    OverlayArtifactSource,
    WorkspaceConfig,
)
from watchtower_core.repo_ops.reference_resolution import (
    reference_urls_by_path_from_index_document,
)
from watchtower_core.repo_ops.sync.reference_index import ReferenceIndexSyncService
from watchtower_core.repo_ops.sync.registry import SYNC_TARGET_SPECS, SyncTargetSpec


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


class TrackingSyncService(Protocol):
    """Protocol for sync services that build Markdown tracking outputs."""

    def build_document(self) -> object:
        """Build one tracker result object."""

    def write_document(
        self,
        result: object,
        destination: Path | None = None,
    ) -> Path:
        """Write one tracker result object."""


class ReferenceAwareSyncService(Protocol):
    """Protocol for sync services that can reuse reference-resolution data."""

    def set_reference_urls_by_path(
        self,
        reference_urls_by_path: dict[str, tuple[str, ...]],
    ) -> None:
        """Inject a precomputed reference-resolution map."""


REFERENCE_RESOLUTION_TARGETS = frozenset(
    {"reference-index", "foundation-index", "standard-index", "workflow-index"}
)


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
        runtime_loader = self._runtime_loader(output_dir)
        specs = SYNC_TARGET_SPECS
        (
            shared_reference_index_document,
            shared_reference_urls_by_path,
        ) = self._build_shared_reference_resolution(runtime_loader, specs)
        records = [
            self._run_registered_sync(
                loader=runtime_loader,
                spec=spec,
                write=write,
                output_dir=output_dir,
                shared_reference_index_document=shared_reference_index_document,
                shared_reference_urls_by_path=shared_reference_urls_by_path,
            )
            for spec in specs
        ]
        return AllSyncResult(
            records=tuple(records),
            wrote=(write or output_dir is not None),
            output_dir=str(output_dir.resolve()) if output_dir is not None else None,
        )

    def _build_shared_reference_resolution(
        self,
        loader: ControlPlaneLoader,
        specs: tuple[SyncTargetSpec, ...],
    ) -> tuple[dict[str, object] | None, dict[str, tuple[str, ...]] | None]:
        """Build one shared reference-resolution snapshot when the sync slice needs it."""

        if not any(spec.target in REFERENCE_RESOLUTION_TARGETS for spec in specs):
            return None, None

        shared_reference_index_document = ReferenceIndexSyncService(loader).build_document()
        return (
            shared_reference_index_document,
            reference_urls_by_path_from_index_document(shared_reference_index_document),
        )

    def _run_registered_sync(
        self,
        *,
        loader: ControlPlaneLoader,
        spec: SyncTargetSpec,
        write: bool,
        output_dir: Path | None,
        shared_reference_index_document: dict[str, object] | None,
        shared_reference_urls_by_path: dict[str, tuple[str, ...]] | None,
    ) -> AllSyncRecord:
        service = spec.service_factory(loader)
        if shared_reference_urls_by_path is not None and hasattr(
            service, "set_reference_urls_by_path"
        ):
            cast(ReferenceAwareSyncService, service).set_reference_urls_by_path(
                shared_reference_urls_by_path
            )
        if spec.mode == "document":
            return self._run_document_sync(
                target=spec.target,
                artifact_kind=spec.artifact_kind,
                relative_output_path=spec.relative_output_path,
                service=cast(DocumentSyncService, service),
                write=write,
                output_dir=output_dir,
                document_override=(
                    shared_reference_index_document
                    if spec.target == "reference-index"
                    else None
                ),
            )
        return self._run_tracking_sync(
            target=spec.target,
            artifact_kind=spec.artifact_kind,
            relative_output_path=spec.relative_output_path,
            service=cast(TrackingSyncService, service),
            record_count_attr=spec.record_count_attr,
            write=write,
            output_dir=output_dir,
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
        document_override: dict[str, object] | None = None,
    ) -> AllSyncRecord:
        document = document_override or service.build_document()
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
        service: TrackingSyncService,
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
            "coordination_entry_count",
            "prd_count",
            "decision_count",
            "task_count",
            "open_count",
            "closed_count",
            "feature_design_count",
            "implementation_plan_count",
            "active_initiative_count",
            "actionable_task_count",
            "recent_closed_count",
        ):
            value = getattr(result, attr, None)
            if isinstance(value, int):
                details[attr] = value
        return details

    def _runtime_loader(self, output_dir: Path | None) -> ControlPlaneLoader:
        if output_dir is None:
            return self._loader

        overlay_workspace = WorkspaceConfig(
            repo_root=output_dir,
            control_plane_root=output_dir / "core" / "control_plane",
            python_workspace_root=output_dir / "core" / "python",
        )
        overlay_source = OverlayArtifactSource(
            primary=FileSystemArtifactIO(overlay_workspace),
            fallback=self._loader.artifact_source,
        )
        return ControlPlaneLoader(
            workspace_config=self._loader.workspace_config,
            schema_store=self._loader.schema_store,
            artifact_source=overlay_source,
            artifact_store=self._loader.artifact_store,
        )
