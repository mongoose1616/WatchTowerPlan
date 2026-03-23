from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tests.unit.schema_store_test_support import (
    REPO_ROOT,
    copy_validation_repo_subset,
    documentation_and_pack_interface_examples,
    materialize_additional_schema_catalog,
    pack_contract_examples,
)
from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.schemas import SchemaStore


def test_schema_store_resolves_cataloged_schema_paths() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    record = store.get_record(
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
    )
    pack_record = store.get_record("urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1")

    assert record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/documentation/reference_front_matter.schema.json"
    )
    assert pack_record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/packs/pack_work_item_note.schema.json"
    )
    assert store.resolve_path(record.schema_id) == REPO_ROOT / record.canonical_relative_path


def test_schema_store_validates_inline_documentation_and_pack_interface_payloads() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    for valid_document, invalid_document, schema_id in documentation_and_pack_interface_examples():
        store.validate_instance(valid_document, schema_id=schema_id)

        with pytest.raises(ValidationError):
            store.validate_instance(invalid_document, schema_id=schema_id)


def test_schema_store_validates_pack_contracts_from_inline_documents() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    for valid_document, invalid_document, schema_id in pack_contract_examples():
        store.validate_instance(valid_document, schema_id=schema_id)

        with pytest.raises(ValidationError):
            store.validate_instance(invalid_document, schema_id=schema_id)


def test_schema_store_accepts_generic_pack_contract_roots_without_plan_specific_fields() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    store.validate_instance(
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
            "surface_name": "pack_settings",
            "contract_version": "v1",
            "description": "Generic pack settings payload.",
            "updated_at": "2026-03-21T21:05:00Z",
            "pack_id": "pack.oversight",
            "workspace_roots": {
                "workspace_root": "oversight",
                "machine_root": "oversight/.wt",
                "docs_root": "oversight/docs",
                "workflows_root": "oversight/workflows",
                "tracking_root": "oversight/tracking",
                "domain_roots": {
                    "reviews": "oversight/reviews",
                    "assessments": "oversight/assessments",
                },
                "overview_path": "oversight/overview.md",
            },
            "default_validation_suite_id": "suite.oversight.validation_baseline",
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
        schema_id="urn:watchtower:schema:interfaces:packs:pack-settings:v1",
    )

    store.validate_instance(
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
            "surface_name": "pack_runtime_manifest",
            "contract_version": "v1",
            "description": "Generic runtime manifest payload.",
            "updated_at": "2026-03-21T21:05:00Z",
            "pack_id": "pack.oversight",
            "pack_slug": "oversight",
            "command_namespace": "oversight",
            "python_distribution": "watchtower-oversight",
            "python_package": "watchtower_oversight",
            "integration_module": "watchtower_oversight.integration",
            "declared_capabilities": [
                "command_registration",
                "query_runtime",
                "sync_targets",
                "validation_provider",
            ],
            "required_validation_suite_ids": ["suite.oversight.validation_baseline"],
            "owned_roots": {
                "workspace_root": "oversight",
                "machine_root": "oversight/.wt",
                "docs_root": "oversight/docs",
                "workflows_root": "oversight/workflows",
                "tracking_root": "oversight/tracking",
                "python_root": "oversight/python",
                "domain_roots": {
                    "reviews": "oversight/reviews",
                    "assessments": "oversight/assessments",
                },
            },
        },
        schema_id="urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
    )


def test_schema_store_accepts_first_party_root_pack_schema_catalog_paths(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    catalog = materialize_additional_schema_catalog(repo_root / "oversight")
    store = SchemaStore.from_repo_root(repo_root)
    document = json.loads((repo_root / catalog["catalog_path"]).read_text(encoding="utf-8"))

    store.validate_instance(
        document,
        schema_id="urn:watchtower:schema:artifacts:registries:schema-catalog:v1",
    )

    assert document["schemas"][0]["canonical_path"] == catalog["schema_relative_path"]


def test_schema_store_rejects_schema_catalog_paths_outside_supported_machine_roots(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    catalog = materialize_additional_schema_catalog(repo_root / "oversight")
    store = SchemaStore.from_repo_root(repo_root)
    document = json.loads((repo_root / catalog["catalog_path"]).read_text(encoding="utf-8"))
    document["schemas"][0]["canonical_path"] = (
        "oversight/schemas/interfaces/packs/schema_store_note.schema.json"
    )

    with pytest.raises(ValidationError):
        store.validate_instance(
            document,
            schema_id="urn:watchtower:schema:artifacts:registries:schema-catalog:v1",
        )


def test_schema_store_rejects_unknown_schema_id() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    with pytest.raises(SchemaResolutionError):
        store.load_schema("urn:watchtower:schema:missing:example:v1")


def test_schema_store_reuses_validators_for_repeat_schema_lookups() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    schema_id = "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"

    first = store.build_validator(schema_id)
    second = store.build_validator(schema_id)

    assert first is second
