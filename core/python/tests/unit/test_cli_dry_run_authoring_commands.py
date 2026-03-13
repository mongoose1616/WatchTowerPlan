from __future__ import annotations

from tests.unit.cli_command_helpers import run_json_command


def test_task_create_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "task",
            "create",
            "--task-id",
            "task.cli_preview.example.001",
            "--title",
            "Preview the task command",
            "--summary",
            "Previews the task create command without writing a file.",
            "--task-kind",
            "documentation",
            "--priority",
            "medium",
            "--owner",
            "repository_maintainer",
            "--scope",
            "Preview the create command.",
            "--done-when",
            "The dry-run payload is returned.",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core task create"
    assert payload["status"] == "ok"
    assert payload["task_id"] == "task.cli_preview.example.001"
    assert payload["wrote"] is False
    assert payload["changed"] is True


def test_plan_scaffold_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "scaffold",
            "--kind",
            "prd",
            "--trace-id",
            "trace.plan_cli_preview",
            "--document-id",
            "prd.plan_cli_preview",
            "--title",
            "Plan CLI Preview PRD",
            "--summary",
            "Previews the planning scaffold command without writing a file.",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan scaffold"
    assert payload["status"] == "ok"
    assert payload["kind"] == "prd"
    assert payload["document_id"] == "prd.plan_cli_preview"
    assert payload["wrote"] is False
