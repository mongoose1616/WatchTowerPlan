from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import StandardIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_standard_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = StandardIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["standard_id"] == "std.governance.github_collaboration"
        and entry["uses_external_references"] is True
        and "docs/references/github_collaboration_reference.md"
        in entry.get("reference_doc_paths", [])
        for entry in entries
    )


def test_standard_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = StandardIndexSyncService(loader)
    output_path = tmp_path / "standard_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.standards"
