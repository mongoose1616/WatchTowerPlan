from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.routing import RoutingEngine

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_routing_engine_selects_routes_for_explicit_task_type() -> None:
    result = RoutingEngine(ControlPlaneLoader(REPO_ROOT)).select_for_task_type(
        "Code Implementation"
    )

    assert [route.route_id for route in result.selected_routes] == ["route.code_implementation"]
    assert any(
        workflow.workflow_id == "workflow.code_implementation"
        for workflow in result.selected_workflows
    )


def test_routing_engine_selects_routes_for_request_text() -> None:
    result = RoutingEngine(ControlPlaneLoader(REPO_ROOT)).select_for_request(
        "review code and audit diff"
    )

    assert result.selected_routes
    assert result.selected_routes[0].route_id == "route.code_review"
    assert any(
        workflow.workflow_id == "workflow.code_review" for workflow in result.selected_workflows
    )


def test_routing_engine_fails_closed_on_ambiguous_selection_inputs() -> None:
    engine = RoutingEngine(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValueError, match="exactly one"):
        engine.select()

    with pytest.raises(ValueError, match="exactly one"):
        engine.select(request_text="review code", task_type="Code Review")


def test_routing_engine_returns_assisted_module_suggestions_for_unmatched_requests() -> None:
    result = RoutingEngine(ControlPlaneLoader(REPO_ROOT)).select_for_request(
        "improve the workflow stuff"
    )

    assert result.selected_routes == ()
    assert {
        suggestion.workflow_id for suggestion in result.assisted_module_suggestions
    } >= {
        "workflow.workflow_steward",
        "workflow.workflow_system_review",
    }
