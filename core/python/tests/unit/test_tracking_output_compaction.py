from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.decision_tracking import DecisionTrackingSyncService
from watchtower_core.repo_ops.sync.design_tracking import DesignTrackingSyncService
from watchtower_core.repo_ops.sync.initiative_tracking import InitiativeTrackingSyncService
from watchtower_core.repo_ops.sync.prd_tracking import PrdTrackingSyncService
from watchtower_core.repo_ops.sync.task_tracking import TaskTrackingSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_generated_tracking_outputs_omit_old_boilerplate_sections() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    contents = (
        PrdTrackingSyncService(loader).build_document().content,
        DecisionTrackingSyncService(loader).build_document().content,
        DesignTrackingSyncService(loader).build_document().content,
        TaskTrackingSyncService(loader).build_document().content,
        InitiativeTrackingSyncService(loader).build_document().content,
    )

    for content in contents:
        assert "## Summary" not in content
        assert "## Update Rules" not in content
        assert "## References" not in content
        assert "_Updated At: `" in content


def test_generated_tracking_outputs_use_links_and_not_placeholder_rows() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    contents = (
        PrdTrackingSyncService(loader).build_document().content,
        DecisionTrackingSyncService(loader).build_document().content,
        DesignTrackingSyncService(loader).build_document().content,
        TaskTrackingSyncService(loader).build_document().content,
        InitiativeTrackingSyncService(loader).build_document().content,
    )

    for content in contents:
        assert "](/home/j/WatchTowerPlan/" in content
        assert "| `None` | `None` |" not in content
