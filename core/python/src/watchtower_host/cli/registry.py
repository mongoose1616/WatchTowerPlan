"""Host-owned registry for top-level CLI command families."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PackRegistryEntry, PackRuntimeManifest
from watchtower_core.pack_integration.docs import pack_command_docs_root
from watchtower_core.pack_integration.runtime import load_active_pack_integration

CommandRegistrar = Callable[[argparse._SubParsersAction], object]


@dataclass(frozen=True, slots=True)
class CommandGroupSpec:
    """Registry metadata for one top-level CLI command family."""

    name: str
    registrar: CommandRegistrar
    doc_root: str
    implementation_path: str | None
    subcommand_implementation_paths: tuple[tuple[str, str], ...] = ()
    notes: str | None = None


@dataclass(frozen=True, slots=True)
class PackCommandGroupDiscovery:
    """Metadata-only hosted-pack command discovery that does not import pack code."""

    registry_entry: PackRegistryEntry
    runtime_manifest: PackRuntimeManifest

    @property
    def name(self) -> str:
        return self.registry_entry.command_namespace

    @property
    def doc_root(self) -> str:
        return pack_command_docs_root(docs_root=self.runtime_manifest.owned_roots.docs_root)


QUERY_DISCOVERY_FAMILY_PATH = "core/python/src/watchtower_host/cli/query_discovery_family.py"
QUERY_KNOWLEDGE_FAMILY_PATH = "core/python/src/watchtower_host/cli/query_knowledge_family.py"
QUERY_RECORDS_FAMILY_PATH = "core/python/src/watchtower_host/cli/query_records_family.py"
PACK_FAMILY_HANDLERS_PATH = "core/python/src/watchtower_host/cli/pack_handlers.py"


def _register_doctor_family(subparsers: argparse._SubParsersAction) -> None:
    from watchtower_host.cli.doctor_family import register_doctor_family

    register_doctor_family(subparsers)


def _register_route_family(subparsers: argparse._SubParsersAction) -> None:
    from watchtower_host.cli.route_family import register_route_family

    register_route_family(subparsers)


def _register_query_family(subparsers: argparse._SubParsersAction) -> None:
    from watchtower_host.cli.query_family import register_query_family

    register_query_family(subparsers)


def _register_pack_family(subparsers: argparse._SubParsersAction) -> None:
    from watchtower_host.cli.pack_family import register_pack_family

    register_pack_family(subparsers)


def _register_sync_family(subparsers: argparse._SubParsersAction) -> None:
    from watchtower_host.cli.sync_family import register_sync_family

    register_sync_family(subparsers)


def _register_validate_family(subparsers: argparse._SubParsersAction) -> None:
    from watchtower_host.cli.validate_family import register_validate_family

    register_validate_family(subparsers)


CORE_COMMAND_GROUP_SPECS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(
        name="doctor",
        registrar=_register_doctor_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/doctor_family.py",
    ),
    CommandGroupSpec(
        name="route",
        registrar=_register_route_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/route_family.py",
    ),
    CommandGroupSpec(
        name="query",
        registrar=_register_query_family,
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
        registrar=_register_pack_family,
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
        registrar=_register_sync_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/sync_family.py",
    ),
    CommandGroupSpec(
        name="validate",
        registrar=_register_validate_family,
        doc_root="core/docs/commands/core_python",
        implementation_path="core/python/src/watchtower_host/cli/validate_family.py",
    ),
)


def discover_registered_pack_command_groups(
    loader: ControlPlaneLoader | None = None,
) -> tuple[PackCommandGroupDiscovery, ...]:
    """Return metadata for registered pack namespaces without importing pack modules."""

    active_loader = loader or ControlPlaneLoader()
    discoveries: list[PackCommandGroupDiscovery] = []
    seen_names = {spec.name for spec in CORE_COMMAND_GROUP_SPECS}
    for entry in active_loader.load_pack_registry().packs:
        namespace = entry.command_namespace
        if namespace in seen_names:
            raise ValueError(f"Duplicate top-level command namespace: {namespace}")
        discoveries.append(
            PackCommandGroupDiscovery(
                registry_entry=entry,
                runtime_manifest=active_loader.load_pack_runtime_manifest(
                    pack_settings_path=entry.pack_settings_path
                ),
            )
        )
        seen_names.add(namespace)
    return tuple(discoveries)


def find_registered_pack_command_group(
    command_namespace: str,
    loader: ControlPlaneLoader | None = None,
) -> PackCommandGroupDiscovery | None:
    """Resolve one registered pack namespace by its routed top-level command name."""

    active_loader = loader or ControlPlaneLoader()
    entry = _find_registered_pack_entry(command_namespace, active_loader)
    if entry is None:
        return None
    return PackCommandGroupDiscovery(
        registry_entry=entry,
        runtime_manifest=active_loader.load_pack_runtime_manifest(
            pack_settings_path=entry.pack_settings_path
        ),
    )


def load_pack_command_group_spec(
    command_namespace: str,
    loader: ControlPlaneLoader | None = None,
    *,
    tolerate_import_errors: bool = False,
) -> CommandGroupSpec | None:
    """Load one pack command group, optionally degrading gracefully on import failure."""

    active_loader = loader or ControlPlaneLoader()
    entry = _find_registered_pack_entry(command_namespace, active_loader)
    if entry is None:
        return None
    runtime_manifest = active_loader.load_pack_runtime_manifest(
        pack_settings_path=entry.pack_settings_path
    )
    discovery = PackCommandGroupDiscovery(
        registry_entry=entry,
        runtime_manifest=runtime_manifest,
    )
    try:
        loaded = load_active_pack_integration(
            active_loader,
            pack_settings_path=entry.pack_settings_path,
        )
        if discovery.runtime_manifest.command_namespace != discovery.name:
            raise ValueError(
                "Pack runtime manifest command_namespace does not match the shared pack "
                f"registry: {discovery.runtime_manifest.command_namespace} != {discovery.name}"
            )
        if loaded.integration.command_namespace != discovery.name:
            raise ValueError(
                "Pack integration descriptor command_namespace does not match the shared "
                f"pack registry: {loaded.integration.command_namespace} != {discovery.name}"
            )
        registrar = loaded.integration.command_registration
        if registrar is None:
            raise ValueError(
                "Pack integration descriptor is missing the command_registration hook: "
                f"{discovery.runtime_manifest.integration_module}"
            )
        return CommandGroupSpec(
            name=discovery.name,
            registrar=registrar,
            doc_root=discovery.doc_root,
            implementation_path=(
                loaded.integration.command_implementation_path
                or discovery.registry_entry.pack_runtime_manifest_path
            ),
            subcommand_implementation_paths=(
                loaded.integration.command_subcommand_implementation_paths
            ),
        )
    except Exception as exc:
        if not tolerate_import_errors:
            raise
        return _unavailable_pack_command_group(discovery, exc)


def load_command_group_specs(
    loader: ControlPlaneLoader | None = None,
    *,
    include_pack_namespaces: bool = False,
    tolerate_pack_failures: bool = False,
) -> tuple[CommandGroupSpec, ...]:
    """Return core command groups and optionally the registered pack namespaces."""

    if not include_pack_namespaces:
        return CORE_COMMAND_GROUP_SPECS

    active_loader = loader or ControlPlaneLoader()
    specs = list(CORE_COMMAND_GROUP_SPECS)
    for discovery in discover_registered_pack_command_groups(active_loader):
        loaded_spec = load_pack_command_group_spec(
            discovery.name,
            loader=active_loader,
            tolerate_import_errors=tolerate_pack_failures,
        )
        if loaded_spec is not None:
            specs.append(loaded_spec)
    return tuple(specs)


def _find_registered_pack_entry(
    command_namespace: str,
    loader: ControlPlaneLoader,
) -> PackRegistryEntry | None:
    for entry in loader.load_pack_registry().packs:
        if entry.command_namespace == command_namespace:
            return entry
    return None


def _unavailable_pack_command_group(
    discovery: PackCommandGroupDiscovery,
    exc: Exception,
) -> CommandGroupSpec:
    message = (
        "Registered pack namespace is unavailable because its integration could not be "
        f"loaded: {type(exc).__name__}: {exc}"
    )
    return CommandGroupSpec(
        name=discovery.name,
        registrar=_unavailable_pack_registrar(discovery.name, message),
        doc_root=discovery.doc_root,
        implementation_path=None,
        notes=message,
    )


def _unavailable_pack_registrar(command_namespace: str, message: str) -> CommandRegistrar:
    def _run_unavailable_pack(args: argparse.Namespace) -> int:
        remainder = tuple(getattr(args, "_pack_unavailable_remainder", ()))
        wants_json = False
        for index, token in enumerate(remainder):
            if (
                token == "--format"
                and index + 1 < len(remainder)
                and remainder[index + 1] == "json"
            ):
                wants_json = True
                break
        payload = {
            "command": f"watchtower-core {command_namespace}",
            "status": "error",
            "message": message,
        }
        if wants_json:
            print(json.dumps(payload, sort_keys=True))
        else:
            print(f"Pack namespace unavailable: {message}")
        return 1

    def _registrar(subparsers: argparse._SubParsersAction) -> None:
        parser = subparsers.add_parser(
            command_namespace,
            help=f"{command_namespace} (unavailable)",
            description=message,
        )
        parser.add_argument("_pack_unavailable_remainder", nargs=argparse.REMAINDER)
        parser.set_defaults(handler=_run_unavailable_pack)

    return _registrar


COMMAND_GROUP_SPECS = CORE_COMMAND_GROUP_SPECS


__all__ = [
    "COMMAND_GROUP_SPECS",
    "CORE_COMMAND_GROUP_SPECS",
    "CommandGroupSpec",
    "CommandRegistrar",
    "PACK_FAMILY_HANDLERS_PATH",
    "PackCommandGroupDiscovery",
    "QUERY_DISCOVERY_FAMILY_PATH",
    "QUERY_KNOWLEDGE_FAMILY_PATH",
    "QUERY_RECORDS_FAMILY_PATH",
    "discover_registered_pack_command_groups",
    "find_registered_pack_command_group",
    "load_command_group_specs",
    "load_pack_command_group_spec",
]
