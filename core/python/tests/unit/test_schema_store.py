from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument

REPO_ROOT = Path(__file__).resolve().parents[4]


def load_json(relative_path: str) -> dict[str, object]:
    with (REPO_ROOT / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def test_schema_store_resolves_cataloged_schema_paths() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    record = store.get_record(
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
    )
    pack_record = store.get_record(
        "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1"
    )

    assert record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/documentation/reference_front_matter.v1.schema.json"
    )
    assert pack_record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/packs/pack_work_item_note.v1.schema.json"
    )
    assert store.resolve_path(record.schema_id) == REPO_ROOT / record.canonical_relative_path


def test_schema_store_validates_documentation_and_pack_interface_examples() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    example_pairs = [
        (
            "core/control_plane/examples/valid/documentation/reference_front_matter.v1.example.json",
            "core/control_plane/examples/invalid/documentation/reference_front_matter_missing_tags.v1.example.json",
            "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
        ),
        (
            "core/control_plane/examples/valid/documentation/feature_design_front_matter.v1.example.json",
            "core/control_plane/examples/invalid/documentation/feature_design_front_matter_missing_trace_id.v1.example.json",
            "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1",
        ),
        (
            "core/control_plane/examples/valid/documentation/implementation_plan_front_matter.v1.example.json",
            "core/control_plane/examples/invalid/documentation/implementation_plan_front_matter_wrong_type.v1.example.json",
            "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/pack_work_item_note.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/pack_work_item_note_missing_work_item_id.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/workspace_artifact_manifest.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/workspace_artifact_manifest_missing_role.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:workspace-artifact-manifest:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/extraction_output_envelope.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/extraction_output_envelope_missing_trace_id.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/promoted_knowledge.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/promoted_knowledge_missing_promotion_record_id.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:promoted-knowledge:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/promotion_record.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/promotion_record_approved_missing_promoted_ids.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:promotion-record:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/pack_work_index.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/pack_work_index_missing_note_path.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:pack-work-index:v1",
        ),
        (
            "core/control_plane/examples/valid/interfaces/knowledge_index.v1.example.json",
            "core/control_plane/examples/invalid/interfaces/knowledge_index_missing_promotion_record_id.v1.example.json",
            "urn:watchtower:schema:interfaces:packs:knowledge-index:v1",
        ),
    ]

    for valid_path, invalid_path, schema_id in example_pairs:
        valid_example = load_json(valid_path)
        invalid_example = load_json(invalid_path)

        store.validate_instance(valid_example, schema_id=schema_id)

        with pytest.raises(ValidationError):
            store.validate_instance(invalid_example, schema_id=schema_id)


def test_schema_store_rejects_unknown_schema_id() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    with pytest.raises(SchemaResolutionError):
        store.load_schema("urn:watchtower:schema:missing:example:v1")


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
    schema_path = tmp_path / "schemas" / "external_note.v1.schema.json"
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
        schema_dir / "root_note.v1.schema.json",
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
        schema_dir / "nested" / "nested_note.v1.schema.json",
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
    invalid_schema_path = tmp_path / "schemas" / "invalid.v1.schema.json"
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
    write_json(schema_dir / "first.v1.schema.json", schema_document)
    write_json(schema_dir / "second.v1.schema.json", schema_document)

    with pytest.raises(SchemaResolutionError, match="duplicates an existing schema"):
        SchemaStore.from_repo_root(
            REPO_ROOT,
            supplemental_schema_paths=(schema_dir,),
        )
