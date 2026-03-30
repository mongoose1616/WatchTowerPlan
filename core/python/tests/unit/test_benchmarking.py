from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.unit.control_plane_loader_test_support import copy_validation_repo_subset
from watchtower_core.benchmarking.runner import BenchmarkRunner, BenchmarkRunRequest
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _write_minimal_benchmark_suite_registry(repo_root: Path, *, suite_id: str) -> None:
    document = {
        "$schema": "urn:watchtower:schema:artifacts:registries:benchmark-suite-registry:v1",
        "id": "registry.benchmark_suites",
        "title": "Benchmark Suite Registry",
        "status": "active",
        "suites": [
            {
                "id": suite_id,
                "title": "Benchmark Fixture Suite",
                "description": "Minimal benchmark fixture suite.",
                "status": "active",
                "working_directory": "core/python",
                "warmup_runs": 1,
                "measured_runs": 2,
                "commands": [
                    {
                        "id": "step.benchmark.fixture",
                        "title": "Fixture Command",
                        "description": "Fixture benchmark command.",
                        "argv": ["watchtower-core", "doctor"],
                    }
                ],
            }
        ],
    }
    target = repo_root / "core/control_plane/registries/benchmark_suite_registry.json"
    target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def _write_baseline_record(repo_root: Path, *, suite_id: str) -> Path:
    document = {
        "$schema": "urn:watchtower:schema:artifacts:records:benchmark-record:v1",
        "id": "benchmark.fixture.previous",
        "title": "Previous Fixture Benchmark",
        "status": "active",
        "benchmark_kind": "baseline",
        "suite_id": suite_id,
        "suite_title": "Benchmark Fixture Suite",
        "recorded_at": "2026-03-29T12:00:00Z",
        "working_directory": "core/python",
        "benchmark_contract": {
            "working_directory": "core/python",
            "warmup_runs": 1,
            "measured_runs": 2,
            "execution_mode": "serialized_subprocess",
            "failure_posture": "fail_closed",
            "telemetry_environment": {
                "telemetry_on": {
                    "WATCHTOWER_TELEMETRY": "on",
                    "WATCHTOWER_TELEMETRY_STDERR": "off",
                    "WATCHTOWER_TELEMETRY_DIR": "<temp benchmark dir>",
                },
                "telemetry_off": {
                    "WATCHTOWER_TELEMETRY": "off",
                    "WATCHTOWER_TELEMETRY_STDERR": "off",
                },
            },
        },
        "environment_context": {
            "python_version": "3.12.0",
            "python_executable": "/tmp/python",
            "platform": "linux-test",
        },
        "commands": [
            {
                "command_id": "step.benchmark.fixture",
                "title": "Fixture Command",
                "description": "Fixture benchmark command.",
                "command": "watchtower-core doctor",
                "argv": ["watchtower-core", "doctor"],
                "warmup_runs": 1,
                "measured_runs": 2,
                "telemetry_on_runs_ms": [8.0, 8.0],
                "telemetry_off_runs_ms": [4.0, 4.0],
                "median_ms_telemetry_on": 8.0,
                "median_ms_telemetry_off": 4.0,
                "delta_ms": 4.0,
                "ratio_on_over_off": 2.0,
                "top_nested_operations": [],
            }
        ],
    }
    target = repo_root / "baseline_record.json"
    target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
    return target


