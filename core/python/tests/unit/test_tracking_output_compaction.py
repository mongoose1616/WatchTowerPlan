from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.coordination_tracking import CoordinationTrackingSyncService
from watchtower_core.repo_ops.sync.decision_tracking import DecisionTrackingSyncService
from watchtower_core.repo_ops.sync.design_tracking import DesignTrackingSyncService
from watchtower_core.repo_ops.sync.initiative_tracking import InitiativeTrackingSyncService
from watchtower_core.repo_ops.sync.prd_tracking import PrdTrackingSyncService
from watchtower_core.repo_ops.sync.task_tracking import TaskTrackingSyncService
from watchtower_core.repo_ops.sync.tracking_common import (
    terminal_initiative_status_counts_for_trace_ids,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_generated_tracking_outputs_omit_old_boilerplate_sections() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    contents = (
        PrdTrackingSyncService(loader).build_document().content,
        DecisionTrackingSyncService(loader).build_document().content,
        DesignTrackingSyncService(loader).build_document().content,
        TaskTrackingSyncService(loader).build_document().content,
        InitiativeTrackingSyncService(loader).build_document().content,
        CoordinationTrackingSyncService(loader).build_document().content,
    )

    for content in contents:
        assert "## Summary" not in content
        assert "## Update Rules" not in content
        assert "## References" not in content
        assert "_Updated At: `" in content


def test_generated_tracking_outputs_use_links_and_not_placeholder_rows() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    prd_content = PrdTrackingSyncService(loader).build_document().content
    decision_content = DecisionTrackingSyncService(loader).build_document().content
    design_content = DesignTrackingSyncService(loader).build_document().content
    task_content = TaskTrackingSyncService(loader).build_document().content
    initiative_content = InitiativeTrackingSyncService(loader).build_document().content
    coordination_content = CoordinationTrackingSyncService(loader).build_document().content

    for content in (
        prd_content,
        decision_content,
        design_content,
        task_content,
        initiative_content,
        coordination_content,
    ):
        assert "| `None` | `None` |" not in content

    for content in (task_content, initiative_content, coordination_content):
        assert "](/home/j/WatchTowerPlan/" in content

    assert "No active PRDs" in prd_content or "](/home/j/WatchTowerPlan/" in prd_content
    assert (
        "No active decisions" in decision_content
        or "](/home/j/WatchTowerPlan/" in decision_content
    )
    assert (
        "No active feature designs" in design_content
        or "](/home/j/WatchTowerPlan/" in design_content
    )


def test_design_tracking_uses_neutral_source_label() -> None:
    content = DesignTrackingSyncService(ControlPlaneLoader(REPO_ROOT)).build_document().content

    assert "Source Designs" not in content
    assert "Sources" in content or "No active implementation plans" in content


def test_generated_tracking_outputs_use_active_first_sections_and_history_hints() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    prd_content = PrdTrackingSyncService(loader).build_document().content
    decision_content = DecisionTrackingSyncService(loader).build_document().content
    design_content = DesignTrackingSyncService(loader).build_document().content
    task_content = TaskTrackingSyncService(loader).build_document().content

    assert "## Active PRDs" in prd_content
    assert "## Terminal History" in prd_content
    assert "query planning --trace-id <trace_id>" in prd_content

    assert "## Active Decisions" in decision_content
    assert "## Terminal History" in decision_content
    assert "query decisions --trace-id <trace_id>" in decision_content

    assert "## Active Feature Designs" in design_content
    assert "## Active Implementation Plans" in design_content
    assert "## Terminal History" in design_content
    assert "query designs --trace-id <trace_id>" in design_content

    assert "## Closed Task Summary" in task_content
    assert "## Recently Closed Tasks" in task_content
    assert "query tasks --task-status done" in task_content
    assert "query tasks --task-status cancelled" in task_content


def test_terminal_history_summary_counts_unique_traces() -> None:
    counts = terminal_initiative_status_counts_for_trace_ids(
        (
            "trace.completed.alpha",
            "trace.completed.alpha",
            "trace.completed.beta",
            "trace.cancelled.gamma",
            "trace.active.delta",
        ),
        {
            "trace.completed.alpha": "completed",
            "trace.completed.beta": "completed",
            "trace.cancelled.gamma": "cancelled",
            "trace.active.delta": "active",
        },
    )

    assert counts == (("completed", 2), ("cancelled", 1))
