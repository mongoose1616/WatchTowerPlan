from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree, rmtree

import pytest

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import main

REHOSTED_PACK_SLUG = "rehosted"
REHOSTED_PYTHON_DISTRIBUTION = "watchtower-rehosted-fixture"
REHOSTED_PYTHON_PACKAGE = "watchtower_rehosted_fixture"
REHOSTED_INTEGRATION_MODULE = "watchtower_rehosted_fixture.integration"
_TRANSIENT_PATH_PARTS = {
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "pip-wheel-metadata",
}


def test_shared_core_refresh_round_trip_bootstraps_clean_recipient_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    donor_pack = ControlPlaneLoader(REPO_ROOT).load_pack_registry().default_pack()
    donor_repo_root = materialize_validation_repo_subset(
        tmp_path / "donor_fixture",
        include_shared_discovery_sources=True,
    )
    recipient_root = tmp_path / "recipient_repo"
    recipient_root.mkdir(parents=True, exist_ok=True)

    recipient_surfaces, bootstrap_payload = _run_shared_core_refresh_cycle(
        tmp_path=tmp_path,
        cycle_name="first",
        donor_repo_root=donor_repo_root,
        recipient_root=recipient_root,
        recipient_surfaces=None,
        monkeypatch=monkeypatch,
        capsys=capsys,
    )

    assert bootstrap_payload["workspace_sync_ran"] is False
    assert bootstrap_payload["workspace_sync_required"] is True
    assert bootstrap_payload["validation_passed"] is None

    pack_registry = json.loads(
        (
            recipient_root / "core" / "control_plane" / "registries" / "pack_registry.json"
        ).read_text(encoding="utf-8")
    )
    assert [entry["pack_slug"] for entry in pack_registry["packs"]] == [REHOSTED_PACK_SLUG]
    assert pack_registry["packs"][0]["default_repo_pack"] is True

    pyproject_text = (recipient_root / "core" / "python" / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    assert donor_pack.python_distribution not in pyproject_text
    assert REHOSTED_PYTHON_DISTRIBUTION in pyproject_text
    assert recipient_surfaces["pack_settings_path"] == "rehosted/.wt/manifests/pack_settings.json"


def test_shared_core_refresh_round_trip_is_idempotent_across_repeated_cycles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    donor_repo_root = materialize_validation_repo_subset(
        tmp_path / "donor_fixture",
        include_shared_discovery_sources=True,
    )
    recipient_root = tmp_path / "recipient_repo"
    recipient_root.mkdir(parents=True, exist_ok=True)

    recipient_surfaces, _ = _run_shared_core_refresh_cycle(
        tmp_path=tmp_path,
        cycle_name="first",
        donor_repo_root=donor_repo_root,
        recipient_root=recipient_root,
        recipient_surfaces=None,
        monkeypatch=monkeypatch,
        capsys=capsys,
    )
    first_snapshot = _snapshot_refresh_state(recipient_root)

    _, _ = _run_shared_core_refresh_cycle(
        tmp_path=tmp_path,
        cycle_name="second",
        donor_repo_root=donor_repo_root,
        recipient_root=recipient_root,
        recipient_surfaces=recipient_surfaces,
        monkeypatch=monkeypatch,
        capsys=capsys,
    )
    second_snapshot = _snapshot_refresh_state(recipient_root)

    assert second_snapshot == first_snapshot


def _run_shared_core_refresh_cycle(
    *,
    tmp_path: Path,
    cycle_name: str,
    donor_repo_root: Path,
    recipient_root: Path,
    recipient_surfaces: dict[str, str] | None,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> tuple[dict[str, str], dict[str, object]]:
    output_root = tmp_path / f"shared_core_{cycle_name}"

    monkeypatch.chdir(donor_repo_root / "core" / "python")
    extract_result, extract_payload = _run_cli_json(
        [
            "pack",
            "extract-core",
            "--output-root",
            str(output_root),
            "--overwrite",
            "--format",
            "json",
        ],
        capsys,
    )
    assert extract_result == 0
    assert extract_payload["command"] == "watchtower-core pack extract-core"
    assert extract_payload["passed"] is True
    assert extract_payload["readiness"]["passed"] is True

    _replace_tree(output_root / "core", recipient_root / "core")
    _seed_recipient_root_shell(output_root=output_root, recipient_root=recipient_root)

    if recipient_surfaces is None:
        recipient_surfaces = materialize_pack_validation_suite(
            recipient_root / REHOSTED_PACK_SLUG,
            pack_id=f"pack.{REHOSTED_PACK_SLUG}",
            pack_slug=REHOSTED_PACK_SLUG,
            command_namespace=REHOSTED_PACK_SLUG,
            python_distribution=REHOSTED_PYTHON_DISTRIBUTION,
            python_package=REHOSTED_PYTHON_PACKAGE,
            integration_module=REHOSTED_INTEGRATION_MODULE,
            register_with_host_registry=False,
            register_with_core_python_workspace=False,
        )

    monkeypatch.chdir(recipient_root / "core" / "python")
    bootstrap_result, bootstrap_payload = _run_cli_json(
        [
            "pack",
            "bootstrap",
            "--pack-settings-path",
            recipient_surfaces["pack_settings_path"],
            "--replace-hosted-packs",
            "--write",
            "--no-sync-workspace",
            "--format",
            "json",
        ],
        capsys,
    )
    assert bootstrap_result == 0
    assert bootstrap_payload["command"] == "watchtower-core pack bootstrap"
    assert bootstrap_payload["status"] == "ok"
    assert bootstrap_payload["pack_slug"] == REHOSTED_PACK_SLUG
    assert bootstrap_payload["replace_hosted_packs"] is True
    assert bootstrap_payload["scrubbed_pack_slugs"] == []

    validate_result, validate_payload = _run_cli_json(
        [
            "pack",
            "validate",
            "--pack-settings-path",
            recipient_surfaces["pack_settings_path"],
            "--format",
            "json",
        ],
        capsys,
    )
    assert validate_result == 0
    assert validate_payload["command"] == "watchtower-core pack validate"
    assert validate_payload["passed"] is True

    validate_all_result, validate_all_payload = _run_cli_json(
        [
            "validate",
            "all",
            "--pack-settings-path",
            recipient_surfaces["pack_settings_path"],
            "--skip-front-matter",
            "--skip-document-semantics",
            "--skip-artifacts",
            "--skip-acceptance",
            "--format",
            "json",
        ],
        capsys,
    )
    assert validate_all_result == 0
    assert validate_all_payload["command"] == "watchtower-core validate all"
    assert validate_all_payload["passed"] is True
    assert validate_all_payload["included_families"] == ["pack_contract"]

    return recipient_surfaces, bootstrap_payload


def _run_cli_json(arguments: list[str], capsys) -> tuple[int, dict[str, object]]:
    result = main(arguments)
    return result, json.loads(capsys.readouterr().out)


def _replace_tree(source_root: Path, destination_root: Path) -> None:
    if destination_root.exists():
        rmtree(destination_root)
    copytree(source_root, destination_root)


def _seed_recipient_root_shell(*, output_root: Path, recipient_root: Path) -> None:
    for source_path in sorted(output_root.iterdir(), key=lambda path: path.name):
        if source_path.name == "core":
            continue
        destination_path = recipient_root / source_path.name
        if destination_path.exists():
            continue
        if source_path.is_dir():
            copytree(source_path, destination_path)
            continue
        destination_path.write_bytes(source_path.read_bytes())


def _snapshot_refresh_state(repo_root: Path) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    for relative_root in ("core", REHOSTED_PACK_SLUG, "README.md", "AGENTS.md"):
        candidate = repo_root / relative_root
        if candidate.is_file():
            snapshot[candidate.relative_to(repo_root).as_posix()] = candidate.read_bytes()
            continue
        if not candidate.is_dir():
            continue
        for path in sorted(candidate.rglob("*")):
            if not path.is_file():
                continue
            relative_path = path.relative_to(repo_root).as_posix()
            if _is_transient_snapshot_path(relative_path):
                continue
            snapshot[relative_path] = path.read_bytes()
    return snapshot


def _is_transient_snapshot_path(relative_path: str) -> bool:
    parts = Path(relative_path).parts
    if any(part in _TRANSIENT_PATH_PARTS for part in parts):
        return True
    return "/.wt/runtime/" in f"/{relative_path}"
