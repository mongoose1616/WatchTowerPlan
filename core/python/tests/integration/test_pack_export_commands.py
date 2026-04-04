from __future__ import annotations

import json
import os
import subprocess
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


def test_pack_extract_core_excludes_untracked_donor_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    env = os.environ.copy()
    env.setdefault("GIT_CONFIG_NOSYSTEM", "1")
    subprocess.run(["git", "init", "-q"], cwd=repo_root, check=True, env=env)
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True, env=env)

    injected_path = repo_root / "core" / "python" / "local_extract_probe.txt"
    injected_path.write_text("probe\n", encoding="utf-8")
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
    assert payload["passed"] is True
    assert payload["readiness"]["passed"] is True
    assert not (output_root / "core" / "python" / "local_extract_probe.txt").exists()


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


def test_pack_apply_core_rehydrates_live_recipient_pack_wiring(
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
    recipient_surfaces = materialize_pack_validation_suite(
        recipient_root / "packs" / "recipient",
        pack_slug="recipient",
        registry_mode="replace_default",
        default_repo_pack=True,
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
    extract_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert extract_payload["passed"] is True

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
    assert payload["rehydrated_paths"] == [
        "core/control_plane/registries/pack_registry.json",
        "core/python/pyproject.toml",
    ]
    assert "core/control_plane/indexes/commands/command_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/routes/route_index.json" in payload["changed_paths"]

    pack_registry = json.loads(
        (
            recipient_root / "core" / "control_plane" / "registries" / "pack_registry.json"
        ).read_text(encoding="utf-8")
    )
    assert [entry["pack_slug"] for entry in pack_registry["packs"]] == ["recipient"]
    assert (
        pack_registry["packs"][0]["pack_settings_path"] == recipient_surfaces["pack_settings_path"]
    )

    pyproject_text = (recipient_root / "core" / "python" / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    assert "watchtower-recipient-fixture" in pyproject_text
    assert "watchtower-plan" not in pyproject_text


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
    benchmark_record_path = (
        repo_root
        / "core/control_plane/records/benchmarks/fixture_benchmark_record.json"
    )
    benchmark_record_path.parent.mkdir(parents=True, exist_ok=True)
    benchmark_record_path.write_text("{}\n", encoding="utf-8")
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
    assert (
        "core/control_plane/records/benchmarks/fixture_benchmark_record.json"
        in payload["scrubbed_paths"]
    )
    assert (output_root / "core").is_dir()
    assert not (output_root / "plan").exists()
    assert (output_root / "core/python/tests").is_dir()
    assert not any((output_root / "core/python/tests").iterdir())
    assert not any(
        path.is_file() and path.name != "README.md"
        for path in (output_root / "core/control_plane/records").rglob("*")
    )
    assert not (
        output_root
        / "core/control_plane/records/benchmarks/fixture_benchmark_record.json"
    ).exists()
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


def test_pack_export_core_only_bundle_passes_validate_all(
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
    assert payload["passed"] is True

    monkeypatch.chdir(output_root / "core" / "python")
    result = main(["validate", "all", "--format", "json"])

    validate_payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert validate_payload["command"] == "watchtower-core validate all"
    assert validate_payload["passed"] is True


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


def test_pack_export_selected_plan_pack_scrubs_live_history_and_rebuilds_clean_views(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    if not (REPO_ROOT / "plan").is_dir():
        pytest.skip("Live plan pack root is not present in this repository.")

    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    copytree(REPO_ROOT / "plan", repo_root / "plan", dirs_exist_ok=True)
    output_root = tmp_path / "customer_plan"
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "export",
            "--output-root",
            str(output_root),
            "--include-pack",
            "plan",
            "--overwrite",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack export"
    assert payload["passed"] is True
    assert payload["included_pack_slugs"] == ["plan"]
    assert payload["portability"]["passed"] is True
    assert payload["portability"]["issue_count"] == 0
    assert any(path.startswith("plan/initiatives/") for path in payload["scrubbed_paths"])
    assert any(path.startswith("plan/projects/") for path in payload["scrubbed_paths"])
    assert any(path.startswith("plan/.wt/work_items/") for path in payload["scrubbed_paths"])

    assert (output_root / "plan/initiatives").is_dir()
    assert not any((output_root / "plan/initiatives").iterdir())
    assert (output_root / "plan/projects").is_dir()
    assert not any((output_root / "plan/projects").iterdir())
    assert (output_root / "plan/.wt/work_items").is_dir()
    assert not any((output_root / "plan/.wt/work_items").iterdir())

    plan_overview = (output_root / "plan/plan_overview.md").read_text(encoding="utf-8")
    assert "/home/j/WatchTowerPlan" not in plan_overview

    plan_indexes_root = output_root / "plan" / ".wt" / "indexes"
    initiative_index = json.loads(
        (plan_indexes_root / "initiative_index.json").read_text(encoding="utf-8")
    )
    assert initiative_index["entries"] == []

    project_index = json.loads(
        (plan_indexes_root / "project_index.json").read_text(encoding="utf-8")
    )
    assert project_index["entries"] == []

    coordination_index = json.loads(
        (plan_indexes_root / "coordination_index.json").read_text(encoding="utf-8")
    )
    assert coordination_index["active_initiative_count"] == 0
    assert coordination_index["actionable_task_count"] == 0
    assert coordination_index["recommended_surface_path"] == "plan/plan_overview.md"

    task_tracking = (output_root / "plan/tracking/task_tracking.md").read_text(encoding="utf-8")
    assert "plan/initiatives/" not in task_tracking

    artifact_index = json.loads(
        (plan_indexes_root / "artifact_index.json").read_text(encoding="utf-8")
    )
    assert not any(
        isinstance(entry.get("path"), str)
        and (
            entry["path"].startswith("plan/initiatives/")
            or entry["path"].startswith("plan/projects/")
        )
        for entry in artifact_index["artifacts"]
    )

    handoff_standard = (
        output_root
        / "plan/docs/standards/governance/"
        / "initiative_engineer_handoff_support_standard.md"
    ).read_text(encoding="utf-8")
    assert "/home/j/WatchTowerPlan" not in handoff_standard
