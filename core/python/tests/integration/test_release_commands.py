from __future__ import annotations

import json
import subprocess
from pathlib import Path
from shutil import copytree

import pytest

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_host.cli.main import main


def test_release_check_passes_for_repo_subset_without_git_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    recipient_root = repo_root / "packs" / "recipient"
    materialize_pack_validation_suite(
        recipient_root,
        pack_slug="recipient",
        registry_mode="replace_default",
        default_repo_pack=True,
    )
    output_root = tmp_path / "customer_recipient"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "release",
            "check",
            "--output-root",
            str(output_root),
            "--include-pack",
            "recipient",
            "--schema-path",
            "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json",
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core release check"
    assert payload["passed"] is True
    assert payload["worktree"]["available"] is False
    assert payload["validation_all"]["passed"] is True
    assert payload["schema_validations"][0]["schema_path"] == (
        "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json"
    )
    assert payload["export"]["passed"] is True
    assert payload["export"]["portability"]["issue_count"] == 0


def test_release_check_blocks_dirty_git_worktree_without_allow_dirty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    _initialize_git_repository(repo_root)
    (repo_root / "dirty_note.md").write_text("# Dirty\n", encoding="utf-8")
    output_root = tmp_path / "blocked_release"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "release",
            "check",
            "--output-root",
            str(output_root),
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 1
    assert payload["command"] == "watchtower-core release check"
    assert payload["status"] == "error"
    assert payload["dirty_worktree_blocked"] is True
    assert payload["worktree"]["available"] is True
    assert payload["worktree"]["clean"] is False
    assert payload["validation_all"] is None
    assert payload["export"] is None


def test_release_check_recipient_bootstrap_smoke_flow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    recipient_root = repo_root / "packs" / "recipient"
    recipient_surfaces = materialize_pack_validation_suite(
        recipient_root,
        pack_slug="recipient",
        registry_mode="replace_default",
        default_repo_pack=True,
    )

    core_release_root = tmp_path / "customer_core"
    pack_release_root = tmp_path / "customer_recipient_pack"
    composed_root = tmp_path / "composed_repo"
    reexport_root = tmp_path / "customer_reexport"

    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "release",
            "check",
            "--output-root",
            str(core_release_root),
            "--overwrite",
            "--format",
            "json",
        ]
    )
    core_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert core_payload["passed"] is True

    result = main(
        [
            "release",
            "check",
            "--output-root",
            str(pack_release_root),
            "--include-pack",
            "recipient",
            "--pack-only",
            "--overwrite",
            "--format",
            "json",
        ]
    )
    pack_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert pack_payload["passed"] is True
    assert pack_payload["export_scope"] == "pack_bundle"

    copytree(core_release_root, composed_root)
    copytree(pack_release_root / "packs" / "recipient", composed_root / "packs" / "recipient")
    (composed_root / "packs/recipient/.wt/runtime/telemetry").mkdir(parents=True, exist_ok=True)
    (
        composed_root / "packs/recipient/.wt/runtime/telemetry/example.jsonl"
    ).write_text(
        "{}\n",
        encoding="utf-8",
    )
    (composed_root / "packs/recipient/python/src/watchtower_recipient_fixture/__pycache__").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        composed_root
        / "packs/recipient/python/src/watchtower_recipient_fixture/__pycache__"
        / "helper.cpython-313.pyc"
    ).write_bytes(b"pyc")

    monkeypatch.chdir(composed_root / "core" / "python")

    result = main(
        [
            "pack",
            "bootstrap",
            "--pack-settings-path",
            recipient_surfaces["pack_settings_path"],
            "--write",
            "--no-sync-workspace",
            "--format",
            "json",
        ]
    )
    bootstrap_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert bootstrap_payload["pack_registry_entry"]["default_repo_pack"] is True

    result = main(
        [
            "pack",
            "validate",
            "--pack-settings-path",
            recipient_surfaces["pack_settings_path"],
            "--format",
            "json",
        ]
    )
    validate_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert validate_payload["passed"] is True

    result = main(
        [
            "validate",
            "all",
            "--format",
            "json",
        ]
    )
    validate_all_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert validate_all_payload["passed"] is True

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(reexport_root),
            "--include-pack",
            "recipient",
            "--overwrite",
            "--format",
            "json",
        ]
    )
    reexport_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert reexport_payload["passed"] is True
    assert reexport_payload["portability"]["passed"] is True
    assert reexport_payload["portability"]["issue_count"] == 0
    assert not (
        reexport_root / "packs/recipient/.wt/runtime/telemetry/example.jsonl"
    ).exists()
    assert not (
        reexport_root
        / "packs/recipient/python/src/watchtower_recipient_fixture/__pycache__"
    ).exists()


def _initialize_git_repository(repo_root: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=WatchTower Tests",
            "-c",
            "user.email=watchtower-tests@example.com",
            "commit",
            "-m",
            "fixture baseline",
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
