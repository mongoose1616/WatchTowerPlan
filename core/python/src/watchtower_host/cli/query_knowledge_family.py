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
from watchtower_core.query.references import REFERENCE_REPOSITORY_STATUS_VALUES
from watchtower_host.cli.query_knowledge_handlers import (
    _run_query_authority,
    _run_query_foundations,
    _run_query_references,
    _run_query_standards,
    _run_query_templates,
    _run_query_workflows,
)


def register_query_knowledge_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register knowledge-oriented query commands."""
    query_authority_parser = query_subparsers.add_parser(
        "authority",
        help="Search the authority map.",
        description=dedent(
            """
            Search the governed authority map for recurring questions about
            canonical machine surfaces, preferred commands, and fallback human
            guidance.

            Use this first when the question is "what is authoritative here?"
            or "which governed lookup surface should I trust before scanning the
            repository directly?".
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query authority --query canonical",
            "uv run watchtower-core query authority --question-id "
            "authority.governance.template_selection --format json",
            "uv run watchtower-core query authority --artifact-kind template_catalog",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_authority_parser,
        help_text=(
            "Free-text query over authority-map fields such as question ID, "
            "question text, canonical path, preferred command, aliases, and "
            "fallback paths."
        ),
    )
    query_authority_parser.add_argument(
        "--question-id",
        help="Exact authority question filter such as authority.governance.command_lookup.",
    )
    query_authority_parser.add_argument(
        "--domain",
        help="Exact authority domain filter such as governance or planning.",
    )
    query_authority_parser.add_argument(
        "--artifact-kind",
        help="Exact canonical artifact-kind filter such as command_index or template_catalog.",
    )
    add_limit_argument(query_authority_parser)
    add_human_json_format_argument(query_authority_parser)
    query_authority_parser.set_defaults(handler=_run_query_authority)

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
            "core/workflows/modules/, or a pack-owned workflows/modules/ path."
        ),
    )
    query_foundations_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "core/docs/references/uv_reference.md or "
            "<pack>/docs/references/<topic>_reference.md."
        ),
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
            Search the governed workflow index for workflow documents and the
            standards, references, canonical files, or composed modules that
            govern them.

            Use this when you know the behavior or governing surface you need,
            but not yet the exact workflow document name.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query workflows --query validation",
            "uv run watchtower-core query workflows --workflow-kind role",
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
        "--workflow-kind",
        choices=("module", "role"),
        help="Exact workflow kind filter.",
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
            "core/docs/references/github_collaboration_reference.md or "
            "<pack>/docs/references/<topic>_reference.md."
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
            Search the governed reference index for curated shared-core and
            pack-owned reference documents plus their upstream authority links.

            Use this when you know the topic you want, but not yet the exact
            reference document path.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query references --query uv",
            "uv run watchtower-core query references "
            "--repository-status candidate_future_guidance --format json",
            "uv run watchtower-core query references --related-path core/python/ --format json",
            "uv run watchtower-core query references --related-path "
            "<pack>/workflows/modules/<module>.md --format json",
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
            "Repository-path filter such as core/python/, "
            "<pack>/workflows/modules/<module>.md, or "
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
            "core/docs/standards/engineering/, or a pack-owned standards root."
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
            "core/docs/references/github_collaboration_reference.md or "
            "<pack>/docs/references/<topic>_reference.md."
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
            "core/python/src/watchtower_host/cli/parser.py. "
            "Exact file paths match directly, indexed directory paths match "
            "their concrete descendants, and indexed glob patterns match "
            "concrete files such as nested README.md or AGENTS.md surfaces."
        ),
    )
    add_limit_argument(query_standards_parser)
    add_human_json_format_argument(query_standards_parser)
    query_standards_parser.set_defaults(handler=_run_query_standards)

    query_templates_parser = query_subparsers.add_parser(
        "templates",
        help="Search the template catalog.",
        description=dedent(
            """
            Search the governed template catalog for reusable document
            scaffolds, section requirements, allowed roots, and authoring
            guidance.

            Use this before drafting or refreshing a governed document when the
            repository already defines its shape and required sections.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query templates --query standard",
            "uv run watchtower-core query templates --allowed-root core/docs/commands --format json",
            "uv run watchtower-core query templates --family-id workflow --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_templates_parser,
        help_text=(
            "Free-text query over template IDs, template paths, section IDs, "
            "allowed roots, authoring goals, operator notes, and guidance text."
        ),
    )
    query_templates_parser.add_argument(
        "--template-id",
        help="Exact template identifier such as template.core.workflow.module.",
    )
    query_templates_parser.add_argument(
        "--family-id",
        help="Exact documentation-family filter such as workflow.",
    )
    query_templates_parser.add_argument(
        "--surface-id",
        help="Exact rendered or authored surface filter such as surface.documentation.standard.",
    )
    query_templates_parser.add_argument(
        "--authorship-mode",
        choices=("authored", "rendered"),
        help="Exact authorship-mode filter.",
    )
    query_templates_parser.add_argument(
        "--llm-guidance-mode",
        choices=("required", "advisory", "none"),
        help="Exact LLM-guidance-mode filter.",
    )
    query_templates_parser.add_argument(
        "--allowed-root",
        help="Exact allowed-root filter such as core/docs/standards or plan/docs/commands.",
    )
    query_templates_parser.add_argument(
        "--required-section-id",
        help="Exact required-section filter such as operationalization or command.",
    )
    query_templates_parser.add_argument(
        "--required-rendered-surface-id",
        help="Exact required rendered-surface filter when the template binds to rendered companions.",
    )
    add_limit_argument(query_templates_parser)
    add_human_json_format_argument(query_templates_parser)
    query_templates_parser.set_defaults(handler=_run_query_templates)
