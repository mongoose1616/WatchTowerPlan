from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import _command_group_specs_for_argv
from watchtower_host.cli.registry import (
    CORE_COMMAND_GROUP_SPECS,
    find_registered_pack_command_group,
)


def test_command_group_specs_for_explicit_core_command_scope_to_selected_family() -> None:
    loader = ControlPlaneLoader()

    specs = _command_group_specs_for_argv(["doctor"], loader)

    assert tuple(spec.name for spec in specs) == ("doctor",)


def test_missing_pack_namespace_does_not_load_runtime_manifest(monkeypatch) -> None:
    loader = ControlPlaneLoader()

    def _unexpected_runtime_manifest(*args, **kwargs):
        raise AssertionError("missing namespace lookup should not load pack runtime manifests")

    monkeypatch.setattr(loader, "load_pack_runtime_manifest", _unexpected_runtime_manifest)

    assert find_registered_pack_command_group("missing-pack", loader) is None


def test_unknown_command_falls_back_to_full_core_parser_surface() -> None:
    loader = ControlPlaneLoader()

    specs = _command_group_specs_for_argv(["missing-command"], loader)

    assert specs == CORE_COMMAND_GROUP_SPECS
