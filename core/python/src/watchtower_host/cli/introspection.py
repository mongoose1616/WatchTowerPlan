"""Host-owned command metadata derived from the parser tree."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from watchtower_host.cli.registry import load_command_group_specs

CLI_PARSER_PATH = "core/python/src/watchtower_host/cli/parser.py"
CLI_MAIN_ENTRYPOINT = "watchtower_host.cli.main:main"
COMMAND_DOC_ROOT = "core/docs/commands/core_python"
COMMAND_GROUP_IMPLEMENTATION_PATHS = {
    spec.name: spec.implementation_path for spec in load_command_group_specs()
}
COMMAND_GROUP_SUBCOMMAND_IMPLEMENTATION_PATHS = {
    spec.name: dict(spec.subcommand_implementation_paths)
    for spec in load_command_group_specs()
    if spec.subcommand_implementation_paths
}

@dataclass(frozen=True, slots=True)
class CommandParserSpec:
    """Machine-readable command metadata derived from argparse parsers."""

    command_id: str
    command: str
    summary: str
    kind: str
    workspace: str
    doc_path: str
    synopsis: str
    implementation_path: str
    package_entrypoint: str
    parent_command_id: str | None
    output_formats: tuple[str, ...]
    default_output_format: str | None


def iter_command_parser_specs(parser: argparse.ArgumentParser) -> tuple[CommandParserSpec, ...]:
    """Return parser-backed command specs for the root command and all subcommands."""
    specs = [_build_spec(parser)]
    specs.extend(_walk_subparsers(parser))
    return tuple(specs)


def _walk_subparsers(parser: argparse.ArgumentParser) -> list[CommandParserSpec]:
    specs: list[CommandParserSpec] = []
    subparser_action = _find_subparser_action(parser)
    if subparser_action is None:
        return specs
    for name in sorted(subparser_action.choices):
        child = subparser_action.choices[name]
        specs.append(_build_spec(child))
        specs.extend(_walk_subparsers(child))
    return specs


def _find_subparser_action(
    parser: argparse.ArgumentParser,
) -> argparse._SubParsersAction | None:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    return None


def _build_spec(parser: argparse.ArgumentParser) -> CommandParserSpec:
    command = parser.prog
    tokens = tuple(command.split())
    command_group_specs = load_command_group_specs()
    command_group_implementation_paths = {
        spec.name: spec.implementation_path for spec in command_group_specs
    }
    command_group_subcommand_paths = {
        spec.name: dict(spec.subcommand_implementation_paths)
        for spec in command_group_specs
        if spec.subcommand_implementation_paths
    }
    output_formats, default_output_format = _extract_output_formats(parser)
    return CommandParserSpec(
        command_id=_command_id(tokens),
        command=command,
        summary=_extract_first_paragraph(parser.description or parser.format_help()),
        kind="root_command" if len(tokens) == 1 else "subcommand",
        workspace="core_python",
        doc_path=_command_doc_path(parser, tokens),
        synopsis=_synopsis_for_parser(parser),
        implementation_path=_implementation_path(
            parser,
            tokens,
            command_group_implementation_paths=command_group_implementation_paths,
            command_group_subcommand_paths=command_group_subcommand_paths,
        ),
        package_entrypoint=CLI_MAIN_ENTRYPOINT,
        parent_command_id=_parent_command_id(tokens),
        output_formats=output_formats,
        default_output_format=default_output_format,
    )


def _extract_first_paragraph(text: str) -> str:
    for block in text.split("\n\n"):
        candidate = " ".join(block.split()).strip()
        if candidate:
            return candidate
    raise ValueError("Parser description is missing its expected paragraph content.")


def _synopsis_for_parser(parser: argparse.ArgumentParser) -> str:
    usage = parser.format_usage().strip()
    if usage.startswith("usage: "):
        usage = usage[len("usage: ") :]
    return "uv run " + " ".join(usage.split())


def _extract_output_formats(parser: argparse.ArgumentParser) -> tuple[tuple[str, ...], str | None]:
    for action in parser._actions:
        if "--format" not in action.option_strings:
            continue
        if action.choices is None:
            return (), None
        formats = tuple(str(choice) for choice in action.choices)
        default = action.default if action.default in formats else None
        if default is None and formats:
            default = "human" if "human" in formats else formats[0]
        return formats, default
    return (), None


def _command_doc_path(parser: argparse.ArgumentParser, tokens: tuple[str, ...]) -> str:
    declared_doc_path = parser.get_default("_doc_path")
    if isinstance(declared_doc_path, str) and declared_doc_path:
        return declared_doc_path
    suffix = "_".join(token.replace("-", "_") for token in tokens)
    return f"{COMMAND_DOC_ROOT}/{suffix}.md"


def _implementation_path(
    parser: argparse.ArgumentParser,
    tokens: tuple[str, ...],
    *,
    command_group_implementation_paths: dict[str, str],
    command_group_subcommand_paths: dict[str, dict[str, str]],
) -> str:
    declared_path = parser.get_default("_implementation_path")
    if isinstance(declared_path, str) and declared_path:
        return declared_path
    if len(tokens) == 1:
        return CLI_PARSER_PATH

    family = tokens[1]
    try:
        family_path = command_group_implementation_paths[family]
    except KeyError as exc:
        raise ValueError(f"Unknown CLI command family for parser metadata: {family}") from exc
    if len(tokens) > 2:
        subcommand_paths = command_group_subcommand_paths.get(family)
        if subcommand_paths is not None:
            implementation_path = subcommand_paths.get(tokens[2])
            if implementation_path is not None:
                return implementation_path
    return family_path


def _normalize_command_token(token: str) -> str:
    return token.replace("-", "_")


def _command_id(tokens: tuple[str, ...]) -> str:
    normalized = (_normalize_command_token(token) for token in tokens)
    return "command." + ".".join(normalized)


def _parent_command_id(tokens: tuple[str, ...]) -> str | None:
    if len(tokens) == 1:
        return None
    return _command_id(tokens[:-1])
