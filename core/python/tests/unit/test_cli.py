from __future__ import annotations

import json
from pathlib import Path

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


def test_root_command_prints_help(capsys) -> None:
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert "watchtower-core" in captured.out
    assert "uv run watchtower-core doctor" in captured.out
    assert "uv run watchtower-core sync repository-paths" in captured.out
    assert "uv run watchtower-core sync task-index" in captured.out
    assert "watchtower-core validate artifact" in captured.out


def test_query_group_prints_group_specific_help(capsys) -> None:
    result = main(["query"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Search the governed lookup surfaces" in captured.out
    assert "query commands" in captured.out
    assert "query prds" in captured.out
    assert "query decisions" in captured.out
    assert "query designs" in captured.out
    assert "query tasks" in captured.out
    assert (
        "uv run watchtower-core query trace --trace-id trace.core_python_foundation"
        in captured.out
    )


def test_sync_group_prints_group_specific_help(capsys) -> None:
    result = main(["sync"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Rebuild derived governed artifacts" in captured.out
    assert "command-index" in captured.out
    assert "prd-index" in captured.out
    assert "decision-index" in captured.out
    assert "design-document-index" in captured.out
    assert "task-index" in captured.out
    assert "task-tracking" in captured.out
    assert "traceability-index" in captured.out
    assert "repository-paths" in captured.out
    assert "uv run watchtower-core sync command-index --write" in captured.out


def test_validate_group_prints_group_specific_help(capsys) -> None:
    result = main(["validate"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Run validation commands against governed repository artifacts" in captured.out
    assert "artifact" in captured.out
    assert "front-matter" in captured.out
    assert "uv run watchtower-core validate artifact" in captured.out


def test_query_paths_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "paths",
            "--surface-kind",
            "command_doc",
            "--limit",
            "2",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query paths"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all(entry["surface_kind"] == "command_doc" for entry in payload["results"])


def test_query_commands_supports_json_output(capsys) -> None:
    result = main(["query", "commands", "--query", "doctor", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query commands"
    assert payload["status"] == "ok"
    assert any(entry["command"] == "watchtower-core doctor" for entry in payload["results"])


def test_query_prds_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "prds",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query prds"
    assert payload["status"] == "ok"
    assert any(entry["prd_id"] == "prd.core_python_foundation" for entry in payload["results"])


def test_query_decisions_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "decisions",
            "--decision-status",
            "accepted",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query decisions"
    assert payload["status"] == "ok"
    assert any(
        entry["decision_id"] == "decision.core_python_workspace_root"
        for entry in payload["results"]
    )


def test_query_designs_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "designs",
            "--family",
            "feature_design",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query designs"
    assert payload["status"] == "ok"
    assert any(
        entry["document_id"] == "design.features.python_validator_execution"
        for entry in payload["results"]
    )


def test_query_tasks_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "tasks",
            "--trace-id",
            "trace.local_task_tracking",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query tasks"
    assert payload["status"] == "ok"
    assert any(
        entry["task_id"] == "task.local_task_tracking.github_sync.001"
        for entry in payload["results"]
    )


def test_query_trace_supports_json_output(capsys) -> None:
    result = main(
        ["query", "trace", "--trace-id", "trace.core_python_foundation", "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query trace"
    assert payload["status"] == "ok"
    assert payload["result"]["trace_id"] == "trace.core_python_foundation"


def test_sync_repository_paths_supports_json_output(capsys) -> None:
    result = main(["sync", "repository-paths", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_command_index_supports_json_output(capsys) -> None:
    result = main(["sync", "command-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync command-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_prd_index_supports_json_output(capsys) -> None:
    result = main(["sync", "prd-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync prd-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_decision_index_supports_json_output(capsys) -> None:
    result = main(["sync", "decision-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync decision-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_design_document_index_supports_json_output(capsys) -> None:
    result = main(["sync", "design-document-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync design-document-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_task_index_supports_json_output(capsys) -> None:
    result = main(["sync", "task-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_task_tracking_supports_json_output(capsys) -> None:
    result = main(["sync", "task-tracking", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-tracking"
    assert payload["status"] == "ok"
    assert payload["task_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_traceability_index_supports_json_output(capsys) -> None:
    result = main(["sync", "traceability-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync traceability-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_repository_paths_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "repository_path_index.v1.json"

    result = main(
        ["sync", "repository-paths", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync repository-paths"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_command_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "command_index.v1.json"

    result = main(["sync", "command-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync command-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_prd_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "prd_index.v1.json"

    result = main(["sync", "prd-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync prd-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_decision_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "decision_index.v1.json"

    result = main(["sync", "decision-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync decision-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_design_document_index_can_write_to_explicit_output(
    tmp_path: Path, capsys
) -> None:
    output_path = tmp_path / "design_document_index.v1.json"

    result = main(
        ["sync", "design-document-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync design-document-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_task_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "task_index.v1.json"

    result = main(["sync", "task-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_task_tracking_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "task_tracking.md"

    result = main(["sync", "task-tracking", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync task-tracking"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_traceability_index_can_write_to_explicit_output(
    tmp_path: Path, capsys
) -> None:
    output_path = tmp_path / "traceability_index.v1.json"

    result = main(
        ["sync", "traceability-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync traceability-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_validate_front_matter_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "docs/standards/metadata/front_matter_standard.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate front-matter"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.standard_front_matter"


def test_validate_front_matter_reports_validation_failure(tmp_path: Path, capsys) -> None:
    document_path = tmp_path / "missing_front_matter.md"
    document_path.write_text("# Missing front matter\n", encoding="utf-8")

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            str(document_path),
            "--validator-id",
            "validator.documentation.standard_front_matter",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate front-matter"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["code"] == "front_matter_missing"


def test_validate_front_matter_can_record_evidence_to_temp_outputs(
    tmp_path: Path, capsys
) -> None:
    evidence_output = tmp_path / "validation_evidence.v1.json"
    traceability_output = tmp_path / "traceability_index.v1.json"

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "docs/standards/metadata/front_matter_standard.md",
            "--record-evidence",
            "--trace-id",
            "trace.core_python_foundation",
            "--subject-id",
            "std.metadata.front_matter",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.core_python_foundation"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_artifact_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.control_plane.acceptance_contract"


def test_validate_artifact_reports_parse_failure(tmp_path: Path, capsys) -> None:
    document_path = tmp_path / "invalid.json"
    document_path.write_text("{ invalid json", encoding="utf-8")

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(document_path),
            "--validator-id",
            "validator.control_plane.acceptance_contract",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["code"] == "json_parse_invalid"


def test_validate_artifact_can_record_evidence_to_temp_outputs(
    tmp_path: Path, capsys
) -> None:
    evidence_output = tmp_path / "validation_evidence.v1.json"
    traceability_output = tmp_path / "traceability_index.v1.json"

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "--record-evidence",
            "--trace-id",
            "trace.core_python_foundation",
            "--acceptance-id",
            "ac.core_python_foundation.001",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.core_python_foundation"
    assert evidence_output.exists()
    assert traceability_output.exists()
