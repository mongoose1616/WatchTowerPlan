from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def test_verify_script_continues_to_pack_checks_after_validate_all_failure(
    tmp_path: Path,
) -> None:
    workspace_root = Path(__file__).resolve().parents[2]
    repo_root = workspace_root.parents[1]
    script_path = workspace_root / "tools" / "verify.sh"
    pack_slug = f"verify_fixture_{tmp_path.name.replace('-', '_')}"
    pack_root = repo_root / pack_slug
    (pack_root / "python" / "src").mkdir(parents=True)
    (pack_root / "python" / "tests").mkdir(parents=True)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    log_path = tmp_path / "verify.log"
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "printf '%s\\n' \"$*\" >> \"$WT_VERIFY_LOG\"",
                "if [[ \"$*\" == 'run watchtower-core validate all' ]]; then",
                "  exit 1",
                "fi",
                "exit 0",
                "",
            ]
        ),
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    env["WT_VERIFY_LOG"] = str(log_path)

    try:
        result = subprocess.run(
            ["bash", str(script_path), "all", "--pack", pack_slug],
            cwd=workspace_root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        shutil.rmtree(pack_root, ignore_errors=True)

    assert result.returncode == 1
    assert "Verification failed in 1 step(s):" in result.stderr
    assert "- validate all (exit 1)" in result.stderr
    assert log_path.read_text(encoding="utf-8").splitlines() == [
        "run mypy src",
        "run ruff check src tests/unit tests/integration",
        "run python -m pytest -q tests/unit tests/integration",
        "run watchtower-core validate all",
        f"run mypy src ../../{pack_slug}/python/src",
        f"run ruff check ../../{pack_slug}/python/src ../../{pack_slug}/python/tests",
        f"run python -m pytest -q ../../{pack_slug}/python/tests",
    ]
