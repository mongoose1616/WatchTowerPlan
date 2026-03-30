"""Governed benchmarking runtime for reusable-core CLI performance measurements."""

from __future__ import annotations

import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import ValidationError

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    BenchmarkCommandRecord,
    BenchmarkNestedOperation,
    BenchmarkRecordArtifact,
    BenchmarkSuiteCommandDefinition,
    BenchmarkSuiteDefinition,
)
from watchtower_core.telemetry.config import (
    TELEMETRY_DIR_ENV_VAR,
    TELEMETRY_ENV_VAR,
    TELEMETRY_STDERR_ENV_VAR,
)

BENCHMARK_RECORDS_DIRECTORY = "core/control_plane/records/benchmarks"
_BENCHMARK_RECORD_SCHEMA_ID = "urn:watchtower:schema:artifacts:records:benchmark-record:v1"
_BENCHMARK_TOP_NESTED_OPERATION_LIMIT = 5
_BENCHMARK_COMMAND_MODULE = "watchtower_host.cli.main"
_DEFAULT_SUITE_ID = "suite.benchmark.core_cli_representative_v1"
_BENCHMARK_KIND_BASELINE = "baseline"
_BENCHMARK_KIND_TASK_SLICE = "task_slice"


@dataclass(frozen=True, slots=True)
class BenchmarkRunRequest:
    """Inputs for one governed benchmark execution."""

    suite_id: str = _DEFAULT_SUITE_ID
    measured_runs: int | None = None
    warmup_runs: int | None = None
    baseline_record_path: str | Path | None = None
    output_path: Path | None = None
    write_record: bool = False
    record_id: str | None = None


@dataclass(frozen=True, slots=True)
class BenchmarkRunResult:
    """Outcome of one governed benchmark execution."""

    suite_id: str
    suite_title: str
    benchmark_kind: str
    record_id: str
    document: dict[str, Any]
    output_path: Path | None
    record_path: Path | None


@dataclass(frozen=True, slots=True)
class _BenchmarkCommandExecution:
    """Internal measured execution summary for one benchmark command."""

    document: dict[str, Any]


