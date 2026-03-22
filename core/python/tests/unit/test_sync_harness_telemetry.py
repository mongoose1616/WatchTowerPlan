from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import SyncHarness, SyncTargetSpec
from watchtower_core.telemetry import create_telemetry_session
from watchtower_host.cli.command_index import (
    COMMAND_INDEX_ARTIFACT_PATH,
    CommandIndexSyncService,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_sync_harness_records_telemetry_for_target_runs(tmp_path: Path) -> None:
    session = create_telemetry_session(
        ControlPlaneLoader(REPO_ROOT),
        ["sync", "command-index"],
        environ={
            "WATCHTOWER_TELEMETRY": "on",
            "WATCHTOWER_TELEMETRY_STDERR": "off",
            "WATCHTOWER_TELEMETRY_DIR": str(tmp_path),
        },
    )
    harness = SyncHarness(ControlPlaneLoader(REPO_ROOT))

    with session.activate():
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
            output_dir=tmp_path / "outputs",
        )
    session.finish(status="ok", exit_code=0)

    assert result.records[0].target == "command-index"
    assert session.output_path is not None
    records = [
        json.loads(line)
        for line in session.output_path.read_text(encoding="utf-8").splitlines()
    ]
    assert any(
        record.get("operation_kind") == "sync_harness"
        and record.get("status") == "ok"
        and record["attributes"]["record_count"] == 1
        for record in records
        if record["record_type"] == "operation_result"
    )
    assert any(
        record.get("operation_kind") == "sync_target"
        and record.get("operation_name") == "command-index"
        and record["attributes"]["record_count"] > 0
        for record in records
        if record["record_type"] == "operation_result"
    )
