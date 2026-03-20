"""Registration helpers for knowledge-oriented query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    add_limit_argument,
    add_query_argument,
    examples,
)
from watchtower_core.cli.query_knowledge_handlers import (
    _run_query_foundations,
    _run_query_references,
    _run_query_standards,
    _run_query_workflows,
)
from watchtower_plan.reference_semantics import REFERENCE_REPOSITORY_STATUS_VALUES


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
            "uv run watchtower-core query foundations --reference-path "
            "core/docs/references/uv_reference.md --format json",
            "uv run watchtower-core query foundations --applied-by-path "
            "core/docs/standards/engineering/engineering_best_practices_standard.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_foundations_parser,
        help_text=(
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
        help="Exact audience filter such as shared.",
    )
    query_foundations_parser.add_argument(
        "--authority",
        help="Exact authority filter such as authoritative or supporting.",
    )
    query_foundations_parser.add_argument("--tag", help="Exact tag filter.")
    query_foundations_parser.add_argument(
        "--related-path",
        help=(
            "Exact repository-path filter such as core/python/, "
            "core/workflows/modules/, or plan/workflows/modules/."
        ),
    )
    query_foundations_parser.add_argument(
        "--reference-path",
        help="Exact governed reference-doc filter such as core/docs/references/uv_reference.md.",
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
    add_limit_argument(query_foundations_parser)
    add_human_json_format_argument(query_foundations_parser)
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
            "core/docs/references/github_collaboration_reference.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_workflows_parser,
        help_text=(
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
            "core/docs/standards/documentation/workflow_md_standard.md."
        ),
    )
    query_workflows_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "core/docs/references/github_collaboration_reference.md."
        ),
    )
    add_limit_argument(query_workflows_parser)
    add_human_json_format_argument(query_workflows_parser)
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
            "uv run watchtower-core query references "
            "--repository-status candidate_future_guidance --format json",
            "uv run watchtower-core query references --related-path core/python/ --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_references_parser,
        help_text=(
            "Free-text query over indexed reference fields such as reference ID, "
            "title, summary, upstream URLs, related paths, aliases, and tags."
        ),
    )
    query_references_parser.add_argument(
        "--reference-id",
        help="Exact reference identifier such as ref.uv.",
    )
    query_references_parser.add_argument(
        "--repository-status",
        choices=REFERENCE_REPOSITORY_STATUS_VALUES,
        help=(
            "Exact repository-status filter such as supporting_authority, "
            "active_support, or candidate_future_guidance."
        ),
    )
    query_references_parser.add_argument("--tag", help="Exact tag filter.")
    query_references_parser.add_argument(
        "--related-path",
        help=(
            "Repository-path filter such as core/python/ or "
            "core/docs/standards/engineering/. Directory paths ending in '/' "
            "match descendant touchpoints."
        ),
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
    add_limit_argument(query_references_parser)
    add_human_json_format_argument(query_references_parser)
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
            "uv run watchtower-core query standards --operationalization-mode validation",
            "uv run watchtower-core query standards --reference-path "
            "core/docs/references/github_collaboration_reference.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_standards_parser,
        help_text=(
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
    query_standards_parser.add_argument(
        "--owner",
        help="Exact owner filter such as repository_maintainer.",
    )
    query_standards_parser.add_argument("--tag", help="Exact tag filter.")
    query_standards_parser.add_argument(
        "--applies-to",
        help=(
            "Exact front-matter applies_to filter such as core/python/, "
            "core/docs/standards/engineering/, or plan/docs/standards/governance/."
        ),
    )
    query_standards_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as .github/ or core/python/.",
    )
    query_standards_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "core/docs/references/github_collaboration_reference.md."
        ),
    )
    query_standards_parser.add_argument(
        "--operationalization-mode",
        help="Exact operationalization-mode filter such as validation, query, or workflow.",
    )
    query_standards_parser.add_argument(
        "--operationalization-path",
        help=(
            "Repository-path filter for one operationalizing surface such as "
            "plan/python/src/watchtower_plan/validation/document_semantics.py. "
            "Exact file paths match directly, indexed directory paths match "
            "their concrete descendants, and indexed glob patterns match "
            "concrete files such as nested README.md or AGENTS.md surfaces."
        ),
    )
    add_limit_argument(query_standards_parser)
    add_human_json_format_argument(query_standards_parser)
    query_standards_parser.set_defaults(handler=_run_query_standards)