class BenchmarkRunner:
    """Run a governed benchmark suite and optionally retain the resulting record."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def run(self, request: BenchmarkRunRequest) -> BenchmarkRunResult:
        suite = self._resolve_suite(request.suite_id)
        baseline_record = self._load_baseline_record(request.baseline_record_path)
        self._validate_baseline_compatibility(suite, baseline_record)
        baseline_record_path = None
        if request.baseline_record_path is not None:
            raw_baseline_path = Path(request.baseline_record_path)
            resolved_baseline_path = (
                raw_baseline_path
                if raw_baseline_path.is_absolute()
                else self._loader.resolve_path(str(raw_baseline_path))
            )
            baseline_record_path = _logical_or_absolute_path(self._loader, resolved_baseline_path)

        recorded_at = _utc_now()
        benchmark_kind = (
            _BENCHMARK_KIND_BASELINE
            if baseline_record is None
            else _BENCHMARK_KIND_TASK_SLICE
        )
        record_id = request.record_id or _default_record_id(
            suite_id=suite.suite_id,
            benchmark_kind=benchmark_kind,
            recorded_at=recorded_at,
        )
        baseline_command_map = (
            {command.command_id: command for command in baseline_record.commands}
            if baseline_record is not None
            else {}
        )

        command_documents = [
            self._run_benchmark_command(
                suite=suite,
                command_definition=command_definition,
                warmup_runs=(
                    request.warmup_runs
                    if request.warmup_runs is not None
                    else suite.warmup_runs
                ),
                measured_runs=(
                    request.measured_runs
                    if request.measured_runs is not None
                    else (
                        command_definition.measured_runs_override or suite.measured_runs
                    )
                ),
                baseline_command=baseline_command_map.get(command_definition.command_id),
            ).document
            for command_definition in suite.commands
        ]

        document = {
            "$schema": _BENCHMARK_RECORD_SCHEMA_ID,
            "id": record_id,
            "title": f"{suite.title} {benchmark_kind.replace('_', ' ').title()}",
            "status": "active",
            "benchmark_kind": benchmark_kind,
            "suite_id": suite.suite_id,
            "suite_title": suite.title,
            "recorded_at": _format_timestamp(recorded_at),
            "working_directory": suite.working_directory,
            "benchmark_contract": {
                "working_directory": suite.working_directory,
                "warmup_runs": (
                    request.warmup_runs
                    if request.warmup_runs is not None
                    else suite.warmup_runs
                ),
                "measured_runs": (
                    request.measured_runs
                    if request.measured_runs is not None
                    else suite.measured_runs
                ),
                "execution_mode": "serialized_subprocess",
                "failure_posture": "fail_closed",
                "telemetry_environment": {
                    "telemetry_on": {
                        TELEMETRY_ENV_VAR: "on",
                        TELEMETRY_STDERR_ENV_VAR: "off",
                        TELEMETRY_DIR_ENV_VAR: "<temp benchmark dir>",
                    },
                    "telemetry_off": {
                        TELEMETRY_ENV_VAR: "off",
                        TELEMETRY_STDERR_ENV_VAR: "off",
                    },
                },
                "notes": [
                    "Benchmark runs execute fresh subprocesses in serialized order.",
                    "Warmup runs are excluded from retained measured timing samples.",
                ],
            },
            "environment_context": _environment_context_document(self._loader.repo_root),
            "commands": command_documents,
            "notes": [
                "Runtime telemetry is measured separately from deliberate retained benchmark evidence.",
            ],
        }
        if baseline_record_path is not None:
            document["baseline_record_path"] = baseline_record_path

        self._validate_benchmark_record(document)

        output_path = (
            self._loader.artifact_store.write_json_file(request.output_path, document)
            if request.output_path is not None
            else None
        )

        record_path: Path | None = None
        if request.write_record:
            record_path = self._loader.artifact_store.write_json_object(
                _record_relative_path(record_id),
                document,
            )

        return BenchmarkRunResult(
            suite_id=suite.suite_id,
            suite_title=suite.title,
            benchmark_kind=benchmark_kind,
            record_id=record_id,
            document=document,
            output_path=output_path,
            record_path=record_path,
        )

    def _resolve_suite(self, suite_id: str) -> BenchmarkSuiteDefinition:
        try:
            return self._loader.load_benchmark_suite_registry().get(suite_id)
        except KeyError as exc:
            raise ValueError(f"Unknown benchmark suite ID: {suite_id}") from exc

    def _load_baseline_record(
        self,
        raw_path: str | Path | None,
    ) -> BenchmarkRecordArtifact | None:
        if raw_path is None:
            return None
        path = Path(raw_path)
        resolved = path if path.is_absolute() else self._loader.resolve_path(str(path))
        try:
            loaded = json.loads(resolved.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"Baseline benchmark record does not exist: {raw_path}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Baseline benchmark record is not valid JSON: {raw_path}") from exc
        if not isinstance(loaded, dict):
            raise ValueError(
                f"Baseline benchmark record must be a top-level JSON object: {raw_path}"
            )
        try:
            self._loader.schema_store.validate_instance(
                loaded,
                schema_id=_BENCHMARK_RECORD_SCHEMA_ID,
            )
        except ValidationError as exc:
            raise ValueError(
                f"Baseline benchmark record failed schema validation: {raw_path}: {exc.message}"
            ) from exc
        return BenchmarkRecordArtifact.from_document(
            loaded,
            doc_path=_logical_or_absolute_path(self._loader, resolved),
        )

    def _validate_baseline_compatibility(
        self,
        suite: BenchmarkSuiteDefinition,
        baseline_record: BenchmarkRecordArtifact | None,
    ) -> None:
        if baseline_record is None:
            return
        if baseline_record.suite_id != suite.suite_id:
            raise ValueError(
                "Baseline benchmark record suite ID does not match the requested suite: "
                f"{baseline_record.suite_id} != {suite.suite_id}"
            )
        baseline_command_ids = tuple(command.command_id for command in baseline_record.commands)
        suite_command_ids = tuple(command.command_id for command in suite.commands)
        if baseline_command_ids != suite_command_ids:
            raise ValueError(
                "Baseline benchmark record command IDs do not match the requested suite."
            )

    def _run_benchmark_command(
        self,
        *,
        suite: BenchmarkSuiteDefinition,
        command_definition: BenchmarkSuiteCommandDefinition,
        warmup_runs: int,
        measured_runs: int,
        baseline_command: BenchmarkCommandRecord | None,
    ) -> _BenchmarkCommandExecution:
        if warmup_runs < 0:
            raise ValueError("Benchmark warmup runs must be zero or greater.")
        if measured_runs < 1:
            raise ValueError("Benchmark measured runs must be at least one.")

        telemetry_on_runs: list[float] = []
        telemetry_off_runs: list[float] = []
        telemetry_on_hotspots: dict[tuple[str, str], list[float]] = {}
        total_runs = warmup_runs + measured_runs
        working_directory = self._loader.resolve_path(suite.working_directory)

        for run_index in range(total_runs):
            with tempfile.TemporaryDirectory(prefix="watchtower_benchmark_on_") as temp_root:
                elapsed_ms, telemetry_path = _run_subprocess_command(
                    argv=command_definition.argv,
                    working_directory=working_directory,
                    env_overrides={
                        TELEMETRY_ENV_VAR: "on",
                        TELEMETRY_STDERR_ENV_VAR: "off",
                        TELEMETRY_DIR_ENV_VAR: temp_root,
                    },
                    require_telemetry=True,
                )
                if run_index >= warmup_runs:
                    telemetry_on_runs.append(elapsed_ms)
                    if telemetry_path is None:
                        raise ValueError(
                            "Benchmark command required telemetry output but no telemetry "
                            "JSONL path was returned."
                        )
                    for key, duration_ms in _extract_hotspots_from_telemetry(telemetry_path):
                        telemetry_on_hotspots.setdefault(key, []).append(duration_ms)

            elapsed_ms, _ = _run_subprocess_command(
                argv=command_definition.argv,
                working_directory=working_directory,
                env_overrides={
                    TELEMETRY_ENV_VAR: "off",
                    TELEMETRY_STDERR_ENV_VAR: "off",
                },
                require_telemetry=False,
            )
            if run_index >= warmup_runs:
                telemetry_off_runs.append(elapsed_ms)

        median_on = _rounded(statistics.median(telemetry_on_runs))
        median_off = _rounded(statistics.median(telemetry_off_runs))
        document: dict[str, Any] = {
            "command_id": command_definition.command_id,
            "title": command_definition.title,
            "description": command_definition.description,
            "command": " ".join(command_definition.argv),
            "argv": list(command_definition.argv),
            "warmup_runs": warmup_runs,
            "measured_runs": measured_runs,
            "telemetry_on_runs_ms": [_rounded(value) for value in telemetry_on_runs],
            "telemetry_off_runs_ms": [_rounded(value) for value in telemetry_off_runs],
            "median_ms_telemetry_on": median_on,
            "median_ms_telemetry_off": median_off,
            "delta_ms": _rounded(median_on - median_off),
            "ratio_on_over_off": _ratio_on_over_off(median_on, median_off),
            "top_nested_operations": _top_nested_operation_documents(telemetry_on_hotspots),
        }
        if baseline_command is not None:
            document["comparison"] = {
                "baseline_telemetry_on_median_ms": baseline_command.median_ms_telemetry_on,
                "current_telemetry_on_median_ms": median_on,
                "telemetry_on_change_ms": _rounded(
                    median_on - baseline_command.median_ms_telemetry_on
                ),
                "telemetry_on_change_percent": _percent_change(
                    baseline_command.median_ms_telemetry_on,
                    median_on,
                ),
                "baseline_telemetry_off_median_ms": baseline_command.median_ms_telemetry_off,
                "current_telemetry_off_median_ms": median_off,
                "telemetry_off_change_ms": _rounded(
                    median_off - baseline_command.median_ms_telemetry_off
                ),
                "telemetry_off_change_percent": _percent_change(
                    baseline_command.median_ms_telemetry_off,
                    median_off,
                ),
            }
        return _BenchmarkCommandExecution(document=document)

    def _validate_benchmark_record(self, document: dict[str, Any]) -> None:
        try:
            self._loader.schema_store.validate_instance(document)
        except ValidationError as exc:
            raise ValueError(f"Generated benchmark record failed schema validation: {exc.message}") from exc


def _run_subprocess_command(
    *,
    argv: tuple[str, ...],
    working_directory: Path,
    env_overrides: dict[str, str],
    require_telemetry: bool,
) -> tuple[float, Path | None]:
    executed_argv = _executable_argv(argv)
    env = os.environ.copy()
    env.update(env_overrides)
    if not require_telemetry:
        env.pop(TELEMETRY_DIR_ENV_VAR, None)
    started_ns = time_perf_counter_ns()
    completed = subprocess.run(
        executed_argv,
        cwd=working_directory,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    elapsed_ms = _rounded((time_perf_counter_ns() - started_ns) / 1_000_000)
    if completed.returncode != 0:
        raise ValueError(
            "Benchmark command failed: "
            f"{' '.join(argv)} (exit={completed.returncode})\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    if not require_telemetry:
        return elapsed_ms, None
    telemetry_root = Path(env_overrides[TELEMETRY_DIR_ENV_VAR])
    jsonl_paths = sorted(path for path in telemetry_root.rglob("*.jsonl") if path.is_file())
    if len(jsonl_paths) != 1:
        raise ValueError(
            "Telemetry-on benchmark runs must produce exactly one JSONL file: "
            f"{' '.join(argv)} produced {len(jsonl_paths)} files under {telemetry_root}"
        )
    return elapsed_ms, jsonl_paths[0]


def _executable_argv(argv: tuple[str, ...]) -> list[str]:
    if argv and argv[0] == "watchtower-core":
        return [sys.executable, "-m", _BENCHMARK_COMMAND_MODULE, *argv[1:]]
    return list(argv)


def _extract_hotspots_from_telemetry(path: Path) -> tuple[tuple[tuple[str, str], float], ...]:
    hotspots: list[tuple[tuple[str, str], float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        loaded = json.loads(line)
        if loaded.get("record_type") != "operation_result":
            continue
        operation_kind = loaded.get("operation_kind")
        operation_name = loaded.get("operation_name")
        duration_ms = loaded.get("duration_ms")
        if not isinstance(operation_kind, str) or not isinstance(operation_name, str):
            continue
        if operation_kind == "cli_command":
            continue
        if not isinstance(duration_ms, int | float):
            continue
        hotspots.append(((operation_kind, operation_name), float(duration_ms)))
    return tuple(hotspots)


def _top_nested_operation_documents(
    hotspots: dict[tuple[str, str], list[float]],
) -> list[dict[str, object]]:
    ranked: list[BenchmarkNestedOperation] = []
    for (operation_kind, operation_name), durations in hotspots.items():
        ranked.append(
            BenchmarkNestedOperation(
                operation_kind=operation_kind,
                operation_name=operation_name,
                median_duration_ms=_rounded(statistics.median(durations)),
            )
        )
    ranked.sort(
        key=lambda entry: (
            -entry.median_duration_ms,
            entry.operation_kind,
            entry.operation_name,
        )
    )
    return [
        {
            "operation_kind": entry.operation_kind,
            "operation_name": entry.operation_name,
            "median_duration_ms": entry.median_duration_ms,
        }
        for entry in ranked[:_BENCHMARK_TOP_NESTED_OPERATION_LIMIT]
    ]


def _environment_context_document(repo_root: Path) -> dict[str, object]:
    git_commit = _git_output(repo_root, "rev-parse", "HEAD")
    status_output = _git_output(repo_root, "status", "--porcelain")
    return {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "git_commit": git_commit,
        "worktree_dirty": bool(status_output.strip()) if status_output is not None else None,
    }


def _git_output(repo_root: Path, *args: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _default_record_id(
    *,
    suite_id: str,
    benchmark_kind: str,
    recorded_at: datetime,
) -> str:
    suite_suffix = suite_id.split(".", maxsplit=2)[-1].replace(".", "_")
    timestamp = recorded_at.strftime("%Y%m%dt%H%M%Sz").lower()
    return f"benchmark.{suite_suffix}.{timestamp}_{benchmark_kind}"


def _record_relative_path(record_id: str) -> str:
    filename = record_id.replace(".", "_") + ".json"
    return f"{BENCHMARK_RECORDS_DIRECTORY}/{filename}"


def _logical_or_absolute_path(loader: ControlPlaneLoader, path: Path) -> str:
    try:
        return loader.workspace_config.logical_path_for(path)
    except ValueError:
        return str(path)


def _format_timestamp(value: datetime) -> str:
    normalized = value.astimezone(UTC).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def _rounded(value: float) -> float:
    return round(float(value), 3)


def _percent_change(baseline: float, current: float) -> float | None:
    if baseline <= 0:
        return None
    return _rounded(((current - baseline) / baseline) * 100)


def _ratio_on_over_off(median_on: float, median_off: float) -> float:
    if median_off <= 0:
        raise ValueError("Telemetry-off median duration must be greater than zero.")
    return _rounded(median_on / median_off)


def time_perf_counter_ns() -> int:
    """Indirection for perf_counter_ns so unit tests can patch it cleanly."""

    import time

    return time.perf_counter_ns()


__all__ = [
    "BENCHMARK_RECORDS_DIRECTORY",
    "BenchmarkRunRequest",
    "BenchmarkRunResult",
    "BenchmarkRunner",
]
