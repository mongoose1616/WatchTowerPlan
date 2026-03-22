from __future__ import annotations

from tests.pack_fixture_support import REPO_ROOT
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.context import PackValidationContext


def test_pack_validation_context_loads_only_shared_validation_surfaces(
    monkeypatch,
) -> None:
    loader = ControlPlaneLoader(
        REPO_ROOT,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
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
