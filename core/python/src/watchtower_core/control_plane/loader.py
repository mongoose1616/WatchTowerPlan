"""High-level loaders for governed control-plane artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    CommandIndex,
    DecisionIndex,
    DesignDocumentIndex,
    PrdIndex,
    RepositoryPathIndex,
    SchemaCatalog,
    TaskIndex,
    TraceabilityIndex,
    ValidationEvidenceArtifact,
    ValidatorRegistry,
)
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.control_plane.schemas import SchemaStore

VALIDATOR_REGISTRY_PATH = "core/control_plane/registries/validators/validator_registry.v1.json"
REPOSITORY_PATH_INDEX_PATH = (
    "core/control_plane/indexes/repository_paths/repository_path_index.v1.json"
)
COMMAND_INDEX_PATH = "core/control_plane/indexes/commands/command_index.v1.json"
PRD_INDEX_PATH = "core/control_plane/indexes/prds/prd_index.v1.json"
DECISION_INDEX_PATH = "core/control_plane/indexes/decisions/decision_index.v1.json"
DESIGN_DOCUMENT_INDEX_PATH = (
    "core/control_plane/indexes/design_documents/design_document_index.v1.json"
)
TASK_INDEX_PATH = "core/control_plane/indexes/tasks/task_index.v1.json"
TRACEABILITY_INDEX_PATH = "core/control_plane/indexes/traceability/traceability_index.v1.json"
ACCEPTANCE_CONTRACTS_DIRECTORY = "core/control_plane/contracts/acceptance"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"


class ControlPlaneLoader:
    """Load and validate current governed control-plane artifacts."""

    def __init__(
        self,
        repo_root: Path | None = None,
        schema_store: SchemaStore | None = None,
    ) -> None:
        self.repo_root = discover_repo_root(repo_root)
        self.schema_store = schema_store or SchemaStore.from_repo_root(self.repo_root)

    def load_json_object(self, relative_path: str) -> dict[str, Any]:
        """Load a repository-relative JSON object."""
        path = self.repo_root / relative_path
        try:
            with path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
        except FileNotFoundError as exc:
            raise ArtifactLoadError(f"Could not load governed artifact at {relative_path}") from exc

        if not isinstance(loaded, dict):
            raise ArtifactLoadError(
                f"Expected JSON object at {relative_path}, found {type(loaded).__name__}"
            )
        return loaded

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

    def load_repository_path_index(self) -> RepositoryPathIndex:
        """Load the current repository path index."""
        return RepositoryPathIndex.from_document(
            self.load_validated_document(REPOSITORY_PATH_INDEX_PATH)
        )

    def load_command_index(self) -> CommandIndex:
        """Load the current command index."""
        return CommandIndex.from_document(self.load_validated_document(COMMAND_INDEX_PATH))

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
        directory = self.repo_root / relative_directory
        documents: list[tuple[str, dict[str, Any]]] = []
        for path in sorted(directory.glob("*.json")):
            relative_path = path.relative_to(self.repo_root).as_posix()
            documents.append((relative_path, self.load_validated_document(relative_path)))
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
