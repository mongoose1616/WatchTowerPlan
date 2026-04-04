from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)


def test_verify_sh_all_runs_pack_ruff_when_pack_requested(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    materialize_pack_validation_suite(repo_root / "fixture")
    (repo_root / "fixture" / "python" / "tests").mkdir(parents=True, exist_ok=True)

    log_path = tmp_path / "uv_calls.txt"
    uv_stub = tmp_path / "uv"
    uv_stub.write_text(
        "\n".join(
            (
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                f'printf "%s\\n" \"$*\" >> "{log_path}"',
                "",
            )
        ),
        encoding="utf-8",
    )
    uv_stub.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{tmp_path}:{env['PATH']}"

    subprocess.run(
        ["bash", "./tools/verify.sh", "all", "--pack", "fixture"],
        cwd=repo_root / "core" / "python",
        check=True,
        env=env,
    )

    assert log_path.read_text(encoding="utf-8").splitlines() == [
        "run mypy src",
        "run ruff check src tests/unit tests/integration",
        "run python -m pytest -q tests/unit tests/integration",
        "run watchtower-core validate all",
        "run mypy src ../../fixture/python/src",
        "run ruff check ../../fixture/python/src ../../fixture/python/tests",
        "run python -m pytest -q ../../fixture/python/tests",
    ]
