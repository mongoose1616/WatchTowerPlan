"""Registration helpers for planning-record query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.query_records_handlers import (
    _run_query_acceptance,
    _run_query_decisions,
    _run_query_designs,
    _run_query_evidence,
    _run_query_prds,
)


def register_query_record_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register planning-record query commands."""
    query_prds_parser = query_subparsers.add_parser(
        "prds",
        help="Search the PRD index.",
        description=dedent(
            """
            Search the PRD index for governed product requirements documents.

            Use this when you need to find a PRD by trace, requirement ID,
            acceptance ID, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query prds --trace-id trace.core_python_foundation",
            "uv run watchtower-core query prds --requirement-id req.core_python_foundation.003 "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_prds_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed PRD fields such as IDs, title, "
            "summary, tags, and linked surfaces."
        ),
    )
    query_prds_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_prds_parser.add_argument(
        "--tag",
        help="Exact tag filter.",
    )
    query_prds_parser.add_argument(
        "--requirement-id",
        help="Exact requirement-ID filter such as req.core_python_foundation.003.",
    )
    query_prds_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.core_python_foundation.002.",
    )
    query_prds_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_prds_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_prds_parser.set_defaults(handler=_run_query_prds)

    query_decisions_parser = query_subparsers.add_parser(
        "decisions",
        help="Search the decision index.",
        description=dedent(
            """
            Search the decision index for governed durable decision records.

            Use this when you need to find a decision by trace, decision status,
            linked PRD, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query decisions --decision-status accepted",
            "uv run watchtower-core query decisions --linked-prd-id prd.core_python_foundation "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_decisions_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed decision fields such as IDs, title, "
            "summary, tags, and linked surfaces."
        ),
    )
    query_decisions_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_decisions_parser.add_argument(
        "--decision-status",
        help="Exact decision-status filter such as accepted or proposed.",
    )
    query_decisions_parser.add_argument(
        "--tag",
        help="Exact tag filter.",
    )
    query_decisions_parser.add_argument(
        "--linked-prd-id",
        help="Exact linked PRD filter such as prd.core_python_foundation.",
    )
    query_decisions_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_decisions_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_decisions_parser.set_defaults(handler=_run_query_decisions)

    query_designs_parser = query_subparsers.add_parser(
        "designs",
        help="Search the design-document index.",
        description=dedent(
            """
            Search the design-document index for governed feature designs and
            implementation plans.

            Use this when you need to find designs by trace, family, tag, or
            free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query designs --family feature_design",
            "uv run watchtower-core query designs --trace-id trace.core_python_foundation "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_designs_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed design fields such as IDs, title, "
            "summary, tags, and linked paths."
        ),
    )
    query_designs_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_designs_parser.add_argument(
        "--family",
        help="Exact design-family filter such as feature_design or implementation_plan.",
    )
    query_designs_parser.add_argument(
        "--tag",
        help="Exact tag filter.",
    )
    query_designs_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_designs_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_designs_parser.set_defaults(handler=_run_query_designs)

    query_acceptance_parser = query_subparsers.add_parser(
        "acceptance",
        help="Search governed acceptance contracts.",
        description=dedent(
            """
            Search governed acceptance contracts by trace, source PRD, or
            acceptance ID.

            Use this when you need the machine-readable acceptance boundary for
            a traced initiative without opening the raw contract JSON by hand.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core query acceptance --acceptance-id "
            "ac.core_python_foundation.002 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_acceptance_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_acceptance_parser.add_argument(
        "--source-prd-id",
        help="Exact source PRD filter such as prd.core_python_foundation.",
    )
    query_acceptance_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.core_python_foundation.002.",
    )
    query_acceptance_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_acceptance_parser.set_defaults(handler=_run_query_acceptance)

    query_evidence_parser = query_subparsers.add_parser(
        "evidence",
        help="Search governed validation evidence.",
        description=dedent(
            """
            Search governed validation-evidence artifacts by trace, overall
            result, acceptance ID, or validator ID.

            Use this when you need to inspect durable validation proof without
            opening the raw ledger JSON directly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query evidence --trace-id trace.core_python_foundation",
            "uv run watchtower-core query evidence --acceptance-id "
            "ac.core_python_foundation.003 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_evidence_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_evidence_parser.add_argument(
        "--result",
        help="Exact overall-result filter such as passed or failed.",
    )
    query_evidence_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.core_python_foundation.003.",
    )
    query_evidence_parser.add_argument(
        "--validator-id",
        help="Exact validator-ID filter such as validator.control_plane.traceability_index.",
    )
    query_evidence_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_evidence_parser.set_defaults(handler=_run_query_evidence)
