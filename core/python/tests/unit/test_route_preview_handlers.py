from __future__ import annotations

from types import SimpleNamespace

from tests.unit.route_query_handler_test_support import route_args
from watchtower_host.cli import route_handlers


def test_route_preview_prints_no_match_guidance(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(selected_routes=(), selected_workflows=(), warnings=())

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
                        title="Repository Review",
                        doc_path="core/workflows/modules/repository_review.md",
                        phase_type="assessment",
                        task_family="review",
                    ),
                ),
                warnings=("Prefer a bounded scope.",),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Selected routes:" in captured.out
    assert "workflow.repository_review" in captured.out
    assert "Warning: Prefer a bounded scope." in captured.out
