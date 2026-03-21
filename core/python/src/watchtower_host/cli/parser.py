"""Host-owned parser construction for the WatchTower CLI."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_host.cli.registry import CORE_COMMAND_GROUP_SPECS, CommandGroupSpec


def build_parser(
    command_group_specs: tuple[CommandGroupSpec, ...] | None = None,
) -> argparse.ArgumentParser:
    """Build the root CLI parser from an explicit set of command groups."""
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
            "uv run watchtower-core pack list --format json",
            "uv run watchtower-core pack validate --pack plan --format json",
            'uv run watchtower-core route preview --request "review code and commit"',
            "uv run watchtower-core plan bootstrap --trace-id trace.example "
            '--title "Example Initiative" '
            '--summary "Bootstraps the example initiative." --format json',
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query workflows --query validation",
            "uv run watchtower-core query references --query uv",
            "uv run watchtower-core query standards --category governance --format json",
            "uv run watchtower-core query acceptance --trace-id trace.governed_acceptance_example",
            "uv run watchtower-core plan query coordination --format json",
            "uv run watchtower-core plan query artifacts "
            "--artifact-family initiative_state --format json",
            "uv run watchtower-core plan query readiness --ready-for-execution true --format json",
            "uv run watchtower-core plan query projects --slug watchtower --format json",
            "uv run watchtower-core plan query authority --domain planning --format json",
            "uv run watchtower-core plan query tasks --task-status planned",
            "uv run watchtower-core plan query tasks --blocked-only --include-dependency-details",
            "uv run watchtower-core plan task transition --task-id task.example.001 "
            "--task-status completed --format json",
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core plan closeout initiative --initiative-slug plan_example "
            '--initiative-status completed --closure-reason "Delivered and validated" --write',
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core plan sync all",
            "uv run watchtower-core plan sync coordination",
            "uv run watchtower-core plan sync foundation-index",
            "uv run watchtower-core plan sync initiative-index",
            "uv run watchtower-core plan sync initiative-tracking",
            "uv run watchtower-core plan sync reference-index",
            "uv run watchtower-core plan sync standard-index",
            "uv run watchtower-core plan sync workflow-index",
            "uv run watchtower-core plan sync task-index",
            "uv run watchtower-core plan sync task-tracking",
            "uv run watchtower-core plan sync github-tasks --repo owner/repo",
            "uv run watchtower-core plan sync traceability-index",
            "uv run watchtower-core validate all --skip-acceptance",
            "uv run watchtower-core validate document-semantics --path "
            "core/docs/standards/documentation/workflow_md_standard.md",
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.governed_acceptance_example",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/"
            "governed_acceptance_example_acceptance.json",
        ),
        formatter_class=HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")
    for spec in command_group_specs or CORE_COMMAND_GROUP_SPECS:
        spec.registrar(subparsers)
    return parser
