from __future__ import annotations

import json
import tempfile
from pathlib import Path
from shutil import copytree

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


def _copy_validation_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _discover_repo_root(start: Path) -> Path:
    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    raise ValueError(f"Could not discover repo root for fixture destination: {start}")


def materialize_additional_schema_catalog(pack_root: Path) -> dict[str, str]:
    repo_root = _discover_repo_root(pack_root)
    control_plane_root = pack_root / ".wt"
    relative_root = control_plane_root.relative_to(repo_root).as_posix()
    schema_id = "urn:watchtower:schema:interfaces:packs:schema-store-note:v1"
    schema_relative_path = f"{relative_root}/schemas/interfaces/packs/schema_store_note.schema.json"
    catalog_path = f"{relative_root}/registries/schema_catalog.json"
    write_json(
        repo_root / schema_relative_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Schema Store Note",
            "description": "Schema discovered through an additional schema catalog.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "schema_store_note"},
            },
            "required": ["$schema", "kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        repo_root / catalog_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:schema-catalog:v1",
            "id": "registry.schema_catalog",
            "title": "Additional Schema Catalog",
            "status": "active",
            "schemas": [
                {
                    "schema_id": schema_id,
                    "title": "Schema Store Note",
                    "description": "Pack-local schema catalog record.",
                    "status": "active",
                    "schema_family": "interface",
                    "subject_kind": "schema_store_note",
                    "version": "v1",
                    "canonical_path": schema_relative_path,
                }
            ],
        },
    )
    return {
        "catalog_path": catalog_path,
        "schema_id": schema_id,
        "schema_relative_path": schema_relative_path,
    }


def test_schema_store_resolves_cataloged_schema_paths() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    record = store.get_record(
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
    )
    pack_record = store.get_record(
        "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1"
    )

    assert record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/documentation/reference_front_matter.schema.json"
    )
    assert pack_record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/packs/pack_work_item_note.schema.json"
    )
    assert store.resolve_path(record.schema_id) == REPO_ROOT / record.canonical_relative_path


