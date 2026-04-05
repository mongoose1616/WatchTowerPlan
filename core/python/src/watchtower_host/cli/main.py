"""Host-owned console entrypoint for the WatchTower CLI."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from contextlib import nullcontext

from watchtower_core.control_plane.errors import RepoRootNotFoundError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import TelemetrySession, create_telemetry_session
from watchtower_host.cli.parser import build_parser
from watchtower_host.cli.registry import (
    CORE_COMMAND_GROUP_SPECS,
    CommandGroupSpec,
    find_registered_pack_command_group,
    load_pack_command_group_spec,
)

_REPO_OPTIONAL_CORE_COMMAND_NAMES = frozenset({"git"})


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    active_argv = list(argv) if argv is not None else sys.argv[1:]
    loader: ControlPlaneLoader | None = None
    try:
        loader = ControlPlaneLoader()
    except RepoRootNotFoundError as exc:
        if not _repo_optional_startup_allowed(active_argv):
            return _emit_startup_repo_root_error(active_argv, str(exc))
    telemetry = create_telemetry_session(loader, active_argv) if loader is not None else None
    with (telemetry.activate() if telemetry is not None else nullcontext()):
        try:
            parser = _build_parser_for_argv(active_argv, loader, telemetry)
            try:
                args = _parse_args(active_argv, parser, telemetry)
            except SystemExit as exc:
                if telemetry is not None:
                    telemetry.finish(
                        status=_system_exit_status(active_argv, exc.code),
                        exit_code=_system_exit_code(exc.code),
                    )
                raise

            handler = getattr(args, "handler", None)
            if handler is None:
                parser.print_help()
                if telemetry is not None:
                    telemetry.finish(
                        status=_help_status(active_argv),
                        exit_code=0,
                    )
                return 0

            result = _run_command(active_argv, args, telemetry)
            return result
        except Exception as exc:
            if telemetry is not None:
                telemetry.finish(status="exception", exit_code=1, error=exc)
            raise


def _build_parser_for_argv(
    argv: Sequence[str],
    loader: ControlPlaneLoader | None,
    telemetry: TelemetrySession | None,
) -> argparse.ArgumentParser:
    command_group_specs = (
        _command_group_specs_for_argv(argv, loader)
        if loader is not None
        else _core_command_group_specs_for_argv(argv)
    )
    if telemetry is None:
        return build_parser(command_group_specs)
    with telemetry.operation(
        "cli_stage",
        "parser_build",
        attributes={"argv": list(argv)},
    ):
        return build_parser(command_group_specs)


def _parse_args(
    argv: Sequence[str],
    parser: argparse.ArgumentParser,
    telemetry: TelemetrySession | None,
) -> argparse.Namespace:
    if telemetry is None:
        return parser.parse_args(argv)
    with telemetry.operation(
        "cli_stage",
        "argv_parse",
        attributes={"argv": list(argv)},
    ) as operation:
        args = parser.parse_args(argv)
        operation.add_attributes(parsed_command=getattr(args, "command", None))
        return args


def _run_command(
    argv: Sequence[str],
    args: argparse.Namespace,
    telemetry: TelemetrySession | None,
) -> int:
    handler = args.handler
    if telemetry is None:
        return int(handler(args))
    with telemetry.operation(
        "cli_command",
        telemetry.command_name,
        attributes={"argv": list(argv)},
    ) as operation:
        result = int(handler(args))
        operation.set_result(
            status=_command_status(result, operation),
            exit_code=result,
        )
    telemetry.finish(
        status=_command_status(result, operation),
        exit_code=result,
    )
    return result


def _command_group_specs_for_argv(
    argv: Sequence[str],
    loader: ControlPlaneLoader,
) -> tuple[CommandGroupSpec, ...]:
    first_token = argv[0] if argv else None
    if first_token is None or first_token.startswith("-"):
        return CORE_COMMAND_GROUP_SPECS
    selected_core_spec = _selected_core_command_group_spec(first_token)
    if selected_core_spec is not None:
        return (selected_core_spec,)
    if find_registered_pack_command_group(first_token, loader) is None:
        return CORE_COMMAND_GROUP_SPECS
    selected_pack = load_pack_command_group_spec(
        first_token,
        loader=loader,
        tolerate_import_errors=True,
        selected_subcommand=(
            argv[1] if len(argv) >= 2 and not argv[1].startswith("-") else None
        ),
    )
    if selected_pack is None:
        return CORE_COMMAND_GROUP_SPECS
    return (selected_pack,)


def _core_command_group_specs_for_argv(argv: Sequence[str]) -> tuple[CommandGroupSpec, ...]:
    first_token = argv[0] if argv else None
    if first_token is None or first_token.startswith("-"):
        return CORE_COMMAND_GROUP_SPECS
    selected_core_spec = _selected_core_command_group_spec(first_token)
    if selected_core_spec is not None:
        return (selected_core_spec,)
    return CORE_COMMAND_GROUP_SPECS


def _selected_core_command_group_spec(command_name: str) -> CommandGroupSpec | None:
    for spec in CORE_COMMAND_GROUP_SPECS:
        if spec.name == command_name:
            return spec
    return None


def _repo_optional_startup_allowed(argv: Sequence[str]) -> bool:
    first_token = argv[0] if argv else None
    if first_token is None or first_token.startswith("-"):
        return True
    return first_token in _REPO_OPTIONAL_CORE_COMMAND_NAMES


def _emit_startup_repo_root_error(argv: Sequence[str], message: str) -> int:
    payload = {
        "command": _startup_command_name(argv),
        "status": "error",
        "message": message,
    }
    if _requested_output_format(argv) == "json":
        print(json.dumps(payload, sort_keys=True))
        return 1
    print(f"Workspace error: {message}")
    return 1


def _requested_output_format(argv: Sequence[str]) -> str:
    for index, token in enumerate(argv):
        if token == "--format" and index + 1 < len(argv):
            return argv[index + 1]
    return "human"


def _startup_command_name(argv: Sequence[str]) -> str:
    command_tokens = ["watchtower-core"]
    for token in argv:
        if token.startswith("-"):
            break
        command_tokens.append(token)
        if len(command_tokens) == 3:
            break
    return " ".join(command_tokens)


def _command_status(result: int, operation: object) -> str:
    if result == 0:
        return "ok"
    error_kind = getattr(operation, "attributes", {}).get("cli_error_kind")
    if isinstance(error_kind, str):
        return error_kind
    return "command_error"


def _help_status(argv: Sequence[str]) -> str:
    return "help_empty" if not argv else "help"


def _system_exit_code(code: object) -> int:
    if isinstance(code, int):
        return code
    return 1


def _system_exit_status(argv: Sequence[str], code: object) -> str:
    exit_code = _system_exit_code(code)
    if exit_code == 0:
        return _help_status(argv)
    return "parse_error"


if __name__ == "__main__":
    raise SystemExit(main())
