from __future__ import annotations

import json
from dataclasses import replace

from watchtower_core.pack_integration import PackQueryRuntime
from watchtower_host.cli.main import main
from watchtower_plan import integration as plan_integration


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
    assert "coordination" in payload["integration"]["query_runtime_commands"]
    assert payload["integration"]["query_runtime_error"] is None
    assert "all" in payload["integration"]["sync_runtime_targets"]
    assert payload["integration"]["sync_runtime_error"] is None


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


def test_pack_describe_reports_runtime_hook_errors_without_masking_import_success(
    capsys,
    monkeypatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        query_runtime=lambda: PackQueryRuntime(commands=()),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["integration"]["importable"] is True
    assert payload["integration"]["error"] is None
    assert payload["integration"]["query_runtime_commands"] is None
    assert "non-empty command names" in payload["integration"]["query_runtime_error"]
    assert "all" in payload["integration"]["sync_runtime_targets"]
