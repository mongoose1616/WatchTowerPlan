from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tests.pack_fixture_support import materialize_validation_repo_subset


def _git_config_get(
    repo_root: Path,
    key: str,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "config", "--get", key],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_install_git_hooks_script_activates_tracked_hooks(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    env = os.environ.copy()
    env.setdefault("GIT_CONFIG_NOSYSTEM", "1")

    subprocess.run(
        ["git", "init", "-q"],
        cwd=repo_root,
        check=True,
        env=env,
    )

    assert (repo_root / ".githooks" / "pre-push").exists()

    subprocess.run(
        ["bash", "./tools/install_git_hooks.sh"],
        cwd=repo_root / "core/python",
        check=True,
        env=env,
    )

    hooks_path = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    ).stdout.strip()
    assert hooks_path == ".githooks"

    for key in (
        "watchtower.verifyMode",
        "watchtower.verifyPack",
        "watchtower.verifyFailFast",
    ):
        completed = _git_config_get(repo_root, key, env)
        assert completed.returncode == 1
        assert completed.stdout == ""


def test_pre_push_hook_runs_mypy_and_ruff_only(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    env = os.environ.copy()
    env.setdefault("GIT_CONFIG_NOSYSTEM", "1")

    subprocess.run(
        ["git", "init", "-q"],
        cwd=repo_root,
        check=True,
        env=env,
    )

    fake_bin = repo_root / ".fake-bin"
    fake_bin.mkdir()
    uv_stub = fake_bin / "uv"
    captured_args_path = repo_root / "uv_args.txt"
    uv_stub.write_text(
        "\n".join(
            (
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                f'printf "%s\\n" "$*" >> "{captured_args_path}"',
                "",
            )
        ),
        encoding="utf-8",
    )
    uv_stub.chmod(0o755)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"

    subprocess.run(
        ["bash", ".githooks/pre-push"],
        cwd=repo_root,
        check=True,
        env=env,
    )

    assert captured_args_path.read_text(encoding="utf-8").splitlines() == [
        "run mypy src",
        "run ruff check src tests/unit tests/integration",
    ]
