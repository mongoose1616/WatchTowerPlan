from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import GitHubTaskSyncParams, GitHubTaskSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_github_task_sync_dry_run_includes_managed_labels() -> None:
    service = GitHubTaskSyncService(ControlPlaneLoader(REPO_ROOT))

    result = service.sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            task_ids=("task.local_task_tracking.github_sync.001",),
        ),
        write=False,
    )

    assert result.wrote is False
    assert result.synced_task_count == 0
    assert len(result.records) == 1
    assert result.records[0].labels == (
        "source:watchtower",
        "kind:feature",
        "status:done",
        "priority:medium",
    )


def test_github_task_sync_dry_run_can_disable_managed_labels() -> None:
    service = GitHubTaskSyncService(ControlPlaneLoader(REPO_ROOT))

    result = service.sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            task_ids=("task.local_task_tracking.github_sync.001",),
            sync_labels=False,
        ),
        write=False,
    )

    assert result.wrote is False
    assert len(result.records) == 1
    assert result.records[0].labels == ()
