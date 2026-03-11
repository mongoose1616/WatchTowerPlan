"""High-level loaders for governed control-plane artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    CommandIndex,
    CoordinationIndex,
    DecisionIndex,
    DesignDocumentIndex,
    FoundationIndex,
    InitiativeIndex,
    PlanningCatalog,
    PrdIndex,
    ReferenceIndex,
    RepositoryPathIndex,
    RouteIndex,
    SchemaCatalog,
    StandardIndex,
    TaskIndex,
    TraceabilityIndex,
    ValidationEvidenceArtifact,
    ValidatorRegistry,
    WorkflowIndex,
    WorkflowMetadataRegistry,
)
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument
from watchtower_core.control_plane.workspace import (
    ArtifactSource,
    ArtifactStore,
    FileSystemArtifactIO,
    WorkspaceConfig,
)

VALIDATOR_REGISTRY_PATH = "core/control_plane/registries/validators/validator_registry.v1.json"
WORKFLOW_METADATA_REGISTRY_PATH = (
    "core/control_plane/registries/workflows/workflow_metadata_registry.v1.json"
)
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
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"


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

    def load_json_object(self, relative_path: str) -> dict[str, Any]:
        """Load a repository-relative JSON object."""
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
        document = self.load_json_object(relative_path)
        self.schema_store.validate_instance(document)
        return document

    def load_schema_catalog(self) -> SchemaCatalog:
        """Return the current typed schema catalog."""
        return self.schema_store.catalog

    def load_validator_registry(self) -> ValidatorRegistry:
        """Load the current validator registry."""
        return ValidatorRegistry.from_document(
            self.load_validated_document(VALIDATOR_REGISTRY_PATH)
        )

    def load_workflow_metadata_registry(self) -> WorkflowMetadataRegistry:
        """Load the current workflow metadata registry."""
        return WorkflowMetadataRegistry.from_document(
            self.load_validated_document(WORKFLOW_METADATA_REGISTRY_PATH)
        )

    def load_repository_path_index(self) -> RepositoryPathIndex:
        """Load the current repository path index."""
        return RepositoryPathIndex.from_document(
            self.load_validated_document(REPOSITORY_PATH_INDEX_PATH)
        )

    def load_command_index(self) -> CommandIndex:
        """Load the current command index."""
        return CommandIndex.from_document(self.load_validated_document(COMMAND_INDEX_PATH))

    def load_route_index(self) -> RouteIndex:
        """Load the current route index."""
        return RouteIndex.from_document(self.load_validated_document(ROUTE_INDEX_PATH))

    def load_reference_index(self) -> ReferenceIndex:
        """Load the current reference index."""
        return ReferenceIndex.from_document(self.load_validated_document(REFERENCE_INDEX_PATH))

    def load_foundation_index(self) -> FoundationIndex:
        """Load the current foundation index."""
        return FoundationIndex.from_document(self.load_validated_document(FOUNDATION_INDEX_PATH))

    def load_initiative_index(self) -> InitiativeIndex:
        """Load the current initiative index."""
        return InitiativeIndex.from_document(self.load_validated_document(INITIATIVE_INDEX_PATH))

    def load_coordination_index(self) -> CoordinationIndex:
        """Load the current coordination index."""
        return CoordinationIndex.from_document(
            self.load_validated_document(COORDINATION_INDEX_PATH)
        )

    def load_standard_index(self) -> StandardIndex:
        """Load the current standard index."""
        return StandardIndex.from_document(self.load_validated_document(STANDARD_INDEX_PATH))

    def load_workflow_index(self) -> WorkflowIndex:
        """Load the current workflow index."""
        return WorkflowIndex.from_document(self.load_validated_document(WORKFLOW_INDEX_PATH))

    def load_prd_index(self) -> PrdIndex:
        """Load the current PRD index."""
        return PrdIndex.from_document(self.load_validated_document(PRD_INDEX_PATH))

    def load_decision_index(self) -> DecisionIndex:
        """Load the current decision index."""
        return DecisionIndex.from_document(self.load_validated_document(DECISION_INDEX_PATH))

    def load_design_document_index(self) -> DesignDocumentIndex:
        """Load the current design-document index."""
        return DesignDocumentIndex.from_document(
            self.load_validated_document(DESIGN_DOCUMENT_INDEX_PATH)
        )

    def load_task_index(self) -> TaskIndex:
        """Load the current task index."""
        return TaskIndex.from_document(self.load_validated_document(TASK_INDEX_PATH))

    def load_traceability_index(self) -> TraceabilityIndex:
        """Load the current traceability index."""
        return TraceabilityIndex.from_document(
            self.load_validated_document(TRACEABILITY_INDEX_PATH)
        )

    def load_planning_catalog(self) -> PlanningCatalog:
        """Load the current canonical planning catalog."""
        return PlanningCatalog.from_document(
            self.load_validated_document(PLANNING_CATALOG_PATH)
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
        documents: list[tuple[str, dict[str, Any]]] = []
        for relative_path, document in self.artifact_source.iter_json_objects(relative_directory):
            self.schema_store.validate_instance(document)
            documents.append((relative_path, document))
        return tuple(documents)

    def load_acceptance_contracts(self) -> tuple[AcceptanceContract, ...]:
        """Load all governed acceptance-contract artifacts."""
        return tuple(
            AcceptanceContract.from_document(document, doc_path=relative_path)
            for relative_path, document in self.iter_validated_documents_with_paths_under(
                ACCEPTANCE_CONTRACTS_DIRECTORY
            )
        )

    def load_validation_evidence_artifacts(self) -> tuple[ValidationEvidenceArtifact, ...]:
        """Load all governed validation-evidence artifacts."""
        return tuple(
            ValidationEvidenceArtifact.from_document(document, doc_path=relative_path)
            for relative_path, document in self.iter_validated_documents_with_paths_under(
                VALIDATION_EVIDENCE_DIRECTORY
            )
        )
