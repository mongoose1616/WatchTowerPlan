"""Benchmark command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent
from pathlib import Path

from watchtower_core.cli.common import HelpFormatter, add_human_json_format_argument, examples


def register_benchmark_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the benchmark command family and its subcommands."""

    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.benchmark_handlers import _run_benchmark_run

    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Run governed reusable-core performance benchmarks.",
        description=dedent(
            """
            Run deliberate, fail-closed reusable-core performance benchmarks.

            Use this command family when you need repeatable subprocess timing,
            telemetry-on versus telemetry-off comparison, retained benchmark
            evidence, or governed benchmark suite execution rather than default-on
            runtime telemetry.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core benchmark run --format json",
            "uv run watchtower-core benchmark run --output /tmp/core_cli_benchmark.json --format json",
            "uv run watchtower-core benchmark run --write-record --record-id benchmark.core_cli_representative_v1.20260329_baseline --format json",
        ),
        formatter_class=HelpFormatter,
    )
    benchmark_subparsers = benchmark_parser.add_subparsers(
        dest="benchmark_command",
        title="benchmark commands",
        metavar="<benchmark_command>",
    )
    benchmark_parser.set_defaults(handler=_run_help, help_parser=benchmark_parser)

    run_parser = benchmark_subparsers.add_parser(
        "run",
        help="Run one governed benchmark suite and optionally retain the result.",
        description=dedent(
            """
            Run one governed benchmark suite through fresh serialized subprocesses.

            The runner compares telemetry-on and telemetry-off timing, extracts
            top nested operations from telemetry JSONL files, validates the
            generated benchmark record, and can write both an explicit output file
            and the canonical retained benchmark-record artifact.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core benchmark run --format json",
            "uv run watchtower-core benchmark run --suite-id suite.benchmark.core_cli_representative_v1 --runs 3 --format json",
            "uv run watchtower-core benchmark run --baseline-record core/control_plane/records/benchmarks/benchmark_core_cli_representative_v1_20260329_baseline.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    run_parser.add_argument(
        "--suite-id",
        default="suite.benchmark.core_cli_representative_v1",
        help="Benchmark suite identifier declared in the benchmark-suite registry.",
    )
    run_parser.add_argument(
        "--runs",
        type=int,
        help="Optional measured-run override applied to each command in the suite.",
    )
    run_parser.add_argument(
        "--warmup-runs",
        type=int,
        help="Optional warmup-run override applied to each command in the suite.",
    )
    run_parser.add_argument(
        "--baseline-record",
        help="Optional prior benchmark record used for baseline-to-current comparison.",
    )
    run_parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Optional explicit output file for the generated benchmark record JSON. "
            "The file is validated before it is written."
        ),
    )
    run_parser.add_argument(
        "--write-record",
        action="store_true",
        help="Write the generated benchmark record to the canonical retained record family.",
    )
    run_parser.add_argument(
        "--record-id",
        help="Optional explicit benchmark record identifier.",
    )
    add_human_json_format_argument(run_parser)
    run_parser.set_defaults(handler=_run_benchmark_run)
