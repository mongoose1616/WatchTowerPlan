"""Document-oriented sync command handlers."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from typing import TypedDict

from watchtower_core.cli.sync_runtime_helpers import (
    load_document_sync_service,
    run_document_sync_command,
)


class _DocumentHandlerSpec(TypedDict):
    handler_key: str
    export_name: str
    module_name: str
    class_name: str
    command_name: str
    artifact_label: str


_DOCUMENT_SYNC_HANDLER_SPECS: tuple[_DocumentHandlerSpec, ...] = (
    {
        "handler_key": "repository_paths",
        "export_name": "_run_sync_repository_paths",
        "module_name": "watchtower_core.sync.repository_paths",
        "class_name": "RepositoryPathIndexSyncService",
        "command_name": "watchtower-core sync repository-paths",
        "artifact_label": "repository path index",
    },
    {
        "handler_key": "command_index",
        "export_name": "_run_sync_command_index",
        "module_name": "watchtower_host.cli.command_index",
        "class_name": "CommandIndexSyncService",
        "command_name": "watchtower-core sync command-index",
        "artifact_label": "command index",
    },
    {
        "handler_key": "route_index",
        "export_name": "_run_sync_route_index",
        "module_name": "watchtower_core.sync.route_index",
        "class_name": "RouteIndexSyncService",
        "command_name": "watchtower-core sync route-index",
        "artifact_label": "route index",
    },
)


def _build_document_sync_handler(
    spec: _DocumentHandlerSpec,
) -> Callable[[argparse.Namespace], int]:
    def _handler(args: argparse.Namespace) -> int:
        return run_document_sync_command(
            args,
            command_name=spec["command_name"],
            artifact_label=spec["artifact_label"],
            service=load_document_sync_service(spec["module_name"], spec["class_name"]),
        )

    _handler.__name__ = spec["export_name"]
    return _handler


DOCUMENT_SYNC_HANDLERS: dict[str, Callable[[argparse.Namespace], int]] = {
    spec["handler_key"]: _build_document_sync_handler(spec)
    for spec in _DOCUMENT_SYNC_HANDLER_SPECS
}

globals().update(
    {
        spec["export_name"]: DOCUMENT_SYNC_HANDLERS[spec["handler_key"]]
        for spec in _DOCUMENT_SYNC_HANDLER_SPECS
    }
)

__all__ = [
    "DOCUMENT_SYNC_HANDLERS",
    *[spec["export_name"] for spec in _DOCUMENT_SYNC_HANDLER_SPECS],
]
