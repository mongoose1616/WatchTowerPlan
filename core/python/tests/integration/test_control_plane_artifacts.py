from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore


REPO_ROOT = Path(__file__).resolve().parents[4]


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

    assert catalog.artifact_id == "registry.schema_catalog"
    assert validators.artifact_id == "registry.validators"
    assert path_index.artifact_id == "index.repository_paths"
    assert command_index.artifact_id == "index.commands"
