"""High-level loaders for governed control-plane artifacts."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any, TypeVar, cast

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    ActorRegistry,
    ArtifactFamilyRegistry,
    ArtifactIndex,
    AuthorityMap,
    CommandIndex,
    CoordinationIndex,
    DecisionIndex,
    DesignDocumentIndex,
    DocumentationFamilyRegistry,
    FoundationIndex,
    GovernanceSurfaceMap,
    HumanSurfacePolicyRegistry,
    InitiativeIndex,
    LifecycleStageRegistry,
    PackSettings,
    PathPatternRegistry,
    PlanningCatalog,
    PrdIndex,
    ProjectSurfacePolicyRegistry,
    PromotionPolicyRegistry,
    ReferenceIndex,
    RenderedSurfaceRegistry,
    RepositoryPathIndex,
    RetentionPolicyRegistry,
    ReviewStatusRegistry,
    RouteIndex,
    SchemaCatalog,
    SourceTypeRegistry,
    StandardIndex,
    StatusRegistry,
    TaskIndex,
    TemplateCatalog,
    TraceabilityIndex,
    TracePurgeRecord,
    ValidationEvidenceArtifact,
    ValidationSuiteRegistry,
    ValidatorRegistry,
    WorkflowIndex,
    WorkflowMetadataRegistry,
)
from watchtower_core.control_plane.pack_context import PackContext
from watchtower_core.control_plane.schemas import (
    SCHEMA_CATALOG_ARTIFACT_PATH,
    SchemaStore,
    SupplementalSchemaDocument,
)
from watchtower_core.control_plane.workspace import (
    ArtifactSource,
    ArtifactStore,
    FileSystemArtifactIO,
    WorkspaceConfig,
)

VALIDATOR_REGISTRY_PATH = "core/control_plane/registries/validator_registry.json"
VALIDATION_SUITE_REGISTRY_PATH = "core/control_plane/registries/validation_suite_registry.json"
AUTHORITY_MAP_PATH = "core/control_plane/registries/authority_map.json"
WORKFLOW_METADATA_REGISTRY_PATH = (
    "core/control_plane/registries/workflow_metadata_registry.json"
)
DOCUMENTATION_FAMILY_REGISTRY_PATH = "plan/.wt/registries/documentation_family_registry.json"
TEMPLATE_CATALOG_PATH = "plan/.wt/registries/template_catalog.json"
ARTIFACT_FAMILY_REGISTRY_PATH = "plan/.wt/registries/artifact_family_registry.json"
LIFECYCLE_STAGE_REGISTRY_PATH = "plan/.wt/registries/lifecycle_stage_registry.json"
REVIEW_STATUS_REGISTRY_PATH = "plan/.wt/registries/review_status_registry.json"
SOURCE_TYPE_REGISTRY_PATH = "plan/.wt/registries/source_type_registry.json"
PROMOTION_POLICY_REGISTRY_PATH = "plan/.wt/registries/promotion_policy_registry.json"
PROJECT_SURFACE_POLICY_REGISTRY_PATH = "plan/.wt/registries/project_surface_policy_registry.json"
HUMAN_SURFACE_POLICY_REGISTRY_PATH = "plan/.wt/registries/human_surface_policy_registry.json"
RETENTION_POLICY_REGISTRY_PATH = "plan/.wt/registries/retention_policy_registry.json"
ARTIFACT_INDEX_PATH = "plan/.wt/indexes/artifact_index.json"
PACK_SETTINGS_PATH = "core/control_plane/manifests/pack_settings.json"
GOVERNANCE_SURFACE_MAP_PATH = "core/control_plane/registries/governance_surface_map.json"
PATH_PATTERN_REGISTRY_PATH = "core/control_plane/registries/path_pattern_registry.json"
STATUS_REGISTRY_PATH = "core/control_plane/registries/status_registry.json"
ACTOR_REGISTRY_PATH = "core/control_plane/registries/actor_registry.json"
RENDERED_SURFACE_REGISTRY_PATH = "core/control_plane/registries/rendered_surface_registry.json"
REPOSITORY_PATH_INDEX_PATH = (
    "core/control_plane/indexes/repository_paths/repository_path_index.json"
)
COMMAND_INDEX_PATH = "core/control_plane/indexes/commands/command_index.json"
ROUTE_INDEX_PATH = "core/control_plane/indexes/routes/route_index.json"
REFERENCE_INDEX_PATH = "core/control_plane/indexes/references/reference_index.json"
FOUNDATION_INDEX_PATH = "core/control_plane/indexes/foundations/foundation_index.json"
INITIATIVE_INDEX_PATH = "core/control_plane/indexes/initiatives/initiative_index.json"
COORDINATION_INDEX_PATH = "core/control_plane/indexes/coordination/coordination_index.json"
STANDARD_INDEX_PATH = "core/control_plane/indexes/standards/standard_index.json"
WORKFLOW_INDEX_PATH = "core/control_plane/indexes/workflows/workflow_index.json"
PRD_INDEX_PATH = "core/control_plane/indexes/prds/prd_index.json"
DECISION_INDEX_PATH = "core/control_plane/indexes/decisions/decision_index.json"
DESIGN_DOCUMENT_INDEX_PATH = (
    "core/control_plane/indexes/design_documents/design_document_index.json"
)
TASK_INDEX_PATH = "core/control_plane/indexes/tasks/task_index.json"
TRACEABILITY_INDEX_PATH = "core/control_plane/indexes/traceability/traceability_index.json"
PLANNING_CATALOG_PATH = "core/control_plane/indexes/planning/planning_catalog.json"
ACCEPTANCE_CONTRACTS_DIRECTORY = "core/control_plane/contracts/acceptance"
TRACE_PURGE_LEDGER_DIRECTORY = "core/control_plane/ledgers/purges"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"
TArtifact = TypeVar("TArtifact")
_KEEP_ACTIVE_PACK_SETTINGS = object()


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

    def derive(
        self,
        *,
        artifact_source: ArtifactSource | None = None,
        artifact_store: ArtifactStore | None = None,
        active_pack_settings_path: str | None | object = _KEEP_ACTIVE_PACK_SETTINGS,
    ) -> ControlPlaneLoader:
        """Return a sibling loader that preserves current-run validated overrides."""

        effective_pack_settings_path = (
            self.active_pack_settings_path
            if active_pack_settings_path is _KEEP_ACTIVE_PACK_SETTINGS
            else active_pack_settings_path
        )
        derived = ControlPlaneLoader(
            workspace_config=self.workspace_config,
            schema_store=self.schema_store,
            artifact_source=artifact_source or self.artifact_source,
            artifact_store=artifact_store or self.artifact_store,
            active_pack_settings_path=effective_pack_settings_path,
        )
        derived._validated_document_overrides = dict(self._validated_document_overrides)
        derived._validated_directory_overrides = {
            relative_directory: tuple(documents)
            for relative_directory, documents in self._validated_directory_overrides.items()
        }
        return derived

    def _activate_pack_settings(self, pack_settings_path: str) -> None:
        """Configure pack-aware validation surfaces for one active pack settings path."""

        pack_settings = self.load_pack_settings(pack_settings_path)
        self.active_pack_settings_path = pack_settings_path
        self._active_pack_settings = pack_settings

        try:
            schema_catalog_path = pack_settings.get("schema_catalog").path
        except KeyError as exc:
            raise ValueError(
                "Active pack settings must declare a schema_catalog surface."
            ) from exc
        self._active_schema_catalog_path = schema_catalog_path
        if schema_catalog_path != SCHEMA_CATALOG_ARTIFACT_PATH:
            self.schema_store = self.schema_store.with_additional_catalog_paths(
                (schema_catalog_path,)
            )
            self.supplemental_schema_ids = self.schema_store.supplemental_schema_ids

        try:
            validator_registry_path = pack_settings.get("validator_registry").path
        except KeyError as exc:
            raise ValueError(
                "Active pack settings must declare a validator_registry surface."
            ) from exc
        self._active_validator_registry_path = validator_registry_path
        suite_registry_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "validation_suite_registry"
            ),
            None,
        )
        self._active_validation_suite_registry_path = (
            suite_registry_declaration.path if suite_registry_declaration is not None else None
        )
        documentation_family_registry_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "documentation_family_registry"
            ),
            None,
        )
        self._active_documentation_family_registry_path = (
            documentation_family_registry_declaration.path
            if documentation_family_registry_declaration is not None
            else None
        )
        template_catalog_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "template_catalog"
            ),
            None,
        )
        self._active_template_catalog_path = (
            template_catalog_declaration.path if template_catalog_declaration is not None else None
        )
        artifact_family_registry_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "artifact_family_registry"
            ),
            None,
        )
        self._active_artifact_family_registry_path = (
            artifact_family_registry_declaration.path
            if artifact_family_registry_declaration is not None
            else None
        )
        lifecycle_stage_registry_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "lifecycle_stage_registry"
            ),
            None,
        )
        self._active_lifecycle_stage_registry_path = (
            lifecycle_stage_registry_declaration.path
            if lifecycle_stage_registry_declaration is not None
            else None
        )
        review_status_registry_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "review_status_registry"
            ),
            None,
        )
        self._active_review_status_registry_path = (
            review_status_registry_declaration.path
            if review_status_registry_declaration is not None
            else None
        )
        source_type_registry_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "source_type_registry"
            ),
            None,
        )
        self._active_source_type_registry_path = (
            source_type_registry_declaration.path
            if source_type_registry_declaration is not None
            else None
        )
        promotion_policy_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "promotion_policy_registry"
            ),
            None,
        )
        self._active_promotion_policy_registry_path = (
            promotion_policy_declaration.path
            if promotion_policy_declaration is not None
            else None
        )
        project_surface_policy_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "project_surface_policy_registry"
            ),
            None,
        )
        self._active_project_surface_policy_registry_path = (
            project_surface_policy_declaration.path
            if project_surface_policy_declaration is not None
            else None
        )
        human_surface_policy_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "human_surface_policy_registry"
            ),
            None,
        )
        self._active_human_surface_policy_registry_path = (
            human_surface_policy_declaration.path
            if human_surface_policy_declaration is not None
            else None
        )
        retention_policy_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "retention_policy_registry"
            ),
            None,
        )
        self._active_retention_policy_registry_path = (
            retention_policy_declaration.path
            if retention_policy_declaration is not None
            else None
        )
        artifact_index_declaration = next(
            (
                declaration
                for declaration in pack_settings.surfaces
                if declaration.surface_name == "artifact_index"
            ),
            None,
        )
        self._active_artifact_index_path = (
            artifact_index_declaration.path if artifact_index_declaration is not None else None
        )

    def set_validated_document_override(
        self,
        relative_path: str,
        document: dict[str, Any],
    ) -> None:
        """Publish one current-run validated document for later loader reuse."""

        self._validated_document_overrides[relative_path] = document
        self._validated_document_cache[relative_path] = document
        self._typed_document_cache.pop(relative_path, None)
        self._invalidate_parent_directory_state(relative_path)

    def set_validated_directory_override(
        self,
        relative_directory: str,
        documents: tuple[tuple[str, dict[str, Any]], ...],
    ) -> None:
        """Publish one current-run validated governed directory for later reuse."""

        previous_override = self._validated_directory_overrides.get(relative_directory, ())
        previous_paths = {relative_path for relative_path, _ in previous_override}
        next_paths = {relative_path for relative_path, _ in documents}

        self._validated_directory_overrides[relative_directory] = documents
        self._validated_directory_cache[relative_directory] = documents
        self._typed_directory_cache.pop(relative_directory, None)
        for relative_path, document in documents:
            self._validated_document_overrides[relative_path] = document
            self._validated_document_cache[relative_path] = document
            self._typed_document_cache.pop(relative_path, None)

        for stale_relative_path in previous_paths.difference(next_paths):
            self._validated_document_overrides.pop(stale_relative_path, None)
            self._validated_document_cache.pop(stale_relative_path, None)
            self._typed_document_cache.pop(stale_relative_path, None)

    def _invalidate_parent_directory_state(self, relative_path: str) -> None:
        """Drop stale directory-level override and cache state after one document update."""

        stale_directories = tuple(
            relative_directory
            for relative_directory in {
                *self._validated_directory_overrides,
                *self._validated_directory_cache,
                *self._typed_directory_cache,
            }
            if relative_path.startswith(f"{relative_directory.rstrip('/')}/")
        )
        for relative_directory in stale_directories:
            self._validated_directory_overrides.pop(relative_directory, None)
            self._validated_directory_cache.pop(relative_directory, None)
            self._typed_directory_cache.pop(relative_directory, None)

    def load_json_object(self, relative_path: str) -> dict[str, Any]:
        """Load a repository-relative JSON object."""
        override = self._validated_document_overrides.get(relative_path)
        if override is not None:
            return override
        try:
            return self.artifact_source.load_json_object(relative_path)
        except ArtifactLoadError:
            raise
        except FileNotFoundError as exc:
            raise ArtifactLoadError(f"Could not load governed artifact at {relative_path}") from exc

    def resolve_path(self, relative_path: str) -> Path:
        """Resolve one repository-relative path through the current workspace mapping."""
        return self.workspace_config.resolve_path(relative_path)

    def load_validated_document(self, relative_path: str) -> dict[str, Any]:
        """Load and validate a governed artifact that declares its own $schema."""
        override = self._validated_document_overrides.get(relative_path)
        if override is not None:
            return override
        cached = self._validated_document_cache.get(relative_path)
        if cached is not None:
            return cached
        document = self.load_json_object(relative_path)
        self.schema_store.validate_instance(document)
        self._validated_document_cache[relative_path] = document
        return document

    def load_schema_catalog(self) -> SchemaCatalog:
        """Return the current typed schema catalog."""
        return self.schema_store.catalog

    def load_validator_registry(self) -> ValidatorRegistry:
        """Load the current validator registry."""
        return self._load_typed_document(
            self._current_validator_registry_path(),
            ValidatorRegistry.from_document,
        )

    def load_validation_suite_registry(self) -> ValidationSuiteRegistry:
        """Load the current validation-suite registry."""

        return self._load_typed_document(
            self._current_validation_suite_registry_path(),
            ValidationSuiteRegistry.from_document,
        )

    def load_pack_settings(self, relative_path: str = PACK_SETTINGS_PATH) -> PackSettings:
        """Load one typed pack-settings surface."""
        effective_path = self._current_pack_settings_path(relative_path)
        return self._load_typed_document(
            effective_path,
            PackSettings.from_document,
        )

    def load_governance_surface_map(
        self,
        relative_path: str = GOVERNANCE_SURFACE_MAP_PATH,
    ) -> GovernanceSurfaceMap:
        """Load one typed governance-surface map."""

        return self._load_typed_document(
            relative_path,
            GovernanceSurfaceMap.from_document,
        )

    def load_path_pattern_registry(
        self,
        relative_path: str = PATH_PATTERN_REGISTRY_PATH,
    ) -> PathPatternRegistry:
        """Load one typed path-pattern registry."""

        return self._load_typed_document(
            relative_path,
            PathPatternRegistry.from_document,
        )

    def load_status_registry(self, relative_path: str = STATUS_REGISTRY_PATH) -> StatusRegistry:
        """Load one typed status registry."""

        return self._load_typed_document(
            relative_path,
            StatusRegistry.from_document,
        )

    def load_actor_registry(self, relative_path: str = ACTOR_REGISTRY_PATH) -> ActorRegistry:
        """Load one typed actor registry."""

        return self._load_typed_document(
            relative_path,
            ActorRegistry.from_document,
        )

    def load_authority_map(self) -> AuthorityMap:
        """Load the current authority-map registry."""
        return self._load_typed_document(
            AUTHORITY_MAP_PATH,
            AuthorityMap.from_document,
        )

    def load_rendered_surface_registry(self) -> RenderedSurfaceRegistry:
        """Load the current rendered-surface registry."""
        return self._load_typed_document(
            RENDERED_SURFACE_REGISTRY_PATH,
            RenderedSurfaceRegistry.from_document,
        )

    def load_workflow_metadata_registry(self) -> WorkflowMetadataRegistry:
        """Load the current workflow metadata registry."""
        return self._load_typed_document(
            WORKFLOW_METADATA_REGISTRY_PATH,
            WorkflowMetadataRegistry.from_document,
        )

    def load_documentation_family_registry(
        self,
        relative_path: str = DOCUMENTATION_FAMILY_REGISTRY_PATH,
    ) -> DocumentationFamilyRegistry:
        """Load the current documentation-family registry."""

        effective_path = self._current_documentation_family_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            DocumentationFamilyRegistry.from_document,
        )

    def load_template_catalog(
        self,
        relative_path: str = TEMPLATE_CATALOG_PATH,
    ) -> TemplateCatalog:
        """Load the current template catalog."""

        effective_path = self._current_template_catalog_path(relative_path)
        return self._load_typed_document(
            effective_path,
            TemplateCatalog.from_document,
        )

    def load_artifact_family_registry(
        self,
        relative_path: str = ARTIFACT_FAMILY_REGISTRY_PATH,
    ) -> ArtifactFamilyRegistry:
        """Load the current artifact-family registry."""

        effective_path = self._current_artifact_family_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            ArtifactFamilyRegistry.from_document,
        )

    def load_lifecycle_stage_registry(
        self,
        relative_path: str = LIFECYCLE_STAGE_REGISTRY_PATH,
    ) -> LifecycleStageRegistry:
        """Load the current lifecycle-stage registry."""

        effective_path = self._current_lifecycle_stage_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            LifecycleStageRegistry.from_document,
        )

    def load_review_status_registry(
        self,
        relative_path: str = REVIEW_STATUS_REGISTRY_PATH,
    ) -> ReviewStatusRegistry:
        """Load the current review-status registry."""

        effective_path = self._current_review_status_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            ReviewStatusRegistry.from_document,
        )

    def load_source_type_registry(
        self,
        relative_path: str = SOURCE_TYPE_REGISTRY_PATH,
    ) -> SourceTypeRegistry:
        """Load the current source-type registry."""

        effective_path = self._current_source_type_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            SourceTypeRegistry.from_document,
        )

    def load_promotion_policy_registry(
        self,
        relative_path: str = PROMOTION_POLICY_REGISTRY_PATH,
    ) -> PromotionPolicyRegistry:
        """Load the current promotion-policy registry."""

        effective_path = self._current_promotion_policy_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            PromotionPolicyRegistry.from_document,
        )

    def load_project_surface_policy_registry(
        self,
        relative_path: str = PROJECT_SURFACE_POLICY_REGISTRY_PATH,
    ) -> ProjectSurfacePolicyRegistry:
        """Load the current project-surface policy registry."""

        effective_path = self._current_project_surface_policy_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            ProjectSurfacePolicyRegistry.from_document,
        )

    def load_human_surface_policy_registry(
        self,
        relative_path: str = HUMAN_SURFACE_POLICY_REGISTRY_PATH,
    ) -> HumanSurfacePolicyRegistry:
        """Load the current human-surface policy registry."""

        effective_path = self._current_human_surface_policy_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            HumanSurfacePolicyRegistry.from_document,
        )

    def load_retention_policy_registry(
        self,
        relative_path: str = RETENTION_POLICY_REGISTRY_PATH,
    ) -> RetentionPolicyRegistry:
        """Load the current retention-policy registry."""

        effective_path = self._current_retention_policy_registry_path(relative_path)
        return self._load_typed_document(
            effective_path,
            RetentionPolicyRegistry.from_document,
        )

    def load_artifact_index(
        self,
        relative_path: str = ARTIFACT_INDEX_PATH,
    ) -> ArtifactIndex:
        """Load the current pack artifact index."""

        effective_path = self._current_artifact_index_path(relative_path)
        return self._load_typed_document(
            effective_path,
            ArtifactIndex.from_document,
        )

    def load_repository_path_index(self) -> RepositoryPathIndex:
        """Load the current repository path index."""
        return self._load_typed_document(
            REPOSITORY_PATH_INDEX_PATH,
            RepositoryPathIndex.from_document,
        )

    def load_command_index(self) -> CommandIndex:
        """Load the current command index."""
        return self._load_typed_document(
            COMMAND_INDEX_PATH,
            CommandIndex.from_document,
        )

    def load_route_index(self) -> RouteIndex:
        """Load the current route index."""
        return self._load_typed_document(
            ROUTE_INDEX_PATH,
            RouteIndex.from_document,
        )

    def load_reference_index(self) -> ReferenceIndex:
        """Load the current reference index."""
        return self._load_typed_document(
            REFERENCE_INDEX_PATH,
            ReferenceIndex.from_document,
        )

    def load_foundation_index(self) -> FoundationIndex:
        """Load the current foundation index."""
        return self._load_typed_document(
            FOUNDATION_INDEX_PATH,
            FoundationIndex.from_document,
        )

    def load_initiative_index(self) -> InitiativeIndex:
        """Load the current initiative index."""
        return self._load_typed_document(
            INITIATIVE_INDEX_PATH,
            InitiativeIndex.from_document,
        )

    def load_coordination_index(self) -> CoordinationIndex:
        """Load the current coordination index."""
        return self._load_typed_document(
            COORDINATION_INDEX_PATH,
            CoordinationIndex.from_document,
        )

    def load_standard_index(self) -> StandardIndex:
        """Load the current standard index."""
        return self._load_typed_document(
            STANDARD_INDEX_PATH,
            StandardIndex.from_document,
        )

    def load_workflow_index(self) -> WorkflowIndex:
        """Load the current workflow index."""
        return self._load_typed_document(
            WORKFLOW_INDEX_PATH,
            WorkflowIndex.from_document,
        )

    def load_prd_index(self) -> PrdIndex:
        """Load the current PRD index."""
        return self._load_typed_document(PRD_INDEX_PATH, PrdIndex.from_document)

    def load_decision_index(self) -> DecisionIndex:
        """Load the current decision index."""
        return self._load_typed_document(
            DECISION_INDEX_PATH,
            DecisionIndex.from_document,
        )

    def load_design_document_index(self) -> DesignDocumentIndex:
        """Load the current design-document index."""
        return self._load_typed_document(
            DESIGN_DOCUMENT_INDEX_PATH,
            DesignDocumentIndex.from_document,
        )

    def load_task_index(self) -> TaskIndex:
        """Load the current task index."""
        return self._load_typed_document(TASK_INDEX_PATH, TaskIndex.from_document)

    def load_traceability_index(self) -> TraceabilityIndex:
        """Load the current traceability index."""
        return self._load_typed_document(
            TRACEABILITY_INDEX_PATH,
            TraceabilityIndex.from_document,
        )

    def load_planning_catalog(self) -> PlanningCatalog:
        """Load the current canonical planning catalog."""
        return self._load_typed_document(
            PLANNING_CATALOG_PATH,
            PlanningCatalog.from_document,
        )

    def iter_validated_documents_under(self, relative_directory: str) -> tuple[dict[str, Any], ...]:
        """Load and validate every JSON document directly under one governed directory."""
        return tuple(
            document
            for _, document in self.iter_validated_documents_with_paths_under(
                relative_directory
            )
        )

    def iter_validated_documents_with_paths_under(
        self,
        relative_directory: str,
    ) -> tuple[tuple[str, dict[str, Any]], ...]:
        """Load and validate every JSON document directly under one governed directory."""
        override = self._validated_directory_overrides.get(relative_directory)
        if override is not None:
            return override
        cached = self._validated_directory_cache.get(relative_directory)
        if cached is not None:
            return cached
        documents_by_path: dict[str, dict[str, Any]] = dict(
            self.artifact_source.iter_json_objects(relative_directory)
        )
        for relative_path, document in self._validated_document_overrides.items():
            if _is_direct_child_of_directory(relative_directory, relative_path):
                documents_by_path[relative_path] = document

        documents: list[tuple[str, dict[str, Any]]] = []
        for relative_path in sorted(documents_by_path):
            document = documents_by_path[relative_path]
            self.schema_store.validate_instance(document)
            documents.append((relative_path, document))
            self._validated_document_cache[relative_path] = document
        cached_documents = tuple(documents)
        self._validated_directory_cache[relative_directory] = cached_documents
        return cached_documents

    def load_acceptance_contracts(self) -> tuple[AcceptanceContract, ...]:
        """Load all governed acceptance-contract artifacts."""
        return self._load_typed_directory(
            ACCEPTANCE_CONTRACTS_DIRECTORY,
            lambda relative_path, document: AcceptanceContract.from_document(
                document,
                doc_path=relative_path,
            ),
        )

    def load_validation_evidence_artifacts(self) -> tuple[ValidationEvidenceArtifact, ...]:
        """Load all governed validation-evidence artifacts."""
        return self._load_typed_directory(
            VALIDATION_EVIDENCE_DIRECTORY,
            lambda relative_path, document: ValidationEvidenceArtifact.from_document(
                document,
                doc_path=relative_path,
            ),
        )

    def load_trace_purge_records(self) -> tuple[TracePurgeRecord, ...]:
        """Load all governed trace-purge ledger artifacts."""
        return self._load_typed_directory(
            TRACE_PURGE_LEDGER_DIRECTORY,
            lambda relative_path, document: TracePurgeRecord.from_document(
                document,
                doc_path=relative_path,
            ),
        )

    def load_pack_context(self, pack_settings_path: str = PACK_SETTINGS_PATH) -> PackContext:
        """Load one PackContext from pack settings and its declared governed surfaces."""

        return PackContext.from_loader(
            self,
            pack_settings_path=self._current_pack_settings_path(pack_settings_path),
        )

    def load_declared_surface(
        self,
        *,
        surface_name: str,
        relative_path: str,
    ) -> object:
        """Load one pack-declared surface as a typed artifact when the surface is known."""

        if surface_name == "schema_catalog":
            return self._load_typed_document(
                relative_path,
                lambda document: SchemaCatalog.from_document(document, self.workspace_config),
            )
        if surface_name == "validator_registry":
            return self._load_typed_document(relative_path, ValidatorRegistry.from_document)
        if surface_name == "validation_suite_registry":
            return self._load_typed_document(
                relative_path,
                ValidationSuiteRegistry.from_document,
            )
        if surface_name == "authority_map":
            return self._load_typed_document(relative_path, AuthorityMap.from_document)
        if surface_name == "rendered_surface_registry":
            return self._load_typed_document(
                relative_path,
                RenderedSurfaceRegistry.from_document,
            )
        if surface_name == "workflow_metadata_registry":
            return self._load_typed_document(relative_path, WorkflowMetadataRegistry.from_document)
        if surface_name == "documentation_family_registry":
            return self._load_typed_document(
                relative_path,
                DocumentationFamilyRegistry.from_document,
            )
        if surface_name == "template_catalog":
            return self._load_typed_document(relative_path, TemplateCatalog.from_document)
        if surface_name == "artifact_family_registry":
            return self._load_typed_document(
                relative_path,
                ArtifactFamilyRegistry.from_document,
            )
        if surface_name == "lifecycle_stage_registry":
            return self._load_typed_document(
                relative_path,
                LifecycleStageRegistry.from_document,
            )
        if surface_name == "review_status_registry":
            return self._load_typed_document(
                relative_path,
                ReviewStatusRegistry.from_document,
            )
        if surface_name == "source_type_registry":
            return self._load_typed_document(
                relative_path,
                SourceTypeRegistry.from_document,
            )
        if surface_name == "promotion_policy_registry":
            return self._load_typed_document(
                relative_path,
                PromotionPolicyRegistry.from_document,
            )
        if surface_name == "project_surface_policy_registry":
            return self._load_typed_document(
                relative_path,
                ProjectSurfacePolicyRegistry.from_document,
            )
        if surface_name == "human_surface_policy_registry":
            return self._load_typed_document(
                relative_path,
                HumanSurfacePolicyRegistry.from_document,
            )
        if surface_name == "retention_policy_registry":
            return self._load_typed_document(
                relative_path,
                RetentionPolicyRegistry.from_document,
            )
        if surface_name == "artifact_index":
            return self._load_typed_document(relative_path, ArtifactIndex.from_document)
        if surface_name == "pack_settings":
            return self._load_typed_document(relative_path, PackSettings.from_document)
        if surface_name == "governance_surface_map":
            return self._load_typed_document(relative_path, GovernanceSurfaceMap.from_document)
        if surface_name == "path_pattern_registry":
            return self._load_typed_document(relative_path, PathPatternRegistry.from_document)
        if surface_name == "status_registry":
            return self._load_typed_document(relative_path, StatusRegistry.from_document)
        if surface_name == "actor_registry":
            return self._load_typed_document(relative_path, ActorRegistry.from_document)
        if surface_name == "repository_path_index":
            return self._load_typed_document(relative_path, RepositoryPathIndex.from_document)
        if surface_name == "command_index":
            return self._load_typed_document(relative_path, CommandIndex.from_document)
        if surface_name == "route_index":
            return self._load_typed_document(relative_path, RouteIndex.from_document)
        if surface_name == "reference_index":
            return self._load_typed_document(relative_path, ReferenceIndex.from_document)
        if surface_name == "foundation_index":
            return self._load_typed_document(relative_path, FoundationIndex.from_document)
        if surface_name == "initiative_index":
            return self._load_typed_document(relative_path, InitiativeIndex.from_document)
        if surface_name == "coordination_index":
            return self._load_typed_document(relative_path, CoordinationIndex.from_document)
        if surface_name == "standard_index":
            return self._load_typed_document(relative_path, StandardIndex.from_document)
        if surface_name == "workflow_index":
            return self._load_typed_document(relative_path, WorkflowIndex.from_document)
        if surface_name == "prd_index":
            return self._load_typed_document(relative_path, PrdIndex.from_document)
        if surface_name == "decision_index":
            return self._load_typed_document(relative_path, DecisionIndex.from_document)
        if surface_name == "design_document_index":
            return self._load_typed_document(relative_path, DesignDocumentIndex.from_document)
        if surface_name == "task_index":
            return self._load_typed_document(relative_path, TaskIndex.from_document)
        if surface_name == "traceability_index":
            return self._load_typed_document(relative_path, TraceabilityIndex.from_document)
        if surface_name == "planning_catalog":
            return self._load_typed_document(relative_path, PlanningCatalog.from_document)
        return self.load_known_surface(relative_path)

    def load_known_surface(self, relative_path: str) -> object:
        """Load one known governed surface as a typed artifact when available."""

        if relative_path == SCHEMA_CATALOG_ARTIFACT_PATH:
            return self.load_schema_catalog()
        if relative_path == VALIDATOR_REGISTRY_PATH:
            return self.load_validator_registry()
        if relative_path == VALIDATION_SUITE_REGISTRY_PATH:
            return self.load_validation_suite_registry()
        if relative_path == AUTHORITY_MAP_PATH:
            return self.load_authority_map()
        if relative_path == RENDERED_SURFACE_REGISTRY_PATH:
            return self.load_rendered_surface_registry()
        if relative_path == WORKFLOW_METADATA_REGISTRY_PATH:
            return self.load_workflow_metadata_registry()
        if relative_path == DOCUMENTATION_FAMILY_REGISTRY_PATH:
            return self.load_documentation_family_registry()
        if relative_path == TEMPLATE_CATALOG_PATH:
            return self.load_template_catalog()
        if relative_path == ARTIFACT_FAMILY_REGISTRY_PATH:
            return self.load_artifact_family_registry()
        if relative_path == LIFECYCLE_STAGE_REGISTRY_PATH:
            return self.load_lifecycle_stage_registry()
        if relative_path == REVIEW_STATUS_REGISTRY_PATH:
            return self.load_review_status_registry()
        if relative_path == SOURCE_TYPE_REGISTRY_PATH:
            return self.load_source_type_registry()
        if relative_path == PROMOTION_POLICY_REGISTRY_PATH:
            return self.load_promotion_policy_registry()
        if relative_path == PROJECT_SURFACE_POLICY_REGISTRY_PATH:
            return self.load_project_surface_policy_registry()
        if relative_path == HUMAN_SURFACE_POLICY_REGISTRY_PATH:
            return self.load_human_surface_policy_registry()
        if relative_path == RETENTION_POLICY_REGISTRY_PATH:
            return self.load_retention_policy_registry()
        if relative_path == ARTIFACT_INDEX_PATH:
            return self.load_artifact_index()
        if relative_path == PACK_SETTINGS_PATH:
            return self.load_pack_settings()
        if (
            self.active_pack_settings_path is not None
            and relative_path == self.active_pack_settings_path
        ):
            return self.load_pack_settings(relative_path)
        if (
            self._active_validator_registry_path is not None
            and relative_path == self._active_validator_registry_path
        ):
            return self.load_validator_registry()
        if (
            self._active_validation_suite_registry_path is not None
            and relative_path == self._active_validation_suite_registry_path
        ):
            return self.load_validation_suite_registry()
        if (
            self._active_documentation_family_registry_path is not None
            and relative_path == self._active_documentation_family_registry_path
        ):
            return self.load_documentation_family_registry(relative_path)
        if (
            self._active_template_catalog_path is not None
            and relative_path == self._active_template_catalog_path
        ):
            return self.load_template_catalog(relative_path)
        if (
            self._active_artifact_family_registry_path is not None
            and relative_path == self._active_artifact_family_registry_path
        ):
            return self.load_artifact_family_registry(relative_path)
        if (
            self._active_lifecycle_stage_registry_path is not None
            and relative_path == self._active_lifecycle_stage_registry_path
        ):
            return self.load_lifecycle_stage_registry(relative_path)
        if (
            self._active_review_status_registry_path is not None
            and relative_path == self._active_review_status_registry_path
        ):
            return self.load_review_status_registry(relative_path)
        if (
            self._active_source_type_registry_path is not None
            and relative_path == self._active_source_type_registry_path
        ):
            return self.load_source_type_registry(relative_path)
        if (
            self._active_promotion_policy_registry_path is not None
            and relative_path == self._active_promotion_policy_registry_path
        ):
            return self.load_promotion_policy_registry(relative_path)
        if (
            self._active_project_surface_policy_registry_path is not None
            and relative_path == self._active_project_surface_policy_registry_path
        ):
            return self.load_project_surface_policy_registry(relative_path)
        if (
            self._active_human_surface_policy_registry_path is not None
            and relative_path == self._active_human_surface_policy_registry_path
        ):
            return self.load_human_surface_policy_registry(relative_path)
        if (
            self._active_retention_policy_registry_path is not None
            and relative_path == self._active_retention_policy_registry_path
        ):
            return self.load_retention_policy_registry(relative_path)
        if (
            self._active_artifact_index_path is not None
            and relative_path == self._active_artifact_index_path
        ):
            return self.load_artifact_index(relative_path)
        if relative_path == GOVERNANCE_SURFACE_MAP_PATH:
            return self.load_governance_surface_map()
        if relative_path == PATH_PATTERN_REGISTRY_PATH:
            return self.load_path_pattern_registry()
        if relative_path == STATUS_REGISTRY_PATH:
            return self.load_status_registry()
        if relative_path == ACTOR_REGISTRY_PATH:
            return self.load_actor_registry()
        if relative_path == REPOSITORY_PATH_INDEX_PATH:
            return self.load_repository_path_index()
        if relative_path == COMMAND_INDEX_PATH:
            return self.load_command_index()
        if relative_path == ROUTE_INDEX_PATH:
            return self.load_route_index()
        if relative_path == REFERENCE_INDEX_PATH:
            return self.load_reference_index()
        if relative_path == FOUNDATION_INDEX_PATH:
            return self.load_foundation_index()
        if relative_path == INITIATIVE_INDEX_PATH:
            return self.load_initiative_index()
        if relative_path == COORDINATION_INDEX_PATH:
            return self.load_coordination_index()
        if relative_path == STANDARD_INDEX_PATH:
            return self.load_standard_index()
        if relative_path == WORKFLOW_INDEX_PATH:
            return self.load_workflow_index()
        if relative_path == PRD_INDEX_PATH:
            return self.load_prd_index()
        if relative_path == DECISION_INDEX_PATH:
            return self.load_decision_index()
        if relative_path == DESIGN_DOCUMENT_INDEX_PATH:
            return self.load_design_document_index()
        if relative_path == TASK_INDEX_PATH:
            return self.load_task_index()
        if relative_path == TRACEABILITY_INDEX_PATH:
            return self.load_traceability_index()
        if relative_path == PLANNING_CATALOG_PATH:
            return self.load_planning_catalog()
        return self.load_validated_document(relative_path)

    def _current_pack_settings_path(self, relative_path: str) -> str:
        """Resolve the effective pack-settings path for this loader instance."""

        if relative_path == PACK_SETTINGS_PATH and self.active_pack_settings_path is not None:
            return self.active_pack_settings_path
        return relative_path

    def _current_validator_registry_path(self) -> str:
        """Return the validator registry path active for this loader instance."""

        if self._active_validator_registry_path is not None:
            return self._active_validator_registry_path
        return VALIDATOR_REGISTRY_PATH

    def _current_validation_suite_registry_path(self) -> str:
        """Return the validation-suite registry path active for this loader instance."""

        if self._active_validation_suite_registry_path is not None:
            return self._active_validation_suite_registry_path
        return VALIDATION_SUITE_REGISTRY_PATH

    def _current_documentation_family_registry_path(self, relative_path: str) -> str:
        """Return the documentation-family registry path active for this loader instance."""

        if (
            relative_path == DOCUMENTATION_FAMILY_REGISTRY_PATH
            and self._active_documentation_family_registry_path is not None
        ):
            return self._active_documentation_family_registry_path
        return relative_path

    def _current_template_catalog_path(self, relative_path: str) -> str:
        """Return the template-catalog path active for this loader instance."""

        if (
            relative_path == TEMPLATE_CATALOG_PATH
            and self._active_template_catalog_path is not None
        ):
            return self._active_template_catalog_path
        return relative_path

    def _current_artifact_family_registry_path(self, relative_path: str) -> str:
        """Return the artifact-family registry path active for this loader instance."""

        if (
            relative_path == ARTIFACT_FAMILY_REGISTRY_PATH
            and self._active_artifact_family_registry_path is not None
        ):
            return self._active_artifact_family_registry_path
        return relative_path

    def _current_lifecycle_stage_registry_path(self, relative_path: str) -> str:
        """Return the lifecycle-stage registry path active for this loader instance."""

        if (
            relative_path == LIFECYCLE_STAGE_REGISTRY_PATH
            and self._active_lifecycle_stage_registry_path is not None
        ):
            return self._active_lifecycle_stage_registry_path
        return relative_path

    def _current_review_status_registry_path(self, relative_path: str) -> str:
        """Return the review-status registry path active for this loader instance."""

        if (
            relative_path == REVIEW_STATUS_REGISTRY_PATH
            and self._active_review_status_registry_path is not None
        ):
            return self._active_review_status_registry_path
        return relative_path

    def _current_source_type_registry_path(self, relative_path: str) -> str:
        """Return the source-type registry path active for this loader instance."""

        if (
            relative_path == SOURCE_TYPE_REGISTRY_PATH
            and self._active_source_type_registry_path is not None
        ):
            return self._active_source_type_registry_path
        return relative_path

    def _current_promotion_policy_registry_path(self, relative_path: str) -> str:
        """Return the promotion-policy registry path active for this loader instance."""

        if (
            relative_path == PROMOTION_POLICY_REGISTRY_PATH
            and self._active_promotion_policy_registry_path is not None
        ):
            return self._active_promotion_policy_registry_path
        return relative_path

    def _current_project_surface_policy_registry_path(self, relative_path: str) -> str:
        """Return the project-surface policy registry path active for this loader instance."""

        if (
            relative_path == PROJECT_SURFACE_POLICY_REGISTRY_PATH
            and self._active_project_surface_policy_registry_path is not None
        ):
            return self._active_project_surface_policy_registry_path
        return relative_path

    def _current_human_surface_policy_registry_path(self, relative_path: str) -> str:
        """Return the human-surface policy registry path active for this loader instance."""

        if (
            relative_path == HUMAN_SURFACE_POLICY_REGISTRY_PATH
            and self._active_human_surface_policy_registry_path is not None
        ):
            return self._active_human_surface_policy_registry_path
        return relative_path

    def _current_retention_policy_registry_path(self, relative_path: str) -> str:
        """Return the retention-policy registry path active for this loader instance."""

        if (
            relative_path == RETENTION_POLICY_REGISTRY_PATH
            and self._active_retention_policy_registry_path is not None
        ):
            return self._active_retention_policy_registry_path
        return relative_path

    def _current_artifact_index_path(self, relative_path: str) -> str:
        """Return the artifact-index path active for this loader instance."""

        if relative_path == ARTIFACT_INDEX_PATH and self._active_artifact_index_path is not None:
            return self._active_artifact_index_path
        return relative_path

    def load_typed_document(
        self,
        relative_path: str,
        builder: Callable[[dict[str, Any]], TArtifact],
    ) -> TArtifact:
        """Load one typed governed document through the loader cache."""

        return self._load_typed_document(relative_path, builder)

    def load_typed_directory(
        self,
        relative_directory: str,
        builder: Callable[[str, dict[str, Any]], TArtifact],
    ) -> tuple[TArtifact, ...]:
        """Load one typed governed directory through the loader cache."""

        return self._load_typed_directory(relative_directory, builder)

    def _load_typed_document(
        self,
        relative_path: str,
        builder: Callable[[dict[str, Any]], TArtifact],
    ) -> TArtifact:
        """Materialize one typed artifact once per loader-backed command run."""

        cached = self._typed_document_cache.get(relative_path)
        if cached is not None:
            return cast(TArtifact, cached)
        artifact = builder(self.load_validated_document(relative_path))
        self._typed_document_cache[relative_path] = artifact
        return artifact

    def _load_typed_directory(
        self,
        relative_directory: str,
        builder: Callable[[str, dict[str, Any]], TArtifact],
    ) -> tuple[TArtifact, ...]:
        """Materialize one typed directory-backed artifact tuple once per loader run."""

        cached = self._typed_directory_cache.get(relative_directory)
        if cached is not None:
            return cast(tuple[TArtifact, ...], cached)
        artifacts = tuple(
            builder(relative_path, document)
            for relative_path, document in self.iter_validated_documents_with_paths_under(
                relative_directory
            )
        )
        self._typed_directory_cache[relative_directory] = artifacts
        return artifacts


def _is_direct_child_of_directory(relative_directory: str, relative_path: str) -> bool:
    """Return whether one logical path is a direct child of the governed directory."""

    directory = PurePosixPath(relative_directory.rstrip("/"))
    candidate = PurePosixPath(relative_path)
    return candidate.parent == directory
