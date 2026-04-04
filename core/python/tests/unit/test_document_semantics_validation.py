from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.cache import PreparedDocumentSyncCache
from watchtower_core.sync.reference_index import ReferenceIndexSyncService
from watchtower_core.validation import document_semantics as document_semantics_module
from watchtower_core.validation.document_semantics import (
    CoreDocumentSemanticsValidationService,
)


def test_reference_index_failures_are_cached_across_validation_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = CoreDocumentSemanticsValidationService(ControlPlaneLoader())
    call_count = 0

    monkeypatch.setattr(
        document_semantics_module,
        "prepare_document_sync_cache",
        lambda *_args, **_kwargs: PreparedDocumentSyncCache(
            cache_status="miss",
            input_file_count=0,
            document=None,
            canonical_output_path=Path("unused"),
            relative_output_path=ReferenceIndexSyncService.OUTPUT_PATH,
        ),
    )

    def _raise_invalid_reference(*_args: Any, **_kwargs: Any) -> dict[str, object]:
        nonlocal call_count
        call_count += 1
        raise ValueError("invalid reference document")

    monkeypatch.setattr(
        ReferenceIndexSyncService,
        "build_document",
        _raise_invalid_reference,
    )

    first = service.validate("core/docs/references/adr_guidance_reference.md")
    second = service.validate("core/docs/references/commonmark_reference.md")

    assert first.passed is False
    assert second.passed is False
    assert first.issues[0].message == "invalid reference document"
    assert second.issues[0].message == "invalid reference document"
    assert call_count == 1
