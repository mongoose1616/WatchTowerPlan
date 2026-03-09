"""Thin CLI entrypoints for the WatchTower core workspace."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the root CLI parser."""
    parser = argparse.ArgumentParser(
        prog="watchtower-core",
        description="WatchTower core helper and harness workspace.",
    )
    subparsers = parser.add_subparsers(dest="command")

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Run a lightweight workspace smoke check.",
    )
    doctor_parser.set_defaults(handler=_run_doctor)
    return parser


def _run_doctor(_: argparse.Namespace) -> int:
    print("watchtower_core workspace scaffold is available.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
