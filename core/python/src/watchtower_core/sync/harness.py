"""Reusable sync-harness primitives for deterministic multi-target rebuilds."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, cast

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.control_plane.workspace import (
    FileSystemArtifactIO,
    OverlayArtifactSource,
    WorkspaceConfig,
)
from watchtower_core.telemetry import telemetry_operation

SyncServiceFactory = Callable[[ControlPlaneLoader], object]
SyncTargetMode = Literal["document", "tracking"]


@dataclass(frozen=True, slots=True)
class SyncTargetSpec:
    """One deterministic sync target included in aggregate orchestration."""

    target: str
    mode: SyncTargetMode
    artifact_kind: str
    relative_output_path: str
    service_factory: SyncServiceFactory
    record_count_attr: str | None = None
    groups: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SyncRecord:
    """One sync target executed by a sync harness."""

    target: str
    artifact_kind: str
    relative_output_path: str
    output_path: str | None
    wrote: bool
    record_count: int
    details: dict[str, int]


@dataclass(frozen=True, slots=True)
class SyncResult:
    """Aggregated output for one sync-harness run."""

    records: tuple[SyncRecord, ...]
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


class SyncHarness:
    """Reusable harness for dependency-ordered sync target execution."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> SyncHarness:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def run_specs(
        self,
        specs: tuple[SyncTargetSpec, ...],
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> SyncResult:
        with telemetry_operation(
            "sync_harness",
            "run_specs",
            attributes={
                "spec_count": len(specs),
                "write": write,
                "output_dir": str(output_dir.resolve()) if output_dir is not None else None,
            },
        ) as operation:
            runtime_loader = self._runtime_loader(output_dir)
            shared_state = self.build_shared_state(runtime_loader, specs)
            self.prepare_runtime_loader(runtime_loader, specs, shared_state)
            records = tuple(
                self._run_registered_sync(
                    loader=runtime_loader,
                    spec=spec,
                    write=write,
                    output_dir=output_dir,
                    shared_state=shared_state,
                )
                for spec in specs
            )
            result = SyncResult(
                records=records,
                wrote=(write or output_dir is not None),
                output_dir=str(output_dir.resolve()) if output_dir is not None else None,
            )
            if operation is not None:
                operation.set_result(
                    status="ok",
                    record_count=len(result.records),
                    wrote=result.wrote,
                    output_dir=result.output_dir,
                )
            return result

    def build_shared_state(
        self,
        loader: ControlPlaneLoader,
        specs: tuple[SyncTargetSpec, ...],
    ) -> object | None:
        """Build any shared state that multiple targets can reuse."""

        return None

    def prepare_runtime_loader(
        self,
        loader: ControlPlaneLoader,
        specs: tuple[SyncTargetSpec, ...],
        shared_state: object | None,
    ) -> None:
        """Prime any loader overrides needed before target execution."""

    def configure_service(
        self,
        service: object,
        spec: SyncTargetSpec,
        shared_state: object | None,
    ) -> None:
        """Apply any shared-state configuration to one target service."""

    def document_override_for_spec(
        self,
        spec: SyncTargetSpec,
        shared_state: object | None,
    ) -> dict[str, object] | None:
        """Return a prebuilt JSON document override for one target if available."""

        return None

    def _run_registered_sync(
        self,
        *,
        loader: ControlPlaneLoader,
        spec: SyncTargetSpec,
        write: bool,
        output_dir: Path | None,
        shared_state: object | None,
    ) -> SyncRecord:
        with telemetry_operation(
            "sync_target",
            spec.target,
            attributes={
                "mode": spec.mode,
                "artifact_kind": spec.artifact_kind,
                "relative_output_path": spec.relative_output_path,
                "write": write,
                "output_dir": str(output_dir.resolve()) if output_dir is not None else None,
            },
        ) as operation:
            service = spec.service_factory(loader)
            self.configure_service(service, spec, shared_state)
            if spec.mode == "document":
                record = self._run_document_sync(
                    loader=loader,
                    target=spec.target,
                    artifact_kind=spec.artifact_kind,
                    relative_output_path=spec.relative_output_path,
                    service=cast(DocumentSyncService, service),
                    write=write,
                    output_dir=output_dir,
                    document_override=self.document_override_for_spec(spec, shared_state),
                )
            else:
                record = self._run_tracking_sync(
                    target=spec.target,
                    artifact_kind=spec.artifact_kind,
                    relative_output_path=spec.relative_output_path,
                    service=cast(TrackingSyncService, service),
                    record_count_attr=spec.record_count_attr,
                    write=write,
                    output_dir=output_dir,
                )
            if operation is not None:
                operation.set_result(
                    status="ok",
                    wrote=record.wrote,
                    record_count=record.record_count,
                    output_path=record.output_path,
                )
            return record

    def _run_document_sync(
        self,
        *,
        loader: ControlPlaneLoader,
        target: str,
        artifact_kind: str,
        relative_output_path: str,
        service: DocumentSyncService,
        write: bool,
        output_dir: Path | None,
        document_override: dict[str, object] | None = None,
    ) -> SyncRecord:
        document = document_override or service.build_document()
        entries = document.get("entries")
        if not isinstance(entries, list):
            raise RuntimeError(f"{target} document is missing its entries list.")
        loader.schema_store.validate_instance(document)
        loader.set_validated_document_override(relative_output_path, document)
        destination = self._resolve_destination(relative_output_path, write, output_dir)
        wrote = destination is not None
        if destination is not None:
            service.write_document(document, destination)
        return SyncRecord(
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
    ) -> SyncRecord:
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

        return SyncRecord(
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
            "task_count",
            "open_count",
            "closed_count",
            "active_initiative_count",
            "actionable_task_count",
            "recent_closed_count",
        ):
            value = getattr(result, attr, None)
            if isinstance(value, int):
                details[attr] = value
        return details

    def _runtime_loader(self, output_dir: Path | None) -> ControlPlaneLoader:
        overlay_source = self._loader.artifact_source
        if output_dir is not None:
            overlay_workspace = WorkspaceConfig(
                repo_root=output_dir,
                control_plane_root=output_dir / "core" / "control_plane",
                python_workspace_root=output_dir / "core" / "python",
            )
            overlay_source = OverlayArtifactSource(
                primary=FileSystemArtifactIO(overlay_workspace),
                fallback=self._loader.artifact_source,
            )
        active_pack_settings_path = self._loader.active_pack_settings_path
        if active_pack_settings_path is None:
            try:
                active_pack_settings_path = self._loader.activate_pack_settings()
            except Exception:
                active_pack_settings_path = None
        return ControlPlaneLoader(
            workspace_config=self._loader.workspace_config,
            schema_store=self._loader.schema_store,
            artifact_source=overlay_source,
            artifact_store=self._loader.artifact_store,
            active_pack_settings_path=active_pack_settings_path,
        )
