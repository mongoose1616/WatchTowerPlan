"""Local schema resolution and validation for governed control-plane artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from watchtower_core.control_plane.errors import ArtifactLoadError, SchemaResolutionError
from watchtower_core.control_plane.models import SchemaCatalog, SchemaCatalogRecord
from watchtower_core.control_plane.paths import control_plane_path, discover_repo_root

SCHEMA_CATALOG_SCHEMA_PATH = "core/control_plane/schemas/artifacts/schema_catalog.v1.schema.json"
SCHEMA_CATALOG_ARTIFACT_PATH = "core/control_plane/registries/schema_catalog/schema_catalog.v1.json"


def _load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except FileNotFoundError as exc:
        raise ArtifactLoadError(f"Could not load governed artifact at {path}") from exc

    if not isinstance(loaded, dict):
        raise ArtifactLoadError(f"Expected JSON object at {path}, found {type(loaded).__name__}")
    return loaded


class SchemaStore:
    """Resolve and validate published schemas through the schema catalog."""

    def __init__(
        self,
        *,
        repo_root: Path,
        catalog: SchemaCatalog,
        schema_documents: dict[str, dict[str, Any]],
        registry: Registry,
    ) -> None:
        self.repo_root = repo_root
        self.catalog = catalog
        self._schema_documents = schema_documents
        self._registry = registry

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> SchemaStore:
        """Bootstrap the schema store from the local schema catalog."""
        resolved_root = discover_repo_root(repo_root)
        catalog_schema_path = control_plane_path(resolved_root, SCHEMA_CATALOG_SCHEMA_PATH)
        catalog_artifact_path = control_plane_path(resolved_root, SCHEMA_CATALOG_ARTIFACT_PATH)

        catalog_schema = _load_json(catalog_schema_path)
        catalog_document = _load_json(catalog_artifact_path)
        Draft202012Validator(catalog_schema).validate(catalog_document)

        catalog = SchemaCatalog.from_document(catalog_document, resolved_root)
        schema_documents: dict[str, dict[str, Any]] = {}
        registry = Registry()

        for record in catalog.records:
            if not record.canonical_path.exists():
                raise SchemaResolutionError(
                    f"Cataloged schema path does not exist: {record.canonical_relative_path}"
                )

            schema_document = _load_json(record.canonical_path)
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

        return cls(
            repo_root=resolved_root,
            catalog=catalog,
            schema_documents=schema_documents,
            registry=registry,
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
        """Return the loaded JSON schema document for a published schema identifier."""
        try:
            return self._schema_documents[schema_id]
        except KeyError as exc:
            raise SchemaResolutionError(f"Unknown schema ID: {schema_id}") from exc

    def build_validator(self, schema_id: str) -> Draft202012Validator:
        """Build a validator for a published schema identifier."""
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
