from __future__ import annotations

from pathlib import Path

import pytest
from jsonschema import ValidationError

from tests.unit.schema_store_test_support import (
    REPO_ROOT,
    copy_validation_repo_subset,
    materialize_additional_schema_catalog,
    write_json,
)
from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument


def test_schema_store_accepts_supplemental_schema_documents() -> None:
    schema_id = "urn:watchtower:schema:external:test-note:v1"
    store = SchemaStore.from_repo_root(
        REPO_ROOT,
        supplemental_schema_documents=(
            SupplementalSchemaDocument.from_document(
                {
                    "$id": schema_id,
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {
                        "$schema": {"type": "string"},
                        "kind": {"const": "external_note"},
                    },
                    "required": ["kind"],
                    "additionalProperties": False,
                },
                source_label="external:test-note",
            ),
        ),
    )

    store.validate_instance({"kind": "external_note"}, schema_id=schema_id)

    with pytest.raises(ValidationError):
        store.validate_instance({"kind": "wrong"}, schema_id=schema_id)

    assert store.supplemental_schema_ids == (schema_id,)


def test_schema_store_merges_additional_schema_catalog_paths(tmp_path: Path) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    catalog = materialize_additional_schema_catalog(repo_root / "packs" / "plan")
    base_store = SchemaStore.from_repo_root(repo_root)
    store = base_store.with_additional_catalog_paths((catalog["catalog_path"],))

    assert (
        store.get_record(catalog["schema_id"]).canonical_relative_path
        == (catalog["schema_relative_path"])
    )
    store.validate_instance(
        {
            "$schema": catalog["schema_id"],
            "kind": "schema_store_note",
        },
        schema_id=catalog["schema_id"],
    )


def test_schema_store_rejects_duplicate_supplemental_schema_ids() -> None:
    with pytest.raises(SchemaResolutionError, match="duplicates an existing schema"):
        SchemaStore.from_repo_root(
            REPO_ROOT,
            supplemental_schema_documents=(
                SupplementalSchemaDocument.from_document(
                    {
                        "$id": (
                            "urn:watchtower:schema:interfaces:documentation:"
                            "reference-front-matter:v1"
                        ),
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "type": "object",
                    },
                    source_label="external:duplicate",
                ),
            ),
        )


def test_schema_store_accepts_supplemental_schema_file_paths(tmp_path: Path) -> None:
    schema_path = tmp_path / "schemas" / "external_note.schema.json"
    schema_id = "urn:watchtower:schema:external:test-note-from-file:v1"
    write_json(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "External Test Note",
            "description": "Test schema loaded from one explicit file path.",
            "type": "object",
            "properties": {"kind": {"const": "external_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )

    store = SchemaStore.from_repo_root(
        REPO_ROOT,
        supplemental_schema_paths=(schema_path,),
    )

    store.validate_instance({"kind": "external_note"}, schema_id=schema_id)
    assert store.supplemental_schema_ids == (schema_id,)


def test_schema_store_accepts_supplemental_schema_directory_paths(tmp_path: Path) -> None:
    schema_dir = tmp_path / "schemas"
    root_schema_id = "urn:watchtower:schema:external:root-note:v1"
    nested_schema_id = "urn:watchtower:schema:external:nested-note:v1"
    write_json(
        schema_dir / "root_note.schema.json",
        {
            "$id": root_schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Root Note",
            "description": "Root-level supplemental schema.",
            "type": "object",
            "properties": {"kind": {"const": "root_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        schema_dir / "nested" / "nested_note.schema.json",
        {
            "$id": nested_schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Nested Note",
            "description": "Nested supplemental schema.",
            "type": "object",
            "properties": {"kind": {"const": "nested_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )

    store = SchemaStore.from_repo_root(
        REPO_ROOT,
        supplemental_schema_paths=(schema_dir,),
    )

    store.validate_instance({"kind": "root_note"}, schema_id=root_schema_id)
    store.validate_instance({"kind": "nested_note"}, schema_id=nested_schema_id)
    assert store.supplemental_schema_ids == (nested_schema_id, root_schema_id)


def test_schema_store_rejects_empty_supplemental_schema_directory(tmp_path: Path) -> None:
    empty_dir = tmp_path / "schemas"
    empty_dir.mkdir()

    with pytest.raises(SchemaResolutionError, match="does not contain any JSON files"):
        SchemaStore.from_repo_root(
            REPO_ROOT,
            supplemental_schema_paths=(empty_dir,),
        )


def test_schema_store_rejects_invalid_supplemental_schema_from_path(tmp_path: Path) -> None:
    invalid_schema_path = tmp_path / "schemas" / "invalid.schema.json"
    invalid_schema_path.parent.mkdir(parents=True, exist_ok=True)
    invalid_schema_path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(SchemaResolutionError, match="is not valid JSON"):
        SchemaStore.from_repo_root(
            REPO_ROOT,
            supplemental_schema_paths=(invalid_schema_path,),
        )


def test_schema_store_rejects_duplicate_supplemental_schema_ids_from_paths(
    tmp_path: Path,
) -> None:
    schema_dir = tmp_path / "schemas"
    duplicate_schema_id = "urn:watchtower:schema:external:duplicate-note:v1"
    schema_document = {
        "$id": duplicate_schema_id,
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Duplicate Note",
        "description": "Duplicate supplemental schema.",
        "type": "object",
    }
    write_json(schema_dir / "first.schema.json", schema_document)
    write_json(schema_dir / "second.schema.json", schema_document)

    with pytest.raises(SchemaResolutionError, match="duplicates an existing schema"):
        SchemaStore.from_repo_root(
            REPO_ROOT,
            supplemental_schema_paths=(schema_dir,),
        )
