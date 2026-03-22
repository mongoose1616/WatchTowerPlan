from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.sync.repository_paths import RepositoryPathIndexSyncService


def test_repository_path_index_sync_filters_stale_related_paths(tmp_path: Path) -> None:
    (tmp_path / "core/python/src").mkdir(parents=True)
    (tmp_path / "core/python/tests").mkdir(parents=True)
    (tmp_path / "core/control_plane/indexes/repository_paths").mkdir(parents=True)

    (tmp_path / "core/python/README.md").write_text(
        "\n".join(
            [
                "# `core/python`",
                "",
                "## Paths",
                "| Path | Description |",
                "|---|---|",
                "| `core/python/src/` | Holds Python source files. |",
                "| `core/python/tests/` | Holds Python tests. |",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    existing_index = {
        "$schema": "urn:watchtower:schema:artifacts:indexes:repository-path-index:v1",
        "id": "index.repository_paths",
        "title": "Repository Path Index",
        "status": "active",
        "coverage_mode": "entrypoints",
        "root_path": ".",
        "entries": [
            {
                "path": "core/python/tests/",
                "kind": "directory",
                "surface_kind": "python_tests",
                "summary": "Holds Python tests.",
                "parent_path": "core/python/",
                "maturity": "supporting",
                "priority": "medium",
                "audience_hint": "maintainer",
                "related_paths": [
                    "core/python/src/",
                    "core/control_plane/examples/",
                ],
            }
        ],
    }
    (
        tmp_path / "core/control_plane/indexes/repository_paths/repository_path_index.json"
    ).write_text(f"{json.dumps(existing_index, indent=2)}\n", encoding="utf-8")

    class _FakeLoader:
        def __init__(self, repo_root: Path) -> None:
            self.repo_root = repo_root

        def load_json_object(self, relative_path: str) -> dict[str, object]:
            return json.loads((self.repo_root / relative_path).read_text(encoding="utf-8"))

    document = RepositoryPathIndexSyncService(_FakeLoader(tmp_path)).build_document()

    entry = next(item for item in document["entries"] if item["path"] == "core/python/tests/")
    assert entry["related_paths"] == ["core/python/src/"]
