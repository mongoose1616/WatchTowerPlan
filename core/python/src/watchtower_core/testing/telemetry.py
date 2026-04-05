"""Reusable telemetry test fixtures for isolated test environments."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def telemetry_output_dir_fixture(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a session-scoped temporary directory for telemetry output."""

    return tmp_path_factory.mktemp("runtime_telemetry")


def redirect_runtime_telemetry_fixture(
    monkeypatch: pytest.MonkeyPatch,
    telemetry_output_dir: Path,
) -> None:
    """Redirect runtime telemetry to the isolated temporary directory."""

    monkeypatch.setenv("WATCHTOWER_TELEMETRY_DIR", str(telemetry_output_dir))
    monkeypatch.setenv("WATCHTOWER_TELEMETRY_STDERR", "off")
