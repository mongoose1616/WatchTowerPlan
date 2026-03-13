from __future__ import annotations

from tests.unit.cli_command_helpers import run_json_command


def test_query_commands_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "commands", "--query", "doctor"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query commands"
    assert payload["status"] == "ok"
    assert any(entry["command"] == "watchtower-core doctor" for entry in payload["results"])


def test_query_references_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "references", "--query", "uv"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query references"
    assert payload["status"] == "ok"
    assert any(entry["reference_id"] == "ref.uv" for entry in payload["results"])
    assert all("repository_status" in entry for entry in payload["results"])


def test_query_foundations_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "foundations", "--query", "philosophy"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query foundations"
    assert payload["status"] == "ok"
    assert any(
        entry["foundation_id"] == "foundation.engineering_design_principles"
        for entry in payload["results"]
    )


def test_query_foundations_supports_reference_path_filter(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "foundations",
            "--reference-path",
            "docs/references/uv_reference.md",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query foundations"
    assert payload["status"] == "ok"
    assert any(
        entry["foundation_id"] == "foundation.engineering_stack_direction"
        for entry in payload["results"]
    )


def test_query_standards_respects_foundation_document_family_boundary(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--operationalization-path",
            "docs/foundations/repository_scope.md",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query standards"
    assert payload["status"] == "ok"
    assert any(
        entry["standard_id"] == "std.documentation.foundation_md"
        for entry in payload["results"]
    )

    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--operationalization-path",
            "docs/foundations/README.md",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query standards"
    assert payload["status"] == "ok"
    assert all(
        entry["standard_id"] != "std.documentation.foundation_md"
        for entry in payload["results"]
    )


def test_query_workflows_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "workflows", "--query", "validation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query workflows"
    assert payload["status"] == "ok"
    assert any(
        entry["workflow_id"] == "workflow.code_validation" for entry in payload["results"]
    )


def test_query_workflows_supports_retrieval_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "workflows",
            "--phase-type",
            "reconciliation",
            "--task-family",
            "traceability",
            "--trigger-tag",
            "trace",
        ],
    )

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


def test_query_workflows_supports_boundary_discovery_terms(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "workflows", "--query", "current cli behavior"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query workflows"
    assert payload["status"] == "ok"
    assert any(
        entry["workflow_id"] == "workflow.documentation_implementation_reconciliation"
        for entry in payload["results"]
    )

    result, payload = run_json_command(
        capsys,
        ["query", "workflows", "--query", "successor tasks"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query workflows"
    assert payload["status"] == "ok"
    assert any(
        entry["workflow_id"] == "workflow.task_phase_transition"
        for entry in payload["results"]
    )


def test_query_references_supports_reverse_citation_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "references",
            "--applied-by-path",
            "docs/standards/governance/github_collaboration_standard.md",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query references"
    assert payload["status"] == "ok"
    assert any(
        entry["reference_id"] == "ref.github_collaboration" for entry in payload["results"]
    )


def test_query_references_supports_repository_status_filter(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "references",
            "--repository-status",
            "candidate_future_guidance",
            "--query",
            "telemetry",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query references"
    assert payload["status"] == "ok"
    assert any(entry["reference_id"] == "ref.opentelemetry" for entry in payload["results"])
    assert all(
        entry["repository_status"] == "candidate_future_guidance"
        for entry in payload["results"]
    )


def test_query_references_supports_directory_descendant_related_path_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "references", "--related-path", "core/python/"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query references"
    assert payload["status"] == "ok"
    assert any(entry["reference_id"] == "ref.uv" for entry in payload["results"])


def test_query_standards_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--reference-path",
            "docs/references/github_collaboration_reference.md",
        ],
    )

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
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--applies-to",
            ".github/",
            "--operationalization-path",
            ".github/",
        ],
    )

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
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--operationalization-path",
            "docs/templates/standard_document_template.md",
        ],
    )

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
        result, payload = run_json_command(
            capsys,
            [
                "query",
                "standards",
                "--operationalization-path",
                operationalization_path,
            ],
        )

        assert result == 0
        assert payload["command"] == "watchtower-core query standards"
        assert payload["status"] == "ok"
        assert any(
            entry["standard_id"] == expected_standard_id for entry in payload["results"]
        ), payload["results"]


def test_query_standards_supports_canonical_directory_path_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--applies-to",
            "docs/commands/",
            "--related-path",
            "docs/commands/",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query standards"
    assert payload["status"] == "ok"
    assert any(
        entry["standard_id"] == "std.engineering.cli_help_text"
        and "docs/commands/" in entry["applies_to"]
        and "docs/commands/" in entry["related_paths"]
        for entry in payload["results"]
    )


def test_query_standards_supports_shared_family_tag_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "standards",
            "--category",
            "data_contracts",
            "--tag",
            "planning_index_family",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query standards"
    assert payload["status"] == "ok"
    standard_ids = {entry["standard_id"] for entry in payload["results"]}
    assert "std.data_contracts.planning_index_family" in standard_ids
    assert "std.data_contracts.prd_index" in standard_ids
    assert "std.data_contracts.decision_index" in standard_ids
