from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import main


def test_pack_extract_core_stages_engineering_shared_core(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    donor_pack = ControlPlaneLoader(REPO_ROOT).load_pack_registry().default_pack()
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    output_root = tmp_path / "shared_core"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "extract-core",
            "--output-root",
            str(output_root),
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack extract-core"
    assert payload["passed"] is True
    assert payload["readiness"]["passed"] is True
    assert (output_root / "core").is_dir()
    assert (output_root / "AGENTS.md").is_file()
    assert (output_root / "README.md").is_file()
    assert "core" in {path.name for path in output_root.iterdir()}
    assert (output_root / "core/python/tests").is_dir()
    assert any((output_root / "core/python/tests").rglob("*.py"))

    pack_registry = json.loads(
        (output_root / "core/control_plane/registries/pack_registry.json").read_text(
            encoding="utf-8"
        )
    )
    assert pack_registry["packs"] == []

    pyproject_text = (output_root / "core/python/pyproject.toml").read_text(encoding="utf-8")
    assert donor_pack.python_distribution not in pyproject_text
    assert not (output_root / "core/python/uv.lock").exists()

    assert (
        output_root
        / "core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json"
    ).is_file()
    assert (
        output_root
        / "core/control_plane/records/validation_evidence/"
        / "governed_acceptance_example_validation_baseline.json"
    ).is_file()
    traceability = json.loads(
        (
            output_root / "core/control_plane/indexes/traceability/traceability_index.json"
        ).read_text(encoding="utf-8")
    )
    assert [entry["trace_id"] for entry in traceability["entries"]] == [
        "trace.governed_acceptance_example"
    ]
    assert all(
        path.startswith("core/")
        for path in traceability["entries"][0]["source_surface_paths"]
    )


def test_pack_apply_core_replaces_local_core_and_preserves_dev_residue(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    donor_repo_root = materialize_validation_repo_subset(
        tmp_path / "donor_fixture",
        include_shared_discovery_sources=True,
    )
    recipient_root = materialize_validation_repo_subset(
        tmp_path / "recipient_fixture",
        include_shared_discovery_sources=True,
    )
    output_root = tmp_path / "shared_core"

    monkeypatch.chdir(donor_repo_root / "core" / "python")
    result = main(
        [
            "pack",
            "extract-core",
            "--output-root",
            str(output_root),
            "--overwrite",
            "--format",
            "json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["passed"] is True

    preserved_marker = recipient_root / "core/python/.venv/bin/marker.txt"
    preserved_marker.parent.mkdir(parents=True, exist_ok=True)
    preserved_marker.write_text("keep\n", encoding="utf-8")
    stale_path = recipient_root / "core/stale.txt"
    stale_path.write_text("delete\n", encoding="utf-8")

    monkeypatch.chdir(recipient_root / "core" / "python")
    result = main(
        [
            "pack",
            "apply-core",
            "--source-root",
            str(output_root),
            "--write",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack apply-core"
    assert payload["source_readiness"]["passed"] is True
    assert payload["wrote"] is True
    assert "core/stale.txt" in payload["deleted_paths"]
    assert "core/python/.venv" in payload["preserved_paths"]
    assert preserved_marker.is_file()
    assert preserved_marker.read_text(encoding="utf-8") == "keep\n"
    assert not stale_path.exists()


def test_pack_apply_core_rejects_missing_staged_core_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    recipient_root = materialize_validation_repo_subset(
        tmp_path / "recipient_fixture",
        include_shared_discovery_sources=True,
    )
    missing_source_root = tmp_path / "missing_extract"
    missing_source_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.chdir(recipient_root / "core" / "python")
    result = main(
        [
            "pack",
            "apply-core",
            "--source-root",
            str(missing_source_root),
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 1
    assert payload["command"] == "watchtower-core pack apply-core"
    assert "missing the staged core/ directory" in payload["message"]


def test_pack_export_core_only_scrubs_donor_hosted_pack_wiring(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    output_root = tmp_path / "customer_core"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(output_root),
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack export"
    assert payload["passed"] is True
    assert payload["export_scope"] == "repository_bundle"
    assert payload["included_pack_slugs"] == []
    assert payload["default_pack_slug"] is None
    assert payload["pack_validation_note"] is None
    assert payload["portability"]["passed"] is True
    assert (output_root / "core").is_dir()
    assert not (output_root / "plan").exists()
    assert (output_root / "core/python/tests").is_dir()
    assert not any((output_root / "core/python/tests").iterdir())
    assert not any(
        path.is_file() and path.name != "README.md"
        for path in (output_root / "core/control_plane/records").rglob("*")
    )
    assert not any(
        path.is_file() and path.suffix == ".json"
        for path in (output_root / "core/control_plane/contracts/acceptance").glob("*.json")
    )
    traceability = json.loads(
        (
            output_root / "core/control_plane/indexes/traceability/traceability_index.json"
        ).read_text(encoding="utf-8")
    )
    assert traceability["entries"] == []

    pack_registry = json.loads(
        (output_root / "core/control_plane/registries/pack_registry.json").read_text(
            encoding="utf-8"
        )
    )
    assert pack_registry["packs"] == []

    pyproject_text = (output_root / "core/python/pyproject.toml").read_text(encoding="utf-8")
    assert "watchtower-plan" not in pyproject_text
    assert not (output_root / "core/python/uv.lock").exists()


def test_pack_export_selected_pack_scrubs_internal_release_residue(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    recipient_root = repo_root / "packs" / "recipient"
    omitted_root = repo_root / "packs" / "oversight"
    recipient_surfaces = materialize_pack_validation_suite(
        recipient_root,
        pack_slug="recipient",
        registry_mode="replace_default",
        default_repo_pack=True,
    )
    materialize_pack_validation_suite(
        omitted_root,
        pack_slug="oversight",
        registry_mode="append",
    )

    (recipient_root / "docs/references").mkdir(parents=True, exist_ok=True)
    (
        recipient_root
        / "docs/references"
        / "recipient_assessment_closeout_reference.md"
    ).write_text(
        "# Internal Assessment\n",
        encoding="utf-8",
    )
    (recipient_root / ".wt/runtime/telemetry").mkdir(parents=True, exist_ok=True)
    (recipient_root / "python/tests/unit").mkdir(parents=True, exist_ok=True)
    (recipient_root / "python/tests/unit/test_example.py").write_text("", encoding="utf-8")
    (recipient_root / "python/src/watchtower_recipient_fixture/testing").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        recipient_root / "python/src/watchtower_recipient_fixture/testing/helper.py"
    ).write_text(
        "",
        encoding="utf-8",
    )
    (recipient_root / "projects/example/.wt").mkdir(parents=True, exist_ok=True)
    (
        recipient_root / "projects/example/.wt/project_repository_map.json"
    ).write_text(
        "{}\n",
        encoding="utf-8",
    )

    output_root = tmp_path / "customer_recipient"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(output_root),
            "--include-pack",
            "recipient",
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack export"
    assert payload["passed"] is True
    assert payload["export_scope"] == "repository_bundle"
    assert payload["included_pack_slugs"] == ["recipient"]
    assert payload["default_pack_slug"] == "recipient"
    assert payload["pack_validation_note"] is None
    assert payload["portability"]["passed"] is True
    assert (
        payload["pack_validations"][0]["pack_settings_path"]
        == recipient_surfaces["pack_settings_path"]
    )
    assert payload["pack_validations"][0]["passed"] is True

    assert (output_root / "packs/recipient").is_dir()
    assert not (output_root / "packs/oversight").exists()
    assert not any(
        path.is_file() and path.name != "README.md"
        for path in (output_root / "core/control_plane/records").rglob("*")
    )
    assert not any(
        path.is_file() and path.suffix == ".json"
        for path in (output_root / "core/control_plane/contracts/acceptance").glob("*.json")
    )
    traceability = json.loads(
        (
            output_root / "core/control_plane/indexes/traceability/traceability_index.json"
        ).read_text(encoding="utf-8")
    )
    assert traceability["entries"] == []
    assert (output_root / "packs/recipient/.wt/runtime").is_dir()
    assert not any((output_root / "packs/recipient/.wt/runtime").iterdir())
    assert (output_root / "packs/recipient/python/tests").is_dir()
    assert not any((output_root / "packs/recipient/python/tests").iterdir())
    assert (
        output_root / "packs/recipient/python/src/watchtower_recipient_fixture/testing"
    ).is_dir()
    assert not any(
        (output_root / "packs/recipient/python/src/watchtower_recipient_fixture/testing").iterdir()
    )
    assert not (
        output_root / "packs/recipient/projects/example/.wt/project_repository_map.json"
    ).exists()
    assert not (
        output_root / "packs/recipient/docs/references/recipient_assessment_closeout_reference.md"
    ).exists()

    pack_registry = json.loads(
        (output_root / "core/control_plane/registries/pack_registry.json").read_text(
            encoding="utf-8"
        )
    )
    assert [entry["pack_slug"] for entry in pack_registry["packs"]] == ["recipient"]

    pyproject_text = (output_root / "core/python/pyproject.toml").read_text(encoding="utf-8")
    assert "watchtower-recipient-fixture" in pyproject_text
    assert "watchtower-oversight-fixture" not in pyproject_text
    assert "watchtower-plan" not in pyproject_text
    assert not (output_root / "core/python/uv.lock").exists()


def test_pack_export_pack_only_scrubs_selected_pack_without_shared_core(
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

    (recipient_root / "docs/references").mkdir(parents=True, exist_ok=True)
    (
        recipient_root
        / "docs/references"
        / "recipient_assessment_closeout_reference.md"
    ).write_text(
        "# Internal Assessment\n",
        encoding="utf-8",
    )
    (recipient_root / ".wt/runtime/telemetry").mkdir(parents=True, exist_ok=True)
    (recipient_root / "python/tests/unit").mkdir(parents=True, exist_ok=True)
    (recipient_root / "python/tests/unit/test_example.py").write_text("", encoding="utf-8")
    (recipient_root / "python/src/watchtower_recipient_fixture/testing").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        recipient_root / "python/src/watchtower_recipient_fixture/testing/helper.py"
    ).write_text(
        "",
        encoding="utf-8",
    )
    (recipient_root / "projects/example/.wt").mkdir(parents=True, exist_ok=True)
    (
        recipient_root / "projects/example/.wt/project_repository_map.json"
    ).write_text(
        "{}\n",
        encoding="utf-8",
    )

    output_root = tmp_path / "customer_recipient_pack"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(output_root),
            "--include-pack",
            "recipient",
            "--pack-only",
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack export"
    assert payload["passed"] is True
    assert payload["export_scope"] == "pack_bundle"
    assert payload["included_pack_slugs"] == ["recipient"]
    assert payload["default_pack_slug"] is None
    assert payload["pack_validations"] == []
    assert payload["pack_validation_note"] is not None
    assert "skips shared-core hosted-pack contract validation" in payload["pack_validation_note"]
    assert payload["portability"]["passed"] is True

    assert not (output_root / "core").exists()
    assert (output_root / "packs/recipient").is_dir()
    assert (output_root / "packs/recipient/.wt/runtime").is_dir()
    assert not any((output_root / "packs/recipient/.wt/runtime").iterdir())
    assert (output_root / "packs/recipient/python/tests").is_dir()
    assert not any((output_root / "packs/recipient/python/tests").iterdir())
    assert (
        output_root / "packs/recipient/python/src/watchtower_recipient_fixture/testing"
    ).is_dir()
    assert not any(
        (output_root / "packs/recipient/python/src/watchtower_recipient_fixture/testing").iterdir()
    )
    assert not (
        output_root / "packs/recipient/projects/example/.wt/project_repository_map.json"
    ).exists()
    assert not (
        output_root / "packs/recipient/docs/references/recipient_assessment_closeout_reference.md"
    ).exists()


def test_pack_export_reexports_bootstrapped_bundle_after_runtime_residue(
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

    core_export_root = tmp_path / "customer_core"
    pack_export_root = tmp_path / "customer_recipient_pack"
    composed_root = tmp_path / "composed_repo"
    reexport_root = tmp_path / "customer_reexport"

    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(core_export_root),
            "--overwrite",
            "--format",
            "json",
        ]
    )
    core_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert core_payload["passed"] is True
    assert core_payload["export_scope"] == "repository_bundle"

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(pack_export_root),
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

    copytree(core_export_root, composed_root)
    copytree(pack_export_root / "packs" / "recipient", composed_root / "packs" / "recipient")
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
    pycache_root = (
        reexport_root / "packs/recipient/python/src/watchtower_recipient_fixture/__pycache__"
    )
    assert not pycache_root.exists()
