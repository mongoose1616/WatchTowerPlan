from __future__ import annotations

from pathlib import Path

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.context import PackValidationContext


def test_pack_validation_context_loads_only_shared_validation_surfaces(
    tmp_path: Path,
    monkeypatch,
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
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )
    requested_surface_names: list[str] = []
    original = loader.load_declared_surface

    def _wrapped_load_declared_surface(
        *,
        surface_name: str,
        relative_path: str,
    ) -> object:
        requested_surface_names.append(surface_name)
        return original(surface_name=surface_name, relative_path=relative_path)

    monkeypatch.setattr(loader, "load_declared_surface", _wrapped_load_declared_surface)

    context = PackValidationContext.from_loader(loader)

    assert requested_surface_names == [
        "validator_registry",
        "validation_suite_registry",
    ]
    assert set(context.surfaces) == {
        "schema_catalog",
        "validator_registry",
        "validation_suite_registry",
    }
