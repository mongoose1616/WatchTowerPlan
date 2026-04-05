from __future__ import annotations

from types import SimpleNamespace

from tests.unit.route_query_handler_test_support import route_args
from watchtower_host.cli import route_handlers


def test_route_preview_prints_no_match_guidance(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(
                selected_routes=(),
                selected_workflows=(),
                warnings=(),
                assisted_module_suggestions=(),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No route matched the request text strongly enough." in captured.out


def test_route_preview_supports_human_route_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(
                selected_routes=(
                    SimpleNamespace(
                        route_id="route.repository_review",
                        task_type="Repository Review",
                        score=0.9,
                        matched_keywords=("review",),
                        required_workflow_ids=("workflow.repository_review",),
                        required_workflow_paths=("core/workflows/modules/repository_review.md",),
                    ),
                ),
                selected_workflows=(
                    SimpleNamespace(
                        workflow_id="workflow.repository_review",
                        workflow_kind="module",
                        title="Repository Review",
                        doc_path="core/workflows/modules/repository_review.md",
                        phase_type="assessment",
                        task_family="review",
                        composes_module_paths=(),
                    ),
                ),
                warnings=("Prefer a bounded scope.",),
                assisted_module_suggestions=(),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Selected routes:" in captured.out
    assert "workflow.repository_review" in captured.out
    assert "Warning: Prefer a bounded scope." in captured.out


def test_route_preview_supports_role_workflow_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(
                selected_routes=(
                    SimpleNamespace(
                        route_id="route.workflow_system_review",
                        task_type="Workflow System Review",
                        score=0.95,
                        matched_keywords=("workflow system",),
                        required_workflow_ids=(
                            "workflow.workflow_steward",
                            "workflow.workflow_system_review",
                        ),
                        required_workflow_paths=(
                            "core/workflows/roles/workflow_steward.md",
                            "core/workflows/modules/workflow_system_review.md",
                        ),
                    ),
                ),
                selected_workflows=(
                    SimpleNamespace(
                        workflow_id="workflow.workflow_steward",
                        workflow_kind="role",
                        title="Workflow Steward Role",
                        doc_path="core/workflows/roles/workflow_steward.md",
                        phase_type="review",
                        task_family="workflow_governance",
                        composes_module_paths=(
                            "core/workflows/modules/workflow_system_review.md",
                        ),
                    ),
                    SimpleNamespace(
                        workflow_id="workflow.workflow_system_review",
                        workflow_kind="module",
                        title="Workflow System Review Workflow",
                        doc_path="core/workflows/modules/workflow_system_review.md",
                        phase_type="review",
                        task_family="workflow_governance",
                        composes_module_paths=(),
                    ),
                ),
                warnings=(),
                assisted_module_suggestions=(),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Workflow System Review" in captured.out
    assert "workflow.workflow_steward" in captured.out
    assert "workflow.workflow_system_review" in captured.out


def test_route_preview_prints_activated_intents(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(
                selected_routes=(
                    SimpleNamespace(
                        route_id="route.review_remediation_loop",
                        task_type="Review Remediation Loop",
                        score=15,
                        matched_keywords=("fix loop",),
                        required_workflow_ids=("workflow.review_remediation_loop",),
                        required_workflow_paths=(
                            "core/workflows/modules/review_remediation_loop.md",
                        ),
                    ),
                ),
                selected_workflows=(
                    SimpleNamespace(
                        workflow_id="workflow.review_remediation_loop",
                        workflow_kind="module",
                        title="Review Remediation Loop Workflow",
                        doc_path="core/workflows/modules/review_remediation_loop.md",
                        phase_type="execution",
                        task_family="review_remediation",
                        composes_module_paths=(),
                    ),
                ),
                warnings=(),
                activated_intents=(
                    SimpleNamespace(
                        intent_id="route.overlay_review_remediation_loop_intent",
                        title="Review Remediation Loop Intent Overlay",
                        intent_kind="companion_route",
                        matched_trigger_terms=("fix loop",),
                        attached_route_task_types=("Review Remediation Loop",),
                        attached_workflow_ids=(),
                        dominant_route_retention_mode="all_compatible",
                        exclude_attached_task_types_from_base_scoring=True,
                        suppresses_intent_ids=(
                            "route.overlay_review_remediation_intent",
                        ),
                    ),
                ),
                assisted_module_suggestions=(),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Activated intents:" in captured.out
    assert "route.overlay_review_remediation_loop_intent" in captured.out
    assert "retain=all_compatible" in captured.out


def test_route_preview_prints_agent_assisted_module_suggestions(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(
                selected_routes=(),
                selected_workflows=(),
                warnings=(
                    "Advisory workflow suggestions were included for "
                    "agent-assisted module loading.",
                ),
                assisted_module_suggestions=(
                    SimpleNamespace(
                        workflow_id="workflow.workflow_system_review",
                        workflow_kind="module",
                        title="Workflow System Review Workflow",
                        doc_path="core/workflows/modules/workflow_system_review.md",
                        phase_type="review",
                        task_family="workflow_governance",
                        score=17,
                        matched_signals=("workflow system review", "workflow governance"),
                        suggested_load_paths=(
                            "core/workflows/modules/workflow_system_review.md",
                        ),
                    ),
                ),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Advisory workflow suggestions:" in captured.out
    assert "workflow.workflow_system_review" in captured.out
    assert "load=core/workflows/modules/workflow_system_review.md" in captured.out
