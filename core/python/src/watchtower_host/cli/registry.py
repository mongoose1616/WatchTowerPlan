"""Host-owned registry for top-level CLI command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.pack_integration import pack_command_docs_root
from watchtower_core.pack_integration.runtime import load_registered_pack_integrations
from watchtower_host.cli.doctor_family import register_doctor_family
from watchtower_host.cli.pack_family import register_pack_family
from watchtower_host.cli.query_family import register_query_family
from watchtower_host.cli.route_family import register_route_family
from watchtower_host.cli.sync_family import register_sync_family
from watchtower_host.cli.validate_family import register_validate_family

CommandRegistrar = Callable[[argparse._SubParsersAction], None]


@dataclass(frozen=True, slots=True)
class CommandGroupSpec:
    """Registry metadata for one top-level CLI command family."""

    name: str
    registrar: CommandRegistrar
    doc_root: str
    implementation_path: str
    subcommand_implementation_paths: tuple[tuple[str, str], ...] = ()


QUERY_DISCOVERY_FAMILY_PATH = "core/python/src/watchtower_host/cli/query_discovery_family.py"
QUERY_KNOWLEDGE_FAMILY_PATH = "core/python/src/watchtower_host/cli/query_knowledge_family.py"
QUERY_RECORDS_FAMILY_PATH = "core/python/src/watchtower_host/cli/query_records_family.py"
PACK_FAMILY_HANDLERS_PATH = "core/python/src/watchtower_host/cli/pack_handlers.py"

CORE_COMMAND_GROUP_SPECS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(
        name="doctor",
        registrar=register_doctor_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/doctor_family.py",
    ),
    CommandGroupSpec(
        name="route",
        registrar=register_route_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/route_family.py",
    ),
    CommandGroupSpec(
        name="query",
        registrar=register_query_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/query_family.py",
        subcommand_implementation_paths=(
            ("paths", QUERY_DISCOVERY_FAMILY_PATH),
            ("commands", QUERY_DISCOVERY_FAMILY_PATH),
            ("foundations", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("workflows", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("references", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("standards", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("acceptance", QUERY_RECORDS_FAMILY_PATH),
            ("evidence", QUERY_RECORDS_FAMILY_PATH),
        ),
    ),
    CommandGroupSpec(
        name="pack",
        registrar=register_pack_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/pack_family.py",
        subcommand_implementation_paths=(
            ("bootstrap", PACK_FAMILY_HANDLERS_PATH),
            ("list", PACK_FAMILY_HANDLERS_PATH),
            ("describe", PACK_FAMILY_HANDLERS_PATH),
            ("validate", PACK_FAMILY_HANDLERS_PATH),
            ("scaffold", PACK_FAMILY_HANDLERS_PATH),
        ),
    ),
    CommandGroupSpec(
        name="sync",
        registrar=register_sync_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/sync_family.py",
    ),
    CommandGroupSpec(
        name="validate",
        registrar=register_validate_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/validate_family.py",
    ),
)


def load_command_group_specs(
    loader: ControlPlaneLoader | None = None,
) -> tuple[CommandGroupSpec, ...]:
    """Return the host-owned core command groups plus registered pack namespaces."""

    active_loader = loader or ControlPlaneLoader()
    specs = list(CORE_COMMAND_GROUP_SPECS)
    seen_names = {spec.name for spec in specs}
    for loaded in load_registered_pack_integrations(active_loader):
        registrar = loaded.integration.command_registration
        if registrar is None:
            continue
        namespace = loaded.integration.command_namespace
        if namespace in seen_names:
            raise ValueError(f"Duplicate top-level command namespace: {namespace}")
        specs.append(
            CommandGroupSpec(
                name=namespace,
                registrar=registrar,
                doc_root=pack_command_docs_root(
                    docs_root=loaded.runtime_manifest.owned_roots.docs_root
                ),
                implementation_path=loaded.integration.command_implementation_path
                or loaded.registry_entry.pack_runtime_manifest_path,
                subcommand_implementation_paths=loaded.integration.command_subcommand_implementation_paths,
            )
        )
        seen_names.add(namespace)
    return tuple(specs)


COMMAND_GROUP_SPECS = load_command_group_specs()


__all__ = [
    "COMMAND_GROUP_SPECS",
    "CORE_COMMAND_GROUP_SPECS",
    "CommandGroupSpec",
    "CommandRegistrar",
    "PACK_FAMILY_HANDLERS_PATH",
    "QUERY_DISCOVERY_FAMILY_PATH",
    "QUERY_KNOWLEDGE_FAMILY_PATH",
    "QUERY_RECORDS_FAMILY_PATH",
    "load_command_group_specs",
]
