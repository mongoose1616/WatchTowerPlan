"""Registration helpers for knowledge-oriented query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.query_knowledge_handlers import (
    _run_query_foundations,
    _run_query_references,
    _run_query_standards,
    _run_query_workflows,
)


def register_query_knowledge_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register knowledge-oriented query commands."""
    query_foundations_parser = query_subparsers.add_parser(
        "foundations",
        help="Search the foundation index.",
        description=dedent(
            """
            Search the governed foundation index for repository intent-layer
            documents such as design philosophy, product shape, and technology
            direction.

            Use this when you need to confirm which foundation doc governs an
            area or where a foundation doc is currently cited or applied.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query foundations --audience maintainers",
            "uv run watchtower-core query foundations --applied-by-path "
            "docs/standards/engineering/engineering_best_practices_standard.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_foundations_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed foundation fields such as ID, title, "
            "summary, aliases, and related paths."
        ),
    )
    query_foundations_parser.add_argument(
        "--foundation-id",
        help="Exact foundation identifier such as foundation.engineering_design_principles.",
    )
    query_foundations_parser.add_argument(
        "--audience",
        help="Exact audience filter such as shared, maintainers, or contributors.",
    )
    query_foundations_parser.add_argument(
        "--authority",
        help="Exact authority filter such as authoritative or supporting.",
    )
    query_foundations_parser.add_argument("--tag", help="Exact tag filter.")
    query_foundations_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as core/python/ or workflows/modules/.",
    )
    query_foundations_parser.add_argument(
        "--reference-path",
        help="Exact governed reference-doc filter such as docs/references/uv_reference.md.",
    )
    query_foundations_parser.add_argument(
        "--cited-by-path",
        help="Exact doc-path filter for documents that cite the foundation doc.",
    )
    query_foundations_parser.add_argument(
        "--applied-by-path",
        help=(
            "Exact doc-path filter for documents that apply the foundation doc "
            "in an applied-reference section."
        ),
    )
    query_foundations_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_foundations_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_foundations_parser.set_defaults(handler=_run_query_foundations)

    query_workflows_parser = query_subparsers.add_parser(
        "workflows",
        help="Search the workflow index.",
        description=dedent(
            """
            Search the governed workflow index for workflow modules and the
            standards, references, or canonical files that govern them.

            Use this when you know the behavior or governing surface you need,
            but not yet the exact workflow module name.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query workflows --query validation",
            "uv run watchtower-core query workflows --phase-type reconciliation",
            "uv run watchtower-core query workflows --reference-path "
            "docs/references/github_collaboration_reference.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_workflows_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed workflow fields such as workflow ID, "
            "title, summary, related paths, and references."
        ),
    )
    query_workflows_parser.add_argument(
        "--workflow-id",
        help="Exact workflow identifier such as workflow.code_validation.",
    )
    query_workflows_parser.add_argument(
        "--phase-type",
        help="Exact workflow phase filter such as execution, validation, or reconciliation.",
    )
    query_workflows_parser.add_argument(
        "--task-family",
        help="Exact workflow task-family filter such as engineering_validation or traceability.",
    )
    query_workflows_parser.add_argument(
        "--trigger-tag",
        help="Exact trigger-tag filter such as github, validation, or scope.",
    )
    query_workflows_parser.add_argument(
        "--related-path",
        help=(
            "Exact repository-path filter such as "
            "docs/standards/documentation/workflow_md_standard.md."
        ),
    )
    query_workflows_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "docs/references/github_collaboration_reference.md."
        ),
    )
    query_workflows_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_workflows_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_workflows_parser.set_defaults(handler=_run_query_workflows)

    query_references_parser = query_subparsers.add_parser(
        "references",
        help="Search the reference index.",
        description=dedent(
            """
            Search the governed reference index for curated internal reference
            documents and their upstream authority links.

            Use this when you know the topic you want, but not yet the exact
            reference document path.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query references --query uv",
            "uv run watchtower-core query references --related-path core/python/ --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_references_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed reference fields such as reference ID, "
            "title, summary, upstream URLs, related paths, aliases, and tags."
        ),
    )
    query_references_parser.add_argument(
        "--reference-id",
        help="Exact reference identifier such as ref.uv.",
    )
    query_references_parser.add_argument("--tag", help="Exact tag filter.")
    query_references_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as core/python/ or docs/standards/engineering/.",
    )
    query_references_parser.add_argument(
        "--upstream-url",
        help="Exact canonical-upstream URL filter.",
    )
    query_references_parser.add_argument(
        "--cited-by-path",
        help="Exact doc-path filter for documents that cite the reference.",
    )
    query_references_parser.add_argument(
        "--applied-by-path",
        help=(
            "Exact doc-path filter for documents that apply the reference in an "
            "applied-reference section."
        ),
    )
    query_references_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_references_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_references_parser.set_defaults(handler=_run_query_references)

    query_standards_parser = query_subparsers.add_parser(
        "standards",
        help="Search the standard index.",
        description=dedent(
            """
            Search the governed standard index for repository standards and
            best-practice docs.

            Use this when you need to find standards by category, local
            reference doc, related path, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query standards --category governance",
            "uv run watchtower-core query standards --reference-path "
            "docs/references/github_collaboration_reference.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_standards_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed standard fields such as ID, title, "
            "summary, category, references, and related paths."
        ),
    )
    query_standards_parser.add_argument(
        "--standard-id",
        help="Exact standard identifier such as std.engineering.best_practices.",
    )
    query_standards_parser.add_argument(
        "--category",
        help="Exact top-level standards category such as governance or engineering.",
    )
    query_standards_parser.add_argument("--tag", help="Exact tag filter.")
    query_standards_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as .github/ or core/python/.",
    )
    query_standards_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "docs/references/github_collaboration_reference.md."
        ),
    )
    query_standards_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_standards_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_standards_parser.set_defaults(handler=_run_query_standards)
