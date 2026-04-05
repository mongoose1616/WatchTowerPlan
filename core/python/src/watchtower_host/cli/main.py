"""Host-owned console entrypoint for the WatchTower CLI."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from watchtower_core.control_plane.errors import RepoRootNotFoundError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import create_telemetry_session
from watchtower_host.cli.parser import build_parser
from watchtower_host.cli.registry import (
    CORE_COMMAND_GROUP_SPECS,
    CommandGroupSpec,
    find_registered_pack_command_group,
    load_pack_command_group_spec,
)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    active_argv = list(argv) if argv is not None else sys.argv[1:]
    try:
        loader = ControlPlaneLoader()
    except RepoRootNotFoundError as exc:
        return _emit_startup_repo_root_error(active_argv, str(exc))
    telemetry = create_telemetry_session(loader, active_argv)
    with telemetry.activate():
        try:
            with telemetry.operation(
                "cli_stage",
                "parser_build",
                attributes={"argv": active_argv},
            ):
                parser = build_parser(_command_group_specs_for_argv(active_argv, loader))
            try:
                with telemetry.operation(
                    "cli_stage",
                    "argv_parse",
                    attributes={"argv": active_argv},
                ) as operation:
                    args = parser.parse_args(active_argv)
                    operation.add_attributes(parsed_command=getattr(args, "command", None))
            except SystemExit as exc:
                telemetry.finish(
                    status=_system_exit_status(active_argv, exc.code),
                    exit_code=_system_exit_code(exc.code),
                )
                raise

            handler = getattr(args, "handler", None)
            if handler is None:
                parser.print_help()
                telemetry.finish(
                    status=_help_status(active_argv),
                    exit_code=0,
                )
                return 0

            with telemetry.operation(
                "cli_command",
                telemetry.command_name,
                attributes={"argv": active_argv},
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
        except Exception as exc:
            telemetry.finish(status="exception", exit_code=1, error=exc)
            raise


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


def _selected_core_command_group_spec(command_name: str) -> CommandGroupSpec | None:
    for spec in CORE_COMMAND_GROUP_SPECS:
        if spec.name == command_name:
            return spec
    return None


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
