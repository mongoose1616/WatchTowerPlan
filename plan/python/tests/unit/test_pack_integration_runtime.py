from __future__ import annotations

import importlib
import json
from dataclasses import replace
from pathlib import Path

import pytest
from watchtower_plan.testing.externalized_plan_fixtures import (
    materialize_externalized_plan_validation_suite,
)

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_externalized_fixture_python,
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
from watchtower_core.telemetry import create_telemetry_session
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets


def _materialize_unbootstrapped_oversight_root_pack(repo_root: Path) -> dict[str, str]:
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
    materialize_externalized_fixture_python(
        repo_root / "oversight" / "python",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        source_package_root=(
            REPO_ROOT
            / "core"
            / "python"
            / "tests"
            / "fixtures"
            / "python"
            / "watchtower_oversight_fixture"
        ),
        description="Synthetic oversight runtime package used to prove hosted-pack portability.",
    )
    return surfaces


def _current_plan_integration_module():
    return importlib.import_module("watchtower_plan.integration")


def test_load_pack_validation_runtime_uses_repo_pack_contract() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    runtime = load_pack_validation_runtime(loader)
    service = runtime.document_semantics_factory(loader)
    service_module = importlib.import_module(service.__class__.__module__)

    assert isinstance(runtime, PackValidationRuntime)
    assert service.__class__.__module__ == "watchtower_plan.validation.document_semantics"
    assert service.__class__.__name__ == "DocumentSemanticsValidationService"
    assert service.__class__ is service_module.DocumentSemanticsValidationService
    assert runtime.suite_target_resolver is resolve_pack_validation_suite_targets


def test_load_active_pack_integration_uses_pack_settings_surface(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
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
    assert "export_cleanup" in loaded.integration.declared_capabilities
    assert loaded.integration.export_cleanup is not None


def test_load_active_pack_integration_records_pack_runtime_telemetry(tmp_path: Path) -> None:
    session = create_telemetry_session(
        ControlPlaneLoader(REPO_ROOT),
        ["pack", "describe", "--pack", "plan"],
        environ={
            "WATCHTOWER_TELEMETRY": "on",
            "WATCHTOWER_TELEMETRY_STDERR": "off",
            "WATCHTOWER_TELEMETRY_DIR": str(tmp_path),
        },
    )
    loader = ControlPlaneLoader(REPO_ROOT)

    with session.activate():
        loaded = load_active_pack_integration(loader)
    session.finish(status="ok", exit_code=0)

    assert loaded.registry_entry.pack_slug == "plan"
    assert session.output_path is not None
    records = [
        json.loads(line)
        for line in session.output_path.read_text(encoding="utf-8").splitlines()
    ]
    assert any(
        record.get("operation_name") == "watchtower_plan.integration"
        and record.get("operation_kind") == "pack_runtime_import"
        and record.get("status") == "ok"
        for record in records
        if record["record_type"] == "operation_result"
    )
    assert any(
        record.get("operation_name") == "load_active_pack_integration"
        and record["attributes"]["pack_slug"] == "plan"
        for record in records
        if record["record_type"] == "operation_result"
    )


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
    plan_integration = _current_plan_integration_module()
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
    plan_integration = _current_plan_integration_module()
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
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
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

    assert {item.registry_entry.pack_slug for item in loaded} == {"plan", "oversight"}
    oversight = next(item for item in loaded if item.registry_entry.pack_slug == "oversight")
    assert (
        oversight.runtime_manifest.integration_module == "watchtower_oversight_fixture.integration"
    )
    assert oversight.integration.command_namespace == "oversight"


def test_selected_pack_loading_still_works_when_another_registered_pack_is_broken(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    plan_surfaces = materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
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


def test_load_active_pack_integration_supports_unbootstrapped_root_pack_fixture(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = _materialize_unbootstrapped_oversight_root_pack(repo_root)
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )

    loaded = load_active_pack_integration(
        loader,
        pack_settings_path=surfaces["pack_settings_path"],
    )

    assert loaded.registry_entry.pack_slug == "oversight"
    assert loaded.runtime_manifest.command_namespace == "oversight"
    assert loaded.integration.command_namespace == "oversight"


def test_load_registered_pack_integrations_discovers_unbootstrapped_root_pack_fixture(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_oversight_root_pack(repo_root)
    loader = ControlPlaneLoader(repo_root)

    loaded = load_registered_pack_integrations(loader)

    assert tuple(item.registry_entry.pack_slug for item in loaded) == ("oversight",)
