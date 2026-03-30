"""Typed models for benchmark registries and benchmark record artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BenchmarkNestedOperation:
    """Hot nested operation observed during telemetry-on benchmark runs."""

    operation_kind: str
    operation_name: str
    median_duration_ms: float

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkNestedOperation:
        return cls(
            operation_kind=document["operation_kind"],
            operation_name=document["operation_name"],
            median_duration_ms=float(document["median_duration_ms"]),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkCommandComparison:
    """Optional baseline-versus-current benchmark comparison."""

    baseline_telemetry_on_median_ms: float
    current_telemetry_on_median_ms: float
    telemetry_on_change_ms: float
    telemetry_on_change_percent: float | None
    baseline_telemetry_off_median_ms: float
    current_telemetry_off_median_ms: float
    telemetry_off_change_ms: float
    telemetry_off_change_percent: float | None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkCommandComparison:
        return cls(
            baseline_telemetry_on_median_ms=float(document["baseline_telemetry_on_median_ms"]),
            current_telemetry_on_median_ms=float(document["current_telemetry_on_median_ms"]),
            telemetry_on_change_ms=float(document["telemetry_on_change_ms"]),
            telemetry_on_change_percent=(
                float(document["telemetry_on_change_percent"])
                if document.get("telemetry_on_change_percent") is not None
                else None
            ),
            baseline_telemetry_off_median_ms=float(document["baseline_telemetry_off_median_ms"]),
            current_telemetry_off_median_ms=float(document["current_telemetry_off_median_ms"]),
            telemetry_off_change_ms=float(document["telemetry_off_change_ms"]),
            telemetry_off_change_percent=(
                float(document["telemetry_off_change_percent"])
                if document.get("telemetry_off_change_percent") is not None
                else None
            ),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkCommandRecord:
    """Measured results for one benchmark suite command."""

    command_id: str
    title: str
    description: str
    command: str
    argv: tuple[str, ...]
    warmup_runs: int
    measured_runs: int
    telemetry_on_runs_ms: tuple[float, ...]
    telemetry_off_runs_ms: tuple[float, ...]
    median_ms_telemetry_on: float
    median_ms_telemetry_off: float
    delta_ms: float
    ratio_on_over_off: float
    top_nested_operations: tuple[BenchmarkNestedOperation, ...]
    comparison: BenchmarkCommandComparison | None = None
    notes: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkCommandRecord:
        comparison_document = document.get("comparison")
        return cls(
            command_id=document["command_id"],
            title=document["title"],
            description=document["description"],
            command=document["command"],
            argv=tuple(document["argv"]),
            warmup_runs=int(document["warmup_runs"]),
            measured_runs=int(document["measured_runs"]),
            telemetry_on_runs_ms=tuple(float(value) for value in document["telemetry_on_runs_ms"]),
            telemetry_off_runs_ms=tuple(
                float(value) for value in document["telemetry_off_runs_ms"]
            ),
            median_ms_telemetry_on=float(document["median_ms_telemetry_on"]),
            median_ms_telemetry_off=float(document["median_ms_telemetry_off"]),
            delta_ms=float(document["delta_ms"]),
            ratio_on_over_off=float(document["ratio_on_over_off"]),
            top_nested_operations=tuple(
                BenchmarkNestedOperation.from_document(entry)
                for entry in document.get("top_nested_operations", ())
            ),
            comparison=(
                BenchmarkCommandComparison.from_document(comparison_document)
                if isinstance(comparison_document, dict)
                else None
            ),
            notes=tuple(document.get("notes", ())),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkModeEnvironment:
    """Environment variables applied to one benchmark mode."""

    telemetry_on: tuple[tuple[str, str], ...]
    telemetry_off: tuple[tuple[str, str], ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkModeEnvironment:
        def _pairs(key: str) -> tuple[tuple[str, str], ...]:
            mapping = document[key]
            return tuple(sorted((str(name), str(value)) for name, value in mapping.items()))

        return cls(
            telemetry_on=_pairs("telemetry_on"),
            telemetry_off=_pairs("telemetry_off"),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkContract:
    """Benchmark execution contract recorded with one benchmark artifact."""

    working_directory: str
    warmup_runs: int
    measured_runs: int
    execution_mode: str
    failure_posture: str
    telemetry_environment: BenchmarkModeEnvironment
    notes: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkContract:
        return cls(
            working_directory=document["working_directory"],
            warmup_runs=int(document["warmup_runs"]),
            measured_runs=int(document["measured_runs"]),
            execution_mode=document["execution_mode"],
            failure_posture=document["failure_posture"],
            telemetry_environment=BenchmarkModeEnvironment.from_document(
                document["telemetry_environment"]
            ),
            notes=tuple(document.get("notes", ())),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkEnvironmentContext:
    """Captured repo and runtime environment metadata for one benchmark run."""

    python_version: str
    python_executable: str
    platform: str
    cpu_count: int | None = None
    git_commit: str | None = None
    worktree_dirty: bool | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkEnvironmentContext:
        return cls(
            python_version=document["python_version"],
            python_executable=document["python_executable"],
            platform=document["platform"],
            cpu_count=(
                int(document["cpu_count"]) if document.get("cpu_count") is not None else None
            ),
            git_commit=document.get("git_commit"),
            worktree_dirty=(
                bool(document["worktree_dirty"])
                if document.get("worktree_dirty") is not None
                else None
            ),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkRecordArtifact:
    """Typed retained benchmark record artifact."""

    schema_id: str
    record_id: str
    title: str
    status: str
    benchmark_kind: str
    suite_id: str
    suite_title: str
    recorded_at: str
    working_directory: str
    doc_path: str
    benchmark_contract: BenchmarkContract
    environment_context: BenchmarkEnvironmentContext
    commands: tuple[BenchmarkCommandRecord, ...]
    baseline_record_path: str | None = None
    notes: tuple[str, ...] = ()

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        *,
        doc_path: str,
    ) -> BenchmarkRecordArtifact:
        return cls(
            schema_id=document["$schema"],
            record_id=document["id"],
            title=document["title"],
            status=document["status"],
            benchmark_kind=document["benchmark_kind"],
            suite_id=document["suite_id"],
            suite_title=document["suite_title"],
            recorded_at=document["recorded_at"],
            working_directory=document["working_directory"],
            doc_path=doc_path,
            benchmark_contract=BenchmarkContract.from_document(document["benchmark_contract"]),
            environment_context=BenchmarkEnvironmentContext.from_document(
                document["environment_context"]
            ),
            commands=tuple(
                BenchmarkCommandRecord.from_document(entry) for entry in document["commands"]
            ),
            baseline_record_path=document.get("baseline_record_path"),
            notes=tuple(document.get("notes", ())),
        )
