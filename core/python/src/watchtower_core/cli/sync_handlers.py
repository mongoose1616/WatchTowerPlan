"""Runtime handlers for sync command families."""

from __future__ import annotations

from watchtower_core.cli.sync_document_handlers import (
    DOCUMENT_SYNC_HANDLERS,
)
from watchtower_core.cli.sync_runtime_helpers import run_document_sync_command

SYNC_HANDLERS = {**DOCUMENT_SYNC_HANDLERS}

_SYNC_EXPORT_NAMES = {
    "_run_sync_command_index": "command_index",
    "_run_sync_repository_paths": "repository_paths",
    "_run_sync_route_index": "route_index",
}

globals().update({name: SYNC_HANDLERS[key] for name, key in _SYNC_EXPORT_NAMES.items()})

__all__ = [
    "SYNC_HANDLERS",
    "run_document_sync_command",
    *_SYNC_EXPORT_NAMES,
]
