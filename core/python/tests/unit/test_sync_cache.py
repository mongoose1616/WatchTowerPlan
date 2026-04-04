from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from jsonschema import ValidationError

from watchtower_core.control_plane.workspace import WorkspaceConfig
from watchtower_core.sync.cache import (
    SYNC_CACHE_FALLBACK_ROOT,
    SyncCacheInputSpec,
    finalize_document_sync_cache,
    prepare_document_sync_cache,
    resolve_sync_cache_root,
    validate_prepared_document_sync_cache,
)


class _FakeSchemaStore:
    def __init__(self) -> None:
        self.fail_validation = False

    def validate_instance(self, document: dict[str, object]) -> None:
        if self.fail_validation:
            raise ValidationError("synthetic cache validation failure")


class _FakeLoader:
    def __init__(self, repo_root: Path, *, machine_root: str = "fixture_pack/.wt") -> None:
        self.repo_root = repo_root
        self.workspace_config = WorkspaceConfig(
            repo_root=repo_root,
            control_plane_root=repo_root / "core" / "control_plane",
            python_workspace_root=repo_root / "core" / "python",
        )
        self.schema_store = _FakeSchemaStore()
        self.active_pack_settings_path = "fixture_pack/.wt/manifests/pack_settings.json"
        self._machine_root = machine_root

    def default_pack_settings_path(self) -> str:
        return self.active_pack_settings_path

    def load_pack_settings(self, path: str) -> object:
        return SimpleNamespace(workspace_roots=SimpleNamespace(machine_root=self._machine_root))


class _FakeDocumentSyncService:
    OUTPUT_PATH = "core/control_plane/indexes/example/example_index.json"

    def sync_cache_inputs(self) -> SyncCacheInputSpec:
        return SyncCacheInputSpec(tracked_paths=("docs/source.md",))


def _write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def test_prepare_document_sync_cache_hits_after_finalize(tmp_path: Path) -> None:
    loader = _FakeLoader(tmp_path)
    service = _FakeDocumentSyncService()
    source_path = tmp_path / "docs/source.md"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("# source\n", encoding="utf-8")
    document = {"entries": [{"id": "entry.example"}]}
    canonical_output_path = tmp_path / service.OUTPUT_PATH

    prepared = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )

    assert prepared.cache_status == "miss"
    _write_json(canonical_output_path, document)
    finalize_document_sync_cache(prepared, document=document)

    prepared_again = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )

    assert prepared_again.cache_status == "hit"
    assert prepared_again.document == document
    assert prepared_again.input_file_count == 1
    assert prepared_again.manifest_path is not None
    assert prepared_again.manifest_path.exists()


def test_prepare_document_sync_cache_invalidates_when_tracked_input_changes(
    tmp_path: Path,
) -> None:
    loader = _FakeLoader(tmp_path)
    service = _FakeDocumentSyncService()
    source_path = tmp_path / "docs/source.md"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("# source\n", encoding="utf-8")
    document = {"entries": [{"id": "entry.example"}]}
    canonical_output_path = tmp_path / service.OUTPUT_PATH

    prepared = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )
    _write_json(canonical_output_path, document)
    finalize_document_sync_cache(prepared, document=document)

    source_path.write_text("# changed source\n", encoding="utf-8")
    prepared_after_change = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )

    assert prepared_after_change.cache_status == "miss"
    assert prepared_after_change.document is None


def test_resolve_sync_cache_root_uses_fallback_when_machine_root_is_core_control_plane(
    tmp_path: Path,
) -> None:
    loader = _FakeLoader(tmp_path, machine_root="core/control_plane")

    assert resolve_sync_cache_root(loader) == tmp_path / SYNC_CACHE_FALLBACK_ROOT


def test_validate_prepared_document_sync_cache_downgrades_invalid_hit_to_miss(
    tmp_path: Path,
) -> None:
    loader = _FakeLoader(tmp_path)
    service = _FakeDocumentSyncService()
    source_path = tmp_path / "docs/source.md"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("# source\n", encoding="utf-8")
    document = {"$schema": "urn:test:schema", "entries": [{"id": "entry.example"}]}
    canonical_output_path = tmp_path / service.OUTPUT_PATH

    prepared = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )
    _write_json(canonical_output_path, document)
    finalize_document_sync_cache(prepared, document=document)

    prepared_hit = prepare_document_sync_cache(
        loader,
        service,
        relative_output_path=service.OUTPUT_PATH,
    )
    assert prepared_hit.cache_status == "hit"

    loader.schema_store.fail_validation = True
    validated = validate_prepared_document_sync_cache(loader, prepared_hit)

    assert validated is not None
    assert validated.cache_status == "miss"
    assert validated.document is None
