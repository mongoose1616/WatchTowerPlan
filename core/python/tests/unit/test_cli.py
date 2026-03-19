from __future__ import annotations

import importlib
import json
import sys

import pytest

from watchtower_core.cli.main import main
from watchtower_core.cli.query_coordination_lookup_handlers import (
    _run_query_tasks as split_query_tasks,
)
from watchtower_core.cli.query_coordination_rendered_handlers import (
    _run_query_coordination as split_query_coordination,
)


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
    assert callable(split_query_coordination)
    assert callable(split_query_tasks)


def test_root_command_prints_help(capsys) -> None:
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert "watchtower-core" in captured.out
    assert "uv run watchtower-core doctor" in captured.out
    assert (
        "uv run watchtower-core route preview --request "
        "\"review code and commit\"" in captured.out
    )
    assert "uv run watchtower-core query coordination --format json" in captured.out
    assert (
        "uv run watchtower-core query artifacts --artifact-family initiative_state --format json"
        in captured.out
    )
    assert (
        "uv run watchtower-core query readiness --ready-for-execution true --format json"
        in captured.out
    )
    assert "uv run watchtower-core query projects --slug watchtower --format json" in captured.out
    assert "uv run watchtower-core query authority --domain planning --format json" in captured.out
    assert (
        "uv run watchtower-core query standards --category governance --format json"
        in captured.out
    )
    assert (
        "uv run watchtower-core query acceptance --trace-id "
        "trace.governed_acceptance_example"
        in captured.out
    )
    assert "uv run watchtower-core query foundations --query philosophy" in captured.out
    assert "uv run watchtower-core query workflows --query validation" in captured.out
    assert (
        "uv run watchtower-core task transition --task-id task.example.001 "
        "--task-status completed --format json" in captured.out
    )
    assert "uv run watchtower-core sync standard-index" in captured.out
    assert "uv run watchtower-core sync foundation-index" in captured.out
    assert "uv run watchtower-core sync workflow-index" in captured.out
    assert "uv run watchtower-core sync coordination" in captured.out
    assert "uv run watchtower-core sync repository-paths" in captured.out
    assert "uv run watchtower-core sync route-index" in captured.out
    assert "uv run watchtower-core sync task-index" in captured.out
    assert "uv run watchtower-core validate all --skip-acceptance" in captured.out
    assert (
        "uv run watchtower-core validate document-semantics --path "
        "docs/standards/documentation/workflow_md_standard.md" in captured.out
    )
    assert (
        "uv run watchtower-core validate acceptance --trace-id "
        "trace.governed_acceptance_example"
        in captured.out
    )
    assert "watchtower-core validate artifact" in captured.out


def test_query_group_prints_group_specific_help(capsys) -> None:
    result = main(["query"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Search the governed lookup surfaces" in captured.out
    assert "query commands" in captured.out
    assert "query coordination" in captured.out
    assert "query artifacts" in captured.out
    assert "query readiness" in captured.out
    assert "query discrepancies" in captured.out
    assert "query projects" in captured.out
    assert "query project-context" in captured.out
    assert "query authority" in captured.out
    assert "query foundations" in captured.out
    assert "query workflows" in captured.out
    assert "query references" in captured.out
    assert "query standards" in captured.out
    assert "query acceptance" in captured.out
    assert "query evidence" in captured.out
    assert "query tasks" in captured.out
    assert "query initiatives" in captured.out
    assert (
        "uv run watchtower-core query trace --trace-id "
        "trace.governed_acceptance_example"
        in captured.out
    )


def test_query_foundations_help_uses_live_examples(capsys) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["query", "foundations", "--help"])

    captured = capsys.readouterr()
    assert excinfo.value.code == 0
    assert "uv run watchtower-core query foundations --query philosophy" in captured.out
    assert (
        "uv run watchtower-core query foundations --reference-path "
        "docs/references/uv_reference.md --format json"
    ) in captured.out


@pytest.mark.parametrize(
    "command",
    (
        ["query", "coordination", "--help"],
        ["query", "initiatives", "--help"],
    ),
)
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


def test_task_group_prints_group_specific_help(capsys) -> None:
    result = main(["task"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Create, update, and transition initiative-local live task records" in captured.out
    assert "create" in captured.out
    assert "update" in captured.out
    assert "transition" in captured.out
    assert "uv run watchtower-core task create --task-id task.example.001" in captured.out


def test_sync_group_prints_group_specific_help(capsys) -> None:
    result = main(["sync"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Rebuild derived governed artifacts" in captured.out
    assert "command-index" in captured.out
    assert "all" in captured.out
    assert "coordination" in captured.out
    assert "foundation-index" in captured.out
    assert "reference-index" in captured.out
    assert "route-index" in captured.out
    assert "standard-index" in captured.out
    assert "workflow-index" in captured.out
    assert "task-index" in captured.out
    assert "task-tracking" in captured.out
    assert "initiative-index" in captured.out
    assert "initiative-tracking" in captured.out
    assert "traceability-index" in captured.out
    assert "repository-paths" in captured.out
    assert "uv run watchtower-core sync command-index --write" in captured.out


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


def test_closeout_group_prints_group_specific_help(capsys) -> None:
    result = main(["closeout"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Apply terminal initiative state to live `plan/**` initiative" in captured.out
    assert "plan-initiative" in captured.out
    assert "initiative" in captured.out
    assert "purge-trace" in captured.out
    assert "uv run watchtower-core closeout purge-trace" in captured.out
