"""Host-owned command metadata derived from the parser tree."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.parser import build_parser
from watchtower_host.cli.registry import (
    CORE_COMMAND_GROUP_SPECS,
    CommandGroupSpec,
    discover_registered_pack_command_groups,
    load_pack_command_group_spec,
)

CLI_PARSER_PATH = "core/python/src/watchtower_host/cli/parser.py"
CLI_MAIN_ENTRYPOINT = "watchtower_host.cli.main:main"
_DEFAULT_CORE_DOC_ROOT = "core/docs/commands/core_python"


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
    implementation_path: str | None
    package_entrypoint: str
    parent_command_id: str | None
    output_formats: tuple[str, ...]
    default_output_format: str | None
    notes: str | None = None


@dataclass(frozen=True, slots=True)
class _CommandGroupMetadata:
    doc_root: str
    implementation_path: str | None
    subcommand_implementation_paths: dict[str, str]
    notes: str | None


def iter_command_parser_specs(
    parser: argparse.ArgumentParser,
    *,
    command_group_specs: tuple[CommandGroupSpec, ...] = CORE_COMMAND_GROUP_SPECS,
) -> tuple[CommandParserSpec, ...]:
    """Return parser-backed command specs for the root command and all subcommands."""

    metadata = {
        spec.name: _CommandGroupMetadata(
            doc_root=spec.doc_root,
            implementation_path=spec.implementation_path,
            subcommand_implementation_paths=dict(spec.subcommand_implementation_paths),
            notes=spec.notes,
        )
        for spec in command_group_specs
    }
    specs = [_build_spec(parser, command_group_metadata=metadata)]
    specs.extend(_walk_subparsers(parser, command_group_metadata=metadata))
    return tuple(specs)


def iter_command_group_parser_specs(
    command_group_spec: CommandGroupSpec,
) -> tuple[CommandParserSpec, ...]:
    """Return command specs for one command group without duplicating the root entry."""

    parser = build_parser((command_group_spec,))
    return tuple(
        spec
        for spec in iter_command_parser_specs(parser, command_group_specs=(command_group_spec,))
        if spec.command_id != "command.watchtower_core"
    )


def iter_host_command_parser_specs(
    loader: ControlPlaneLoader | None = None,
) -> tuple[CommandParserSpec, ...]:
    """Return deterministic parser specs for core commands and all registered pack namespaces."""

    active_loader = loader or ControlPlaneLoader()
    specs = list(
        iter_command_parser_specs(
            build_parser(CORE_COMMAND_GROUP_SPECS),
            command_group_specs=CORE_COMMAND_GROUP_SPECS,
        )
    )
    for discovery in discover_registered_pack_command_groups(active_loader):
        command_group_spec = load_pack_command_group_spec(
            discovery.name,
            loader=active_loader,
            tolerate_import_errors=True,
        )
        if command_group_spec is None:
            continue
        specs.extend(iter_command_group_parser_specs(command_group_spec))
    return tuple(specs)


def _walk_subparsers(
    parser: argparse.ArgumentParser,
    *,
    command_group_metadata: dict[str, _CommandGroupMetadata],
) -> list[CommandParserSpec]:
    specs: list[CommandParserSpec] = []
    subparser_action = _find_subparser_action(parser)
    if subparser_action is None:
        return specs
    for name in sorted(subparser_action.choices):
        child = subparser_action.choices[name]
        specs.append(_build_spec(child, command_group_metadata=command_group_metadata))
        specs.extend(_walk_subparsers(child, command_group_metadata=command_group_metadata))
    return specs


def _find_subparser_action(
    parser: argparse.ArgumentParser,
) -> argparse._SubParsersAction | None:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    return None


def _build_spec(
    parser: argparse.ArgumentParser,
    *,
    command_group_metadata: dict[str, _CommandGroupMetadata],
) -> CommandParserSpec:
    command = parser.prog
    tokens = tuple(command.split())
    family_notes = None
    if len(tokens) >= 2:
        family_notes = command_group_metadata.get(
            tokens[1],
            _CommandGroupMetadata(_DEFAULT_CORE_DOC_ROOT, None, {}, None),
        ).notes
    output_formats, default_output_format = _extract_output_formats(parser)
    return CommandParserSpec(
        command_id=_command_id(tokens),
        command=command,
        summary=_extract_first_paragraph(parser.description or parser.format_help()),
        kind="root_command" if len(tokens) == 1 else "subcommand",
        workspace="core_python",
        doc_path=_command_doc_path(parser, tokens, command_group_metadata=command_group_metadata),
        synopsis=_synopsis_for_parser(parser),
        implementation_path=_implementation_path(
            parser,
            tokens,
            command_group_metadata=command_group_metadata,
        ),
        package_entrypoint=CLI_MAIN_ENTRYPOINT,
        parent_command_id=_parent_command_id(tokens),
        output_formats=output_formats,
        default_output_format=default_output_format,
        notes=family_notes,
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


def _command_doc_path(
    parser: argparse.ArgumentParser,
    tokens: tuple[str, ...],
    *,
    command_group_metadata: dict[str, _CommandGroupMetadata],
) -> str:
    declared_doc_path = parser.get_default("_doc_path")
    if isinstance(declared_doc_path, str) and declared_doc_path:
        return declared_doc_path
    suffix = "_".join(token.replace("-", "_") for token in tokens)
    if len(tokens) == 1:
        doc_root = command_group_metadata.get(
            "doctor",
            _CommandGroupMetadata(_DEFAULT_CORE_DOC_ROOT, None, {}, None),
        ).doc_root
        return f"{doc_root}/watchtower_core.md"
    family = tokens[1]
    try:
        doc_root = command_group_metadata[family].doc_root
    except KeyError as exc:
        raise ValueError(f"Unknown CLI command family for parser metadata: {family}") from exc
    return f"{doc_root}/{suffix}.md"


def _implementation_path(
    parser: argparse.ArgumentParser,
    tokens: tuple[str, ...],
    *,
    command_group_metadata: dict[str, _CommandGroupMetadata],
) -> str | None:
    declared_path = parser.get_default("_implementation_path")
    if isinstance(declared_path, str) and declared_path:
        return declared_path
    if len(tokens) == 1:
        return CLI_PARSER_PATH

    family = tokens[1]
    try:
        family_metadata = command_group_metadata[family]
    except KeyError as exc:
        raise ValueError(f"Unknown CLI command family for parser metadata: {family}") from exc
    if len(tokens) > 2:
        implementation_path = family_metadata.subcommand_implementation_paths.get(tokens[2])
        if implementation_path is not None:
            return implementation_path
    return family_metadata.implementation_path


def _normalize_command_token(token: str) -> str:
    return token.replace("-", "_")


def _command_id(tokens: tuple[str, ...]) -> str:
    normalized = (_normalize_command_token(token) for token in tokens)
    return "command." + ".".join(normalized)


def _parent_command_id(tokens: tuple[str, ...]) -> str | None:
    if len(tokens) == 1:
        return None
    return _command_id(tokens[:-1])
