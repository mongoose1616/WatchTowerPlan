from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.cli.main import main


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


def test_root_command_prints_help(capsys) -> None:
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert "watchtower-core" in captured.out
    assert "uv run watchtower-core doctor" in captured.out
    assert "uv run watchtower-core query coordination --format json" in captured.out
    assert (
        "uv run watchtower-core query standards --category governance --format json"
        in captured.out
    )
    assert (
        "uv run watchtower-core query acceptance --trace-id trace.core_python_foundation"
        in captured.out
    )
    assert "uv run watchtower-core query foundations --query philosophy" in captured.out
    assert "uv run watchtower-core query workflows --query validation" in captured.out
    assert "uv run watchtower-core sync standard-index" in captured.out
    assert "uv run watchtower-core sync foundation-index" in captured.out
    assert "uv run watchtower-core sync workflow-index" in captured.out
    assert "uv run watchtower-core sync coordination" in captured.out
    assert "uv run watchtower-core sync repository-paths" in captured.out
    assert "uv run watchtower-core sync task-index" in captured.out
    assert "uv run watchtower-core validate all --skip-acceptance" in captured.out
    assert (
        "uv run watchtower-core validate document-semantics --path "
        "docs/standards/documentation/workflow_md_standard.md" in captured.out
    )
    assert (
        "uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation"
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
    assert "query foundations" in captured.out
    assert "query workflows" in captured.out
    assert "query references" in captured.out
    assert "query standards" in captured.out
    assert "query prds" in captured.out
    assert "query decisions" in captured.out
    assert "query designs" in captured.out
    assert "query acceptance" in captured.out
    assert "query evidence" in captured.out
    assert "query tasks" in captured.out
    assert "query initiatives" in captured.out
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
    assert "all" in captured.out
    assert "coordination" in captured.out
    assert "foundation-index" in captured.out
    assert "reference-index" in captured.out
    assert "standard-index" in captured.out
    assert "workflow-index" in captured.out
    assert "prd-index" in captured.out
    assert "decision-index" in captured.out
    assert "design-document-index" in captured.out
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
    assert "uv run watchtower-core validate all --skip-acceptance" in captured.out
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


def test_query_paths_supports_retrieval_metadata_filters(capsys) -> None:
    result = main(
        [
            "query",
            "paths",
            "--maturity",
            "authoritative",
            "--priority",
            "high",
            "--audience-hint",
            "shared",
            "--limit",
            "5",
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
    assert all(entry["maturity"] == "authoritative" for entry in payload["results"])
    assert all(entry["priority"] == "high" for entry in payload["results"])
    assert all(entry["audience_hint"] == "shared" for entry in payload["results"])


def test_query_commands_supports_json_output(capsys) -> None:
    result = main(["query", "commands", "--query", "doctor", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query commands"
    assert payload["status"] == "ok"
    assert any(entry["command"] == "watchtower-core doctor" for entry in payload["results"])


def test_query_references_supports_json_output(capsys) -> None:
    result = main(["query", "references", "--query", "uv", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query references"
    assert payload["status"] == "ok"
    assert any(entry["reference_id"] == "ref.uv" for entry in payload["results"])


def test_query_foundations_supports_json_output(capsys) -> None:
    result = main(["query", "foundations", "--query", "philosophy", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query foundations"
    assert payload["status"] == "ok"
    assert any(
        entry["foundation_id"] == "foundation.engineering_design_principles"
        for entry in payload["results"]
    )


def test_query_workflows_supports_json_output(capsys) -> None:
    result = main(["query", "workflows", "--query", "validation", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query workflows"
    assert payload["status"] == "ok"
    assert any(
        entry["workflow_id"] == "workflow.code_validation" for entry in payload["results"]
    )


def test_query_workflows_supports_retrieval_filters(capsys) -> None:
    result = main(
        [
            "query",
            "workflows",
            "--phase-type",
            "reconciliation",
            "--task-family",
            "traceability",
            "--trigger-tag",
            "trace",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query workflows"
    assert payload["status"] == "ok"
    assert any(
        entry["workflow_id"] == "workflow.traceability_reconciliation"
        for entry in payload["results"]
    )
    assert all(entry["phase_type"] == "reconciliation" for entry in payload["results"])
    assert all(entry["task_family"] == "traceability" for entry in payload["results"])
    assert all("trace" in entry["trigger_tags"] for entry in payload["results"])


def test_query_references_supports_reverse_citation_filters(capsys) -> None:
    result = main(
        [
            "query",
            "references",
            "--applied-by-path",
            "docs/standards/governance/github_collaboration_standard.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query references"
    assert payload["status"] == "ok"
    assert any(
        entry["reference_id"] == "ref.github_collaboration" for entry in payload["results"]
    )


def test_query_standards_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "standards",
            "--reference-path",
            "docs/references/github_collaboration_reference.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query standards"
    assert payload["status"] == "ok"
    assert any(
        entry["standard_id"] == "std.governance.github_collaboration"
        for entry in payload["results"]
    )


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
            "--trace-id",
            "trace.core_python_foundation",
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


def test_query_acceptance_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "acceptance",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query acceptance"
    assert payload["status"] == "ok"
    assert any(
        entry["contract_id"] == "contract.acceptance.core_python_foundation"
        for entry in payload["results"]
    )


def test_query_evidence_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "evidence",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query evidence"
    assert payload["status"] == "ok"
    assert any(
        entry["evidence_id"] == "evidence.core_python_foundation.traceability_baseline"
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


def test_query_initiatives_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "initiatives",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    assert payload["status"] == "ok"
    assert any(
        entry["trace_id"] == "trace.core_python_foundation" for entry in payload["results"]
    )


def test_query_coordination_defaults_to_active_status(capsys) -> None:
    result = main(["query", "coordination", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query coordination"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"


def test_query_coordination_supports_explicit_historical_lookup(capsys) -> None:
    result = main(
        [
            "query",
            "coordination",
            "--initiative-status",
            "completed",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query coordination"
    assert payload["status"] == "ok"
    assert any(
        entry["trace_id"] == "trace.core_python_foundation" for entry in payload["results"]
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


def test_sync_all_supports_json_output(capsys) -> None:
    result = main(["sync", "all", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync all"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert payload["wrote"] is False
    assert payload["output_dir"] is None
    assert any(entry["target"] == "command-index" for entry in payload["results"])
    assert any(entry["target"] == "repository-paths" for entry in payload["results"])


def test_sync_coordination_supports_json_output(capsys) -> None:
    result = main(["sync", "coordination", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync coordination"
    assert payload["status"] == "ok"
    assert payload["result_count"] == 5
    assert payload["wrote"] is False
    assert payload["output_dir"] is None
    assert [entry["target"] for entry in payload["results"]] == [
        "task-index",
        "traceability-index",
        "initiative-index",
        "task-tracking",
        "initiative-tracking",
    ]


def test_sync_reference_index_supports_json_output(capsys) -> None:
    result = main(["sync", "reference-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync reference-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_foundation_index_supports_json_output(capsys) -> None:
    result = main(["sync", "foundation-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync foundation-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_standard_index_supports_json_output(capsys) -> None:
    result = main(["sync", "standard-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync standard-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_workflow_index_supports_json_output(capsys) -> None:
    result = main(["sync", "workflow-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync workflow-index"
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


def test_sync_initiative_index_supports_json_output(capsys) -> None:
    result = main(["sync", "initiative-index", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-index"
    assert payload["status"] == "ok"
    assert payload["entry_count"] >= 1
    assert payload["wrote"] is False
    assert payload["artifact_path"] is None


def test_sync_initiative_tracking_supports_json_output(capsys) -> None:
    result = main(["sync", "initiative-tracking", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-tracking"
    assert payload["status"] == "ok"
    assert payload["initiative_count"] >= 1
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


def test_sync_github_tasks_supports_json_output(capsys) -> None:
    result = main(
        [
            "sync",
            "github-tasks",
            "--repo",
            "owner/repo",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync github-tasks"
    assert payload["status"] == "ok"
    assert payload["wrote"] is False
    assert payload["result_count"] >= 1
    assert "labels" in payload["results"][0]


def test_sync_github_tasks_supports_disabling_label_sync(capsys) -> None:
    result = main(
        [
            "sync",
            "github-tasks",
            "--repo",
            "owner/repo",
            "--no-label-sync",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync github-tasks"
    assert all(entry["labels"] == [] for entry in payload["results"])


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


def test_sync_all_can_write_to_explicit_output_dir(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "sync_all"

    result = main(["sync", "all", "--output-dir", str(output_dir), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync all"
    assert payload["wrote"] is True
    assert payload["output_dir"] == str(output_dir.resolve())
    assert (
        output_dir / "core/control_plane/indexes/commands/command_index.v1.json"
    ).exists()
    assert (output_dir / "docs/planning/tasks/task_tracking.md").exists()


def test_sync_coordination_can_write_to_explicit_output_dir(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "sync_coordination"

    result = main(
        ["sync", "coordination", "--output-dir", str(output_dir), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync coordination"
    assert payload["wrote"] is True
    assert payload["output_dir"] == str(output_dir.resolve())
    assert (output_dir / "core/control_plane/indexes/tasks/task_index.v1.json").exists()
    assert (
        output_dir / "core/control_plane/indexes/traceability/traceability_index.v1.json"
    ).exists()
    assert (output_dir / "docs/planning/tasks/task_tracking.md").exists()
    assert (output_dir / "docs/planning/initiatives/initiative_tracking.md").exists()


def test_sync_standard_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "standard_index.v1.json"

    result = main(["sync", "standard-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync standard-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_workflow_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "workflow_index.v1.json"

    result = main(["sync", "workflow-index", "--output", str(output_path), "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync workflow-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_foundation_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "foundation_index.v1.json"

    result = main(
        ["sync", "foundation-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync foundation-index"
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


def test_sync_initiative_index_can_write_to_explicit_output(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "initiative_index.v1.json"

    result = main(
        ["sync", "initiative-index", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-index"
    assert payload["wrote"] is True
    assert payload["artifact_path"] == str(output_path.resolve())
    assert output_path.exists()


def test_sync_initiative_tracking_can_write_to_explicit_output(
    tmp_path: Path, capsys
) -> None:
    output_path = tmp_path / "initiative_tracking.md"

    result = main(
        ["sync", "initiative-tracking", "--output", str(output_path), "--format", "json"]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core sync initiative-tracking"
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


def test_validate_document_semantics_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "document-semantics",
            "--path",
            "workflows/modules/code_validation.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate document-semantics"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.workflow_semantics"


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


def test_validate_acceptance_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "acceptance",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate acceptance"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.trace.acceptance_reconciliation"


def test_validate_all_supports_json_output_when_acceptance_is_skipped(capsys) -> None:
    result = main(["validate", "all", "--skip-acceptance", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["failed_count"] == 0
    assert payload["included_families"] == ["front_matter", "document_semantics", "artifacts"]
    assert any(summary["family"] == "front_matter" for summary in payload["family_summaries"])
    assert any(
        summary["family"] == "document_semantics" for summary in payload["family_summaries"]
    )
    assert any(summary["family"] == "artifacts" for summary in payload["family_summaries"])


def test_validate_all_supports_json_output(capsys) -> None:
    result = main(["validate", "all", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["failed_count"] == 0
    acceptance_summary = next(
        summary for summary in payload["family_summaries"] if summary["family"] == "acceptance"
    )
    assert acceptance_summary["failed_count"] == 0
