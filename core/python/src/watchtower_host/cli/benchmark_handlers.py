"""Runtime handlers for governed benchmark commands."""

from __future__ import annotations

import argparse

from watchtower_core.benchmarking import BenchmarkRunRequest, BenchmarkRunner
from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _emit_detail_result,
    _resolve_output_path,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _run_benchmark_run(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    output_path = _resolve_output_path(args.output)

    try:
        result = BenchmarkRunner(loader).run(
            BenchmarkRunRequest(
                suite_id=args.suite_id,
                measured_runs=args.runs,
                warmup_runs=args.warmup_runs,
                baseline_record_path=args.baseline_record,
                output_path=output_path,
                write_record=args.write_record,
                record_id=args.record_id,
            )
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core benchmark run",
            str(exc),
            prefix="Benchmark error",
        )

    payload = {
        "command": "watchtower-core benchmark run",
        "status": "ok",
        "suite_id": result.suite_id,
        "suite_title": result.suite_title,
        "benchmark_kind": result.benchmark_kind,
        "record_id": result.record_id,
        "output_path": str(result.output_path) if result.output_path is not None else None,
        "record_path": str(result.record_path) if result.record_path is not None else None,
        "benchmark_record": result.document,
    }
    exit_code = 0

    def _render_human() -> None:
        print(
            f"Ran benchmark suite {result.suite_id} [{result.benchmark_kind}] "
            f"with record ID {result.record_id}."
        )
        if result.output_path is not None:
            print(f"Output: {result.output_path}")
        if result.record_path is not None:
            print(f"Retained record: {result.record_path}")
        for command in result.document["commands"]:
            print(
                f"- {command['command_id']}: on={command['median_ms_telemetry_on']} ms, "
                f"off={command['median_ms_telemetry_off']} ms, "
                f"delta={command['delta_ms']} ms"
            )

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=exit_code,
    )
