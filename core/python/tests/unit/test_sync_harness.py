from pathlib import Path
from types import SimpleNamespace

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import SyncHarness, SyncTargetSpec
from watchtower_host.cli.command_index import (
    COMMAND_INDEX_ARTIFACT_PATH,
    CommandIndexSyncService,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_sync_harness_runs_one_document_target_to_overlay_output(tmp_path: Path) -> None:
    harness = SyncHarness(ControlPlaneLoader(REPO_ROOT))

    result = harness.run_specs(
        (
            SyncTargetSpec(
                target="command-index",
                mode="document",
                artifact_kind="index",
                relative_output_path=COMMAND_INDEX_ARTIFACT_PATH,
                service_factory=CommandIndexSyncService,
            ),
        ),
        output_dir=tmp_path,
    )

    assert result.wrote is True
    assert result.output_dir == str(tmp_path.resolve())
    assert len(result.records) == 1
    record = result.records[0]
    assert record.target == "command-index"
    assert record.record_count > 0
    assert (tmp_path / COMMAND_INDEX_ARTIFACT_PATH).exists()


def test_sync_harness_tracking_details_ignore_retired_planning_count_fields() -> None:
    harness = SyncHarness(ControlPlaneLoader(REPO_ROOT))

    details = harness._tracking_details(
        SimpleNamespace(
            task_count=3,
            open_count=2,
            closed_count=1,
            active_initiative_count=1,
            actionable_task_count=1,
            recent_closed_count=0,
            prd_count=9,
            decision_count=4,
            feature_design_count=5,
            implementation_plan_count=6,
        )
    )

    assert details == {
        "task_count": 3,
        "open_count": 2,
        "closed_count": 1,
        "active_initiative_count": 1,
        "actionable_task_count": 1,
        "recent_closed_count": 0,
    }
