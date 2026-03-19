"""Shared sync parser registration helpers."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Iterable, Mapping
from textwrap import dedent
from typing import TypedDict

from watchtower_core.cli.common import HelpFormatter, add_common_sync_arguments, examples

HandlerMap = Mapping[str, Callable[..., int]]


class SyncCommandSpec(TypedDict):
    name: str
    handler: str
    help: str
    description: str
    examples: tuple[str, ...]


def register_spec_sync_commands(
    sync_subparsers: argparse._SubParsersAction,
    *,
    handlers: HandlerMap,
    specs: Iterable[SyncCommandSpec],
) -> None:
    """Register sync subcommands from a shared spec table."""

    for spec in specs:
        parser = sync_subparsers.add_parser(
            spec["name"],
            help=spec["help"],
            description=dedent(spec["description"]).strip(),
            epilog=examples(*spec["examples"]),
            formatter_class=HelpFormatter,
        )
        add_common_sync_arguments(parser)
        parser.set_defaults(handler=handlers[spec["handler"]])
