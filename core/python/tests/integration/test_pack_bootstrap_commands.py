from __future__ import annotations

import json

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


def test_pack_bootstrap_replace_hosted_packs_scrubs_donor_wiring_in_copied_core_repo(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    donor_pack = ControlPlaneLoader(REPO_ROOT).load_pack_registry().default_pack()
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    surfaces = materialize_pack_validation_suite(
        repo_root / REHOSTED_PACK_SLUG,
        pack_id=f"pack.{REHOSTED_PACK_SLUG}",
        pack_slug=REHOSTED_PACK_SLUG,
        command_namespace=REHOSTED_PACK_SLUG,
        python_distribution=REHOSTED_PYTHON_DISTRIBUTION,
        python_package=REHOSTED_PYTHON_PACKAGE,
        integration_module=REHOSTED_INTEGRATION_MODULE,
        register_with_host_registry=False,
        register_with_core_python_workspace=False,
    )
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "bootstrap",
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--replace-hosted-packs",
            "--write",
            "--no-sync-workspace",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack bootstrap"
    assert payload["status"] == "ok"
    assert payload["pack_slug"] == REHOSTED_PACK_SLUG
    assert payload["replace_hosted_packs"] is True
    assert donor_pack.pack_slug in payload["scrubbed_pack_slugs"]
    assert payload["pack_registry_entry"]["default_repo_pack"] is True
    assert payload["workspace_sync_ran"] is False
    assert payload["workspace_sync_required"] is True
    assert payload["validation_passed"] is None

    pack_registry = json.loads(
        (
            repo_root / "core" / "control_plane" / "registries" / "pack_registry.json"
        ).read_text(encoding="utf-8")
    )
    assert [entry["pack_slug"] for entry in pack_registry["packs"]] == [REHOSTED_PACK_SLUG]

    pyproject_text = (repo_root / "core" / "python" / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    assert donor_pack.python_distribution not in pyproject_text
    assert REHOSTED_PYTHON_DISTRIBUTION in pyproject_text


def test_pack_bootstrap_reports_deferred_workspace_sync_extras(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    surfaces = materialize_pack_validation_suite(
        repo_root / REHOSTED_PACK_SLUG,
        pack_id=f"pack.{REHOSTED_PACK_SLUG}",
        pack_slug=REHOSTED_PACK_SLUG,
        command_namespace=REHOSTED_PACK_SLUG,
        python_distribution=REHOSTED_PYTHON_DISTRIBUTION,
        python_package=REHOSTED_PYTHON_PACKAGE,
        integration_module=REHOSTED_INTEGRATION_MODULE,
        register_with_host_registry=False,
        register_with_core_python_workspace=False,
    )
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "bootstrap",
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--write",
            "--no-sync-workspace",
            "--sync-extra",
            "dev",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["workspace_sync_ran"] is False
    assert payload["workspace_sync_required"] is True
    assert payload["workspace_sync_extras"] == ["dev"]
    assert payload["next_steps"][0].startswith("Run `uv sync --extra dev` in core/python")
