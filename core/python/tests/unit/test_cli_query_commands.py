from __future__ import annotations

import json

from watchtower_core.cli.main import main


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


def test_route_preview_supports_json_output(capsys) -> None:
    result = main(
        [
            "route",
            "preview",
            "--task-type",
            "Repository Review",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core route preview"
    assert payload["status"] == "ok"
    assert payload["selected_route_count"] == 1
    assert payload["selected_routes"][0]["task_type"] == "Repository Review"
    assert any(
        workflow["workflow_id"] == "workflow.repository_review"
        for workflow in payload["selected_workflows"]
    )


def test_route_preview_matches_realistic_maintenance_request(capsys) -> None:
    result = main(
        [
            "route",
            "preview",
            "--request",
            (
                "review /home/j/WatchTower/report and fix the valid issues with "
                "planning, tasks, validation, and commits"
            ),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    workflow_ids = {entry["workflow_id"] for entry in payload["selected_workflows"]}
    assert result == 0
    assert payload["command"] == "watchtower-core route preview"
    assert payload["status"] == "ok"
    assert payload["selected_route_count"] >= 4
    assert "Repository Review" in task_types
    assert "Task Lifecycle Management" in task_types
    assert "Code Validation" in task_types
    assert "Commit Closeout" in task_types
    assert "Code Review" not in task_types
    assert "workflow.repository_review" in workflow_ids
    assert "workflow.task_lifecycle_management" in workflow_ids
    assert "workflow.code_validation" in workflow_ids
    assert "workflow.commit_closeout" in workflow_ids


def test_task_create_supports_json_output(capsys) -> None:
    result = main(
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
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core task create"
    assert payload["status"] == "ok"
    assert payload["task_id"] == "task.cli_preview.example.001"
    assert payload["wrote"] is False
    assert payload["changed"] is True


def test_plan_scaffold_supports_json_output(capsys) -> None:
    result = main(
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
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan scaffold"
    assert payload["status"] == "ok"
    assert payload["kind"] == "prd"
    assert payload["document_id"] == "prd.plan_cli_preview"
    assert payload["wrote"] is False


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


def test_query_foundations_supports_reference_path_filter(capsys) -> None:
    result = main(
        [
            "query",
            "foundations",
            "--reference-path",
            "docs/references/uv_reference.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query foundations"
    assert payload["status"] == "ok"
    assert any(
        entry["foundation_id"] == "foundation.engineering_stack_direction"
        for entry in payload["results"]
    )


def test_query_standards_respects_foundation_document_family_boundary(capsys) -> None:
    result = main(
        [
            "query",
            "standards",
            "--operationalization-path",
            "docs/foundations/repository_scope.md",
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
        entry["standard_id"] == "std.documentation.foundation_md"
        for entry in payload["results"]
    )

    result = main(
        [
            "query",
            "standards",
            "--operationalization-path",
            "docs/foundations/README.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query standards"
    assert payload["status"] == "ok"
    assert all(
        entry["standard_id"] != "std.documentation.foundation_md"
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
    assert all("owner" in entry for entry in payload["results"])
    assert all("operationalization_modes" in entry for entry in payload["results"])


def test_query_standards_supports_operationalization_filters(capsys) -> None:
    result = main(
        [
            "query",
            "standards",
            "--applies-to",
            ".github/",
            "--operationalization-path",
            ".github/",
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
        and entry["owner"] == "repository_maintainer"
        and ".github/" in entry["applies_to"]
        and ".github/" in entry["operationalization_paths"]
        for entry in payload["results"]
    )


def test_query_standards_exposes_standard_template_operationalization_path(capsys) -> None:
    result = main(
        [
            "query",
            "standards",
            "--operationalization-path",
            "docs/templates/standard_document_template.md",
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
        entry["standard_id"] == "std.documentation.standard_md"
        and "docs/templates/standard_document_template.md"
        in entry["operationalization_paths"]
        for entry in payload["results"]
    )


def test_query_standards_matches_descendant_and_glob_operationalization_paths(
    capsys,
) -> None:
    cases = (
        (
            "docs/planning/prds/reference_and_workflow_standards_alignment.md",
            "std.documentation.prd_md",
        ),
        (
            "docs/planning/decisions/reference_and_workflow_standards_alignment_direction.md",
            "std.documentation.decision_record_md",
        ),
        (
            "docs/templates/documentation_template.md",
            "std.documentation.compact_document_authoring",
        ),
        (
            "docs/references/AGENTS.md",
            "std.documentation.agents_md",
        ),
        (
            "docs/planning/README.md",
            "std.documentation.readme_md",
        ),
        (
            "docs/references/commonmark_reference.md",
            "std.documentation.reference_md",
        ),
        (
            "docs/standards/documentation/readme_md_standard.md",
            "std.documentation.standard_md",
        ),
        (
            "core/control_plane/examples/valid/contracts/acceptance_contract.v1.example.json",
            "std.data_contracts.acceptance_contract",
        ),
        (
            "core/control_plane/examples/valid/registries/authority_map.v1.example.json",
            "std.data_contracts.authority_map",
        ),
        (
            "core/control_plane/examples/valid/indexes/standard_index.v1.example.json",
            "std.data_contracts.standard_index",
        ),
        (
            "core/python/src/watchtower_core/repo_ops/sync/foundation_index.py",
            "std.data_contracts.foundation_index",
        ),
        (
            "core/python/src/watchtower_core/repo_ops/query/foundations.py",
            "std.data_contracts.foundation_index",
        ),
        (
            "docs/commands/core_python/watchtower_core_query_foundations.md",
            "std.data_contracts.foundation_index",
        ),
        (
            "docs/commands/core_python/watchtower_core_sync_foundation_index.md",
            "std.data_contracts.foundation_index",
        ),
        (
            "core/control_plane/indexes/foundations/README.md",
            "std.data_contracts.foundation_index",
        ),
        (
            "core/control_plane/examples/valid/ledgers/validation_evidence.v1.example.json",
            "std.data_contracts.validation_evidence",
        ),
        (
            "core/control_plane/examples/valid/indexes/workflow_index.v1.example.json",
            "std.data_contracts.workflow_index",
        ),
    )

    for operationalization_path, expected_standard_id in cases:
        result = main(
            [
                "query",
                "standards",
                "--operationalization-path",
                operationalization_path,
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
            entry["standard_id"] == expected_standard_id for entry in payload["results"]
        ), payload["results"]


def test_query_standards_supports_canonical_directory_path_filters(capsys) -> None:
    result = main(
        [
            "query",
            "standards",
            "--applies-to",
            "docs/commands/",
            "--related-path",
            "docs/commands/",
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
        entry["standard_id"] == "std.engineering.cli_help_text"
        and "docs/commands/" in entry["applies_to"]
        and "docs/commands/" in entry["related_paths"]
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


def test_query_tasks_supports_dependency_details_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "tasks",
            "--task-id",
            "task.local_task_tracking.github_sync.001",
            "--include-dependency-details",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query tasks"
    entry = payload["results"][0]
    assert entry["task_id"] == "task.local_task_tracking.github_sync.001"
    assert "blocked_by_details" in entry
    assert "depends_on_details" in entry
    assert "reverse_dependency_details" in entry


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
    assert payload["coordination_mode"] in {
        "active_work",
        "blocked_work",
        "ready_for_bootstrap",
    }
    assert payload["recommended_next_action"]
    assert payload["recommended_surface_path"]
    assert "actionable_tasks" in payload
    assert "recent_closed_initiatives" in payload


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
    matched = next(
        entry for entry in payload["results"] if entry["trace_id"] == "trace.core_python_foundation"
    )
    assert matched["artifact_status"] == "active"
    assert matched["initiative_status"] == "completed"
    assert "status" not in matched


def test_query_planning_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "planning",
            "--trace-id",
            "trace.core_python_foundation",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query planning"
    assert payload["status"] == "ok"
    assert payload["results"][0]["trace_id"] == "trace.core_python_foundation"
    assert "artifact_status" in payload["results"][0]
    assert "status" not in payload["results"][0]
    assert payload["results"][0]["coordination"]["current_phase"]


def test_query_initiatives_uses_explicit_artifact_status_field(capsys) -> None:
    result = main(
        [
            "query",
            "initiatives",
            "--trace-id",
            "trace.core_python_foundation",
            "--initiative-status",
            "completed",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    entry = next(
        item for item in payload["results"] if item["trace_id"] == "trace.core_python_foundation"
    )
    assert entry["artifact_status"] == "active"
    assert entry["initiative_status"] == "completed"
    assert "status" not in entry


def test_query_authority_supports_json_output(capsys) -> None:
    result = main(
        [
            "query",
            "authority",
            "--question-id",
            "authority.planning.deep_trace_context",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query authority"
    assert payload["status"] == "ok"
    assert payload["results"][0]["question_id"] == "authority.planning.deep_trace_context"
    assert payload["results"][0]["artifact_kind"] == "planning_catalog"
    assert payload["results"][0]["preferred_command"] == "watchtower-core query planning"


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
