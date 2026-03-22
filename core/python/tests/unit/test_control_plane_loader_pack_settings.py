from __future__ import annotations

from pathlib import Path

import pytest

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from tests.unit.control_plane_loader_test_support import (
    REPO_ROOT,
    copy_validation_repo_subset,
    materialize_pack_validation_surfaces,
    write_json,
)
from watchtower_core.control_plane.loader import (
    PACK_SETTINGS_PATH,
    ControlPlaneLoader,
)
from watchtower_core.control_plane.models import PackRegistry, PackRuntimeManifest, PackSettings
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument
from watchtower_core.pack_integration.roots import discover_pack_workspace_roots


def test_control_plane_loader_reads_pack_registry_and_runtime_manifest() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    pack_registry = loader.load_pack_registry()
    runtime_manifest = loader.load_pack_runtime_manifest()

    assert isinstance(pack_registry, PackRegistry)
    assert pack_registry.default_pack().pack_slug == "plan"
    assert isinstance(runtime_manifest, PackRuntimeManifest)
    assert runtime_manifest.integration_module == "watchtower_plan.integration"
    assert loader.pack_runtime_manifest_path() == "plan/.wt/manifests/pack_runtime_manifest.json"


def test_control_plane_loader_active_pack_settings_merge_pack_schema_catalog(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_surfaces(repo_root / "packs" / "plan")
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )

    pack_settings = loader.load_pack_settings()
    pack_schema = loader.load_schema_catalog().get(surfaces["schema_id"])

    assert pack_settings.pack_id == "pack.loader_test"
    assert loader.active_pack_settings_path == surfaces["pack_settings_path"]
    assert pack_schema.canonical_relative_path == surfaces["schema_relative_path"]


def test_control_plane_loader_active_pack_settings_read_pack_validator_registry(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_surfaces(repo_root / "packs" / "plan")
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )

    registry = loader.load_validator_registry()
    validator = registry.get(surfaces["validator_id"])
    shared_validator = registry.get("validator.control_plane.pack_registry")

    assert validator.engine == "json_schema"
    assert validator.schema_ids == (surfaces["schema_id"],)
    assert shared_validator.artifact_kind == "pack_registry"


def test_control_plane_loader_discovers_repo_local_default_pack_settings_path(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_surfaces(repo_root / "oversight")
    loader = ControlPlaneLoader(repo_root)

    pack_settings = loader.load_pack_settings()

    assert loader.default_pack_settings_path() == surfaces["pack_settings_path"]
    assert pack_settings.pack_id == "pack.loader_test"


def test_control_plane_loader_prefers_registry_default_pack_settings_path(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(
        repo_root / "plan",
        default_repo_pack=False,
    )
    oversight_surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
        registry_mode="append",
    )
    loader = ControlPlaneLoader(repo_root)

    assert loader.default_pack_settings_path() == oversight_surfaces["pack_settings_path"]


def test_control_plane_loader_fallback_prefers_root_pack_before_nested_pack(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    plan_surfaces = materialize_pack_validation_suite(
        repo_root / "plan",
        default_repo_pack=False,
    )
    materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
    )
    loader = ControlPlaneLoader(repo_root)

    assert loader.default_pack_settings_path() == plan_surfaces["pack_settings_path"]


def test_pack_workspace_root_discovery_prefers_root_pack_paths_before_nested_paths(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(
        repo_root / "plan",
        default_repo_pack=False,
    )
    materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
    )
    (repo_root / "core" / "control_plane" / "registries" / "pack_registry.json").unlink()

    roots = discover_pack_workspace_roots(repo_root)

    assert tuple(root.workspace_root for root in roots) == ("plan", "packs/oversight")


def test_control_plane_loader_falls_back_to_core_shared_pack_settings_without_pack_root(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    loader = ControlPlaneLoader(repo_root)

    assert loader.default_pack_settings_path() == "core/control_plane/manifests/pack_settings.json"


def test_control_plane_loader_accepts_supplemental_schema_documents() -> None:
    schema_id = "urn:watchtower:schema:external:loader-check:v1"
    loader = ControlPlaneLoader(
        REPO_ROOT,
        supplemental_schema_documents=(
            SupplementalSchemaDocument.from_document(
                {
                    "$id": schema_id,
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {"kind": {"const": "loader_check"}},
                    "required": ["kind"],
                    "additionalProperties": False,
                },
                source_label="external:loader-check",
            ),
        ),
    )

    loader.schema_store.validate_instance({"kind": "loader_check"}, schema_id=schema_id)
    assert loader.supplemental_schema_ids == (schema_id,)


def test_control_plane_loader_accepts_supplemental_schema_paths(tmp_path: Path) -> None:
    schema_path = tmp_path / "schemas" / "loader_path.schema.json"
    schema_id = "urn:watchtower:schema:external:loader-path-check:v1"
    write_json(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Loader Path Check",
            "description": "Schema loaded from a filesystem path.",
            "type": "object",
            "properties": {"kind": {"const": "loader_path_check"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )

    loader = ControlPlaneLoader(
        REPO_ROOT,
        supplemental_schema_paths=(schema_path,),
    )

    loader.schema_store.validate_instance({"kind": "loader_path_check"}, schema_id=schema_id)
    assert loader.supplemental_schema_ids == (schema_id,)


def test_control_plane_loader_rejects_supplemental_docs_with_explicit_schema_store() -> None:
    schema_store = SchemaStore.from_repo_root(REPO_ROOT)

    with pytest.raises(ValueError, match="supplemental schema documents or paths"):
        ControlPlaneLoader(
            REPO_ROOT,
            schema_store=schema_store,
            supplemental_schema_documents=(
                SupplementalSchemaDocument.from_document(
                    {
                        "$id": "urn:watchtower:schema:external:conflict:v1",
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "type": "object",
                    },
                    source_label="external:conflict",
                ),
            ),
        )


def test_control_plane_loader_rejects_supplemental_paths_with_explicit_schema_store() -> None:
    schema_store = SchemaStore.from_repo_root(REPO_ROOT)

    with pytest.raises(ValueError, match="supplemental schema documents or paths"):
        ControlPlaneLoader(
            REPO_ROOT,
            schema_store=schema_store,
            supplemental_schema_paths=("core/control_plane/schemas/interfaces/packs",),
        )


def test_control_plane_loader_reads_pack_settings() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    pack_settings = loader.load_pack_settings()

    assert pack_settings.pack_id == "pack.plan"
    assert pack_settings.get("schema_catalog").path == ("plan/.wt/registries/schema_catalog.json")
    assert pack_settings.get("rendered_surface_registry").path == (
        "plan/.wt/registries/rendered_surface_registry.json"
    )
    assert pack_settings.get("status_registry").surface_kind == "status_registry"
    assert pack_settings.workspace_roots.workspace_root == "plan"
    assert pack_settings.default_validation_suite_id == "suite.plan.validation_baseline"


def test_control_plane_loader_exposes_generic_typed_document_path() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    typed = loader.load_typed_document(
        PACK_SETTINGS_PATH,
        PackSettings.from_document,
    )

    assert typed.surface_name == "pack_settings"
