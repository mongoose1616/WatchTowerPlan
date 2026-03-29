"""Shared parser helpers for the `watchtower-core plan query` namespace."""

from __future__ import annotations

import argparse

from watchtower_core.cli.common import add_human_json_format_argument, add_limit_argument

IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/query.py"


def add_live_scope_arguments(
    parser: argparse.ArgumentParser,
    *,
    initiative_help: str,
    trace_help: str,
    project_help: str = "Exact project identifier such as project.watchtower.",
) -> None:
    """Add the shared initiative, project, and trace scope arguments."""

    parser.add_argument("--initiative-id", help=initiative_help)
    parser.add_argument("--project-id", help=project_help)
    parser.add_argument("--trace-id", help=trace_help)


def add_output_arguments(
    parser: argparse.ArgumentParser,
    *,
    limit_default: int = 10,
) -> None:
    """Add the shared output-format and result-limit arguments."""

    add_limit_argument(parser, default=limit_default)
    add_human_json_format_argument(parser)
