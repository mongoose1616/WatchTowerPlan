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


def add_common_validation_arguments(parser: argparse.ArgumentParser) -> None:
    """Add shared validation command arguments."""
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
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
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
