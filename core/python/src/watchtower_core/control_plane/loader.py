"""High-level loaders for governed control-plane artifacts."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any, TypeVar, cast

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    ActorRegistry,
    AuthorityMap,
    CommandIndex,
    CoordinationIndex,
    DecisionIndex,
    DesignDocumentIndex,
    FoundationIndex,
    GovernanceSurfaceMap,
    InitiativeIndex,
    PackRuntimeManifest,
    PackSettings,
    PathPatternRegistry,
    PlanningCatalog,
    PrdIndex,
    ReferenceIndex,
    RepositoryPathIndex,
    RouteIndex,
    SchemaCatalog,
    StandardIndex,
    StatusRegistry,
    TaskIndex,
    TraceabilityIndex,
    TracePurgeRecord,
    ValidationEvidenceArtifact,
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

VALIDATOR_REGISTRY_PATH = "core/control_plane/registries/validators/validator_registry.v1.json"
AUTHORITY_MAP_PATH = "core/control_plane/registries/authority_map/authority_map.v1.json"
WORKFLOW_METADATA_REGISTRY_PATH = (
    "core/control_plane/registries/workflows/workflow_metadata_registry.v1.json"
)
PACK_RUNTIME_MANIFEST_PATH = "core/control_plane/manifests/pack_runtime_manifest.v1.json"
PACK_SETTINGS_PATH = "core/control_plane/manifests/pack_settings.json"
GOVERNANCE_SURFACE_MAP_PATH = "core/control_plane/registries/governance_surface_map.json"
PATH_PATTERN_REGISTRY_PATH = "core/control_plane/registries/path_pattern_registry.json"
STATUS_REGISTRY_PATH = "core/control_plane/registries/status_registry.json"
ACTOR_REGISTRY_PATH = "core/control_plane/registries/actor_registry.json"
REPOSITORY_PATH_INDEX_PATH = (
    "core/control_plane/indexes/repository_paths/repository_path_index.v1.json"
)
COMMAND_INDEX_PATH = "core/control_plane/indexes/commands/command_index.v1.json"
ROUTE_INDEX_PATH = "core/control_plane/indexes/routes/route_index.v1.json"
REFERENCE_INDEX_PATH = "core/control_plane/indexes/references/reference_index.v1.json"
FOUNDATION_INDEX_PATH = "core/control_plane/indexes/foundations/foundation_index.v1.json"
INITIATIVE_INDEX_PATH = "core/control_plane/indexes/initiatives/initiative_index.v1.json"
COORDINATION_INDEX_PATH = "core/control_plane/indexes/coordination/coordination_index.v1.json"
STANDARD_INDEX_PATH = "core/control_plane/indexes/standards/standard_index.v1.json"
WORKFLOW_INDEX_PATH = "core/control_plane/indexes/workflows/workflow_index.v1.json"
PRD_INDEX_PATH = "core/control_plane/indexes/prds/prd_index.v1.json"
DECISION_INDEX_PATH = "core/control_plane/indexes/decisions/decision_index.v1.json"
DESIGN_DOCUMENT_INDEX_PATH = (
    "core/control_plane/indexes/design_documents/design_document_index.v1.json"
)
TASK_INDEX_PATH = "core/control_plane/indexes/tasks/task_index.v1.json"
TRACEABILITY_INDEX_PATH = "core/control_plane/indexes/traceability/traceability_index.v1.json"
PLANNING_CATALOG_PATH = "core/control_plane/indexes/planning/planning_catalog.v1.json"
ACCEPTANCE_CONTRACTS_DIRECTORY = "core/control_plane/contracts/acceptance"
TRACE_PURGE_LEDGER_DIRECTORY = "core/control_plane/ledgers/purges"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"
TArtifact = TypeVar("TArtifact")


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
            VALIDATOR_REGISTRY_PATH,
            ValidatorRegistry.from_document,
        )

    def load_pack_runtime_manifest(self) -> PackRuntimeManifest:
        """Load the current pack-runtime manifest."""
        return self._load_typed_document(
            PACK_RUNTIME_MANIFEST_PATH,
            PackRuntimeManifest.from_document,
        )

    def load_pack_settings(self, relative_path: str = PACK_SETTINGS_PATH) -> PackSettings:
        """Load one typed pack-settings surface."""
        return self._load_typed_document(
            relative_path,
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

    def load_workflow_metadata_registry(self) -> WorkflowMetadataRegistry:
        """Load the current workflow metadata registry."""
        return self._load_typed_document(
            WORKFLOW_METADATA_REGISTRY_PATH,
            WorkflowMetadataRegistry.from_document,
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
        documents_by_path: dict[str, dict[str, Any]] = {
            relative_path: document
            for relative_path, document in self.artifact_source.iter_json_objects(
                relative_directory
            )
        }
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

        return PackContext.from_loader(self, pack_settings_path=pack_settings_path)

    def load_known_surface(self, relative_path: str) -> object:
        """Load one known governed surface as a typed artifact when available."""

        if relative_path == SCHEMA_CATALOG_ARTIFACT_PATH:
            return self.load_schema_catalog()
        if relative_path == VALIDATOR_REGISTRY_PATH:
            return self.load_validator_registry()
        if relative_path == AUTHORITY_MAP_PATH:
            return self.load_authority_map()
        if relative_path == WORKFLOW_METADATA_REGISTRY_PATH:
            return self.load_workflow_metadata_registry()
        if relative_path == PACK_RUNTIME_MANIFEST_PATH:
            return self.load_pack_runtime_manifest()
        if relative_path == PACK_SETTINGS_PATH:
            return self.load_pack_settings()
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
