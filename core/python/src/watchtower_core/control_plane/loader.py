"""High-level loaders for governed control-plane artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader_cache import (
    _invalidate_parent_directory_state as _invalidate_parent_directory_state_method,
)
from watchtower_core.control_plane.loader_cache import (
    derive as _derive_method,
)
from watchtower_core.control_plane.loader_cache import (
    load_json_object as _load_json_object_method,
)
from watchtower_core.control_plane.loader_cache import (
    load_validated_document as _load_validated_document_method,
)
from watchtower_core.control_plane.loader_cache import (
    resolve_path as _resolve_path_method,
)
from watchtower_core.control_plane.loader_cache import (
    set_validated_directory_override as _set_validated_directory_override_method,
)
from watchtower_core.control_plane.loader_cache import (
    set_validated_document_override as _set_validated_document_override_method,
)
from watchtower_core.control_plane.loader_constants import (
    _KEEP_ACTIVE_PACK_SETTINGS,
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    ACTOR_REGISTRY_PATH,
    AUTHORITY_MAP_PATH,
    COMMAND_INDEX_PATH,
    CORE_PACK_SETTINGS_PATH,
    FOUNDATION_INDEX_PATH,
    GOVERNANCE_SURFACE_MAP_PATH,
    PACK_REGISTRY_PATH,
    PACK_RUNTIME_MANIFEST_FILENAME,
    PACK_SETTINGS_PATH,
    PATH_PATTERN_REGISTRY_PATH,
    REFERENCE_INDEX_PATH,
    RENDERED_SURFACE_REGISTRY_PATH,
    REPOSITORY_PATH_INDEX_PATH,
    ROUTE_INDEX_PATH,
    STANDARD_INDEX_PATH,
    STATUS_REGISTRY_PATH,
    TRACE_PURGE_RECORD_DIRECTORY,
    TRACEABILITY_INDEX_PATH,
    VALIDATION_EVIDENCE_DIRECTORY,
    VALIDATION_SUITE_REGISTRY_PATH,
    VALIDATOR_REGISTRY_PATH,
    WORKFLOW_INDEX_PATH,
    WORKFLOW_METADATA_REGISTRY_PATH,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _activate_pack_settings as _activate_pack_settings_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _current_pack_settings_path as _current_pack_settings_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _current_surface_path as _current_surface_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _current_validation_suite_registry_path as _current_validation_suite_registry_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _current_validator_registry_path as _current_validator_registry_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _default_pack_surface_path as _default_pack_surface_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _discover_default_pack_settings_path as _discover_default_pack_settings_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _required_surface_path as _required_surface_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    _surface_name_for_active_path as _surface_name_for_active_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    default_pack_settings_path as _default_pack_settings_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    effective_pack_settings_path as _effective_pack_settings_path_method,
)
from watchtower_core.control_plane.loader_pack_settings import (
    pack_runtime_manifest_path as _pack_runtime_manifest_path_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_acceptance_contracts as _load_acceptance_contracts_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_actor_registry as _load_actor_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_artifact_family_registry as _load_artifact_family_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_artifact_index as _load_artifact_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_authority_map as _load_authority_map_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_command_index as _load_command_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_coordination_index as _load_coordination_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_declared_surface as _load_declared_surface_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_documentation_family_registry as _load_documentation_family_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_foundation_index as _load_foundation_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_governance_surface_map as _load_governance_surface_map_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_human_surface_policy_registry as _load_human_surface_policy_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_initiative_index as _load_initiative_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_known_surface as _load_known_surface_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_lifecycle_stage_registry as _load_lifecycle_stage_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_pack_context as _load_pack_context_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_pack_registry as _load_pack_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_pack_runtime_manifest as _load_pack_runtime_manifest_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_pack_settings as _load_pack_settings_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_path_pattern_registry as _load_path_pattern_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_project_surface_policy_registry as _load_project_surface_policy_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_promotion_policy_registry as _load_promotion_policy_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_reference_index as _load_reference_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_rendered_surface_registry as _load_rendered_surface_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_repository_path_index as _load_repository_path_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_retention_policy_registry as _load_retention_policy_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_review_status_registry as _load_review_status_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_route_index as _load_route_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_schema_catalog as _load_schema_catalog_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_source_type_registry as _load_source_type_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_standard_index as _load_standard_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_status_registry as _load_status_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_task_index as _load_task_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_template_catalog as _load_template_catalog_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_trace_purge_records as _load_trace_purge_records_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_traceability_index as _load_traceability_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_validation_evidence_artifacts as _load_validation_evidence_artifacts_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_validation_suite_registry as _load_validation_suite_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_validator_registry as _load_validator_registry_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_workflow_index as _load_workflow_index_method,
)
from watchtower_core.control_plane.loader_surfaces import (
    load_workflow_metadata_registry as _load_workflow_metadata_registry_method,
)
from watchtower_core.control_plane.loader_typed import (
    _load_typed_directory as _load_typed_directory_method,
)
from watchtower_core.control_plane.loader_typed import (
    _load_typed_document as _load_typed_document_method,
)
from watchtower_core.control_plane.loader_typed import (
    iter_validated_documents_under as _iter_validated_documents_under_method,
)
from watchtower_core.control_plane.loader_typed import (
    iter_validated_documents_with_paths_under as _iter_validated_documents_with_paths_under_method,
)
from watchtower_core.control_plane.loader_typed import (
    load_typed_directory as _load_typed_directory_public_method,
)
from watchtower_core.control_plane.loader_typed import (
    load_typed_document as _load_typed_document_public_method,
)
from watchtower_core.control_plane.models import PackSettings
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument
from watchtower_core.control_plane.workspace import (
    ArtifactSource,
    ArtifactStore,
    FileSystemArtifactIO,
    WorkspaceConfig,
)

__all__ = [
    "ACCEPTANCE_CONTRACTS_DIRECTORY",
    "ACTOR_REGISTRY_PATH",
    "AUTHORITY_MAP_PATH",
    "COMMAND_INDEX_PATH",
    "CORE_PACK_SETTINGS_PATH",
    "ControlPlaneLoader",
    "FOUNDATION_INDEX_PATH",
    "GOVERNANCE_SURFACE_MAP_PATH",
    "PACK_REGISTRY_PATH",
    "PACK_RUNTIME_MANIFEST_FILENAME",
    "PACK_SETTINGS_PATH",
    "PATH_PATTERN_REGISTRY_PATH",
    "REFERENCE_INDEX_PATH",
    "RENDERED_SURFACE_REGISTRY_PATH",
    "REPOSITORY_PATH_INDEX_PATH",
    "ROUTE_INDEX_PATH",
    "STANDARD_INDEX_PATH",
    "STATUS_REGISTRY_PATH",
    "TRACEABILITY_INDEX_PATH",
    "TRACE_PURGE_RECORD_DIRECTORY",
    "VALIDATION_EVIDENCE_DIRECTORY",
    "VALIDATION_SUITE_REGISTRY_PATH",
    "VALIDATOR_REGISTRY_PATH",
    "WORKFLOW_INDEX_PATH",
    "WORKFLOW_METADATA_REGISTRY_PATH",
    "_KEEP_ACTIVE_PACK_SETTINGS",
]


class ControlPlaneLoader:
    """Load and validate current governed control-plane artifacts."""

    def __init__(
        self,
        repo_root: Path | None = None,
        schema_store: SchemaStore | None = None,
        *,
        workspace_config: WorkspaceConfig | None = None,
        artifact_source: ArtifactSource | None = None,
        artifact_store: ArtifactStore | None = None,
        supplemental_schema_documents: tuple[SupplementalSchemaDocument, ...] = (),
        supplemental_schema_paths: tuple[Path | str, ...] = (),
        active_pack_settings_path: str | None = None,
    ) -> None:
        effective_workspace = workspace_config or (
            schema_store.workspace_config
            if schema_store is not None
            else WorkspaceConfig.from_repo_root(repo_root)
        )
        if (
            workspace_config is not None
            and schema_store is not None
            and schema_store.workspace_config != workspace_config
        ):
            raise ValueError(
                "ControlPlaneLoader received mismatched workspace_config and schema_store."
            )
        if schema_store is not None and (
            supplemental_schema_documents or supplemental_schema_paths
        ):
            raise ValueError(
                "ControlPlaneLoader cannot accept supplemental schema documents or paths "
                "when schema_store is provided explicitly."
            )

        default_io = FileSystemArtifactIO(effective_workspace)
        self.workspace_config = effective_workspace
        self.repo_root = effective_workspace.repo_root
        self.artifact_source = artifact_source or (
            schema_store.artifact_source if schema_store is not None else default_io
        )
        self.artifact_store = artifact_store or default_io
        self.active_pack_settings_path = active_pack_settings_path
        self._active_pack_settings: PackSettings | None = None
        self._active_surface_paths: dict[str, str] = {}
        self._active_schema_catalog_path: str | None = None
        self._active_validator_registry_path: str | None = None
        self._active_validation_suite_registry_path: str | None = None
        self._active_documentation_family_registry_path: str | None = None
        self._active_template_catalog_path: str | None = None
        self._active_artifact_family_registry_path: str | None = None
        self._active_lifecycle_stage_registry_path: str | None = None
        self._active_review_status_registry_path: str | None = None
        self._active_source_type_registry_path: str | None = None
        self._active_promotion_policy_registry_path: str | None = None
        self._active_project_surface_policy_registry_path: str | None = None
        self._active_human_surface_policy_registry_path: str | None = None
        self._active_retention_policy_registry_path: str | None = None
        self._active_artifact_index_path: str | None = None
        self.schema_store = schema_store or SchemaStore.from_workspace(
            effective_workspace,
            artifact_source=self.artifact_source,
            supplemental_schema_documents=supplemental_schema_documents,
            supplemental_schema_paths=supplemental_schema_paths,
        )
        self.supplemental_schema_ids = self.schema_store.supplemental_schema_ids
        self._validated_document_overrides: dict[str, dict[str, Any]] = {}
        self._validated_directory_overrides: dict[str, tuple[tuple[str, dict[str, Any]], ...]] = {}
        self._validated_document_cache: dict[str, dict[str, Any]] = {}
        self._validated_directory_cache: dict[str, tuple[tuple[str, dict[str, Any]], ...]] = {}
        self._typed_document_cache: dict[str, object] = {}
        self._typed_directory_cache: dict[str, object] = {}
        if active_pack_settings_path is not None:
            self._activate_pack_settings(active_pack_settings_path)

    derive = _derive_method
    _activate_pack_settings = _activate_pack_settings_method

    set_validated_document_override = _set_validated_document_override_method
    set_validated_directory_override = _set_validated_directory_override_method
    _invalidate_parent_directory_state = _invalidate_parent_directory_state_method
    load_json_object = _load_json_object_method
    resolve_path = _resolve_path_method
    load_validated_document = _load_validated_document_method

    load_schema_catalog = _load_schema_catalog_method
    load_validator_registry = _load_validator_registry_method
    load_validation_suite_registry = _load_validation_suite_registry_method
    load_pack_registry = _load_pack_registry_method
    load_pack_settings = _load_pack_settings_method
    pack_runtime_manifest_path = _pack_runtime_manifest_path_method
    load_pack_runtime_manifest = _load_pack_runtime_manifest_method
    load_governance_surface_map = _load_governance_surface_map_method
    load_path_pattern_registry = _load_path_pattern_registry_method
    load_status_registry = _load_status_registry_method
    load_actor_registry = _load_actor_registry_method
    load_authority_map = _load_authority_map_method
    load_rendered_surface_registry = _load_rendered_surface_registry_method
    load_workflow_metadata_registry = _load_workflow_metadata_registry_method
    load_documentation_family_registry = _load_documentation_family_registry_method
    load_template_catalog = _load_template_catalog_method
    load_artifact_family_registry = _load_artifact_family_registry_method
    load_lifecycle_stage_registry = _load_lifecycle_stage_registry_method
    load_review_status_registry = _load_review_status_registry_method
    load_source_type_registry = _load_source_type_registry_method
    load_promotion_policy_registry = _load_promotion_policy_registry_method
    load_project_surface_policy_registry = _load_project_surface_policy_registry_method
    load_human_surface_policy_registry = _load_human_surface_policy_registry_method
    load_retention_policy_registry = _load_retention_policy_registry_method
    load_artifact_index = _load_artifact_index_method
    load_repository_path_index = _load_repository_path_index_method
    load_command_index = _load_command_index_method
    load_route_index = _load_route_index_method
    load_reference_index = _load_reference_index_method
    load_foundation_index = _load_foundation_index_method
    load_initiative_index = _load_initiative_index_method
    load_coordination_index = _load_coordination_index_method
    load_standard_index = _load_standard_index_method
    load_workflow_index = _load_workflow_index_method
    load_task_index = _load_task_index_method
    load_traceability_index = _load_traceability_index_method
    load_acceptance_contracts = _load_acceptance_contracts_method
    load_validation_evidence_artifacts = _load_validation_evidence_artifacts_method
    load_trace_purge_records = _load_trace_purge_records_method
    load_pack_context = _load_pack_context_method
    load_declared_surface = _load_declared_surface_method
    load_known_surface = _load_known_surface_method

    _current_pack_settings_path = _current_pack_settings_path_method
    default_pack_settings_path = _default_pack_settings_path_method
    effective_pack_settings_path = _effective_pack_settings_path_method
    _current_validator_registry_path = _current_validator_registry_path_method
    _current_validation_suite_registry_path = _current_validation_suite_registry_path_method
    _current_surface_path = _current_surface_path_method
    _required_surface_path = _required_surface_path_method
    _surface_name_for_active_path = _surface_name_for_active_path_method
    _default_pack_surface_path = _default_pack_surface_path_method
    _discover_default_pack_settings_path = _discover_default_pack_settings_path_method

    iter_validated_documents_under = _iter_validated_documents_under_method
    iter_validated_documents_with_paths_under = _iter_validated_documents_with_paths_under_method
    load_typed_document = _load_typed_document_public_method
    load_typed_directory = _load_typed_directory_public_method
    _load_typed_document = _load_typed_document_method
    _load_typed_directory = _load_typed_directory_method
