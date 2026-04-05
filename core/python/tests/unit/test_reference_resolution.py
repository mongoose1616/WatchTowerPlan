from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import watchtower_core.sync.reference_resolution as reference_resolution
from watchtower_core.sync.cache import PreparedDocumentSyncCache


def test_build_reference_urls_by_path_downgrades_invalid_cached_hits(
    monkeypatch,
    tmp_path: Path,
) -> None:
    loader = SimpleNamespace(repo_root=tmp_path)
    cached_document = {
        "entries": [
            {
                "doc_path": "core/docs/references/example.md",
                "canonical_upstream_urls": ["https://cached.example/spec"],
            }
        ]
    }
    rebuilt_document = {
        "entries": [
            {
                "doc_path": "core/docs/references/example.md",
                "canonical_upstream_urls": ["https://rebuilt.example/spec"],
            }
        ]
    }
    prepared_hit = PreparedDocumentSyncCache(
        cache_status="hit",
        input_file_count=1,
        document=cached_document,
        canonical_output_path=tmp_path / "reference_index.json",
        relative_output_path=reference_resolution.ReferenceIndexSyncService.OUTPUT_PATH,
    )
    build_calls = 0

    monkeypatch.setattr(
        reference_resolution,
        "prepare_document_sync_cache",
        lambda _loader, _service, *, relative_output_path: prepared_hit,
    )

    def _validate(
        _loader: object,
        prepared: PreparedDocumentSyncCache,
    ) -> PreparedDocumentSyncCache:
        return replace(prepared, cache_status="miss", document=None)

    monkeypatch.setattr(
        reference_resolution,
        "validate_prepared_document_sync_cache",
        _validate,
    )

    def _build_document(
        self: reference_resolution.ReferenceIndexSyncService,
    ) -> dict[str, object]:
        nonlocal build_calls
        build_calls += 1
        return rebuilt_document

    monkeypatch.setattr(
        reference_resolution.ReferenceIndexSyncService,
        "build_document",
        _build_document,
    )

    result = reference_resolution.build_reference_urls_by_path(loader)

    assert result == {
        "core/docs/references/example.md": ("https://rebuilt.example/spec",),
    }
    assert build_calls == 1
