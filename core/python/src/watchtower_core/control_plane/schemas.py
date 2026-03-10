"""Local schema resolution and validation for governed control-plane artifacts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.models import SchemaCatalog, SchemaCatalogRecord
from watchtower_core.control_plane.workspace import (
    ArtifactSource,
    FileSystemArtifactIO,
    WorkspaceConfig,
)

SCHEMA_CATALOG_SCHEMA_PATH = "core/control_plane/schemas/artifacts/schema_catalog.v1.schema.json"
SCHEMA_CATALOG_ARTIFACT_PATH = "core/control_plane/registries/schema_catalog/schema_catalog.v1.json"


@dataclass(frozen=True, slots=True)
class SupplementalSchemaDocument:
    """In-memory schema document added to validation without mutating the catalog."""

    source_label: str
    document: dict[str, Any]

    @classmethod
    def from_document(
        cls,
        document: Mapping[str, Any],
        *,
        source_label: str,
    ) -> SupplementalSchemaDocument:
        return cls(source_label=source_label, document=dict(document))

    def schema_id(self) -> str:
        """Return the published schema identifier declared by the document."""
        schema_id = self.document.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise SchemaResolutionError(
                f"Supplemental schema {self.source_label} is missing a non-empty $id."
            )
        return schema_id


class SchemaStore:
    """Resolve and validate published schemas through the schema catalog."""

    def __init__(
        self,
        *,
        workspace_config: WorkspaceConfig,
        artifact_source: ArtifactSource,
        catalog: SchemaCatalog,
        schema_documents: dict[str, dict[str, Any]],
        registry: Registry,
        supplemental_schema_ids: tuple[str, ...] = (),
    ) -> None:
        self.workspace_config = workspace_config
        self.repo_root = workspace_config.repo_root
        self.artifact_source = artifact_source
        self.catalog = catalog
        self._schema_documents = schema_documents
        self._registry = registry
        self.supplemental_schema_ids = supplemental_schema_ids

    @classmethod
    def from_repo_root(
        cls,
        repo_root: Path | None = None,
        *,
        supplemental_schema_documents: Sequence[SupplementalSchemaDocument] = (),
    ) -> SchemaStore:
        """Bootstrap the schema store from the local schema catalog."""
        return cls.from_workspace(
            WorkspaceConfig.from_repo_root(repo_root),
            supplemental_schema_documents=supplemental_schema_documents,
        )

    @classmethod
    def from_workspace(
        cls,
        workspace_config: WorkspaceConfig,
        *,
        artifact_source: ArtifactSource | None = None,
        supplemental_schema_documents: Sequence[SupplementalSchemaDocument] = (),
    ) -> SchemaStore:
        """Bootstrap the schema store from one injected workspace mapping."""
        source = artifact_source or FileSystemArtifactIO(workspace_config)
        catalog_schema = source.load_json_object(SCHEMA_CATALOG_SCHEMA_PATH)
        catalog_document = source.load_json_object(SCHEMA_CATALOG_ARTIFACT_PATH)
        Draft202012Validator(catalog_schema).validate(catalog_document)

        catalog = SchemaCatalog.from_document(catalog_document, workspace_config)
        schema_documents: dict[str, dict[str, Any]] = {}
        registry = Registry()
        supplemental_schema_ids: list[str] = []

        for record in catalog.records:
            schema_document = source.load_json_object(record.canonical_relative_path)
            schema_id = schema_document.get("$id")
            if schema_id != record.schema_id:
                raise SchemaResolutionError(
                    "Cataloged schema ID does not match the schema file: "
                    f"{record.schema_id} != {schema_id}"
                )

            Draft202012Validator.check_schema(schema_document)
            schema_documents[record.schema_id] = schema_document
            registry = registry.with_resource(
                record.schema_id,
                Resource.from_contents(schema_document),
            )

        for supplemental_schema in supplemental_schema_documents:
            schema_id = supplemental_schema.schema_id()
            if schema_id in schema_documents:
                raise SchemaResolutionError(
                    "Supplemental schema ID duplicates an existing schema: "
                    f"{schema_id} from {supplemental_schema.source_label}"
                )

            Draft202012Validator.check_schema(supplemental_schema.document)
            schema_documents[schema_id] = dict(supplemental_schema.document)
            supplemental_schema_ids.append(schema_id)
            registry = registry.with_resource(
                schema_id,
                Resource.from_contents(supplemental_schema.document),
            )

        return cls(
            workspace_config=workspace_config,
            artifact_source=source,
            catalog=catalog,
            schema_documents=schema_documents,
            registry=registry,
            supplemental_schema_ids=tuple(supplemental_schema_ids),
        )

    def get_record(self, schema_id: str) -> SchemaCatalogRecord:
        """Return the schema-catalog record for a published schema identifier."""
        try:
            return self.catalog.get(schema_id)
        except KeyError as exc:
            raise SchemaResolutionError(f"Unknown schema ID: {schema_id}") from exc

    def resolve_path(self, schema_id: str) -> Path:
        """Return the local canonical path for a published schema identifier."""
        return self.get_record(schema_id).canonical_path

    def load_schema(self, schema_id: str) -> dict[str, Any]:
        """Return the loaded JSON schema document for a cataloged or supplemental schema."""
        try:
            return self._schema_documents[schema_id]
        except KeyError as exc:
            raise SchemaResolutionError(f"Unknown schema ID: {schema_id}") from exc

    def build_validator(self, schema_id: str) -> Draft202012Validator:
        """Build a validator for a cataloged or supplemental schema identifier."""
        return Draft202012Validator(self.load_schema(schema_id), registry=self._registry)

    def validate_instance(
        self,
        instance: dict[str, Any],
        *,
        schema_id: str | None = None,
    ) -> None:
        """Validate an instance against a published schema identifier or its own $schema."""
        effective_schema_id = schema_id or instance.get("$schema")
        if not isinstance(effective_schema_id, str) or not effective_schema_id:
            raise SchemaResolutionError("No published schema ID was provided for validation.")

        validator = self.build_validator(effective_schema_id)
        validator.validate(instance)
