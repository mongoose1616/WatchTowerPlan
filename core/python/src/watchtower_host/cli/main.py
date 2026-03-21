"""Host-owned console entrypoint for the WatchTower CLI."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.parser import build_parser
from watchtower_host.cli.registry import (
    CORE_COMMAND_GROUP_SPECS,
    find_registered_pack_command_group,
    load_pack_command_group_spec,
)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    active_argv = list(argv) if argv is not None else sys.argv[1:]
    loader = ControlPlaneLoader()
    parser = build_parser(_command_group_specs_for_argv(active_argv, loader))
    args = parser.parse_args(active_argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


def _command_group_specs_for_argv(
    argv: Sequence[str],
    loader: ControlPlaneLoader,
) -> tuple:
    first_token = argv[0] if argv else None
    core_names = {spec.name for spec in CORE_COMMAND_GROUP_SPECS}
    if first_token is None or first_token.startswith("-") or first_token in core_names:
        return CORE_COMMAND_GROUP_SPECS
    if find_registered_pack_command_group(first_token, loader) is None:
        return CORE_COMMAND_GROUP_SPECS
    selected_pack = load_pack_command_group_spec(
        first_token,
        loader=loader,
        tolerate_import_errors=True,
    )
    if selected_pack is None:
        return CORE_COMMAND_GROUP_SPECS
    return (*CORE_COMMAND_GROUP_SPECS, selected_pack)


if __name__ == "__main__":
    raise SystemExit(main())
