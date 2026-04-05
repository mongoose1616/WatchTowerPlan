from __future__ import annotations

from tests.cli_command_helpers import run_json_command
from tests.unit.control_plane_loader_test_support import REPO_ROOT
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _active_pack_workflow_module_path(module_name: str) -> str:
    workflows_root = (
        ControlPlaneLoader(REPO_ROOT).load_pack_settings().workspace_roots.workflows_root
    )
    return f"{workflows_root}/modules/{module_name}.md"


def _has_task_lifecycle_route() -> bool:
    return (REPO_ROOT / _active_pack_workflow_module_path("task_lifecycle_management")).exists()


def _has_task_phase_transition_route() -> bool:
    return (REPO_ROOT / _active_pack_workflow_module_path("task_phase_transition")).exists()


def test_query_paths_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "paths",
            "--surface-kind",
            "command_doc",
            "--limit",
            "2",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query paths"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all(entry["surface_kind"] == "command_doc" for entry in payload["results"])


def test_query_paths_supports_retrieval_metadata_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
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
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query paths"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all(entry["maturity"] == "authoritative" for entry in payload["results"])
    assert all(entry["priority"] == "high" for entry in payload["results"])
    assert all(entry["audience_hint"] == "shared" for entry in payload["results"])


def test_route_preview_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["route", "preview", "--task-type", "Repository Review"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core route preview"
    assert payload["status"] == "ok"
    assert payload["selected_route_count"] == 1
    assert payload["activated_intents"] == []
    assert payload["selected_routes"][0]["task_type"] == "Repository Review"
    assert any(
        workflow["workflow_id"] == "workflow.repository_review"
        for workflow in payload["selected_workflows"]
    )


def test_route_preview_keeps_commit_closeout_as_companion_route(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "adversarial refactor and optimization and commit",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Code Implementation",
        "Commit Closeout",
    }
    assert {
        entry["workflow_id"] for entry in payload["selected_workflows"]
    } >= {
        "workflow.code_implementation",
        "workflow.commit_closeout",
        "workflow.adversarial_reviewer",
    }
    assert {
        entry["intent_id"] for entry in payload["activated_intents"]
    } >= {
        "route.overlay_adversarial_lens",
        "route.overlay_commit_closeout_intent",
    }


def test_route_preview_keeps_closeout_and_overlay_routes_flexible(capsys) -> None:
    expectations = {
        "documentation and fix loop and commit": {
            "routes": {
                "Documentation Review",
                "Review Remediation Loop",
                "Commit Closeout",
            },
            "workflows": {
                "workflow.documentation_review",
                "workflow.review_remediation_loop",
                "workflow.commit_closeout",
            },
        },
        "adversarial telemetry, benchmark review and fix and commit": {
            "routes": {
                "Performance Benchmarking",
                "Review Remediation",
                "Commit Closeout",
            },
            "workflows": {
                "workflow.performance_benchmarking",
                "workflow.review_remediation",
                "workflow.commit_closeout",
                "workflow.adversarial_reviewer",
            },
        },
        "adversarial project coherence and fix loop and commit": {
            "routes": {
                "Repository Review",
                "Review Remediation Loop",
                "Commit Closeout",
            },
            "workflows": {
                "workflow.repository_review",
                "workflow.review_remediation_loop",
                "workflow.commit_closeout",
                "workflow.adversarial_reviewer",
            },
        },
    }

    for request_text, expected in expectations.items():
        result, payload = run_json_command(
            capsys,
            [
                "route",
                "preview",
                "--request",
                request_text,
            ],
        )

        assert result == 0
        assert expected["routes"].issubset(
            {entry["task_type"] for entry in payload["selected_routes"]}
        )
        assert expected["workflows"].issubset(
            {entry["workflow_id"] for entry in payload["selected_workflows"]}
        )


def test_route_preview_matches_realistic_maintenance_request(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            (
                "review /external/repository/report and fix the valid issues with "
                "planning, tasks, validation, and commits"
            ),
        ],
    )

    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    workflow_ids = {entry["workflow_id"] for entry in payload["selected_workflows"]}
    assert result == 0
    assert payload["command"] == "watchtower-core route preview"
    assert payload["status"] == "ok"
    assert "Review Remediation" in task_types
    assert "Repository Review" not in task_types
    assert "workflow.review_remediation" in workflow_ids
    assert "workflow.code_validation" in workflow_ids
    if _has_task_lifecycle_route():
        assert "Task Lifecycle Management" in task_types
        assert "workflow.task_lifecycle_management" in workflow_ids
    else:
        assert "Task Lifecycle Management" not in task_types


def test_route_preview_matches_review_remediation_loop_requests(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "fix the findings from this review and rerun the same review until clean",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Review Remediation Loop"
    }
    assert {
        entry["workflow_id"] for entry in payload["selected_workflows"]
    } >= {
        "workflow.review_remediation",
        "workflow.review_remediation_loop",
        "workflow.code_validation",
    }


