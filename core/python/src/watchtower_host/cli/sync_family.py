"""Sync command-family registration."""

from __future__ import annotations

import argparse


def register_sync_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the sync command family and its subcommands."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.sync_family_documents import register_document_sync_commands
    from watchtower_host.cli.sync_family_special import (
        build_sync_subparsers,
        register_special_sync_commands,
    )
    from watchtower_host.cli.sync_handlers import SYNC_HANDLERS

    handlers = dict(SYNC_HANDLERS)
    sync_subparsers = build_sync_subparsers(subparsers, help_handler=_run_help)
    register_special_sync_commands(sync_subparsers, handlers)
    register_document_sync_commands(sync_subparsers, handlers)