def test_benchmark_runner_excludes_warmups_and_builds_comparison(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    suite_id = "suite.benchmark.fixture"
    _write_minimal_benchmark_suite_registry(repo_root, suite_id=suite_id)
    baseline_path = _write_baseline_record(repo_root, suite_id=suite_id)
    loader = ControlPlaneLoader(repo_root)
    runner = BenchmarkRunner(loader)

    elapsed_values = iter((1.0, 2.0, 10.0, 5.0, 20.0, 10.0))
    hotspot_values = iter(
        (
            (((("cli_stage", "parser_build"), 3.0)),),
            (((("cli_stage", "parser_build"), 6.0)),),
        )
    )

    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner._environment_context_document",
        lambda repo_root: {
            "python_version": "3.12.0",
            "python_executable": "/tmp/python",
            "platform": "linux-test",
        },
    )

    def _fake_run_subprocess_command(**kwargs):
        elapsed = next(elapsed_values)
        telemetry_path = repo_root / "dummy.jsonl" if kwargs["require_telemetry"] else None
        return elapsed, telemetry_path

    def _fake_extract_hotspots(path: Path):
        return next(hotspot_values)

    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner._run_subprocess_command",
        _fake_run_subprocess_command,
    )
    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner._extract_hotspots_from_telemetry",
        _fake_extract_hotspots,
    )

    result = runner.run(
        BenchmarkRunRequest(
            suite_id=suite_id,
            baseline_record_path=baseline_path,
            output_path=tmp_path / "benchmark_output.json",
        )
    )

    command = result.document["commands"][0]
    assert command["telemetry_on_runs_ms"] == [10.0, 20.0]
    assert command["telemetry_off_runs_ms"] == [5.0, 10.0]
    assert command["median_ms_telemetry_on"] == 15.0
    assert command["median_ms_telemetry_off"] == 7.5
    assert command["comparison"]["baseline_telemetry_on_median_ms"] == 8.0
    assert command["comparison"]["current_telemetry_on_median_ms"] == 15.0
    assert result.output_path == (tmp_path / "benchmark_output.json").resolve()


def test_benchmark_runner_writes_canonical_record(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    suite_id = "suite.benchmark.fixture"
    _write_minimal_benchmark_suite_registry(repo_root, suite_id=suite_id)
    loader = ControlPlaneLoader(repo_root)
    runner = BenchmarkRunner(loader)

    elapsed_values = iter((1.0, 1.0, 2.0, 1.5, 3.0, 2.5))
    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner._environment_context_document",
        lambda repo_root: {
            "python_version": "3.12.0",
            "python_executable": "/tmp/python",
            "platform": "linux-test",
        },
    )
    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner._run_subprocess_command",
        lambda **kwargs: (
            next(elapsed_values),
            repo_root / "dummy.jsonl" if kwargs["require_telemetry"] else None,
        ),
    )
    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner._extract_hotspots_from_telemetry",
        lambda path: (),
    )

    result = runner.run(
        BenchmarkRunRequest(
            suite_id=suite_id,
            write_record=True,
            record_id="benchmark.fixture.current",
        )
    )

    assert result.record_path is not None
    assert result.record_path.exists()
    written = json.loads(result.record_path.read_text(encoding="utf-8"))
    assert written["id"] == "benchmark.fixture.current"


def test_benchmark_runner_rejects_mismatched_baseline_suite(
    tmp_path: Path,
) -> None:
    repo_root = copy_validation_repo_subset(tmp_path)
    _write_minimal_benchmark_suite_registry(repo_root, suite_id="suite.benchmark.fixture")
    baseline_path = _write_baseline_record(repo_root, suite_id="suite.benchmark.other")
    runner = BenchmarkRunner(ControlPlaneLoader(repo_root))

    with pytest.raises(ValueError, match="suite ID does not match"):
        runner.run(
            BenchmarkRunRequest(
                suite_id="suite.benchmark.fixture",
                baseline_record_path=baseline_path,
            )
        )


def test_benchmark_runner_fails_closed_when_telemetry_file_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Completed:
        returncode = 0
        stdout = ""
        stderr = ""

    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner.subprocess.run",
        lambda *args, **kwargs: _Completed(),
    )
    monkeypatch.setattr(
        "watchtower_core.benchmarking.runner.time_perf_counter_ns",
        lambda: 1_000_000,
    )

    with pytest.raises(ValueError, match="exactly one JSONL file"):
        from watchtower_core.benchmarking.runner import _run_subprocess_command

        _run_subprocess_command(
            argv=("watchtower-core", "doctor"),
            working_directory=tmp_path,
            env_overrides={
                "WATCHTOWER_TELEMETRY": "on",
                "WATCHTOWER_TELEMETRY_STDERR": "off",
                "WATCHTOWER_TELEMETRY_DIR": str(tmp_path / "telemetry"),
            },
            require_telemetry=True,
        )
