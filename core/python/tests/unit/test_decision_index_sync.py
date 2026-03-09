from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import DecisionIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_decision_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = DecisionIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["decision_id"] == "decision.core_python_workspace_root"
        and entry["uses_internal_references"] is True
        for entry in entries
    )


def test_decision_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = DecisionIndexSyncService(loader)
    output_path = tmp_path / "decision_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.decisions"
