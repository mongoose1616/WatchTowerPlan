"""Compatibility wrapper around host-owned CLI metadata introspection."""

from __future__ import annotations

from watchtower_host.cli.introspection import (
    CLI_MAIN_ENTRYPOINT,
    CLI_PARSER_PATH,
    COMMAND_DOC_ROOT,
    COMMAND_GROUP_IMPLEMENTATION_PATHS,
    COMMAND_GROUP_SUBCOMMAND_IMPLEMENTATION_PATHS,
    CommandParserSpec,
    iter_command_parser_specs,
)
