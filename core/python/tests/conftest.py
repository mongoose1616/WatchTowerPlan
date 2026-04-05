from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.testing.telemetry import (
    redirect_runtime_telemetry_fixture,
    telemetry_output_dir_fixture,
)


@pytest.fixture(scope="session")
def telemetry_output_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return telemetry_output_dir_fixture(tmp_path_factory)


@pytest.fixture(autouse=True)
def _redirect_runtime_telemetry(
    monkeypatch: pytest.MonkeyPatch,
    telemetry_output_dir: Path,
) -> None:
    redirect_runtime_telemetry_fixture(monkeypatch, telemetry_output_dir)
