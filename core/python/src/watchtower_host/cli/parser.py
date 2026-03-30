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
            "uv run watchtower-core pack describe --format json",
            "uv run watchtower-core pack validate --format json",
            "uv run watchtower-core pack scaffold --pack-slug oversight "
            "--pack-root oversight --format json",
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "oversight/.wt/manifests/pack_settings.json --write --format json",
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "oversight/.wt/manifests/pack_settings.json --replace-hosted-packs "
            "--write --format json",
            "uv run watchtower-core pack export --output-root /tmp/customer_export "
            "--include-pack <pack-slug> --overwrite --format json",
            "uv run watchtower-core pack export --output-root /tmp/customer_pack_bundle "
            "--include-pack <pack-slug> --pack-only --overwrite --format json",
            "uv run watchtower-core release check --output-root /tmp/customer_release "
            "--include-pack <pack-slug> --overwrite --format json",
            'uv run watchtower-core route preview --request "review code and commit"',
            "uv run watchtower-core query authority --query canonical --format json",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query templates --query standard --format json",
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query workflows --query validation",
            "uv run watchtower-core query references --query uv",
            "uv run watchtower-core query standards --category governance --format json",
            "uv run watchtower-core query acceptance --trace-id trace.governed_acceptance_example",
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
            "uv run watchtower-core validate all --skip-acceptance",
            "uv run watchtower-core validate portability --include-pack <pack-slug> "
            "--format json",
            "uv run watchtower-core validate portability --root /tmp/customer_pack_bundle "
            "--include-pack <pack-slug> --pack-only --format json",
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
