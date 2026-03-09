from __future__ import annotations

import json

from watchtower_core.cli.main import main


def test_doctor_command_returns_zero(capsys) -> None:
    result = main(["doctor"])

    captured = capsys.readouterr()
    assert result == 0
    assert "workspace scaffold is available" in captured.out


def test_doctor_command_supports_json_output(capsys) -> None:
    result = main(["doctor", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core doctor"
    assert payload["workspace"] == "core_python"
    assert payload["status"] == "ok"


def test_query_commands_supports_json_output(capsys) -> None:
    result = main(["query", "commands", "--query", "doctor", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query commands"
    assert payload["result_count"] >= 1
    assert payload["results"][0]["command"].startswith("watchtower-core")


def test_query_trace_supports_json_output(capsys) -> None:
    result = main(
        ["query", "trace", "--trace-id", "trace.core_python_foundation", "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query trace"
    assert payload["result"]["trace_id"] == "trace.core_python_foundation"


def test_sync_repository_paths_supports_json_output(capsys) -> None:
    result = main(["sync", "repository-paths", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["entry_count"] > 0
    assert payload["wrote"] is False


def test_root_command_prints_help(capsys) -> None:
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert "watchtower-core" in captured.out
    assert "query" in captured.out
    assert "sync" in captured.out
