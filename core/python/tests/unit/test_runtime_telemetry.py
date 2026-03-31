from __future__ import annotations

import json
from pathlib import Path
from typing import IO, cast

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import (
    TelemetryConfig,
    add_operation_attributes,
    create_telemetry_session,
)
from watchtower_core.telemetry import runtime as telemetry_runtime


def test_telemetry_config_reads_environment_flags() -> None:
    config = TelemetryConfig.from_env(
        {
            "WATCHTOWER_TELEMETRY": "off",
            "WATCHTOWER_TELEMETRY_STDERR": "off",
            "WATCHTOWER_TELEMETRY_DIR": "/tmp/watchtower-telemetry",
        }
    )

    assert config.enabled is False
    assert config.emit_stderr is False
    assert config.output_dir_override == Path("/tmp/watchtower-telemetry")


def test_telemetry_session_fails_open_when_override_path_is_a_file(
    tmp_path: Path,
) -> None:
    override_path = tmp_path / "not_a_directory"
    override_path.write_text("occupied\n", encoding="utf-8")

    session = create_telemetry_session(
        ControlPlaneLoader(),
        ["doctor"],
        environ={
            "WATCHTOWER_TELEMETRY": "on",
            "WATCHTOWER_TELEMETRY_STDERR": "on",
            "WATCHTOWER_TELEMETRY_DIR": str(override_path),
        },
    )

    assert session.enabled is False
    assert session.output_path is None
    assert session.disabled_reason is not None


def test_resolve_output_dir_uses_fast_default_pack_path_without_schema_store() -> None:
    loader = ControlPlaneLoader()

    output_dir, pack_settings_path, machine_root = telemetry_runtime._resolve_output_dir(
        loader,
        TelemetryConfig(enabled=True, emit_stderr=False, output_dir_override=None),
        telemetry_runtime._utc_now(),
    )

    assert loader._schema_store is None
    assert pack_settings_path is not None
    assert pack_settings_path.endswith("pack_settings.json")
    assert machine_root is not None
    assert f"{machine_root}/runtime/telemetry/" in str(output_dir)


def test_telemetry_session_records_nested_operations(tmp_path: Path) -> None:
    session = create_telemetry_session(
        ControlPlaneLoader(),
        ["doctor"],
        environ={
            "WATCHTOWER_TELEMETRY": "on",
            "WATCHTOWER_TELEMETRY_STDERR": "off",
            "WATCHTOWER_TELEMETRY_DIR": str(tmp_path),
        },
    )

    with session.activate():
        with session.operation("cli_stage", "parser_build"):
            pass
        with session.operation("cli_command", "watchtower-core doctor") as operation:
            add_operation_attributes(cli_output_format="json")
            operation.set_result(status="ok", exit_code=0)
    session.finish(status="ok", exit_code=0)

    assert session.output_path is not None
    records = [
        json.loads(line)
        for line in session.output_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [record["record_type"] for record in records] == [
        "run_started",
        "operation_result",
        "operation_result",
        "run_finished",
    ]
    assert records[2]["operation_kind"] == "cli_command"
    assert records[2]["attributes"]["cli_output_format"] == "json"
    assert records[3]["status"] == "ok"


def test_telemetry_session_promotes_default_sink_output_on_finish(
    tmp_path: Path,
    monkeypatch,
) -> None:
    def _fake_resolve_output_dir(
        loader: ControlPlaneLoader,
        config: TelemetryConfig,
        started_at,
    ) -> tuple[Path, str | None, str | None]:
        return (
            tmp_path / started_at.strftime("%Y/%m/%d"),
            "packs/fixture/.wt/manifests/pack_settings.json",
            "packs/fixture/.wt",
        )

    monkeypatch.setattr(telemetry_runtime, "_resolve_output_dir", _fake_resolve_output_dir)

    session = create_telemetry_session(
        ControlPlaneLoader(),
        ["doctor"],
        environ={
            "WATCHTOWER_TELEMETRY": "on",
            "WATCHTOWER_TELEMETRY_STDERR": "off",
        },
    )

    with session.activate():
        with session.operation("cli_stage", "parser_build"):
            pass
    session.finish(status="ok", exit_code=0)

    assert session.output_path is not None
    assert session.output_path.exists()
    records = [
        json.loads(line)
        for line in session.output_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [record["record_type"] for record in records] == [
        "run_started",
        "operation_result",
        "run_finished",
    ]


def test_telemetry_session_disables_cleanly_when_writer_fails(tmp_path: Path) -> None:
    class _BrokenWriter:
        def __init__(self) -> None:
            self.closed = False

        def write(self, _: str) -> None:
            raise OSError("disk full")

        def flush(self) -> None:
            return None

        def close(self) -> None:
            self.closed = True

    session = create_telemetry_session(
        ControlPlaneLoader(),
        ["doctor"],
        environ={
            "WATCHTOWER_TELEMETRY": "on",
            "WATCHTOWER_TELEMETRY_STDERR": "off",
            "WATCHTOWER_TELEMETRY_DIR": str(tmp_path),
        },
    )

    assert session.enabled is True
    assert session._writer is not None
    session._writer.close()
    broken_writer = _BrokenWriter()
    session._writer = cast(IO[str], broken_writer)

    session._emit_record({"record_type": "test_failure"})

    assert session.enabled is False
    assert session.disabled_reason == "telemetry_write_failed:OSError"
    assert broken_writer.closed is True