def test_route_preview_matches_adversarial_repository_audits(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "run a full-spectrum adversarial audit of the repository",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Adversarial Repository Review"
    }
    assert {
        entry["workflow_id"] for entry in payload["selected_workflows"]
    } >= {
        "workflow.adversarial_reviewer",
        "workflow.repository_review",
        "workflow.code_validation",
    }
    assert payload["activated_intents"] == []


def test_route_preview_merges_adversarial_review_with_fix_loops(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "do an adversarial and fix loop",
        ],
    )

    assert result == 0
    assert "Adversarial Repository Review" not in {
        entry["task_type"] for entry in payload["selected_routes"]
    }
    assert "Review Remediation Loop" in {
        entry["task_type"] for entry in payload["selected_routes"]
    }
    assert {
        entry["workflow_id"] for entry in payload["selected_workflows"]
    } >= {
        "workflow.adversarial_reviewer",
        "workflow.review_remediation",
        "workflow.review_remediation_loop",
        "workflow.code_validation",
    }
    assert "workflow.repository_review" not in {
        entry["workflow_id"] for entry in payload["selected_workflows"]
    }
    assert payload["warnings"] == []


def test_route_preview_keeps_adversarial_mentions_out_of_documentation_reviews(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "do a documentation review of adversarial examples references",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Documentation Review"
    }
    assert "workflow.adversarial_reviewer" not in {
        entry["workflow_id"] for entry in payload["selected_workflows"]
    }


def test_route_preview_filters_non_applying_modifier_intents(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "run an adversarial commit",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Commit Closeout"
    }
    assert {entry["intent_id"] for entry in payload["activated_intents"]} == {
        "route.overlay_commit_closeout_intent"
    }


def test_route_preview_pairs_adversarial_role_with_review_and_fix_routes(capsys) -> None:
    expectations = {
        "run an adversarial code review": {
            "routes": {"Code Review"},
            "workflows": {"workflow.adversarial_reviewer", "workflow.code_review"},
        },
        "run an adversarial documentation review": {
            "routes": {"Documentation Review"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.documentation_review",
            },
        },
        "run an adversarial workflow system review": {
            "routes": {"Workflow System Review"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.workflow_steward",
                "workflow.workflow_system_review",
            },
        },
        "run an adversarial standards audit": {
            "routes": {"Standards Alignment Review"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.standards_alignment_review",
            },
        },
        "run an adversarial validation harness review": {
            "routes": {"Validation Harness Review"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.validation_harness_review",
            },
        },
        "i want a adversarial telemetry, benchmark review and fix": {
            "routes": {"Performance Benchmarking", "Review Remediation"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.performance_benchmarking",
                "workflow.review_remediation",
            },
        },
        "i want a adversarial refactor and optimization": {
            "routes": {"Code Implementation"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.code_implementation",
            },
        },
        "do an adversarial stale test cleanup": {
            "routes": {"Test Suite Optimization"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.test_suite_optimization",
            },
        },
        "i want a adversarial project coherence and fix loop": {
            "routes": {"Repository Review", "Review Remediation Loop"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.repository_review",
                "workflow.review_remediation_loop",
            },
        },
        "do an adversarial repository review and fix loop": {
            "routes": {"Adversarial Repository Review", "Review Remediation Loop"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.repository_review",
                "workflow.review_remediation_loop",
            },
        },
    }

    for request_text, expected in expectations.items():
        result, payload = run_json_command(
            capsys,
            [
                "route",
                "preview",
                "--request",
                request_text,
            ],
        )

        assert result == 0
        route_task_types = {entry["task_type"] for entry in payload["selected_routes"]}
        workflow_ids = {entry["workflow_id"] for entry in payload["selected_workflows"]}
        assert expected["routes"].issubset(route_task_types)
        if request_text != "do an adversarial repository review and fix loop":
            assert "Adversarial Repository Review" not in route_task_types
        if request_text == "do an adversarial repository review and fix loop":
            assert "Repository Review" not in route_task_types
        assert expected["workflows"].issubset(workflow_ids)


def test_route_preview_pairs_fix_loops_with_documentation_and_repository_reviews(capsys) -> None:
    expectations = {
        "i want a documentation and fix loop": {
            "Documentation Review",
            "Review Remediation Loop",
        },
        "i want a docs audit and fix loop": {
            "Documentation Review",
            "Review Remediation Loop",
        },
        "i want a project coherence and fix loop": {
            "Repository Review",
            "Review Remediation Loop",
        },
    }

    for request_text, expected_routes in expectations.items():
        result, payload = run_json_command(
            capsys,
            [
                "route",
                "preview",
                "--request",
                request_text,
            ],
        )

        assert result == 0
        assert expected_routes.issubset(
            {entry["task_type"] for entry in payload["selected_routes"]}
        )


