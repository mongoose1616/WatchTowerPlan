"""Host-owned registry for top-level CLI command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.cli.doctor_family import register_doctor_family
from watchtower_core.cli.query_family import register_query_family
from watchtower_core.cli.route_family import register_route_family
from watchtower_core.cli.sync_family import register_sync_family
from watchtower_core.cli.validate_family import register_validate_family
from watchtower_core.pack_integration.runtime import load_registered_pack_integrations
from watchtower_host.cli.closeout import register_closeout_family

CommandRegistrar = Callable[[argparse._SubParsersAction], None]


@dataclass(frozen=True, slots=True)
class CommandGroupSpec:
    """Registry metadata for one top-level CLI command family."""

    name: str
    registrar: CommandRegistrar
    implementation_path: str
    subcommand_implementation_paths: tuple[tuple[str, str], ...] = ()


QUERY_DISCOVERY_FAMILY_PATH = "core/python/src/watchtower_core/cli/query_discovery_family.py"
QUERY_KNOWLEDGE_FAMILY_PATH = "core/python/src/watchtower_core/cli/query_knowledge_family.py"
QUERY_RECORDS_FAMILY_PATH = "core/python/src/watchtower_core/cli/query_records_family.py"

CORE_COMMAND_GROUP_SPECS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(
        name="doctor",
        registrar=register_doctor_family,
        implementation_path="core/python/src/watchtower_core/cli/doctor_family.py",
    ),
    CommandGroupSpec(
        name="route",
        registrar=register_route_family,
        implementation_path="core/python/src/watchtower_core/cli/route_family.py",
    ),
    CommandGroupSpec(
        name="query",
        registrar=register_query_family,
        implementation_path="core/python/src/watchtower_core/cli/query_family.py",
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
        name="closeout",
        registrar=register_closeout_family,
        implementation_path="core/python/src/watchtower_host/cli/closeout.py",
    ),
    CommandGroupSpec(
        name="sync",
        registrar=register_sync_family,
        implementation_path="core/python/src/watchtower_core/cli/sync_family.py",
    ),
    CommandGroupSpec(
        name="validate",
        registrar=register_validate_family,
        implementation_path="core/python/src/watchtower_core/cli/validate_family.py",
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
    "QUERY_DISCOVERY_FAMILY_PATH",
    "QUERY_KNOWLEDGE_FAMILY_PATH",
    "QUERY_RECORDS_FAMILY_PATH",
    "load_command_group_specs",
]
