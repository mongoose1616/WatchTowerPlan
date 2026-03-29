from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tests.pack_fixture_support import materialize_validation_repo_subset


def test_install_git_hooks_script_materializes_repo_local_hooks(tmp_path: Path) -> None:
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

    assert not (repo_root / ".githooks").exists()

    subprocess.run(
        [
            "bash",
            "./tools/install_git_hooks.sh",
            "--mode",
            "all",
            "--pack",
            "fixture",
        ],
        cwd=repo_root / "core/python",
        check=True,
        env=env,
    )

    hook_root = repo_root / ".githooks"
    template_root = repo_root / "core/python/tools/git_hooks"
    assert hook_root.is_dir()
    assert (hook_root / "README.md").read_text(encoding="utf-8") == (
        template_root / "README.md"
    ).read_text(encoding="utf-8")
    assert (hook_root / "pre-push").read_text(encoding="utf-8") == (
        template_root / "pre-push"
    ).read_text(encoding="utf-8")
    assert os.access(hook_root / "pre-push", os.X_OK)

    hooks_path = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    ).stdout.strip()
    verify_mode = subprocess.run(
        ["git", "config", "--get", "watchtower.verifyMode"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    ).stdout.strip()
    verify_pack = subprocess.run(
        ["git", "config", "--get", "watchtower.verifyPack"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    ).stdout.strip()

    assert hooks_path == ".githooks"
    assert verify_mode == "all"
    assert verify_pack == "fixture"
