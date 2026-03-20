"""Root sync parser registration helpers."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from textwrap import dedent
from typing import cast

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.sync_family_common import HandlerMap


def build_sync_subparsers(
    subparsers: argparse._SubParsersAction,
    *,
    help_handler: Callable[..., int],
) -> argparse._SubParsersAction:
    """Create the root sync parser and return its subparser collection."""

    sync_parser = subparsers.add_parser(
        "sync",
        help="Rebuild reusable-core derived governed artifacts.",
        description=dedent(
            """
            Rebuild reusable-core derived governed artifacts from authored
            repository sources.

            Root `sync` owns only the shared machine surfaces. Pack-owned sync
            operations live under their pack namespaces, such as
            `watchtower-core plan sync ...`.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core sync route-index --write",
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
            "uv run watchtower-core plan sync all",
            "uv run watchtower-core plan sync coordination --write",
            "uv run watchtower-core plan sync reference-index",
            "uv run watchtower-core plan sync github-tasks --repo owner/repo",
        ),
        formatter_class=HelpFormatter,
    )
    sync_subparsers = sync_parser.add_subparsers(
        dest="sync_command",
        title="sync commands",
        metavar="<sync_command>",
    )
    sync_parser.set_defaults(handler=help_handler, help_parser=sync_parser)
    return cast(argparse._SubParsersAction, sync_subparsers)


def register_special_sync_commands(
    sync_subparsers: argparse._SubParsersAction,
    handlers: HandlerMap,
) -> None:
    """Register reusable-core special sync commands."""

    del sync_subparsers
    del handlers
