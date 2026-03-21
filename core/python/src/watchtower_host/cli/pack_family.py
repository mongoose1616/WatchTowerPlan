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
            Inspect hosted pack registry entries, describe one hosted pack's
            runtime contract, and validate pack-interface wiring against the
            governed pack registry plus runtime manifest.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack list --format json",
            "uv run watchtower-core pack describe --pack plan --format json",
            "uv run watchtower-core pack validate --pack plan --format json",
            "uv run watchtower-core pack scaffold --pack-slug oversight "
            "--pack-root packs/oversight --format json",
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
            "uv run watchtower-core pack describe --pack plan",
            "uv run watchtower-core pack describe --pack plan --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_describe_parser.add_argument(
        "--pack",
        help="Hosted pack slug such as plan. Defaults to the default repository pack.",
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
            "uv run watchtower-core pack validate --pack plan",
            "uv run watchtower-core pack validate --pack plan --format json",
            "uv run watchtower-core pack validate --pack-settings-path "
            "packs/oversight/.wt/manifests/pack_settings.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    pack_validate_parser.add_argument(
        "--pack",
        help="Hosted pack slug such as plan. Defaults to the default repository pack.",
    )
    pack_validate_parser.add_argument(
        "--pack-settings-path",
        help="Optional pack settings path override when validating one non-default hosted pack.",
    )
    add_human_json_format_argument(pack_validate_parser)
    pack_validate_parser.set_defaults(handler=_run_pack_validate)

    pack_scaffold_parser = pack_subparsers.add_parser(
        "scaffold",
        help="Render a starter hosted-pack root plus host-wiring snippets.",
        description=dedent(
            """
            Render the pack-owned starter files for one new hosted pack without
            mutating the shared pack registry or core workspace dependency graph.

            The generated pack is self-consistent and validation-ready once the
            emitted registry snippet and core-python workspace snippets are
            applied deliberately.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core pack scaffold --pack-slug oversight "
            "--pack-root packs/oversight",
            "uv run watchtower-core pack scaffold --pack-slug reviews "
            "--pack-root packs/reviews --command-namespace reviews "
            "--domain-root assessments --domain-root reviews --format json",
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
