from __future__ import annotations

from pathlib import Path

import pytest

from tests.pack_fixture_support import (
    materialize_pack_task_index_surface,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from tests.unit.control_plane_loader_test_support import (
    REPO_ROOT,
    copy_validation_repo_subset,
    materialize_pack_validation_surfaces,
    write_json,
)
from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader import (
    PACK_SETTINGS_PATH,
    ControlPlaneLoader,
)
from watchtower_core.control_plane.models import (
    PackRegistry,
    PackRuntimeManifest,
    PackSettings,
)
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument
from watchtower_core.pack_integration.roots import (
    discover_pack_workspace_roots,
    pack_reference_doc_roots,
)
from watchtower_core.pack_integration.runtime_registry import load_pack_registry_runtime_view


def test_control_plane_loader_reads_pack_registry_and_runtime_manifest(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
    )
    loader = ControlPlaneLoader(repo_root)

    pack_registry = loader.load_pack_registry()
    runtime_manifest = loader.load_pack_runtime_manifest()

    assert isinstance(pack_registry, PackRegistry)
    assert pack_registry.default_pack().pack_slug == "oversight"
    assert isinstance(runtime_manifest, PackRuntimeManifest)
    assert runtime_manifest.integration_module == "watchtower_oversight_fixture.integration"
    assert loader.pack_runtime_manifest_path() == surfaces["pack_runtime_manifest_path"]


def test_control_plane_loader_defers_schema_store_until_needed(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
    )
    loader = ControlPlaneLoader(repo_root)

    assert loader._schema_store is None

    _ = loader.load_json_object("core/control_plane/indexes/workflows/workflow_index.json")

    assert loader._schema_store is None

    _ = loader.load_schema_catalog()

    assert loader._schema_store is not None


def test_control_plane_loader_load_pack_runtime_manifest_activates_minimal_pack_first(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
    )
    loader = ControlPlaneLoader(repo_root)

    runtime_manifest = loader.load_pack_runtime_manifest()

    assert runtime_manifest.command_namespace == "oversight"
    assert loader.active_pack_settings_path == surfaces["pack_settings_path"]


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


def test_control_plane_loader_lazily_activates_default_pack_schema_catalog_for_task_index(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        register_with_host_registry=False,
        register_with_core_python_workspace=False,
    )
    task_surface = materialize_pack_task_index_surface(repo_root / "oversight")
    loader = ControlPlaneLoader(repo_root)

    task_index = loader.load_task_index()

    assert task_index.schema_id == task_surface["schema_id"]
    assert loader.active_pack_settings_path == surfaces["pack_settings_path"]
    assert loader.load_schema_catalog().get(task_surface["schema_id"]).canonical_relative_path == (
        task_surface["schema_relative_path"]
    )


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


def test_control_plane_loader_resolves_registry_default_pack_path_without_schema_store(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    oversight_surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
    )
    loader = ControlPlaneLoader(repo_root)

    assert loader._schema_store is None

    assert loader.default_pack_settings_path() == oversight_surfaces["pack_settings_path"]
    assert loader._schema_store is None


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


def test_pack_reference_doc_root_discovery_supports_generic_hosted_pack_docs_roots(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(
        repo_root / "packs" / "fixture",
        default_repo_pack=True,
    )
    reference_root = repo_root / "packs" / "fixture" / "docs" / "references"
    reference_root.mkdir(parents=True, exist_ok=True)

    assert pack_reference_doc_roots(repo_root) == ("packs/fixture/docs/references",)


def test_pack_workspace_root_discovery_ignores_recoverable_pack_registry_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "fixture", default_repo_pack=True)
    loader = ControlPlaneLoader(repo_root)

    def _raise_missing_registry() -> PackRegistry:
        raise ArtifactLoadError("missing pack registry")

    monkeypatch.setattr(loader, "load_pack_registry", _raise_missing_registry)

    roots = discover_pack_workspace_roots(repo_root, loader=loader)

    assert tuple(root.workspace_root for root in roots) == ("fixture",)


def test_pack_workspace_root_discovery_propagates_unexpected_pack_registry_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "fixture", default_repo_pack=True)
    loader = ControlPlaneLoader(repo_root)

    def _raise_unexpected_registry_error() -> PackRegistry:
        raise RuntimeError("boom")

    monkeypatch.setattr(loader, "load_pack_registry", _raise_unexpected_registry_error)

    with pytest.raises(RuntimeError, match="boom"):
        discover_pack_workspace_roots(repo_root, loader=loader)


def test_pack_registry_runtime_view_ignores_recoverable_pack_activation_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "fixture", default_repo_pack=True)
    loader = ControlPlaneLoader(repo_root)

    def _raise_missing_pack_settings(*args: object, **kwargs: object) -> str:
        raise ArtifactLoadError("missing pack settings")

    monkeypatch.setattr(loader, "activate_pack_settings", _raise_missing_pack_settings)

    runtime_view = load_pack_registry_runtime_view(loader)

    assert any(entry.pack_slug == "fixture" for entry in runtime_view.entries)


def test_pack_registry_runtime_view_propagates_unexpected_default_pack_resolution_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "fixture", default_repo_pack=True)
    loader = ControlPlaneLoader(repo_root)

    def _raise_unexpected_default_pack_resolution(*args: object, **kwargs: object) -> str:
        raise RuntimeError("boom")

    monkeypatch.setattr(
        loader,
        "default_pack_settings_path",
        _raise_unexpected_default_pack_resolution,
    )

    with pytest.raises(RuntimeError, match="boom"):
        load_pack_registry_runtime_view(loader)


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


def test_control_plane_loader_reads_pack_settings(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
    )
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )

    pack_settings = loader.load_pack_settings()

    assert pack_settings.pack_id == "pack.oversight"
    assert pack_settings.get("schema_catalog").path == (
        "oversight/.wt/registries/schema_catalog.json"
    )
    assert pack_settings.get("validator_registry").path == (
        "oversight/.wt/registries/validator_registry.json"
    )
    assert {surface.surface_name for surface in pack_settings.surfaces} == {
        "schema_catalog",
        "validator_registry",
        "validation_suite_registry",
    }
    assert pack_settings.workspace_roots.workspace_root == "oversight"
    assert pack_settings.default_validation_suite_id == surfaces["suite_id"]


def test_control_plane_loader_exposes_generic_typed_document_path() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    typed = loader.load_typed_document(
        PACK_SETTINGS_PATH,
        PackSettings.from_document,
    )

    assert typed.surface_name == "pack_settings"
