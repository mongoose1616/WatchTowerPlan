from __future__ import annotations

import json

from watchtower_host.cli.main import main


def test_pack_list_supports_json_output(capsys) -> None:
    result = main(["pack", "list", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack list"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert any(entry["pack_slug"] == "plan" for entry in payload["results"])


def test_pack_describe_supports_json_output(capsys) -> None:
    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack describe"
    assert payload["pack"]["pack_slug"] == "plan"
    assert payload["runtime_manifest"]["integration_module"] == "watchtower_plan.integration"
    assert "query_runtime" in payload["runtime_manifest"]["declared_capabilities"]


def test_pack_validate_supports_json_output(capsys) -> None:
    result = main(["pack", "validate", "--pack", "plan", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack validate"
    assert payload["pack"] == "plan"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.pack.contract"


def test_pack_describe_reports_unknown_pack_as_json_error(capsys) -> None:
    result = main(["pack", "describe", "--pack", "missing", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core pack describe"
    assert payload["status"] == "error"
    assert "Unknown pack slug: missing." in payload["message"]
