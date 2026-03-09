"""High-level loaders for governed control-plane artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.models import (
    CommandIndex,
    RepositoryPathIndex,
    SchemaCatalog,
    TraceabilityIndex,
    ValidatorRegistry,
)
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.control_plane.schemas import SchemaStore


VALIDATOR_REGISTRY_PATH = "core/control_plane/registries/validators/validator_registry.v1.json"
REPOSITORY_PATH_INDEX_PATH = "core/control_plane/indexes/repository_paths/repository_path_index.v1.json"
COMMAND_INDEX_PATH = "core/control_plane/indexes/commands/command_index.v1.json"
TRACEABILITY_INDEX_PATH = "core/control_plane/indexes/traceability/traceability_index.v1.json"


class ControlPlaneLoader:
    """Load and validate current governed control-plane artifacts."""

    def __init__(self, repo_root: Path | None = None, schema_store: SchemaStore | None = None) -> None:
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
        return ValidatorRegistry.from_document(self.load_validated_document(VALIDATOR_REGISTRY_PATH))

    def load_repository_path_index(self) -> RepositoryPathIndex:
        """Load the current repository path index."""
        return RepositoryPathIndex.from_document(
            self.load_validated_document(REPOSITORY_PATH_INDEX_PATH)
        )

    def load_command_index(self) -> CommandIndex:
        """Load the current command index."""
        return CommandIndex.from_document(self.load_validated_document(COMMAND_INDEX_PATH))

    def load_traceability_index(self) -> TraceabilityIndex:
        """Load the current traceability index."""
        return TraceabilityIndex.from_document(
            self.load_validated_document(TRACEABILITY_INDEX_PATH)
        )
