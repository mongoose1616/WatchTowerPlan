from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import PrdIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_prd_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = PrdIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["prd_id"] == "prd.core_python_foundation"
        and entry["uses_internal_references"] is True
        and "internal_reference_paths" in entry
        for entry in entries
    )


def test_prd_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = PrdIndexSyncService(loader)
    output_path = tmp_path / "prd_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.prds"
