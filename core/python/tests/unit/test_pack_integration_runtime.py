from __future__ import annotations

from pathlib import Path

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.pack_integration import PackValidationRuntime
from watchtower_core.pack_integration.runtime import (
    load_active_pack_integration,
    load_pack_validation_runtime,
)
from watchtower_plan.validation.document_semantics import DocumentSemanticsValidationService
from watchtower_plan.validation.targets import resolve_pack_validation_suite_targets


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