def test_route_preview_keeps_origin_scope_for_fix_loop_variants(capsys) -> None:
    expectations = {
        "benchmark review and fix loop": {
            "routes": {"Performance Benchmarking", "Review Remediation Loop"},
            "workflows": {
                "workflow.performance_benchmarking",
                "workflow.review_remediation_loop",
            },
        },
        "workflow audit and fix loop": {
            "routes": {"Workflow System Review", "Review Remediation Loop"},
            "workflows": {
                "workflow.workflow_system_review",
                "workflow.workflow_steward",
                "workflow.review_remediation_loop",
            },
        },
        "full-spectrum audit and fix loop": {
            "routes": {"Adversarial Repository Review", "Review Remediation Loop"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.repository_review",
                "workflow.review_remediation_loop",
            },
        },
        "validator audit and remediation loop": {
            "routes": {"Validation Harness Review", "Review Remediation Loop"},
            "workflows": {
                "workflow.validation_harness_review",
                "workflow.review_remediation_loop",
            },
        },
        "adversarial validator audit and remediation loop": {
            "routes": {"Validation Harness Review", "Review Remediation Loop"},
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.validation_harness_review",
                "workflow.review_remediation_loop",
            },
        },
    }

    for request_text, expected in expectations.items():
        result, payload = run_json_command(
            capsys,
            [
                "route",
                "preview",
                "--request",
                request_text,
            ],
        )

        assert result == 0
        route_task_types = {entry["task_type"] for entry in payload["selected_routes"]}
        workflow_ids = {entry["workflow_id"] for entry in payload["selected_workflows"]}
        assert expected["routes"].issubset(route_task_types)
        assert expected["workflows"].issubset(workflow_ids)
        assert "Review Remediation" not in route_task_types


def test_route_preview_keeps_fix_loops_specific_when_loop_route_is_selected(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "fix the findings from this review and rerun the same review until clean",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Review Remediation Loop"
    }


def test_route_preview_matches_adjacent_boundary_prompts(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "reconcile command docs with current cli behavior",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Documentation-Implementation Reconciliation"
    }

    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "reconcile schema-backed indexes examples and validators for one artifact family",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Governed Artifact Reconciliation"
    }


def test_route_preview_filters_low_signal_route_leakage_for_phase_handoffs(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "hand off this task from implementation to validation and create successor tasks",
        ],
    )

    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    assert result == 0
    if _has_task_phase_transition_route():
        assert task_types == {"Task Phase Transition"}
        assert "Code Validation" not in task_types
    else:
        assert task_types == {"Code Validation"}
        assert "Task Phase Transition" not in task_types


def test_route_preview_prefers_phase_transition_for_successor_task_boundaries(
    capsys,
) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "move task to validation and create successor tasks",
        ],
    )

    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    assert result == 0
    if _has_task_phase_transition_route():
        assert task_types == {"Task Phase Transition"}
    else:
        assert task_types == {"Code Validation"}
        assert "Task Phase Transition" not in task_types
    assert "Task Lifecycle Management" not in task_types


def test_route_preview_returns_agent_assisted_module_suggestions_for_unmatched_requests(
    capsys,
) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "improve the workflow stuff",
        ],
    )

    assert result == 0
    assert payload["selected_route_count"] == 0
    assert payload["activated_intents"] == []
    suggestion_ids = {
        entry["workflow_id"] for entry in payload["assisted_module_suggestions"]
    }
    assert suggestion_ids >= {
        "workflow.workflow_steward",
        "workflow.workflow_system_review",
    }
    assert any(
        "agent-assisted module loading" in warning for warning in payload["warnings"]
    )


def test_route_preview_keeps_generic_no_match_requests_empty(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "make things better",
        ],
    )

    assert result == 0
    assert payload["selected_route_count"] == 0
    assert payload["activated_intents"] == []
    assert payload["assisted_module_suggestions"] == []


def test_route_preview_reports_explicit_activated_intents_for_mixed_requests(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "run an adversarial refactor, standard adherence, and fix loop",
        ],
    )

    assert result == 0
    assert {
        entry["task_type"] for entry in payload["selected_routes"]
    } >= {
        "Code Implementation",
        "Standards Alignment Review",
        "Review Remediation Loop",
    }
    intents = {entry["intent_id"]: entry for entry in payload["activated_intents"]}
    assert intents["route.overlay_adversarial_lens"]["intent_kind"] == "workflow_modifier"
    assert intents["route.overlay_review_remediation_loop_intent"][
        "intent_kind"
    ] == "companion_route"
    assert intents["route.overlay_review_remediation_loop_intent"][
        "exclude_attached_task_types_from_base_scoring"
    ] is True
    assert "route.overlay_review_remediation_intent" not in intents
