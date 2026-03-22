from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def telemetry_output_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("runtime_telemetry")


@pytest.fixture(autouse=True)
def _redirect_runtime_telemetry(
    monkeypatch: pytest.MonkeyPatch,
    telemetry_output_dir: Path,
) -> None:
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(telemetry_output_dir))
