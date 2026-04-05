"""NDJSON event stream engine for governed append-only event records.

Each event stream is a single ``.ndjson`` file where every line is one
self-contained JSON event record.  The engine provides deterministic
sequencing, optional JSON-schema validation on write, and ordered
replay for consumers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader


@dataclass(frozen=True, slots=True)
class EventStreamConfig:
    """Identity and validation configuration for one event stream.

    *relative_path* is the repo-relative POSIX path to the ``.ndjson``
    file (e.g. ``"plan/initiatives/tr001/events.ndjson"``).

    *schema_id* is an optional versioned JSON-schema URN.  When set,
    every event appended through :meth:`NdjsonEventStream.append` is
    validated against the schema via the loader's schema store before
    being written.
    """

    relative_path: str
    schema_id: str | None = None


class NdjsonEventStream:
    """Read, append, and replay a single NDJSON event stream file."""

    def __init__(self, loader: ControlPlaneLoader, config: EventStreamConfig) -> None:
        self._loader = loader
        self._config = config
        self._path = loader.repo_root / config.relative_path

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def replay(self) -> tuple[dict[str, Any], ...]:
        """Return all event records in file order."""

        return tuple(self._iter_entries())

    def entry_count(self) -> int:
        """Return the number of events currently in the stream."""

        return len(self._iter_entries())

    def next_sequence(self) -> int:
        """Return the next 1-based sequence number for the stream."""

        return self.entry_count() + 1

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        """Validate (if configured) and append one event record.

        Returns the event as written (unchanged).
        """

        if self._config.schema_id is not None:
            self._loader.schema_store.validate_instance(
                event, schema_id=self._config.schema_id
            )
        self._ensure_parent()
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, sort_keys=True))
            fh.write("\n")
        return event

    def append_many(self, events: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
        """Validate (if configured) and append multiple event records atomically.

        All events are validated before any are written.
        Returns the events as written.
        """

        if self._config.schema_id is not None:
            for event in events:
                self._loader.schema_store.validate_instance(
                    event, schema_id=self._config.schema_id
                )
        self._ensure_parent()
        with self._path.open("a", encoding="utf-8") as fh:
            for event in events:
                fh.write(json.dumps(event, sort_keys=True))
                fh.write("\n")
        return events

    def seed(self, events: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
        """Write the initial set of events to a new stream file.

        Raises ``FileExistsError`` if the stream file already exists.
        Validates all events before writing if a schema is configured.
        Returns the events as written.
        """

        if self._path.exists():
            raise FileExistsError(
                f"Event stream already exists: {self._config.relative_path}"
            )
        if self._config.schema_id is not None:
            for event in events:
                self._loader.schema_store.validate_instance(
                    event, schema_id=self._config.schema_id
                )
        self._ensure_parent()
        content = "".join(
            f"{json.dumps(event, sort_keys=True)}\n" for event in events
        )
        self._path.write_text(content, encoding="utf-8")
        return events

    def overwrite(self, events: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
        """Replace the entire stream with *events*.

        Use sparingly — the normal pattern is append-only.  This exists
        for migration tooling and export cleanup that must rewrite a
        stream deterministically.

        Validates all events before writing if a schema is configured.
        Returns the events as written.
        """

        if self._config.schema_id is not None:
            for event in events:
                self._loader.schema_store.validate_instance(
                    event, schema_id=self._config.schema_id
                )
        self._ensure_parent()
        content = "".join(
            f"{json.dumps(event, sort_keys=True)}\n" for event in events
        )
        self._path.write_text(content, encoding="utf-8")
        return events

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _iter_entries(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        entries: list[dict[str, Any]] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            entries.append(json.loads(stripped))
        return entries

    def _ensure_parent(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
