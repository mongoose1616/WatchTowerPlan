from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest
from watchtower_plan.cli.query_lookup_handlers import (
    _run_query_tasks as plan_query_tasks,
)
from watchtower_plan.cli.query_rendered_handlers import (
    _run_query_coordination as plan_query_coordination,
)

from watchtower_host.cli.main import main


def test_doctor_command_returns_zero(capsys) -> None:
    result = main(["doctor"])

    captured = capsys.readouterr()
    assert result == 0
    assert "workspace is available and core governed surfaces loaded successfully" in captured.out


def test_doctor_command_supports_json_output(capsys) -> None:
    result = main(["doctor", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core doctor"
    assert payload["workspace"] == "core_python"
    assert payload["status"] == "ok"


def test_doctor_command_emits_telemetry_summary_and_jsonl(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(tmp_path))

    result = main(["doctor", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    telemetry_files = tuple(tmp_path.glob("**/*.jsonl"))
    assert result == 0
    assert payload["status"] == "ok"
    assert len(telemetry_files) == 1
    assert "[telemetry] watchtower-core doctor status=ok" in captured.err
    records = [
        json.loads(line) for line in telemetry_files[0].read_text(encoding="utf-8").splitlines()
    ]
    assert records[0]["record_type"] == "run_started"
    assert records[-1]["record_type"] == "run_finished"
    assert any(
        record.get("operation_name") == "watchtower-core doctor"
        and record.get("status") == "ok"
        for record in records
        if record["record_type"] == "operation_result"
    )


def test_doctor_command_can_disable_telemetry(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setenv("WATCHTOWER_TELEMETRY", "off")
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(tmp_path))

    result = main(["doctor", "--format", "json"])

    captured = capsys.readouterr()
    assert result == 0
    assert captured.err == ""
    assert tuple(tmp_path.glob("**/*.jsonl")) == ()


@pytest.mark.parametrize(
    "module_name",
    (
        "watchtower_core.cli.handlers",
        "watchtower_core.cli.query_handlers",
        "watchtower_core.cli.query_coordination_handlers",
    ),
)
def test_retired_cli_facade_modules_are_not_importable(module_name: str) -> None:
    sys.modules.pop(module_name, None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module_name)


def test_split_query_handler_modules_remain_available() -> None:
    assert callable(plan_query_coordination)
    assert callable(plan_query_tasks)


def test_root_command_prints_help(capsys) -> None:
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert "watchtower-core" in captured.out
    assert "uv run watchtower-core doctor" in captured.out
    assert "uv run watchtower-core pack list --format json" in captured.out
    assert 'uv run watchtower-core route preview --request "review code and commit"' in captured.out
    assert "uv run watchtower-core plan query coordination --format json" in captured.out
    assert (
        "uv run watchtower-core plan query artifacts --artifact-family "
        "initiative_state --format json" in captured.out
    )
    assert (
        "uv run watchtower-core plan query readiness --ready-for-execution true --format json"
        in captured.out
    )
    assert (
        "uv run watchtower-core plan query projects --slug watchtower --format json" in captured.out
    )
    assert (
        "uv run watchtower-core plan query authority --domain planning --format json"
        in captured.out
    )
    assert (
        "uv run watchtower-core query standards --category governance --format json" in captured.out
    )
    assert (
        "uv run watchtower-core query acceptance --trace-id "
        "trace.governed_acceptance_example" in captured.out
    )
    assert "uv run watchtower-core query foundations --query philosophy" in captured.out
    assert "uv run watchtower-core query workflows --query validation" in captured.out
    assert (
        "uv run watchtower-core plan task transition --task-id task.example.001 "
        "--task-status completed --format json" in captured.out
    )
    assert "uv run watchtower-core sync repository-paths" in captured.out
    assert "uv run watchtower-core sync route-index" in captured.out
    assert "uv run watchtower-core plan sync standard-index" in captured.out
    assert "uv run watchtower-core plan sync foundation-index" in captured.out
    assert "uv run watchtower-core plan sync workflow-index" in captured.out
    assert "uv run watchtower-core plan sync coordination" in captured.out
    assert "uv run watchtower-core plan sync task-index" in captured.out
    assert "uv run watchtower-core validate all --skip-acceptance" in captured.out
    assert (
        "uv run watchtower-core validate document-semantics --path "
        "core/docs/standards/documentation/workflow_md_standard.md" in captured.out
    )
    assert (
        "uv run watchtower-core validate acceptance --trace-id "
        "trace.governed_acceptance_example" in captured.out
    )
    assert "watchtower-core validate artifact" in captured.out


def test_query_group_prints_group_specific_help(capsys) -> None:
    result = main(["query"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Search the governed lookup surfaces" in captured.out
    assert "query commands" in captured.out
    assert "query foundations" in captured.out
    assert "query workflows" in captured.out
    assert "query references" in captured.out
    assert "query standards" in captured.out
    assert "query acceptance" in captured.out
    assert "query evidence" in captured.out
    assert "watchtower-core query coordination" not in captured.out
    assert "watchtower-core query initiatives" not in captured.out
    assert "watchtower-core query tasks" not in captured.out
    assert "watchtower-core query trace" not in captured.out


def test_query_foundations_help_uses_live_examples(capsys) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["query", "foundations", "--help"])

    captured = capsys.readouterr()
    assert excinfo.value.code == 0
    assert "uv run watchtower-core query foundations --query philosophy" in captured.out
    assert (
        "uv run watchtower-core query foundations --reference-path "
        "core/docs/references/uv_reference.md --format json"
    ) in captured.out


def test_query_foundations_help_emits_help_telemetry(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(tmp_path))

    with pytest.raises(SystemExit) as excinfo:
        main(["query", "foundations", "--help"])

    captured = capsys.readouterr()
    telemetry_files = tuple(tmp_path.glob("**/*.jsonl"))
    assert excinfo.value.code == 0
    assert len(telemetry_files) == 1
    assert "[telemetry] watchtower-core query foundations status=help" in captured.err


@pytest.mark.parametrize("command", (["plan", "query", "coordination", "--help"],))
def test_query_live_family_help_uses_live_phase_terms(
    command: list[str],
    capsys,
) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(command)

    captured = capsys.readouterr()
    assert excinfo.value.code == 0
    assert "closed" in captured.out
    assert "prd" not in captured.out


def test_route_group_prints_group_specific_help(capsys) -> None:
    result = main(["route"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Preview the workflow modules that the current routing surfaces would" in captured.out
    assert "preview" in captured.out
    assert "uv run watchtower-core route preview --request" in captured.out


def test_plan_group_prints_group_specific_help(capsys) -> None:
    result = main(["plan"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Bootstrap live initiative packages" in captured.out
    assert "bootstrap" in captured.out
    assert "confirm-inputs" in captured.out
    assert "approve" in captured.out
    assert "query" in captured.out
    assert "sync" in captured.out
    assert "closeout" in captured.out
    assert "task" in captured.out


def test_plan_query_group_prints_group_specific_help(capsys) -> None:
    result = main(["plan", "query"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Search the plan-owned machine lookup surfaces" in captured.out
    assert "coordination" in captured.out
    assert "initiatives" in captured.out
    assert "tasks" in captured.out
    assert "artifacts" in captured.out
    assert "readiness" in captured.out
    assert "authority" in captured.out
    assert "trace" in captured.out
    assert "uv run watchtower-core plan query coordination --format json" in captured.out


def test_task_group_prints_group_specific_help(capsys) -> None:
    result = main(["plan", "task"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Create, update, and transition initiative-local live task records" in captured.out
    assert "create" in captured.out
    assert "update" in captured.out
    assert "transition" in captured.out
    assert "uv run watchtower-core plan task create --task-id task.example.001" in captured.out


def test_sync_group_prints_group_specific_help(capsys) -> None:
    result = main(["sync"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Rebuild reusable-core derived governed artifacts" in captured.out
    assert "command-index" in captured.out
    assert "route-index" in captured.out
    assert "repository-paths" in captured.out
    assert "uv run watchtower-core sync command-index --write" in captured.out
    assert "watchtower-core plan sync" in captured.out


def test_plan_sync_group_prints_group_specific_help(capsys) -> None:
    result = main(["plan", "sync"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Rebuild plan-owned derived indexes, trackers, and orchestration" in captured.out
    assert "all" in captured.out
    assert "coordination" in captured.out
    assert "foundation-index" in captured.out
    assert "reference-index" in captured.out
    assert "standard-index" in captured.out
    assert "workflow-index" in captured.out
    assert "task-index" in captured.out
    assert "review-index" in captured.out
    assert "task-tracking" in captured.out
    assert "initiative-index" in captured.out
    assert "initiative-tracking" in captured.out
    assert "traceability-index" in captured.out
    assert "github-tasks" in captured.out
    assert "uv run watchtower-core plan sync all" in captured.out


def test_validate_group_prints_group_specific_help(capsys) -> None:
    result = main(["validate"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Run validation commands against governed repository artifacts" in captured.out
    assert "all" in captured.out
    assert "acceptance" in captured.out
    assert "artifact" in captured.out
    assert "document-semantics" in captured.out
    assert "front-matter" in captured.out
    assert "suite" in captured.out
    assert "uv run watchtower-core validate all --skip-acceptance" in captured.out
    assert "uv run watchtower-core validate suite --suite-id" in captured.out
    assert "uv run watchtower-core validate artifact" in captured.out


def test_plan_closeout_group_prints_group_specific_help(capsys) -> None:
    result = main(["plan", "closeout"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Apply terminal closeout state to live plan initiative packages" in captured.out
    assert "initiative" in captured.out
    assert "retained-initiative" in captured.out
    assert "purge-trace" in captured.out
    assert (
        "uv run watchtower-core plan closeout retained-initiative --trace-id trace.example"
        in captured.out
    )
    assert "uv run watchtower-core plan closeout purge-trace" in captured.out
