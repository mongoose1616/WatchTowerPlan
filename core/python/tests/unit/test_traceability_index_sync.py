from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import TraceabilityIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_traceability_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = TraceabilityIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["trace_id"] == "trace.command_documentation_and_lookup"
        for entry in entries
    )
    assert any(entry["trace_id"] == "trace.core_python_foundation" for entry in entries)


def test_traceability_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = TraceabilityIndexSyncService(loader)
    output_path = tmp_path / "traceability_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.traceability"
