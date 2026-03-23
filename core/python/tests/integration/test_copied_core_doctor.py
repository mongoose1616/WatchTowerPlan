from __future__ import annotations

import json

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_externalized_fixture_python,
    materialize_pack_task_index_surface,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_host.cli.main import main


def test_doctor_succeeds_for_copied_core_repo_without_plan_owned_live_indexes(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    monkeypatch.chdir(repo_root / "core" / "python")

    scaffold_result = main(
        [
            "pack",
            "scaffold",
            "--pack-slug",
            "oversight",
            "--pack-root",
            "oversight",
            "--domain-root",
            "reviews",
            "--format",
            "json",
        ]
    )
    assert scaffold_result == 0
    capsys.readouterr()

    materialize_externalized_fixture_python(
        repo_root / "oversight" / "python",
        python_distribution="watchtower-oversight",
        python_package="watchtower_oversight",
        source_package_root=(
            REPO_ROOT
            / "core"
            / "python"
            / "tests"
            / "fixtures"
            / "python"
            / "watchtower_oversight_fixture"
        ),
        description="Synthetic oversight runtime package used to prove copied-core discovery.",
    )

    bootstrap_result = main(
        [
            "pack",
            "bootstrap",
            "--pack-settings-path",
            "oversight/.wt/manifests/pack_settings.json",
            "--write",
            "--no-sync-workspace",
            "--format",
            "json",
        ]
    )
    assert bootstrap_result == 0
    capsys.readouterr()

    result = main(["doctor", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["status"] == "ok"
    assert payload["counts"]["tasks"] == 0
    assert payload["counts"]["initiatives"] == 0
    assert "watchtower-core oversight sync all --write" in payload["recommended_baseline"]


def test_doctor_uses_discovered_pack_runtime_and_pack_local_task_schema_in_copied_core_repo(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight",
        python_package="watchtower_oversight",
        integration_module="watchtower_oversight.integration",
        register_with_host_registry=False,
        register_with_core_python_workspace=False,
    )
    materialize_pack_task_index_surface(repo_root / "oversight", pack_slug="oversight")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["doctor", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["status"] == "ok"
    assert payload["counts"]["tasks"] == 1
    assert "watchtower-core oversight sync all --write" in payload["recommended_baseline"]
