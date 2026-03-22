from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import (
    TelemetryConfig,
    add_operation_attributes,
    create_telemetry_session,
)


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
