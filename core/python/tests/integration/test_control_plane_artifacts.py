from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore

REPO_ROOT = Path(__file__).resolve().parents[4]
FRONT_MATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _load_json_object(path: Path) -> dict[str, object]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_front_matter(path: Path) -> dict[str, object]:
    match = FRONT_MATTER_PATTERN.search(path.read_text(encoding="utf-8"))
    assert match is not None, f"missing front matter: {path}"
    loaded = yaml.safe_load(match.group(1))
    assert isinstance(loaded, dict)
    return loaded


def test_schema_catalog_records_match_loaded_schema_documents() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    for record in store.catalog.records:
        schema_document = store.load_schema(record.schema_id)
        assert schema_document["$id"] == record.schema_id
        assert record.canonical_path.exists()


def test_control_plane_loader_loads_current_governed_artifacts() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    catalog = loader.load_schema_catalog()
    validators = loader.load_validator_registry()
    path_index = loader.load_repository_path_index()
    command_index = loader.load_command_index()
    task_index = loader.load_task_index()

    assert catalog.artifact_id == "registry.schema_catalog"
    assert validators.artifact_id == "registry.validators"
    assert path_index.artifact_id == "index.repository_paths"
    assert command_index.artifact_id == "index.commands"
    assert task_index.artifact_id == "index.tasks"


def test_control_plane_loader_validates_current_traceability_artifacts() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    acceptance_contract = loader.load_validated_document(
        "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json"
    )
    traceability_index = loader.load_validated_document(
        "core/control_plane/indexes/traceability/traceability_index.v1.json"
    )
    validation_evidence = loader.load_validated_document(
        "core/control_plane/ledgers/validation_evidence/"
        "core_python_foundation_traceability_validation.v1.json"
    )

    assert acceptance_contract["id"] == "contract.acceptance.core_python_foundation"
    assert traceability_index["id"] == "index.traceability"
    assert validation_evidence["id"] == "evidence.core_python_foundation.traceability_baseline"


def test_governed_document_front_matter_profiles_validate() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    governed_families = [
        (
            REPO_ROOT / "docs/references",
            {
                "AGENTS.md",
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/prds",
            {
                "README.md",
                "prd_tracking.md",
            },
            "urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/decisions",
            {
                "README.md",
                "decision_tracking.md",
            },
            "urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/design/features",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/design/implementation",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/tasks/open",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/tasks/closed",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/standards",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1",
        ),
    ]

    for directory, excluded_names, schema_id in governed_families:
        for path in sorted(directory.rglob("*.md")):
            if path.name in excluded_names:
                continue
            store.validate_instance(_load_front_matter(path), schema_id=schema_id)


def test_utc_timestamp_fields_reject_offset_timestamps() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    prd_front_matter = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/valid/documentation/prd_front_matter.v1.example.json"
    )
    prd_front_matter["updated_at"] = "2026-03-09T05:06:54-04:00"
    with pytest.raises(ValidationError):
        store.validate_instance(
            prd_front_matter,
            schema_id="urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        )

    validation_evidence = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/valid/ledgers/validation_evidence.v1.example.json"
    )
    validation_evidence["recorded_at"] = "2026-03-09T05:06:54+01:00"
    with pytest.raises(ValidationError):
        store.validate_instance(validation_evidence)