def test_schema_store_validates_inline_documentation_and_pack_interface_payloads() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    document_pairs = [
        (
            {
                "id": "ref.example.inline_payload",
                "title": "Inline Reference",
                "summary": "Inline reference front matter payload.",
                "type": "reference",
                "status": "active",
                "tags": ["inline"],
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
            },
            {
                "id": "ref.example.inline_payload",
                "title": "Inline Reference",
                "summary": "Missing tags should fail.",
                "type": "reference",
                "status": "active",
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
            },
            "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
        ),
        (
            {
                "id": "std.example.inline_payload",
                "title": "Inline Standard",
                "summary": "Inline standard front matter payload.",
                "type": "standard",
                "status": "active",
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
                "authority": "authoritative",
            },
            {
                "id": "std.example.inline_payload",
                "title": "Inline Standard",
                "summary": "Missing authority should fail for governed standards.",
                "type": "standard",
                "status": "active",
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
            },
            "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
                "id": "note.example.inline_payload",
                "title": "Inline Work Item Note",
                "summary": "Inline pack-facing note.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_id": "task.example.inline_payload",
                "work_item_type": "task",
                "lifecycle_stage": "active",
                "updated_at": "2026-03-16T07:15:00Z",
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
                "id": "note.example.inline_payload",
                "title": "Inline Work Item Note",
                "summary": "Missing work_item_id should fail.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_type": "task",
                "lifecycle_stage": "active",
                "updated_at": "2026-03-16T07:15:00Z",
            },
            "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
                "id": "envelope.example.inline_payload",
                "title": "Inline Extraction Envelope",
                "summary": "Inline extraction payload.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_id": "task.example.inline_payload",
                "trace_id": "trace.example.inline_payload",
                "source_note_id": "note.example.inline_payload",
                "workflow_run_id": "run.example.inline_payload",
                "extraction_method": "manual",
                "created_at": "2026-03-16T07:15:00Z",
                "observations": [
                    {
                        "observation_id": "observation.example.inline_payload",
                        "summary": "Observed one durable fact.",
                    }
                ],
                "candidate_knowledge": [
                    {
                        "candidate_id": "candidate.example.inline_payload",
                        "title": "Inline Candidate",
                        "summary": "Candidate knowledge extracted from the note.",
                        "knowledge_family": "reference",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
                "id": "envelope.example.inline_payload",
                "title": "Inline Extraction Envelope",
                "summary": "Missing trace_id should fail.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_id": "task.example.inline_payload",
                "source_note_id": "note.example.inline_payload",
                "workflow_run_id": "run.example.inline_payload",
                "extraction_method": "manual",
                "created_at": "2026-03-16T07:15:00Z",
                "observations": [
                    {
                        "observation_id": "observation.example.inline_payload",
                        "summary": "Observed one durable fact.",
                    }
                ],
                "candidate_knowledge": [
                    {
                        "candidate_id": "candidate.example.inline_payload",
                        "title": "Inline Candidate",
                        "summary": "Candidate knowledge extracted from the note.",
                        "knowledge_family": "reference",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
        ),
    ]

    for valid_document, invalid_document, schema_id in document_pairs:
        store.validate_instance(valid_document, schema_id=schema_id)

        with pytest.raises(ValidationError):
            store.validate_instance(invalid_document, schema_id=schema_id)


def test_schema_store_validates_pack_contracts_from_inline_documents() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    example_pairs = [
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
                "surface_name": "pack_settings",
                "contract_version": "v1",
                "description": "Inline pack settings payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "pack_id": "pack.example",
                "surfaces": [
                    {
                        "surface_name": "schema_catalog",
                        "surface_kind": "schema_collection",
                        "path": "core/control_plane/registries/schema_catalog.json",
                        "authority": "authoritative",
                        "visibility": "hidden",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
                "surface_name": "pack_settings",
                "contract_version": "v1",
                "description": "Invalid pack settings payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "pack_id": "pack.example",
                "surfaces": [
                    {
                        "surface_name": "schema_catalog",
                        "surface_kind": "wrong_kind",
                        "path": "core/control_plane/registries/schema_catalog.json",
                        "authority": "authoritative",
                        "visibility": "hidden",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:status-registry:v1",
                "surface_name": "status_registry",
                "contract_version": "v1",
                "description": "Inline status registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "statuses": [
                    {
                        "value": "active",
                        "entry_status": "active",
                        "summary": "Currently open.",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:status-registry:v1",
                "surface_name": "status_registry",
                "contract_version": "v1",
                "description": "Invalid status registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "statuses": [
                    {
                        "value": "active",
                        "entry_status": "unsupported",
                        "summary": "Currently open.",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:status-registry:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:actor-registry:v1",
                "surface_name": "actor_registry",
                "contract_version": "v1",
                "description": "Inline actor registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "actors": [
                    {
                        "actor_id": "actor.example",
                        "actor_type": "agent",
                        "label": "Example Agent",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:actor-registry:v1",
                "surface_name": "actor_registry",
                "contract_version": "v1",
                "description": "Invalid actor registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "actors": [
                    {
                        "actor_id": "example",
                        "actor_type": "agent",
                        "label": "Example Agent",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:actor-registry:v1",
        ),
    ]

    for valid_document, invalid_document, schema_id in example_pairs:
        store.validate_instance(valid_document, schema_id=schema_id)

        with pytest.raises(ValidationError):
            store.validate_instance(invalid_document, schema_id=schema_id)


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


def test_schema_store_merges_additional_schema_catalog_paths(tmp_path: Path) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    catalog = materialize_additional_schema_catalog(repo_root / "packs" / "plan")
    base_store = SchemaStore.from_repo_root(repo_root)
    store = base_store.with_additional_catalog_paths((catalog["catalog_path"],))

    assert store.get_record(catalog["schema_id"]).canonical_relative_path == (
        catalog["schema_relative_path"]
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
