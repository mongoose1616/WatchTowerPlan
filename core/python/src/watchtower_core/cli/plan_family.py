"""Planning scaffold command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)


def register_plan_family(subparsers: argparse._SubParsersAction) -> None:
    """Register the plan command family and its subcommands."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_core.cli.plan_handlers import (
        _run_plan_approve,
        _run_plan_bootstrap,
        _run_plan_confirm_inputs,
        _run_plan_scaffold,
    )
    from watchtower_core.repo_ops.planning_scaffolds import PLAN_KIND_CHOICES
    from watchtower_core.repo_ops.task_lifecycle import TASK_KIND_CHOICES, TASK_PRIORITY_CHOICES

    plan_parser = subparsers.add_parser(
        "plan",
        help="Scaffold compact governed planning documents and initiative bootstrap chains.",
        description=dedent(
            """
            Scaffold compact governed planning documents, bootstrap live
            initiative packages, and advance initiative readiness through the
            captured-input and approval gates.

            These commands are dry-run by default. Add `--write` to persist the
            scaffolded documents and refresh the derived planning surfaces.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan scaffold --kind prd --trace-id trace.example "
            "--document-id prd.example --title \"Example PRD\" "
            "--summary \"Frames the example initiative.\" --format json",
            "uv run watchtower-core plan bootstrap --trace-id trace.example "
            "--title \"Example Initiative\" --summary \"Bootstraps the example initiative.\" "
            "--include-decision --write",
            "uv run watchtower-core plan approve --initiative-slug example_initiative --write",
        ),
        formatter_class=HelpFormatter,
    )
    plan_subparsers = plan_parser.add_subparsers(
        dest="plan_command",
        title="plan commands",
        metavar="<plan_command>",
    )
    plan_parser.set_defaults(handler=_run_help, help_parser=plan_parser)

    scaffold_parser = plan_subparsers.add_parser(
        "scaffold",
        help="Scaffold one PRD, feature design, implementation plan, or decision record.",
        description=dedent(
            """
            Scaffold one compact governed planning document using the current
            repository planning shape.

            Optional sections are omitted by default. The scaffold emits one
            compact placeholder per required section when richer inputs are not
            provided.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan scaffold --kind prd --trace-id trace.example "
            "--document-id prd.example --title \"Example PRD\" "
            "--summary \"Frames the example initiative.\"",
            "uv run watchtower-core plan scaffold --kind feature-design --trace-id trace.example "
            "--document-id design.features.example --title \"Example Feature Design\" "
            "--summary \"Defines the example design boundary.\" "
            "--linked-prd prd.example --reference docs/planning/prds/example.md "
            "--include-document --format json",
        ),
        formatter_class=HelpFormatter,
    )
    scaffold_parser.add_argument(
        "--kind",
        required=True,
        choices=PLAN_KIND_CHOICES,
        help="Planning document family to scaffold.",
    )
    scaffold_parser.add_argument("--trace-id", required=True, help="Stable trace identifier.")
    scaffold_parser.add_argument("--document-id", required=True, help="Stable document identifier.")
    scaffold_parser.add_argument("--title", required=True, help="Human-readable document title.")
    scaffold_parser.add_argument(
        "--summary",
        required=True,
        help="One-line document summary used in trackers and indexes.",
    )
    scaffold_parser.add_argument(
        "--owner",
        default="repository_maintainer",
        help="Document owner recorded in front matter.",
    )
    scaffold_parser.add_argument(
        "--status",
        help="Optional explicit document status. Defaults depend on the selected kind.",
    )
    scaffold_parser.add_argument(
        "--applies-to",
        action="append",
        default=[],
        help="Optional applied path or concept. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--alias",
        action="append",
        default=[],
        help="Optional retrieval alias. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--file-stem",
        help="Optional output filename stem. Defaults to a slug derived from the title.",
    )
    scaffold_parser.add_argument(
        "--linked-prd",
        action="append",
        default=[],
        help="Optional linked PRD ID. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--linked-decision",
        action="append",
        default=[],
        help="Optional linked decision ID. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--linked-design",
        action="append",
        default=[],
        help="Optional linked design ID. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--linked-plan",
        action="append",
        default=[],
        help="Optional linked implementation-plan ID. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--linked-acceptance",
        action="append",
        default=[],
        help="Optional linked acceptance-contract ID. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--source-request",
        action="append",
        default=[],
        help="Optional source request or driver. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Optional companion reference or source. Repeat for multiple values.",
    )
    scaffold_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now.",
    )
    scaffold_parser.add_argument(
        "--include-document",
        action="store_true",
        help="Include the rendered document content in the command output.",
    )
    scaffold_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the scaffolded document and refresh derived planning surfaces.",
    )
    add_human_json_format_argument(scaffold_parser)
    scaffold_parser.set_defaults(handler=_run_plan_scaffold)

    bootstrap_parser = plan_subparsers.add_parser(
        "bootstrap",
        help="Scaffold the initial PRD, design, plan, and bootstrap-task chain for one trace.",
        description=dedent(
            """
            Scaffold a compact traced planning chain for one new initiative.

            The bootstrap flow creates a PRD, feature design, implementation
            plan, and one bootstrap task. Add `--include-decision` when you
            want a first decision record in the same chain.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan bootstrap --trace-id trace.example "
            "--title \"Example Initiative\" --summary \"Bootstraps the example initiative.\"",
            "uv run watchtower-core plan bootstrap --trace-id trace.example "
            "--title \"Example Initiative\" --summary \"Bootstraps the example initiative.\" "
            "--include-decision --task-priority high --include-documents --format json",
        ),
        formatter_class=HelpFormatter,
    )
    bootstrap_parser.add_argument("--trace-id", required=True, help="Stable trace identifier.")
    bootstrap_parser.add_argument("--title", required=True, help="Initiative title root.")
    bootstrap_parser.add_argument(
        "--summary",
        required=True,
        help="One-line initiative summary applied to the scaffold chain.",
    )
    bootstrap_parser.add_argument(
        "--owner",
        default="repository_maintainer",
        help="Planning-document owner recorded in front matter.",
    )
    bootstrap_parser.add_argument(
        "--applies-to",
        action="append",
        default=[],
        help="Optional applied path or concept. Repeat for multiple values.",
    )
    bootstrap_parser.add_argument(
        "--alias",
        action="append",
        default=[],
        help="Optional retrieval alias. Repeat for multiple values.",
    )
    bootstrap_parser.add_argument(
        "--file-stem",
        help="Optional shared filename stem for the scaffolded planning documents.",
    )
    bootstrap_parser.add_argument(
        "--include-decision",
        action="store_true",
        help="Also create an initial decision record in the bootstrap chain.",
    )
    bootstrap_parser.add_argument(
        "--decision-id",
        help="Optional explicit decision ID when --include-decision is used.",
    )
    bootstrap_parser.add_argument(
        "--source-request",
        action="append",
        default=[],
        help="Optional source request or driver. Repeat for multiple values.",
    )
    bootstrap_parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Optional companion reference or source. Repeat for multiple values.",
    )
    bootstrap_parser.add_argument(
        "--task-id",
        help="Optional explicit bootstrap task ID. Defaults to task.<trace_suffix>.bootstrap.001.",
    )
    bootstrap_parser.add_argument(
        "--task-owner",
        help="Optional bootstrap task owner. Defaults to --owner.",
    )
    bootstrap_parser.add_argument(
        "--task-kind",
        choices=TASK_KIND_CHOICES,
        default="governance",
        help="Bootstrap task kind.",
    )
    bootstrap_parser.add_argument(
        "--task-priority",
        choices=TASK_PRIORITY_CHOICES,
        default="medium",
        help="Bootstrap task priority.",
    )
    bootstrap_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now.",
    )
    bootstrap_parser.add_argument(
        "--include-documents",
        action="store_true",
        help="Include rendered document content in the command output.",
    )
    bootstrap_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the scaffold chain and refresh derived planning surfaces.",
    )
    add_human_json_format_argument(bootstrap_parser)
    bootstrap_parser.set_defaults(handler=_run_plan_bootstrap)

    confirm_inputs_parser = plan_subparsers.add_parser(
        "confirm-inputs",
        help="Confirm authored initiative inputs into machine state.",
        description=dedent(
            """
            Confirm the current initiative-authored inputs into machine state
            after review so the readiness gate reflects the latest captured
            package before execution approval.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan confirm-inputs --initiative-slug example_initiative",
            "uv run watchtower-core plan confirm-inputs --project-slug watchtower "
            "--initiative-slug watchtower_work_item_notes --write --format json",
        ),
        formatter_class=HelpFormatter,
    )
    confirm_inputs_parser.add_argument(
        "--initiative-slug",
        required=True,
        help="Initiative slug such as example_initiative or watchtower_work_item_notes.",
    )
    confirm_inputs_parser.add_argument(
        "--project-slug",
        help="Project slug when the initiative is project-scoped, such as watchtower.",
    )
    confirm_inputs_parser.add_argument(
        "--actor-id",
        default="actor.repository_maintainer",
        help="Approver actor identifier used for the confirmation event.",
    )
    confirm_inputs_parser.add_argument(
        "--write",
        action="store_true",
        help="Persist the confirmation state and refresh derived plan surfaces.",
    )
    add_human_json_format_argument(confirm_inputs_parser)
    confirm_inputs_parser.set_defaults(handler=_run_plan_confirm_inputs)

    approve_parser = plan_subparsers.add_parser(
        "approve",
        help="Approve one live initiative package for execution.",
        description=dedent(
            """
            Approve one validated live initiative package into
            ready_for_execution so task transitions can begin real execution
            without violating the hard no-start gate.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan approve --initiative-slug example_initiative",
            "uv run watchtower-core plan approve --project-slug watchtower "
            "--initiative-slug watchtower_work_item_notes --write --format json",
        ),
        formatter_class=HelpFormatter,
    )
    approve_parser.add_argument(
        "--initiative-slug",
        required=True,
        help="Initiative slug such as example_initiative or watchtower_work_item_notes.",
    )
    approve_parser.add_argument(
        "--project-slug",
        help="Project slug when the initiative is project-scoped, such as watchtower.",
    )
    approve_parser.add_argument(
        "--actor-id",
        default="actor.repository_maintainer",
        help="Approver actor identifier used for the approval event.",
    )
    approve_parser.add_argument(
        "--write",
        action="store_true",
        help="Persist the approval state and refresh derived plan surfaces.",
    )
    add_human_json_format_argument(approve_parser)
    approve_parser.set_defaults(handler=_run_plan_approve)
