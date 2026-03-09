from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.schemas import SchemaStore

REPO_ROOT = Path(__file__).resolve().parents[4]


def load_json(relative_path: str) -> dict[str, object]:
    with (REPO_ROOT / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_schema_store_resolves_cataloged_schema_paths() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    record = store.get_record(
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
    )

    assert record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/documentation/reference_front_matter.v1.schema.json"
    )
    assert store.resolve_path(record.schema_id) == REPO_ROOT / record.canonical_relative_path


def test_schema_store_validates_documentation_front_matter_examples() -> None:
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
