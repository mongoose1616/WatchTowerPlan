from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tests.cli_command_helpers import run_json_command
from watchtower_host.cli.main import main
from watchtower_host.cli import benchmark_handlers, query_records_handlers


def test_benchmark_run_supports_json_output(monkeypatch, capsys, tmp_path: Path) -> None:
    class FakeRunner:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def run(self, request: object) -> SimpleNamespace:
            return SimpleNamespace(
                suite_id="suite.benchmark.core_cli_representative_v1",
                suite_title="Core CLI Representative Benchmark Suite",
                benchmark_kind="baseline",
                record_id="benchmark.core_cli_representative_v1.20260329_baseline",
                output_path=tmp_path / "benchmark.json",
                record_path=tmp_path / "benchmark_record.json",
                document={
                    "commands": [
                        {
                            "command_id": "step.benchmark.fixture",
                            "median_ms_telemetry_on": 10.0,
                            "median_ms_telemetry_off": 8.0,
                            "delta_ms": 2.0,
                        }
                    ]
                },
            )

    monkeypatch.setattr(benchmark_handlers, "BenchmarkRunner", FakeRunner)
    monkeypatch.setattr(benchmark_handlers, "ControlPlaneLoader", lambda: object())

    result, payload = run_json_command(capsys, ["benchmark", "run"])

    assert result == 0
    assert payload["command"] == "watchtower-core benchmark run"
    assert payload["status"] == "ok"
    assert payload["record_id"] == "benchmark.core_cli_representative_v1.20260329_baseline"
    assert payload["benchmark_record"]["commands"][0]["command_id"] == "step.benchmark.fixture"


def test_query_benchmarks_supports_json_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (
                SimpleNamespace(
                    record_id="benchmark.core_cli_representative_v1.20260329_baseline",
                    title="Core CLI Representative Benchmark Suite Baseline",
                    status="active",
                    benchmark_kind="baseline",
                    suite_id="suite.benchmark.core_cli_representative_v1",
                    suite_title="Core CLI Representative Benchmark Suite",
                    recorded_at="2026-03-29T12:30:00Z",
                    doc_path="core/control_plane/records/benchmarks/benchmark_core_cli_representative_v1_20260329_baseline.json",
                    commands=(object(),),
                    baseline_record_path=None,
                ),
            )

    monkeypatch.setattr(query_records_handlers, "BenchmarkRecordQueryService", FakeService)
    monkeypatch.setattr(query_records_handlers, "ControlPlaneLoader", lambda: object())

    result, payload = run_json_command(
        capsys,
        ["query", "benchmarks", "--suite-id", "suite.benchmark.core_cli_representative_v1"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query benchmarks"
    assert payload["status"] == "ok"
    assert payload["result_count"] == 1
    assert (
        payload["results"][0]["record_id"]
        == "benchmark.core_cli_representative_v1.20260329_baseline"
    )


def test_benchmark_help_lists_run_leaf(capsys) -> None:
    result = main(["benchmark"])

    help_text = capsys.readouterr().out
    assert result == 0
    assert "run" in help_text
