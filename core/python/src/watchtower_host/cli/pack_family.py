"""Hosted-pack command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)


def register_pack_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the hosted-pack command family."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.pack_handlers import (
        _run_pack_bootstrap,
        _run_pack_describe,
        _run_pack_list,
        _run_pack_scaffold,
        _run_pack_validate,
    )

    pack_parser = subparsers.add_parser(
        "pack",
        help="Inspect and validate hosted domain-pack integration contracts.",
        description=dedent(
            """
            Inspect hosted pack registry entries, scaffold new hosted packs,
            bootstrap shared registry and workspace wiring, and validate
            pack-interface contracts against the governed pack registry plus
            runtime manifest.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack list --format json",
            "uv run watchtower-core pack describe --format json",
            "uv run watchtower-core pack validate --format json",
            "uv run watchtower-core pack scaffold --pack-slug oversight "
            "--pack-root packs/oversight --format json",
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --write --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_subparsers = pack_parser.add_subparsers(
        dest="pack_command",
        title="pack commands",
        metavar="<pack_command>",
    )
    pack_parser.set_defaults(handler=_run_help, help_parser=pack_parser)

    pack_list_parser = pack_subparsers.add_parser(
        "list",
        help="List hosted packs from the shared pack registry.",
        description=dedent(
            """
            List the hosted packs declared in the shared pack registry.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack list",
            "uv run watchtower-core pack list --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_human_json_format_argument(pack_list_parser)
    pack_list_parser.set_defaults(handler=_run_pack_list)

    pack_describe_parser = pack_subparsers.add_parser(
        "describe",
        help="Describe one hosted pack registry entry and runtime contract.",
        description=dedent(
            """
            Describe one hosted pack using the shared pack registry plus the
            pack-owned runtime manifest.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack describe",
            "uv run watchtower-core pack describe --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_describe_parser.add_argument(
        "--pack",
        help="Hosted pack slug. Defaults to the default repository pack.",
    )
    add_human_json_format_argument(pack_describe_parser)
    pack_describe_parser.set_defaults(handler=_run_pack_describe)

    pack_validate_parser = pack_subparsers.add_parser(
        "validate",
        help="Validate one hosted pack contract against governed machine surfaces.",
        description=dedent(
            """
            Validate one hosted pack contract using the pack registry, runtime
            manifest, and typed integration descriptor checks.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack validate",
            "uv run watchtower-core pack validate --format json",
            "uv run watchtower-core pack validate --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_validate_parser.add_argument(
        "--pack",
        help="Hosted pack slug. Defaults to the default repository pack.",
    )
    pack_validate_parser.add_argument(
        "--pack-settings-path",
        help="Optional pack settings path override when validating one non-default hosted pack.",
    )
    add_human_json_format_argument(pack_validate_parser)
    pack_validate_parser.set_defaults(handler=_run_pack_validate)

    pack_bootstrap_parser = pack_subparsers.add_parser(
        "bootstrap",
        help="Register one pack into the shared host registry and Python workspace.",
        description=dedent(
            """
            Register one hosted pack into the shared pack registry and the
            shared core/python workspace so the host can load it through the
            normal pack contract.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --format json",
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --write --format json",
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --write "
            "--no-sync-workspace --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_bootstrap_parser.add_argument(
        "--pack-settings-path",
        required=True,
        help="Repository-relative path to the pack settings manifest to bootstrap.",
    )
    pack_bootstrap_parser.add_argument(
        "--write",
        action="store_true",
        help="Persist the shared registry and core/python workspace updates.",
    )
    pack_bootstrap_parser.add_argument(
        "--no-sync-workspace",
        action="store_true",
        help="Skip uv sync after writing shared workspace metadata.",
    )
    add_human_json_format_argument(pack_bootstrap_parser)
    pack_bootstrap_parser.set_defaults(handler=_run_pack_bootstrap)

    pack_scaffold_parser = pack_subparsers.add_parser(
        "scaffold",
        help="Render a starter hosted-pack root plus host-wiring snippets.",
        description=dedent(
            """
            Render the pack-owned starter files for one new hosted pack without
            mutating the shared pack registry or core workspace dependency graph.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack scaffold --pack-slug oversight "
            "--pack-root packs/oversight",
            "uv run watchtower-core pack scaffold --pack-slug reviews "
            "--pack-root packs/reviews --command-namespace reviews "
            "--domain-root assessments --domain-root reviews --format json",
            "uv run watchtower-core pack bootstrap --pack-settings-path "
            "packs/reviews/.wt/manifests/pack_settings.json --write --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_scaffold_parser.add_argument(
        "--pack-slug",
        required=True,
        help="Hosted pack slug such as oversight.",
    )
    pack_scaffold_parser.add_argument(
        "--pack-root",
        required=True,
        help="Repository-relative pack root such as packs/oversight.",
    )
    pack_scaffold_parser.add_argument(
        "--command-namespace",
        help="Optional top-level namespace override. Defaults to --pack-slug.",
    )
    pack_scaffold_parser.add_argument(
        "--python-distribution",
        help="Optional Python distribution override. Defaults to watchtower-<pack-slug>.",
    )
    pack_scaffold_parser.add_argument(
        "--python-package",
        help="Optional Python package override. Defaults to watchtower_<pack_slug>.",
    )
    pack_scaffold_parser.add_argument(
        "--domain-root",
        action="append",
        default=[],
        help="Optional pack-local domain root name. Repeat for multiple values.",
    )
    add_human_json_format_argument(pack_scaffold_parser)
    pack_scaffold_parser.set_defaults(handler=_run_pack_scaffold)
