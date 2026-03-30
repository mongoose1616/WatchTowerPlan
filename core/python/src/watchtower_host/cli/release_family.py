"""Release command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    add_pack_settings_argument,
    examples,
)


def register_release_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the local release-gate command family."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.release_handlers import _run_release_check

    release_parser = subparsers.add_parser(
        "release",
        help="Run local release-gate commands for customer and bootstrap handoff.",
        description=dedent(
            """
            Run local release-gate commands that combine broad repository
            validation, explicit schema-definition validation, dirty-worktree
            protection, and curated export staging.

            This family is local-only orchestration. It is the fail-closed gate
            to use before handing a staged bundle to a customer or downstream
            repository bootstrap flow.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core release check --output-root /tmp/customer_core "
            "--overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/customer_pack_repo "
            "--include-pack <pack-slug> --overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/customer_pack_bundle "
            "--include-pack <pack-slug> --pack-only --overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/rehearsal "
            "--include-pack <pack-slug> --schema-path core/control_plane/schemas/interfaces/"
            "packs/pack_settings.schema.json --allow-dirty --overwrite --format json",
        ),
        formatter_class=HelpFormatter,
    )
    release_subparsers = release_parser.add_subparsers(
        dest="release_command",
        title="release commands",
        metavar="<release_command>",
    )
    release_parser.set_defaults(handler=_run_help, help_parser=release_parser)

    release_check_parser = release_subparsers.add_parser(
        "check",
        help="Run the local release gate and build one staged export.",
        description=dedent(
            """
            Run the local fail-closed release gate for one intended handoff
            bundle.

            The command inspects git worktree cleanliness when git metadata is
            available, runs the current broad repository validation baseline,
            runs explicit schema-definition checks for requested or locally
            changed `*.schema.json` files, and then stages the final export with
            the normal pack-export portability checks.

            Use --allow-dirty only for local rehearsal when you intentionally
            want the command to continue despite a dirty worktree. Customer
            handoff should use a clean donor worktree.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core release check --output-root /tmp/customer_core "
            "--overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/customer_pack_repo "
            "--include-pack <pack-slug> --overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/customer_pack_bundle "
            "--include-pack <pack-slug> --pack-only --overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/customer_release "
            "--include-pack <pack-slug> --schema-path core/control_plane/schemas/interfaces/"
            "packs/pack_settings.schema.json --overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/rehearsal "
            "--include-pack <pack-slug> --allow-dirty --overwrite --format json",
        ),
        formatter_class=HelpFormatter,
    )
    release_check_parser.add_argument(
        "--output-root",
        required=True,
        help="Filesystem path where the staged export should be written.",
    )
    release_check_parser.add_argument(
        "--include-pack",
        action="append",
        default=[],
        help=(
            "Hosted pack slug to include in the staged export. Repeat for multiple "
            "packs. Omit for core-only release bundles. Required with --pack-only."
        ),
    )
    release_check_parser.add_argument(
        "--pack-only",
        action="store_true",
        help=(
            "Stage only the selected hosted-pack roots without shared core. Use this "
            "for additive pack bundles destined for a compatible core repository."
        ),
    )
    release_check_parser.add_argument(
        "--schema-path",
        action="append",
        default=[],
        help=(
            "Explicit schema-definition path to validate as part of the release gate. "
            "Repeat for multiple files."
        ),
    )
    release_check_parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help=(
            "Continue even when git metadata reports a dirty worktree. Use only for "
            "local rehearsal, not final customer handoff."
        ),
    )
    release_check_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing staged export directory.",
    )
    add_pack_settings_argument(release_check_parser)
    add_human_json_format_argument(release_check_parser)
    release_check_parser.set_defaults(handler=_run_release_check)
