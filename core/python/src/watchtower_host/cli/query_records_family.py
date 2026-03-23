"""Registration helpers for planning-record query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)
from watchtower_host.cli.query_records_handlers import (
    _run_query_acceptance,
    _run_query_evidence,
)


def register_query_record_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register machine-record query commands that survive the hard cutover."""

    query_acceptance_parser = query_subparsers.add_parser(
        "acceptance",
        help="Search governed acceptance contracts.",
        description=dedent(
            """
            Search governed acceptance contracts by trace, source surface path, or
            acceptance ID.

            Use this when you need the machine-readable acceptance boundary for
            a traced initiative without opening the raw contract JSON by hand.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query acceptance --trace-id trace.governed_acceptance_example",
            "uv run watchtower-core query acceptance --acceptance-id "
            "ac.governed_acceptance_example.001 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_acceptance_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.governed_acceptance_example.",
    )
    query_acceptance_parser.add_argument(
        "--source-surface-path",
        help=(
            "Exact source surface path filter such as "
            "<pack>/initiatives/example/initiative_brief.md."
        ),
    )
    query_acceptance_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.governed_acceptance_example.001.",
    )
    add_human_json_format_argument(query_acceptance_parser)
    query_acceptance_parser.set_defaults(handler=_run_query_acceptance)

    query_evidence_parser = query_subparsers.add_parser(
        "evidence",
        help="Search governed validation evidence.",
        description=dedent(
            """
            Search governed validation-evidence artifacts by trace, overall
            result, acceptance ID, or validator ID.

            Use this when you need to inspect durable validation proof without
            opening the raw record JSON directly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query evidence --trace-id trace.governed_acceptance_example",
            "uv run watchtower-core query evidence --acceptance-id "
            "ac.governed_acceptance_example.001 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_evidence_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.governed_acceptance_example.",
    )
    query_evidence_parser.add_argument(
        "--result",
        help="Exact overall-result filter such as passed or failed.",
    )
    query_evidence_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.governed_acceptance_example.001.",
    )
    query_evidence_parser.add_argument(
        "--validator-id",
        help="Exact validator-ID filter such as validator.control_plane.traceability_index.",
    )
    add_human_json_format_argument(query_evidence_parser)
    query_evidence_parser.set_defaults(handler=_run_query_evidence)
