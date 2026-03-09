from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import ReferenceIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_reference_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ReferenceIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["reference_id"] == "ref.uv"
        and entry["uses_external_references"] is True
        and "canonical_upstream_urls" in entry
        for entry in entries
    )
    assert any(
        entry["reference_id"] == "ref.github_collaboration"
        and "docs/standards/governance/github_collaboration_standard.md"
        in entry.get("applied_by_paths", [])
        for entry in entries
    )


def test_reference_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ReferenceIndexSyncService(loader)
    output_path = tmp_path / "reference_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.references"
