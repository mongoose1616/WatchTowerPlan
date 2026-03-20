"""Hosted-pack command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)


def register_pack_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the hosted-pack command family."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.pack_handlers import (
        _run_pack_describe,
        _run_pack_list,
        _run_pack_validate,
    )

    pack_parser = subparsers.add_parser(
        "pack",
        help="Inspect and validate hosted domain-pack integration contracts.",
        description=dedent(
            """
            Inspect hosted pack registry entries, describe one hosted pack's
            runtime contract, and validate pack-interface wiring against the
            governed pack registry plus runtime manifest.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack list --format json",
            "uv run watchtower-core pack describe --pack plan --format json",
            "uv run watchtower-core pack validate --pack plan --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_subparsers = pack_parser.add_subparsers(
        dest="pack_command",
        title="pack commands",
        metavar="<pack_command>",
    )
    pack_parser.set_defaults(handler=_run_help, help_parser=pack_parser)

    pack_list_parser = pack_subparsers.add_parser(
        "list",
        help="List hosted packs from the shared pack registry.",
        description=dedent(
            """
            List the hosted packs declared in the shared pack registry.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack list",
            "uv run watchtower-core pack list --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_human_json_format_argument(pack_list_parser)
    pack_list_parser.set_defaults(handler=_run_pack_list)

    pack_describe_parser = pack_subparsers.add_parser(
        "describe",
        help="Describe one hosted pack registry entry and runtime contract.",
        description=dedent(
            """
            Describe one hosted pack using the shared pack registry plus the
            pack-owned runtime manifest.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack describe --pack plan",
            "uv run watchtower-core pack describe --pack plan --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_describe_parser.add_argument(
        "--pack",
        help="Hosted pack slug such as plan. Defaults to the default repository pack.",
    )
    add_human_json_format_argument(pack_describe_parser)
    pack_describe_parser.set_defaults(handler=_run_pack_describe)

    pack_validate_parser = pack_subparsers.add_parser(
        "validate",
        help="Validate one hosted pack contract against governed machine surfaces.",
        description=dedent(
            """
            Validate one hosted pack contract using the pack registry, runtime
            manifest, and typed integration descriptor checks.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack validate --pack plan",
            "uv run watchtower-core pack validate --pack plan --format json",
            "uv run watchtower-core pack validate --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_validate_parser.add_argument(
        "--pack",
        help="Hosted pack slug such as plan. Defaults to the default repository pack.",
    )
    pack_validate_parser.add_argument(
        "--pack-settings-path",
        help="Optional pack settings path override when validating one non-default hosted pack.",
    )
    add_human_json_format_argument(pack_validate_parser)
    pack_validate_parser.set_defaults(handler=_run_pack_validate)
