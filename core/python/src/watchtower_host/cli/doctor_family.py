"""Doctor command family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)


def register_doctor_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the top-level doctor command."""
    from watchtower_host.cli.doctor_handlers import _run_doctor

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Run a lightweight workspace health snapshot.",
        description=dedent(
            """
            Run a small, low-risk workspace health snapshot that confirms the
            core Python CLI is installed and that the main governed lookup
            surfaces load successfully.

            Start here if you are new to the workspace or want the simplest
            successful `watchtower-core` invocation.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core doctor",
            "uv run watchtower-core doctor --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_human_json_format_argument(doctor_parser)
    doctor_parser.set_defaults(handler=_run_doctor)
