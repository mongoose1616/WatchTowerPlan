"""Environment-backed configuration for runtime telemetry."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

TELEMETRY_ENV_VAR = "WATCHTOWER_TELEMETRY"
TELEMETRY_STDERR_ENV_VAR = "WATCHTOWER_TELEMETRY_STDERR"
TELEMETRY_DIR_ENV_VAR = "WATCHTOWER_TELEMETRY_DIR"


@dataclass(frozen=True, slots=True)
class TelemetryConfig:
    """Resolved runtime telemetry configuration for one CLI invocation."""

    enabled: bool
    emit_stderr: bool
    output_dir_override: Path | None

    @classmethod
    def from_env(
        cls,
        environ: Mapping[str, str] | None = None,
    ) -> TelemetryConfig:
        """Resolve telemetry configuration from the current environment."""

        env = environ or {}
        output_dir_raw = env.get(TELEMETRY_DIR_ENV_VAR)
        return cls(
            enabled=_resolve_toggle(env, TELEMETRY_ENV_VAR, default=True),
            emit_stderr=_resolve_toggle(env, TELEMETRY_STDERR_ENV_VAR, default=True),
            output_dir_override=Path(output_dir_raw).expanduser() if output_dir_raw else None,
        )


def _resolve_toggle(
    environ: Mapping[str, str],
    name: str,
    *,
    default: bool,
) -> bool:
    raw_value = environ.get(name)
    if raw_value is None:
        return default
    normalized = raw_value.strip().lower()
    if normalized == "on":
        return True
    if normalized == "off":
        return False
    return default


__all__ = [
    "TELEMETRY_DIR_ENV_VAR",
    "TELEMETRY_ENV_VAR",
    "TELEMETRY_STDERR_ENV_VAR",
    "TelemetryConfig",
]
