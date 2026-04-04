from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tests.cli_command_helpers import run_json_command
from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_host.cli import telemetry_handlers
from watchtower_host.cli.main import main


def test_telemetry_delete_supports_json_output(monkeypatch, capsys, tmp_path: Path) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def delete(self, request: object) -> SimpleNamespace:
            return SimpleNamespace(
                telemetry_root=tmp_path / "telemetry",
                pack_settings_path="offensive_security/.wt/manifests/pack_settings.json",
                machine_root="offensive_security/.wt",
                selection_mode="older_than_days",
                cutoff_utc="2026-03-24T00:00:00Z",
                write=False,
                active_session_output_path=None,
                matched_file_count=2,
                matched_directory_count=1,
                matched_bytes=84,
                deleted_file_count=0,
                deleted_directory_count=0,
                deleted_bytes=0,
                matched_file_paths=(
                    "offensive_security/.wt/runtime/telemetry/2026/03/20/run_a.jsonl",
                    "offensive_security/.wt/runtime/telemetry/2026/03/21/run_b.jsonl",
                ),
                pruned_directory_paths=("offensive_security/.wt/runtime/telemetry/2026/03/20",),
            )

    monkeypatch.setattr(telemetry_handlers, "TelemetryCleanupService", FakeService)
    monkeypatch.setattr(telemetry_handlers, "ControlPlaneLoader", lambda: object())

    result, payload = run_json_command(
        capsys,
        ["telemetry", "delete", "--older-than-days", "7"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core telemetry delete"
    assert payload["status"] == "ok"
    assert payload["selection_mode"] == "older_than_days"
    assert payload["matched_file_count"] == 2
    assert payload["deleted_file_count"] == 0


def test_telemetry_help_lists_delete_leaf(capsys) -> None:
    result = main(["telemetry"])

    help_text = capsys.readouterr().out
    assert result == 0
    assert "delete" in help_text


def test_telemetry_delete_maps_pack_settings_load_errors_to_command_error(
    monkeypatch,
    capsys,
) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def delete(self, request: object) -> SimpleNamespace:
            raise ArtifactLoadError("Could not load governed artifact at missing pack settings")

    monkeypatch.setattr(telemetry_handlers, "TelemetryCleanupService", FakeService)
    monkeypatch.setattr(telemetry_handlers, "ControlPlaneLoader", lambda: object())

    result, payload = run_json_command(
        capsys,
        [
            "telemetry",
            "delete",
            "--all",
            "--pack-settings-path",
            "missing/.wt/manifests/pack_settings.json",
        ],
    )

    assert result == 1
    assert payload["command"] == "watchtower-core telemetry delete"
    assert payload["status"] == "error"
    assert "missing pack settings" in payload["message"]
