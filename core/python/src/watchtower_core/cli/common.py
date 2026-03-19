"""Shared CLI parser helpers."""

from __future__ import annotations

import argparse
from pathlib import Path


class HelpFormatter(
    argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    """Formatter that preserves examples and shows defaults."""


def examples(*lines: str) -> str:
    """Render a short examples block for argparse epilog text."""
    return "Examples:\n" + "\n".join(f"  {line}" for line in lines)


HUMAN_JSON_CHOICES = ("human", "json")
TRI_STATE_BOOL_CHOICES = ("true", "false")


def add_human_json_format_argument(parser: argparse.ArgumentParser) -> None:
    """Add one standard human-or-json output selector."""
    parser.add_argument(
        "--format",
        choices=HUMAN_JSON_CHOICES,
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )


def add_limit_argument(
    parser: argparse.ArgumentParser,
    *,
    default: int = 10,
) -> None:
    """Add one standard bounded result-limit argument."""
    parser.add_argument(
        "--limit",
        type=int,
        default=default,
        help="Maximum number of results to return.",
    )


def add_query_argument(
    parser: argparse.ArgumentParser,
    *,
    help_text: str,
) -> None:
    """Add one free-text query selector."""
    parser.add_argument("--query", help=help_text)


def add_tri_state_bool_argument(
    parser: argparse.ArgumentParser,
    flag: str,
    *,
    help_text: str,
) -> None:
    """Add one tri-state boolean selector that accepts true/false or omission."""
    parser.add_argument(flag, choices=TRI_STATE_BOOL_CHOICES, help=help_text)


def add_common_validation_arguments(parser: argparse.ArgumentParser) -> None:
    """Add shared validation command arguments."""
    add_human_json_format_argument(parser)
    parser.add_argument(
        "--record-evidence",
        action="store_true",
        help="Write a durable validation-evidence artifact and synchronized traceability update.",
    )
    parser.add_argument(
        "--trace-id",
        help="Required with --record-evidence. Shared trace identifier for the recorded evidence.",
    )
    parser.add_argument(
        "--evidence-id",
        help=(
            "Optional explicit evidence identifier. Otherwise the command "
            "derives one deterministically."
        ),
    )
    parser.add_argument(
        "--subject-id",
        action="append",
        default=[],
        help=(
            "Optional subject identifier to attach to the evidence check. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--acceptance-id",
        action="append",
        default=[],
        help=(
            "Optional acceptance identifier to attach to the evidence check. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--evidence-output",
        type=Path,
        help="Optional explicit output path for the evidence artifact.",
    )
    parser.add_argument(
        "--traceability-output",
        type=Path,
        help="Optional explicit output path for the updated traceability index.",
    )


def add_pack_settings_argument(parser: argparse.ArgumentParser) -> None:
    """Add one optional pack-settings-path argument to a validation command."""

    parser.add_argument(
        "--pack-settings-path",
        help=(
            "Optional repository-relative path to the pack settings surface that "
            "declares the active schema, validator, and validation suite registries."
        ),
    )


def add_common_sync_arguments(parser: argparse.ArgumentParser) -> None:
    """Add shared sync command arguments."""
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the rebuilt artifact to the canonical control-plane path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit output path for the rebuilt artifact.",
    )
    parser.add_argument(
        "--include-document",
        action="store_true",
        help="Include the generated document in json output for inspection or downstream tooling.",
    )
    add_human_json_format_argument(parser)
