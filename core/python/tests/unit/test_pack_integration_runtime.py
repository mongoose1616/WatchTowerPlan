from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

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
)
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets
from watchtower_plan import integration as plan_integration
from watchtower_plan.validation.document_semantics import DocumentSemanticsValidationService


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
