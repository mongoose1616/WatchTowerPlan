"""Coordinated rebuild helpers for all local derived sync surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from watchtower_core.control_plane.loader import (
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    DECISION_INDEX_PATH,
    DESIGN_DOCUMENT_INDEX_PATH,
    PRD_INDEX_PATH,
    VALIDATION_EVIDENCE_DIRECTORY,
    ControlPlaneLoader,
)
from watchtower_core.repo_ops.reference_resolution import (
    reference_urls_by_path_from_index_document,
)
from watchtower_core.repo_ops.sync.reference_index import ReferenceIndexSyncService
from watchtower_core.repo_ops.sync.registry import SYNC_TARGET_SPECS, SyncTargetSpec
from watchtower_core.sync.harness import (
    ReferenceAwareSyncService,
    SyncHarness,
    SyncRecord as AllSyncRecord,
    SyncResult as AllSyncResult,
)


REFERENCE_RESOLUTION_TARGETS = frozenset(
    {"reference-index", "foundation-index", "standard-index", "workflow-index"}
)
COORDINATION_REUSE_TARGETS = frozenset(
    {
        "task-index",
        "traceability-index",
        "initiative-index",
        "planning-catalog",
        "coordination-index",
        "task-tracking",
        "initiative-tracking",
        "coordination-tracking",
    }
)
COORDINATION_STABLE_SOURCE_DOCUMENT_PATHS = (
    PRD_INDEX_PATH,
    DECISION_INDEX_PATH,
    DESIGN_DOCUMENT_INDEX_PATH,
)
COORDINATION_STABLE_SOURCE_DIRECTORIES = (
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    VALIDATION_EVIDENCE_DIRECTORY,
)


@dataclass(frozen=True, slots=True)
class _AllSyncSharedState:
    shared_reference_index_document: dict[str, object] | None
    shared_reference_urls_by_path: dict[str, tuple[str, ...]] | None


class AllSyncService(SyncHarness):
    """Run all local deterministic sync operations in dependency order."""

    def run(
        self,
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> AllSyncResult:
        return cast(
            AllSyncResult,
            self.run_specs(
                SYNC_TARGET_SPECS,
                write=write,
                output_dir=output_dir,
            ),
        )

    def build_shared_state(
        self,
        loader: ControlPlaneLoader,
        specs: tuple[SyncTargetSpec, ...],
    ) -> _AllSyncSharedState | None:
        if not any(spec.target in REFERENCE_RESOLUTION_TARGETS for spec in specs):
            return None

        shared_reference_index_document = ReferenceIndexSyncService(loader).build_document()
        return _AllSyncSharedState(
            shared_reference_index_document=shared_reference_index_document,
            shared_reference_urls_by_path=reference_urls_by_path_from_index_document(
                shared_reference_index_document
            ),
        )

    def prepare_runtime_loader(
        self,
        loader: ControlPlaneLoader,
        specs: tuple[SyncTargetSpec, ...],
        shared_state: object | None,
    ) -> None:
        if not any(spec.target in COORDINATION_REUSE_TARGETS for spec in specs):
            return

        for relative_path in COORDINATION_STABLE_SOURCE_DOCUMENT_PATHS:
            loader.set_validated_document_override(
                relative_path,
                loader.load_validated_document(relative_path),
            )
        for relative_directory in COORDINATION_STABLE_SOURCE_DIRECTORIES:
            loader.set_validated_directory_override(
                relative_directory,
                loader.iter_validated_documents_with_paths_under(relative_directory),
            )

    def configure_service(
        self,
        service: object,
        spec: SyncTargetSpec,
        shared_state: object | None,
    ) -> None:
        if shared_state is None or not hasattr(service, "set_reference_urls_by_path"):
            return
        reference_state = cast(_AllSyncSharedState, shared_state)
        if reference_state.shared_reference_urls_by_path is None:
            return
        cast(ReferenceAwareSyncService, service).set_reference_urls_by_path(
            reference_state.shared_reference_urls_by_path
        )

    def document_override_for_spec(
        self,
        spec: SyncTargetSpec,
        shared_state: object | None,
    ) -> dict[str, object] | None:
        if spec.target != "reference-index" or shared_state is None:
            return None
        reference_state = cast(_AllSyncSharedState, shared_state)
        return reference_state.shared_reference_index_document
