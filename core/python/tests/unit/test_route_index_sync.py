from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query.routes import RoutePreviewService
from watchtower_core.sync.route_index import RouteIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _route_entry_map(document: dict[str, object]) -> dict[str, dict[str, object]]:
    entries = document["entries"]
    assert isinstance(entries, list)
    return {
        entry["route_id"]: entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("route_id"), str)
    }


def _route_task_types(loader: ControlPlaneLoader) -> dict[str, str]:
    return {
        entry.route_id: entry.task_type
        for entry in loader.load_route_index().entries
    }


def test_route_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RouteIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    route_entries = _route_entry_map(document)
    assert isinstance(entries, list)
    assert any(
        entry["route_id"] == "route.repository_review"
        and entry["task_type"] == "Repository Review"
        and "workflow.repository_review" in entry["required_workflow_ids"]
        and "core/workflows/modules/repository_review.md" in entry["required_workflow_paths"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.documentation_review"
        and entry["task_type"] == "Documentation Review"
        and "workflow.current_state_inspection" in entry["required_workflow_ids"]
        and "workflow.documentation_review" in entry["required_workflow_ids"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.workflow_system_review"
        and entry["task_type"] == "Workflow System Review"
        and "workflow.workflow_steward" in entry["required_workflow_ids"]
        and "workflow.workflow_system_review" in entry["required_workflow_ids"]
        and "workflow index" in entry["trigger_keywords"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.documentation_refresh"
        and entry["task_type"] == "Documentation Refresh"
        and "workflow.current_state_inspection" in entry["required_workflow_ids"]
        and "workflow.documentation_refresh" in entry["required_workflow_ids"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.documentation_implementation_reconciliation"
        and "reconcile command docs with current cli behavior" in entry["trigger_keywords"]
        and "reconcile workflow docs with current cli behavior" in entry["trigger_keywords"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.governed_artifact_reconciliation"
        and "reconcile schema backed indexes examples and validators" in entry["trigger_keywords"]
        for entry in entries
    )
    task_phase_transition = route_entries.get("route.task_phase_transition")
    if task_phase_transition is not None:
        assert "create successor tasks" in task_phase_transition["trigger_keywords"]
        assert "successor tasks" in task_phase_transition["trigger_keywords"]
        assert (
            "create successor tasks during handoff"
            in task_phase_transition["trigger_keywords"]
        )
    planning_authoring = route_entries.get("route.planning_authoring")
    if planning_authoring is not None:
        assert planning_authoring["task_type"] == "Planning Authoring"
        assert "workflow.planning_author" in planning_authoring["required_workflow_ids"]
        assert (
            "workflow.implementation_slice_planning"
            in planning_authoring["required_workflow_ids"]
        )
    task_coordination = route_entries.get("route.task_coordination")
    if task_coordination is not None:
        assert task_coordination["task_type"] == "Task Coordination"
        assert "workflow.task_coordinator" in task_coordination["required_workflow_ids"]
        assert "workflow.github_task_sync" in task_coordination["required_workflow_ids"]
    traceability_governance = route_entries.get("route.traceability_governance")
    if traceability_governance is not None:
        assert traceability_governance["task_type"] == "Traceability Governance"
        assert (
            "workflow.traceability_steward"
            in traceability_governance["required_workflow_ids"]
        )
        assert (
            "workflow.initiative_closeout"
            in traceability_governance["required_workflow_ids"]
        )
    assert any(
        entry["route_id"] == "route.foundations_alignment_review"
        and entry["task_type"] == "Foundations Alignment Review"
        and "workflow.foundations_context_review" in entry["required_workflow_ids"]
        and "workflow.documentation_refresh" in entry["required_workflow_ids"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.commit_closeout"
        and "workflow.commit_closeout" in entry["required_workflow_ids"]
        and "workflow.task_handoff_review" not in entry["required_workflow_ids"]
        for entry in entries
    )
    assert any(
        entry["route_id"] == "route.test_suite_optimization"
        and entry["task_type"] == "Test Suite Optimization"
        and "slow tests" in entry["trigger_keywords"]
        and "workflow.test_suite_optimization" in entry["required_workflow_ids"]
        and "workflow.code_validation" in entry["required_workflow_ids"]
        for entry in entries
    )


def test_route_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RouteIndexSyncService(loader)
    output_path = tmp_path / "route_index.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.routes"


def test_route_index_sync_ignores_non_route_tables(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    core_workflows_dir = repo_root / "core/workflows"
    core_modules_dir = core_workflows_dir / "modules"
    pack_workflows_dir = repo_root / "packs/example/workflows"
    core_modules_dir.mkdir(parents=True)
    (core_modules_dir / "core.md").write_text("# Core\n", encoding="utf-8")
    (core_modules_dir / "task_scope_definition.md").write_text(
        "# Task Scope Definition\n",
        encoding="utf-8",
    )
    (core_workflows_dir / "ROUTING_TABLE.md").write_text(
        "\n".join(
            [
                "# Core Workflow Routing Table",
                "",
                "## Reconciliation Quick Guide",
                "",
                "| Primary Drift Boundary | Preferred Route | Typical Surfaces |",
                "|---|---|---|",
                "| docs versus code | `Documentation-Implementation Reconciliation` | docs |",
                "",
                "| Task Type | Trigger Keywords (Examples) | Required Workflows |",
                "|---|---|---|",
                "| Example Route | example task | `core/workflows/modules/core.md`, "
                "`core/workflows/modules/task_scope_definition.md` |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    pack_workflows_dir.mkdir(parents=True)
    (pack_workflows_dir / "ROUTING_TABLE.md").write_text(
        "\n".join(
            [
                "# Example Pack Workflow Routing Table",
                "",
                "| Task Type | Trigger Keywords (Examples) | Required Workflows |",
                "|---|---|---|",
                "| Pack Route | pack task | `core/workflows/modules/core.md` |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    service = RouteIndexSyncService(ControlPlaneLoader(REPO_ROOT))
    service._repo_root = repo_root

    document = service.build_document()

    assert document["entries"] == [
        {
            "route_id": "route.example_route",
            "task_type": "Example Route",
            "trigger_keywords": ["example task"],
            "required_workflow_ids": [
                "workflow.core",
                "workflow.task_scope_definition",
            ],
            "required_workflow_paths": [
                "core/workflows/modules/core.md",
                "core/workflows/modules/task_scope_definition.md",
            ],
        },
        {
            "route_id": "route.pack_route",
            "task_type": "Pack Route",
            "trigger_keywords": ["pack task"],
            "required_workflow_ids": ["workflow.core"],
            "required_workflow_paths": [
                "core/workflows/modules/core.md",
            ],
        },
    ]


def test_route_index_sync_normalizes_root_relative_workflow_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    core_workflows_dir = repo_root / "core/workflows"
    core_modules_dir = core_workflows_dir / "modules"
    core_modules_dir.mkdir(parents=True)
    (core_modules_dir / "core.md").write_text("# Core\n", encoding="utf-8")
    (core_modules_dir / "code_validation.md").write_text(
        "# Code Validation\n",
        encoding="utf-8",
    )
    (core_workflows_dir / "ROUTING_TABLE.md").write_text(
        "\n".join(
            [
                "# Core Workflow Routing Table",
                "",
                "| Task Type | Trigger Keywords (Examples) | Required Workflows |",
                "|---|---|---|",
                "| Root Relative Route | normalize root relative | "
                "`/core/workflows/modules/core.md`, "
                "`/core/workflows/modules/code_validation.md` |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    service = RouteIndexSyncService(ControlPlaneLoader(REPO_ROOT))
    service._repo_root = repo_root

    document = service.build_document()

    assert document["entries"] == [
        {
            "route_id": "route.root_relative_route",
            "task_type": "Root Relative Route",
            "trigger_keywords": ["normalize root relative"],
            "required_workflow_ids": [
                "workflow.core",
                "workflow.code_validation",
            ],
            "required_workflow_paths": [
                "core/workflows/modules/core.md",
                "core/workflows/modules/code_validation.md",
            ],
        }
    ]


def test_route_index_sync_accepts_role_root_workflow_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    core_workflows_dir = repo_root / "core/workflows"
    core_modules_dir = core_workflows_dir / "modules"
    core_roles_dir = core_workflows_dir / "roles"
    core_modules_dir.mkdir(parents=True)
    core_roles_dir.mkdir(parents=True)
    (core_modules_dir / "core.md").write_text("# Core\n", encoding="utf-8")
    (core_roles_dir / "architecture_reviewer.md").write_text(
        "# Architecture Reviewer Role\n",
        encoding="utf-8",
    )
    (core_workflows_dir / "ROUTING_TABLE.md").write_text(
        "\n".join(
            [
                "# Core Workflow Routing Table",
                "",
                "| Task Type | Trigger Keywords (Examples) | Required Workflows |",
                "|---|---|---|",
                "| Architecture Review | architecture review | "
                "`/core/workflows/modules/core.md`, "
                "`/core/workflows/roles/architecture_reviewer.md` |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    service = RouteIndexSyncService(ControlPlaneLoader(REPO_ROOT))
    service._repo_root = repo_root

    document = service.build_document()

    assert document["entries"] == [
        {
            "route_id": "route.architecture_review",
            "task_type": "Architecture Review",
            "trigger_keywords": ["architecture review"],
            "required_workflow_ids": [
                "workflow.core",
                "workflow.architecture_reviewer",
            ],
            "required_workflow_paths": [
                "core/workflows/modules/core.md",
                "core/workflows/roles/architecture_reviewer.md",
            ],
        }
    ]


def test_route_preview_service_scores_request_text() -> None:
    service = RoutePreviewService(ControlPlaneLoader(REPO_ROOT))

    result = service.preview(request_text="review code and finalize commit")

    task_types = {match.task_type for match in result.selected_routes}
    workflow_ids = {workflow.workflow_id for workflow in result.selected_workflows}
    assert "Code Review" in task_types
    assert "Commit Closeout" in task_types
    assert "workflow.code_review" in workflow_ids
    assert "workflow.commit_closeout" in workflow_ids


def test_route_preview_service_keeps_commit_closeout_as_companion_route() -> None:
    service = RoutePreviewService(ControlPlaneLoader(REPO_ROOT))

    result = service.preview(
        request_text="adversarial refactor and optimization and commit"
    )

    task_types = {match.task_type for match in result.selected_routes}
    workflow_ids = {workflow.workflow_id for workflow in result.selected_workflows}
    assert task_types == {"Code Implementation", "Commit Closeout"}
    assert "workflow.code_implementation" in workflow_ids
    assert "workflow.commit_closeout" in workflow_ids
    assert "workflow.adversarial_reviewer" in workflow_ids


def test_route_preview_service_keeps_closeout_and_overlay_routes_flexible() -> None:
    service = RoutePreviewService(ControlPlaneLoader(REPO_ROOT))
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
        result = service.preview(request_text=request_text)
        assert expected["routes"].issubset(
            {match.task_type for match in result.selected_routes}
        )
        assert expected["workflows"].issubset(
            {workflow.workflow_id for workflow in result.selected_workflows}
        )


def test_route_preview_service_matches_realistic_maintenance_request() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)
    route_task_types = _route_task_types(loader)

    result = service.preview(
        request_text=(
            "review /external/repository/report and fix the valid issues with planning, "
            "tasks, validation, and commits"
        )
    )

    task_types = {match.task_type for match in result.selected_routes}
    workflow_ids = {workflow.workflow_id for workflow in result.selected_workflows}
    assert route_task_types["route.review_remediation"] in task_types
    assert route_task_types["route.repository_review"] not in task_types
    assert route_task_types["route.code_validation"] in task_types
    assert route_task_types["route.commit_closeout"] in task_types
    if "route.task_lifecycle_management" in route_task_types:
        assert route_task_types["route.task_lifecycle_management"] in task_types
    else:
        assert "Task Lifecycle Management" not in task_types
    assert "Code Review" not in task_types
    assert "Task Phase Transition" not in task_types
    assert "workflow.review_remediation" in workflow_ids
    assert "workflow.repository_review" not in workflow_ids
    assert "workflow.code_validation" in workflow_ids
    assert "workflow.commit_closeout" in workflow_ids
    if "route.task_lifecycle_management" in route_task_types:
        assert "workflow.task_lifecycle_management" in workflow_ids
    else:
        assert "workflow.task_lifecycle_management" not in workflow_ids


def test_route_preview_service_merges_adversarial_fix_loops() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)
    route_task_types = _route_task_types(loader)

    result = service.preview(request_text="do an adversarial and fix loop")

    task_types = {match.task_type for match in result.selected_routes}
    assert route_task_types["route.adversarial_repository_review"] not in task_types
    assert route_task_types["route.review_remediation_loop"] in task_types
    assert {workflow.workflow_id for workflow in result.selected_workflows} >= {
        "workflow.adversarial_reviewer",
        "workflow.review_remediation",
        "workflow.review_remediation_loop",
        "workflow.code_validation",
    }
    assert "workflow.repository_review" not in {
        workflow.workflow_id for workflow in result.selected_workflows
    }
    assert result.warnings == ()


def test_route_preview_service_keeps_adversarial_mentions_out_of_doc_reviews() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)
    route_task_types = _route_task_types(loader)

    result = service.preview(
        request_text="do a documentation review of adversarial examples references"
    )

    assert {match.task_type for match in result.selected_routes} == {
        route_task_types["route.documentation_review"]
    }
    assert "workflow.adversarial_reviewer" not in {
        workflow.workflow_id for workflow in result.selected_workflows
    }


def test_route_preview_service_pairs_adversarial_role_with_review_and_fix_routes() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)
    route_task_types = _route_task_types(loader)
    expectations = {
        "run an adversarial code review": {
            "routes": {
                route_task_types["route.code_review"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.code_review",
            },
        },
        "run an adversarial documentation review": {
            "routes": {
                route_task_types["route.documentation_review"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.documentation_review",
            },
        },
        "run an adversarial workflow system review": {
            "routes": {
                route_task_types["route.workflow_system_review"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.workflow_steward",
                "workflow.workflow_system_review",
            },
        },
        "run an adversarial standards audit": {
            "routes": {
                route_task_types["route.standards_alignment_review"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.standards_alignment_review",
            },
        },
        "run an adversarial validation harness review": {
            "routes": {
                route_task_types["route.validation_harness_review"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.validation_harness_review",
            },
        },
        "i want a adversarial telemetry, benchmark review and fix": {
            "routes": {
                route_task_types["route.performance_benchmarking"],
                route_task_types["route.review_remediation"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.performance_benchmarking",
                "workflow.review_remediation",
            },
        },
        "i want a adversarial refactor and optimization": {
            "routes": {
                route_task_types["route.code_implementation"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.code_implementation",
            },
        },
        "do an adversarial stale test cleanup": {
            "routes": {
                route_task_types["route.test_suite_optimization"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.test_suite_optimization",
            },
        },
        "i want a adversarial project coherence and fix loop": {
            "routes": {
                route_task_types["route.repository_review"],
                route_task_types["route.review_remediation_loop"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.repository_review",
                "workflow.review_remediation_loop",
            },
        },
        "do an adversarial repository review and fix loop": {
            "routes": {
                route_task_types["route.adversarial_repository_review"],
                route_task_types["route.review_remediation_loop"],
            },
            "workflows": {
                "workflow.adversarial_reviewer",
                "workflow.repository_review",
                "workflow.review_remediation_loop",
            },
        },
    }

    for request_text, expected in expectations.items():
        result = service.preview(request_text=request_text)
        task_types = {match.task_type for match in result.selected_routes}
        workflow_ids = {workflow.workflow_id for workflow in result.selected_workflows}
        assert expected["routes"].issubset(task_types)
        if request_text != "do an adversarial repository review and fix loop":
            assert route_task_types["route.adversarial_repository_review"] not in task_types
        if request_text == "do an adversarial repository review and fix loop":
            assert route_task_types["route.repository_review"] not in task_types
        assert expected["workflows"].issubset(workflow_ids)


def test_route_preview_service_pairs_fix_loops_with_documentation_and_repository_reviews() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)
    route_task_types = _route_task_types(loader)
    expectations = {
        "i want a documentation and fix loop": {
            route_task_types["route.documentation_review"],
            route_task_types["route.review_remediation_loop"],
        },
        "i want a docs audit and fix loop": {
            route_task_types["route.documentation_review"],
            route_task_types["route.review_remediation_loop"],
        },
        "i want a project coherence and fix loop": {
            route_task_types["route.repository_review"],
            route_task_types["route.review_remediation_loop"],
        },
    }

    for request_text, expected_routes in expectations.items():
        result = service.preview(request_text=request_text)
        assert expected_routes.issubset(
            {match.task_type for match in result.selected_routes}
        )


def test_route_preview_service_keeps_fix_loops_specific_when_loop_route_is_selected() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)

    result = service.preview(
        request_text="fix the findings from this review and rerun the same review until clean"
    )

    assert {match.task_type for match in result.selected_routes} == {
        "Review Remediation Loop"
    }


def test_route_preview_service_matches_workflow_review_regression_requests() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RoutePreviewService(loader)
    route_task_types = _route_task_types(loader)
    expectations = {
        "Inspect this patch for regressions, maintainability risks, and release issues.": {
            route_task_types["route.code_review"]
        },
        "Review report changes for release risk review.": {
            route_task_types["route.code_review"]
        },
        "Perform a whole-repository health assessment and standards audit.": {
            route_task_types["route.repository_review"]
        },
        "Review the workflow docs against the current CLI behavior and lookup surfaces.": {
            route_task_types["route.documentation_implementation_reconciliation"]
        },
        "Reconcile command docs with current cli behavior.": {
            route_task_types["route.documentation_implementation_reconciliation"]
        },
        "Do a documentation review of the command docs.": {
            route_task_types["route.documentation_review"]
        },
        "Do a standards review of the workflow standards.": {
            route_task_types["route.documentation_review"]
        },
        "Audit the workflow system across core and plan.": {
            route_task_types["route.workflow_system_review"]
        },
        "Verify that the workflow indexes, schemas, and registry stay aligned.": {
            route_task_types["route.governed_artifact_reconciliation"]
        },
        "Reconcile schema-backed indexes examples and validators for one artifact family.": {
            route_task_types["route.governed_artifact_reconciliation"]
        },
        "Review workflow index schema registry alignment.": {
            route_task_types["route.governed_artifact_reconciliation"]
        },
        "Perform schema registry alignment review.": {
            route_task_types["route.governed_artifact_reconciliation"]
        },
        "Make the design and standards docs cohesive with the foundations documents.": {
            route_task_types["route.foundations_alignment_review"]
        },
        "Refresh the workflow guidance so it stays aligned with the foundations docs.": {
            route_task_types["route.documentation_refresh"],
            route_task_types["route.foundations_alignment_review"],
        },
            (
                "Review one last time /external/repository/report and the files inside for "
                "final review. The loop will be: read one file, verify the issues that "
                "are captured are accurate and still validate, if they are, start as "
                "many initiative as needed to fix it, use the standard end to end task "
                "cycle."
            ): {
                route_task_types["route.review_remediation_loop"],
            },
        "build check": {route_task_types["route.code_validation"]},
        "stale command docs": {
            route_task_types["route.documentation_implementation_reconciliation"]
        },
        (
            "Author the full planning package from initiative brief through design "
            "record and implementation slice."
        ): {
            *(
                [route_task_types["route.planning_authoring"]]
                if "route.planning_authoring" in route_task_types
                else [
                    route_task_types[route_id]
                    for route_id in (
                        "route.design_record_planning",
                        "route.implementation_slice_planning",
                    )
                    if route_id in route_task_types
                ]
            )
        },
        "initiative closeout": (
            {route_task_types["route.initiative_closeout"]}
            if "route.initiative_closeout" in route_task_types
            else set()
        ),
        "Coordinate task lifecycle, handoff, and github sync for this initiative.": {
            *(
                route_task_types[route_id]
                for route_id in ("route.task_coordination", "route.github_task_sync")
                if route_id in route_task_types
            )
        },
        "github task sync": (
            {route_task_types["route.github_task_sync"]}
            if "route.github_task_sync" in route_task_types
            else set()
        ),
        "hand off task": (
            {route_task_types["route.task_phase_transition"]}
            if "route.task_phase_transition" in route_task_types
            else set()
        ),
        "Hand off this task from implementation to validation and create successor tasks.": {
            *(
                [route_task_types["route.task_phase_transition"]]
                if "route.task_phase_transition" in route_task_types
                else [route_task_types["route.code_validation"]]
            )
        },
        "Move task to validation and create successor tasks.": {
            *(
                [route_task_types["route.task_phase_transition"]]
                if "route.task_phase_transition" in route_task_types
                else [route_task_types["route.code_validation"]]
            )
        },
    }

    if "route.implementation_slice_planning" in route_task_types:
        expectations["implementation slice"] = {
            route_task_types["route.implementation_slice_planning"]
        }
    expectations[
        (
            "Review one last time /external/repository/report and the files inside for "
            "final review. The loop will be: read one file, verify the issues that "
            "are captured are accurate and still validate, if they are, start as "
            "many initiative as needed to fix it, use the standard end to end task "
            "cycle."
        )
    ] = {
        route_task_types["route.review_remediation_loop"],
        route_task_types["route.task_lifecycle_management"],
    }
    traceability_expectations = {
        *(
            [route_task_types["route.traceability_governance"]]
            if "route.traceability_governance" in route_task_types
            else [
                route_task_types[route_id]
                for route_id in (
                    "route.traceability_reconciliation",
                    "route.acceptance_and_evidence_reconciliation",
                )
                if route_id in route_task_types
            ]
        )
    }
    if traceability_expectations:
        expectations[
            (
                "Need traceability governance across decision capture, traceability "
                "reconciliation, acceptance evidence, and closeout."
            )
        ] = traceability_expectations

    for request_text, expected_task_types in expectations.items():
        result = service.preview(request_text=request_text)
        assert {match.task_type for match in result.selected_routes} == expected_task_types


def test_route_preview_service_supports_explicit_task_type() -> None:
    service = RoutePreviewService(ControlPlaneLoader(REPO_ROOT))

    result = service.preview(task_type="Repository Review")

    assert len(result.selected_routes) == 1
    assert result.selected_routes[0].task_type == "Repository Review"
    assert any(
        workflow.workflow_id == "workflow.repository_review"
        for workflow in result.selected_workflows
    )
