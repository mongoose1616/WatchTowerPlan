"""Registry-backed parser construction for the WatchTower CLI."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.registry import COMMAND_GROUP_SPECS


def build_parser() -> argparse.ArgumentParser:
    """Build the root CLI parser."""
    parser = argparse.ArgumentParser(
        prog="watchtower-core",
        description=dedent(
            """
            WatchTower core helper and harness workspace.

            Run this command from `core/python/` with `uv run` to inspect governed
            control-plane data, preview workflow routes, run workspace health
            snapshots, validate governed artifacts, and rebuild derived indexes
            and trackers.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core doctor",
            "uv run watchtower-core route preview --request \"review code and commit\"",
            "uv run watchtower-core plan scaffold --kind prd --trace-id trace.example "
            "--document-id prd.example --title \"Example PRD\" "
            "--summary \"Frames the example initiative.\" --format json",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query coordination --format json",
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query workflows --query validation",
            "uv run watchtower-core query references --query uv",
            "uv run watchtower-core query standards --category governance --format json",
            "uv run watchtower-core query prds --trace-id trace.core_python_foundation",
            "uv run watchtower-core query acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core query tasks --task-status backlog",
            "uv run watchtower-core query tasks --blocked-only --include-dependency-details",
            "uv run watchtower-core task transition --task-id task.example.001 "
            "--task-status done --format json",
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync all",
            "uv run watchtower-core sync coordination",
            "uv run watchtower-core sync foundation-index",
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core sync initiative-index",
            "uv run watchtower-core sync initiative-tracking",
            "uv run watchtower-core sync reference-index",
            "uv run watchtower-core sync standard-index",
            "uv run watchtower-core sync workflow-index",
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync task-index",
            "uv run watchtower-core sync task-tracking",
            "uv run watchtower-core sync github-tasks --repo owner/repo",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Delivered and validated\"",
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core validate all --skip-acceptance",
            "uv run watchtower-core validate document-semantics --path "
            "docs/standards/documentation/workflow_md_standard.md",
            "uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
        ),
        formatter_class=HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")
    for spec in COMMAND_GROUP_SPECS:
        spec.registrar(subparsers)
    return parser
