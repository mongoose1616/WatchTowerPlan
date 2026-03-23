"""Fail-open local runtime telemetry with JSONL sinks and stderr summaries."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Literal
from uuid import uuid4

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry.config import TelemetryConfig

_ACTIVE_SESSION: ContextVar[TelemetrySession | None] = ContextVar(
    "watchtower_active_telemetry_session",
    default=None,
)
_ACTIVE_OPERATION: ContextVar[TelemetryOperation | None] = ContextVar(
    "watchtower_active_telemetry_operation",
    default=None,
)


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _new_id() -> str:
    return uuid4().hex[:10]


@dataclass(slots=True)
class TelemetrySession:
    """One per-invocation telemetry session."""

    config: TelemetryConfig
    run_id: str
    started_at: datetime
    command_name: str
    repo_root: Path
    output_path: Path | None = None
    pack_settings_path: str | None = None
    machine_root: str | None = None
    _writer: IO[str] | None = None
    _disabled_reason: str | None = None
    _active_token: Token[TelemetrySession | None] | None = None
    _finished: bool = False

    @property
    def enabled(self) -> bool:
        """Return whether this session can currently emit telemetry."""

        return self._writer is not None and self._disabled_reason is None

    @property
    def disabled_reason(self) -> str | None:
        """Return the last disable reason when telemetry is fail-open disabled."""

        return self._disabled_reason

    @contextmanager
    def activate(self) -> Iterator[TelemetrySession]:
        """Expose this session through contextvars for nested operations."""

        token = _ACTIVE_SESSION.set(self)
        self._active_token = token
        try:
            yield self
        finally:
            _ACTIVE_SESSION.reset(token)
            self._active_token = None

    def operation(
        self,
        operation_kind: str,
        operation_name: str,
        *,
        attributes: Mapping[str, object] | None = None,
    ) -> TelemetryOperation:
        """Create one nested operation span within this session."""

        return TelemetryOperation(
            session=self,
            operation_kind=operation_kind,
            operation_name=operation_name,
            attributes=dict(attributes or {}),
        )

    def finish(
        self,
        *,
        status: str,
        exit_code: int,
        error: BaseException | None = None,
    ) -> None:
        """Record one terminal run result and emit the stderr summary."""

        if self._finished:
            return
        self._finished = True
        finished_at = _utc_now()
        duration_ms = _duration_ms(self.started_at, finished_at)
        record: dict[str, object] = {
            "record_type": "run_finished",
            "telemetry_run_id": self.run_id,
            "command_name": self.command_name,
            "status": status,
            "exit_code": exit_code,
            "started_at": _format_timestamp(self.started_at),
            "finished_at": _format_timestamp(finished_at),
            "duration_ms": duration_ms,
            "output_path": str(self.output_path) if self.output_path is not None else None,
        }
        if error is not None:
            record["error_type"] = type(error).__name__
            record["error_message"] = str(error)
        self._emit_record(record)
        self._emit_stderr_summary(status=status, duration_ms=duration_ms)
        self._close()

    def _emit_record(self, record: Mapping[str, object]) -> None:
        if self._writer is None:
            return
        try:
            self._writer.write(json.dumps(_json_safe(record), sort_keys=True))
            self._writer.write("\n")
            self._writer.flush()
        except Exception as exc:
            self._disable(f"telemetry_write_failed:{type(exc).__name__}")

    def _emit_stderr_summary(self, *, status: str, duration_ms: int) -> None:
        if not self.enabled or not self.config.emit_stderr:
            return
        assert self.output_path is not None
        print(
            "[telemetry] "
            f"{self.command_name} status={status} duration_ms={duration_ms} "
            f"path={self.output_path}",
            file=sys.stderr,
        )

    def _disable(self, reason: str) -> None:
        self._disabled_reason = reason
        self._close()

    def _close(self) -> None:
        if self._writer is None:
            return
        self._writer.close()
        self._writer = None


@dataclass(slots=True)
class TelemetryOperation:
    """One timed operation nested under a telemetry session."""

    session: TelemetrySession
    operation_kind: str
    operation_name: str
    attributes: dict[str, object] = field(default_factory=dict)
    operation_id: str = field(default_factory=_new_id)
    parent_operation_id: str | None = None
    started_at: datetime = field(default_factory=_utc_now)
    _active_token: Token[TelemetryOperation | None] | None = None
    _status: str | None = None
    _record_error: BaseException | None = None

    def __enter__(self) -> TelemetryOperation:
        parent = _ACTIVE_OPERATION.get()
        self.parent_operation_id = parent.operation_id if parent is not None else None
        self._active_token = _ACTIVE_OPERATION.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        _traceback: object,
    ) -> Literal[False]:
        if self._active_token is not None:
            _ACTIVE_OPERATION.reset(self._active_token)
            self._active_token = None
        finished_at = _utc_now()
        record_error = self._record_error
        if record_error is None and self._status is None and exc is not None:
            record_error = exc
        status = self._status or ("ok" if exc is None else "error")
        record: dict[str, object] = {
            "record_type": "operation_result",
            "telemetry_run_id": self.session.run_id,
            "operation_id": self.operation_id,
            "parent_operation_id": self.parent_operation_id,
            "operation_kind": self.operation_kind,
            "operation_name": self.operation_name,
            "status": status,
            "started_at": _format_timestamp(self.started_at),
            "finished_at": _format_timestamp(finished_at),
            "duration_ms": _duration_ms(self.started_at, finished_at),
            "attributes": self.attributes,
        }
        if record_error is not None:
            record["error_type"] = type(record_error).__name__
            record["error_message"] = str(record_error)
        self.session._emit_record(record)
        return False

    def add_attributes(self, **attributes: object) -> None:
        """Attach or update structured attributes for this operation."""

        for key, value in attributes.items():
            if value is not None:
                self.attributes[key] = value

    def set_result(
        self,
        *,
        status: str,
        error: BaseException | None = None,
        **attributes: object,
    ) -> None:
        """Override the final operation status and add terminal attributes."""

        self._status = status
        self._record_error = error
        self.add_attributes(**attributes)


def create_telemetry_session(
    loader: ControlPlaneLoader,
    argv: Sequence[str],
    *,
    environ: Mapping[str, str] | None = None,
) -> TelemetrySession:
    """Create one fail-open telemetry session for a CLI invocation."""

    env = environ or os.environ
    config = TelemetryConfig.from_env(env)
    started_at = _utc_now()
    command_name = _command_name_from_argv(argv)
    if not config.enabled:
        return TelemetrySession(
            config=config,
            run_id=_new_id(),
            started_at=started_at,
            command_name=command_name,
            repo_root=loader.repo_root,
            _disabled_reason="telemetry_disabled",
        )

    run_id = _new_id()
    pack_settings_path: str | None = None
    machine_root: str | None = None
    try:
        output_dir, pack_settings_path, machine_root = _resolve_output_dir(
            loader,
            config,
            started_at,
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / _output_filename(started_at, run_id)
        writer = output_path.open("w", encoding="utf-8")
    except Exception as exc:
        return TelemetrySession(
            config=config,
            run_id=run_id,
            started_at=started_at,
            command_name=command_name,
            repo_root=loader.repo_root,
            pack_settings_path=pack_settings_path,
            machine_root=machine_root,
            _disabled_reason=f"telemetry_init_failed:{type(exc).__name__}",
        )

    session = TelemetrySession(
        config=config,
        run_id=run_id,
        started_at=started_at,
        command_name=command_name,
        repo_root=loader.repo_root,
        output_path=output_path,
        pack_settings_path=pack_settings_path,
        machine_root=machine_root,
        _writer=writer,
    )
    session._emit_record(
        {
            "record_type": "run_started",
            "telemetry_run_id": session.run_id,
            "command_name": session.command_name,
            "argv": list(argv),
            "started_at": _format_timestamp(started_at),
            "repo_root": str(loader.repo_root),
            "pack_settings_path": pack_settings_path,
            "machine_root": machine_root,
            "output_path": str(output_path),
        }
    )
    return session


def current_session() -> TelemetrySession | None:
    """Return the currently active telemetry session, if any."""

    return _ACTIVE_SESSION.get()


def add_operation_attributes(**attributes: object) -> None:
    """Attach attributes to the current operation when telemetry is active."""

    operation = _ACTIVE_OPERATION.get()
    if operation is None:
        return
    operation.add_attributes(**attributes)


@contextmanager
def telemetry_operation(
    operation_kind: str,
    operation_name: str,
    *,
    attributes: Mapping[str, object] | None = None,
) -> Iterator[TelemetryOperation | None]:
    """Run one nested telemetry operation when an active session exists."""

    session = current_session()
    if session is None:
        yield None
        return
    with session.operation(
        operation_kind,
        operation_name,
        attributes=attributes,
    ) as operation:
        yield operation


def _command_name_from_argv(argv: Sequence[str]) -> str:
    tokens: list[str] = []
    for token in argv:
        if token.startswith("-"):
            break
        tokens.append(token)
    if not tokens:
        return "watchtower-core"
    return "watchtower-core " + " ".join(tokens)


def _resolve_output_dir(
    loader: ControlPlaneLoader,
    config: TelemetryConfig,
    started_at: datetime,
) -> tuple[Path, str | None, str | None]:
    if config.output_dir_override is not None:
        return (
            config.output_dir_override / started_at.strftime("%Y/%m/%d"),
            None,
            None,
        )

    pack_settings_path = loader.activate_pack_settings()
    pack_settings = loader.load_pack_settings(pack_settings_path)
    machine_root = pack_settings.workspace_roots.machine_root
    machine_root_path = loader.resolve_path(machine_root)
    return (
        machine_root_path / "runtime" / "telemetry" / started_at.strftime("%Y/%m/%d"),
        pack_settings_path,
        machine_root,
    )


def _output_filename(started_at: datetime, run_id: str) -> str:
    return f"{started_at.strftime('%Y%m%dT%H%M%SZ')}_{os.getpid()}_{run_id}.jsonl"


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _duration_ms(started_at: datetime, finished_at: datetime) -> int:
    return int((finished_at - started_at).total_seconds() * 1000)


def _json_safe(value: object) -> object:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return _format_timestamp(value)
    if isinstance(value, Mapping):
        return {str(key): _json_safe(inner) for key, inner in value.items()}
    if isinstance(value, tuple | list):
        return [_json_safe(inner) for inner in value]
    return str(value)


__all__ = [
    "TelemetryOperation",
    "TelemetrySession",
    "add_operation_attributes",
    "create_telemetry_session",
    "current_session",
    "telemetry_operation",
]
