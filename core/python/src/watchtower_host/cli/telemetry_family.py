"""Telemetry command-family registration."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    add_pack_settings_argument,
    examples,
)


def register_telemetry_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the telemetry command family and its subcommands."""

    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.telemetry_handlers import _run_telemetry_delete

    telemetry_parser = subparsers.add_parser(
        "telemetry",
        help="Inspect and clean local runtime telemetry sinks.",
        description=dedent(
            """
            Inspect and clean local runtime telemetry machine state.

            Use this command family when runtime telemetry files have
            accumulated under one pack machine root and you need a governed,
            dry-run-first cleanup path rather than ad hoc filesystem removal.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core telemetry --help",
            "uv run watchtower-core telemetry delete --older-than-days 7 --format json",
            (
                "uv run watchtower-core telemetry delete --all "
                "--pack-settings-path <pack-root>/.wt/manifests/pack_settings.json "
                "--write --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    telemetry_subparsers = telemetry_parser.add_subparsers(
        dest="telemetry_command",
        title="telemetry commands",
        metavar="<telemetry_command>",
    )
    telemetry_parser.set_defaults(handler=_run_help, help_parser=telemetry_parser)

    delete_parser = telemetry_subparsers.add_parser(
        "delete",
        help="Delete retained runtime telemetry files under one telemetry root.",
        description=dedent(
            """
            Delete retained runtime telemetry files under one resolved telemetry root.

            The command defaults to dry-run output. Pass `--write` to remove the
            matched JSONL files and any now-empty dated directories beneath the
            telemetry root. The active command's own telemetry file is always
            excluded from deletion.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core telemetry delete --older-than-days 7 --format json",
            "uv run watchtower-core telemetry delete --before 2026-03-01 --format json",
            (
                "uv run watchtower-core telemetry delete --all "
                "--telemetry-root /tmp/watchtower-telemetry/telemetry --write --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_pack_settings_argument(delete_parser)
    delete_parser.add_argument(
        "--telemetry-root",
        type=Path,
        help=(
            "Optional explicit telemetry root directory. The directory name must be `telemetry`."
        ),
    )
    selection_group = delete_parser.add_mutually_exclusive_group(required=True)
    selection_group.add_argument(
        "--older-than-days",
        type=int,
        help="Delete telemetry files whose modified time is older than this many days.",
    )
    selection_group.add_argument(
        "--before",
        help="Delete telemetry files older than this UTC cutoff (ISO timestamp or YYYY-MM-DD).",
    )
    selection_group.add_argument(
        "--all",
        action="store_true",
        help="Match all retained telemetry files under the resolved telemetry root.",
    )
    delete_parser.add_argument(
        "--write",
        action="store_true",
        help="Apply the deletion. Without this flag the command reports a dry-run preview only.",
    )
    add_human_json_format_argument(delete_parser)
    delete_parser.set_defaults(handler=_run_telemetry_delete)
