from __future__ import annotations

import pytest

from tests.cli_command_helpers import run_json_command
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import _command_group_specs_for_argv
from watchtower_host.cli.registry import (
    CORE_COMMAND_GROUP_SPECS,
    _specialized_selected_subcommand_registrar,
    find_registered_pack_command_group,
    load_pack_command_group_spec,
)


def test_command_group_specs_for_explicit_core_command_scope_to_selected_family() -> None:
    loader = ControlPlaneLoader()

    specs = _command_group_specs_for_argv(["doctor"], loader)

    assert tuple(spec.name for spec in specs) == ("doctor",)


def test_missing_pack_namespace_does_not_load_runtime_manifest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader()

    def _unexpected_runtime_manifest(*args: object, **kwargs: object) -> object:
        raise AssertionError("missing namespace lookup should not load pack runtime manifests")

    monkeypatch.setattr(loader, "load_pack_runtime_manifest", _unexpected_runtime_manifest)

    assert find_registered_pack_command_group("missing-pack", loader) is None


def test_unknown_command_falls_back_to_full_core_parser_surface() -> None:
    loader = ControlPlaneLoader()

    specs = _command_group_specs_for_argv(["missing-command"], loader)

    assert specs == CORE_COMMAND_GROUP_SPECS


def test_pack_command_group_spec_degrades_to_unavailable_namespace_when_tolerating_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader()
    command_namespace = loader.load_pack_runtime_manifest().command_namespace

    monkeypatch.setattr(
        "watchtower_core.pack_integration.runtime.load_active_pack_integration",
        lambda pack_loader: (_ for _ in ()).throw(ModuleNotFoundError("missing pack runtime")),
    )

    spec = load_pack_command_group_spec(
        command_namespace,
        loader=loader,
        tolerate_import_errors=True,
    )

    assert spec is not None
    assert spec.name == command_namespace
    assert spec.implementation_path is None
    assert spec.notes is not None
    assert "ModuleNotFoundError" in spec.notes


def test_pack_command_group_spec_propagates_pack_failure_without_tolerance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader()
    command_namespace = loader.load_pack_runtime_manifest().command_namespace

    monkeypatch.setattr(
        "watchtower_core.pack_integration.runtime.load_active_pack_integration",
        lambda pack_loader: (_ for _ in ()).throw(ModuleNotFoundError("missing pack runtime")),
    )

    with pytest.raises(ModuleNotFoundError, match="missing pack runtime"):
        load_pack_command_group_spec(
            command_namespace,
            loader=loader,
            tolerate_import_errors=False,
        )


def test_pack_describe_reports_import_error_type_in_json_payload(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "watchtower_host.cli.pack_handlers.import_pack_integration_module",
        lambda **kwargs: (_ for _ in ()).throw(ModuleNotFoundError("missing pack runtime")),
    )

    result, payload = run_json_command(capsys, ["pack", "describe"])

    assert result == 0
    assert payload["command"] == "watchtower-core pack describe"
    assert payload["integration"]["importable"] is False
    assert payload["integration"]["error"] == "ModuleNotFoundError: missing pack runtime"


def test_specialized_selected_subcommand_registrar_passes_requested_subcommand() -> None:
    calls: list[str | None] = []

    def _registrar(
        subparsers: object,
        *,
        selected_subcommand: str | None = None,
    ) -> None:
        del subparsers
        calls.append(selected_subcommand)

    specialized = _specialized_selected_subcommand_registrar(
        _registrar,
        selected_subcommand="sync",
    )

    specialized(object())  # type: ignore[arg-type]

    assert calls == ["sync"]


def test_specialized_selected_subcommand_registrar_passes_requested_subcommand_through_kwargs(
) -> None:
    calls: list[str | None] = []

    def _registrar(subparsers: object, **kwargs: object) -> None:
        del subparsers
        calls.append(kwargs.get("selected_subcommand"))  # type: ignore[arg-type]

    specialized = _specialized_selected_subcommand_registrar(
        _registrar,
        selected_subcommand="sync",
    )

    specialized(object())  # type: ignore[arg-type]

    assert calls == ["sync"]
