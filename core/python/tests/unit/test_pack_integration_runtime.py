from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest
from watchtower_plan import integration as plan_integration
from watchtower_plan.validation.document_semantics import DocumentSemanticsValidationService

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.pack_integration import (
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.pack_integration.runtime import (
    load_active_pack_integration,
    load_pack_query_runtime,
    load_pack_sync_runtime,
    load_pack_validation_runtime,
    load_registered_pack_integrations,
)
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets


def test_load_pack_validation_runtime_uses_repo_pack_contract() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    runtime = load_pack_validation_runtime(loader)

    assert isinstance(runtime, PackValidationRuntime)
    assert isinstance(
        runtime.document_semantics_factory(loader),
        DocumentSemanticsValidationService,
    )
    assert runtime.suite_target_resolver is resolve_pack_validation_suite_targets


def test_load_active_pack_integration_uses_pack_settings_surface(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )

    loaded = load_active_pack_integration(
        loader,
        pack_settings_path=surfaces["pack_settings_path"],
    )

    assert loaded.pack_settings.pack_id == "pack.plan"
    assert loaded.registry_entry.command_namespace == "plan"
    assert loaded.runtime_manifest.command_namespace == "plan"
    assert loaded.integration.python_package == "watchtower_plan"


def test_load_pack_query_runtime_returns_plan_query_contract() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    runtime = load_pack_query_runtime(loader)

    assert isinstance(runtime, PackQueryRuntime)
    assert "coordination" in runtime.commands
    assert "tasks" in runtime.commands


def test_load_pack_sync_runtime_returns_plan_sync_contract() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    runtime = load_pack_sync_runtime(loader)

    assert isinstance(runtime, PackSyncRuntime)
    assert "all" in runtime.targets
    assert "traceability-index" in runtime.targets


def test_load_pack_query_runtime_fails_closed_on_empty_command_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        query_runtime=lambda: PackQueryRuntime(commands=()),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)
    loader = ControlPlaneLoader(REPO_ROOT)

    with pytest.raises(ValueError, match="one or more non-empty command names"):
        load_pack_query_runtime(loader)


def test_load_pack_sync_runtime_fails_closed_on_empty_target_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        sync_targets=lambda: PackSyncRuntime(targets=()),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)
    loader = ControlPlaneLoader(REPO_ROOT)

    with pytest.raises(ValueError, match="one or more non-empty target names"):
        load_pack_sync_runtime(loader)


def test_load_registered_pack_integrations_supports_second_pack_fixture(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "packs" / "plan")
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
    monkeypatch.syspath_prepend(
        str(REPO_ROOT / "core" / "python" / "tests" / "fixtures" / "python")
    )
    loader = ControlPlaneLoader(repo_root)

    loaded = load_registered_pack_integrations(loader)

    assert tuple(item.registry_entry.pack_slug for item in loaded) == ("plan", "oversight")
    oversight = next(item for item in loaded if item.registry_entry.pack_slug == "oversight")
    assert (
        oversight.runtime_manifest.integration_module == "watchtower_oversight_fixture.integration"
    )
    assert oversight.integration.command_namespace == "oversight"


def test_selected_pack_loading_still_works_when_another_registered_pack_is_broken(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    plan_surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    oversight_surfaces = materialize_pack_validation_suite(
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
    oversight_manifest_path = repo_root / oversight_surfaces["pack_runtime_manifest_path"]
    oversight_manifest = json.loads(oversight_manifest_path.read_text(encoding="utf-8"))
    oversight_manifest["integration_module"] = "watchtower_oversight_fixture.missing_integration"
    oversight_manifest_path.write_text(
        f"{json.dumps(oversight_manifest, indent=2)}\n",
        encoding="utf-8",
    )
    loader = ControlPlaneLoader(repo_root)

    loaded = load_active_pack_integration(
        loader,
        pack_settings_path=plan_surfaces["pack_settings_path"],
    )

    assert loaded.registry_entry.pack_slug == "plan"
    with pytest.raises(ModuleNotFoundError):
        load_registered_pack_integrations(loader)
