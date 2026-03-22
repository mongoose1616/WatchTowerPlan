"""Helpers for governed append-only event stream records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader

INITIATIVE_EVENT_STREAM_SCHEMA_ID = (
    "urn:watchtower:schema:artifacts:plan:initiative-event-stream:v1"
)
TASK_EVENT_STREAM_SCHEMA_ID = "urn:watchtower:schema:artifacts:plan:task-event-stream:v1"


@dataclass(frozen=True, slots=True)
class EventStreamDescriptor:
    """One concrete event stream root plus identity fields for its records."""

    relative_dir: str
    event_id_prefix: str
    schema_id: str
    initiative_id: str
    trace_id: str | None = None
    task_id: str | None = None

    @classmethod
    def initiative(
        cls,
        *,
        relative_dir: str,
        event_id_prefix: str,
        initiative_id: str,
        trace_id: str,
    ) -> EventStreamDescriptor:
        """Build one initiative-level event stream descriptor."""

        return cls(
            relative_dir=_normalize_relative_dir(relative_dir),
            event_id_prefix=event_id_prefix,
            schema_id=INITIATIVE_EVENT_STREAM_SCHEMA_ID,
            initiative_id=initiative_id,
            trace_id=trace_id,
        )

    @classmethod
    def task(
        cls,
        *,
        relative_dir: str,
        event_id_prefix: str,
        initiative_id: str,
        task_id: str,
    ) -> EventStreamDescriptor:
        """Build one task-level event stream descriptor."""

        return cls(
            relative_dir=_normalize_relative_dir(relative_dir),
            event_id_prefix=event_id_prefix,
            schema_id=TASK_EVENT_STREAM_SCHEMA_ID,
            initiative_id=initiative_id,
            task_id=task_id,
        )


@dataclass(frozen=True, slots=True)
class EventStreamWriteRequest:
    """One requested event write against a descriptor."""

    event_type: str
    actor_id: str
    recorded_at: str
    summary: str
    payload: Mapping[str, Any] | None = None
    related_paths: tuple[str, ...] = ()


class EventStreamHelper:
    """Build, append, validate, and replay governed event stream records."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> EventStreamHelper:
        """Build one helper from a loader and effective pack settings path."""

        effective_pack_settings_path = loader.effective_pack_settings_path(pack_settings_path)
        effective_loader = (
            loader
            if loader.active_pack_settings_path == effective_pack_settings_path
            else loader.derive(active_pack_settings_path=effective_pack_settings_path)
        )
        return cls(effective_loader)

    def build_seed_documents(
        self,
        descriptor: EventStreamDescriptor,
        requests: tuple[EventStreamWriteRequest, ...],
    ) -> dict[str, dict[str, Any]]:
        """Return one deterministic sequence of validated seed event documents."""

        documents: dict[str, dict[str, Any]] = {}
        for sequence, request in enumerate(requests, start=1):
            relative_path, document = self.build_event(
                descriptor,
                request=request,
                sequence=sequence,
            )
            documents[relative_path] = document
        return documents

    def build_event(
        self,
        descriptor: EventStreamDescriptor,
        *,
        request: EventStreamWriteRequest,
        sequence: int,
    ) -> tuple[str, dict[str, Any]]:
        """Build one validated event record for an explicit sequence."""

        if sequence < 1:
            raise ValueError("Event stream sequence must be at least 1.")
        if (
            descriptor.schema_id == INITIATIVE_EVENT_STREAM_SCHEMA_ID
            and descriptor.trace_id is None
        ):
            raise ValueError("Initiative event streams require trace_id.")
        if descriptor.schema_id == TASK_EVENT_STREAM_SCHEMA_ID and descriptor.task_id is None:
            raise ValueError("Task event streams require task_id.")

        relative_path = f"{descriptor.relative_dir}/{sequence:04d}_{request.event_type}.json"
        document: dict[str, Any] = {
            "$schema": descriptor.schema_id,
            "event_id": f"{descriptor.event_id_prefix}.{sequence:04d}_{request.event_type}",
            "initiative_id": descriptor.initiative_id,
            "sequence": sequence,
            "event_type": request.event_type,
            "actor_id": request.actor_id,
            "recorded_at": request.recorded_at,
            "summary": request.summary,
            "payload": dict(request.payload or {}),
        }
        if descriptor.trace_id is not None:
            document["trace_id"] = descriptor.trace_id
        if descriptor.task_id is not None:
            document["task_id"] = descriptor.task_id
        if request.related_paths:
            document["related_paths"] = list(request.related_paths)

        self._loader.schema_store.validate_instance(document, schema_id=descriptor.schema_id)
        return relative_path, document

    def append_event(
        self,
        descriptor: EventStreamDescriptor,
        request: EventStreamWriteRequest,
    ) -> tuple[str, dict[str, Any]]:
        """Append one validated event record to the stream and return it."""

        sequence = self.next_sequence(descriptor)
        relative_path, document = self.build_event(
            descriptor,
            request=request,
            sequence=sequence,
        )
        self._loader.artifact_store.write_json_object(relative_path, document)
        return relative_path, document

    def next_sequence(self, descriptor: EventStreamDescriptor) -> int:
        """Return the next append sequence for one stream."""

        return len(self.replay(descriptor)) + 1

    def replay(self, descriptor: EventStreamDescriptor) -> tuple[dict[str, Any], ...]:
        """Return the validated event records for one stream in deterministic order."""

        stream_dir = self._loader.repo_root / descriptor.relative_dir
        if not stream_dir.exists():
            return ()

        documents: list[dict[str, Any]] = []
        expected_sequence = 1
        for path in sorted(stream_dir.glob("*.json")):
            relative_path = str(path.relative_to(self._loader.repo_root))
            document = self._loader.load_validated_document(relative_path)
            file_sequence, file_event_type = _parse_event_filename(path.name)
            document_sequence = int(document["sequence"])
            if document_sequence != file_sequence:
                raise ValueError(
                    f"Event stream sequence drift in {relative_path}: file sequence "
                    f"{file_sequence} does not match document sequence {document_sequence}."
                )
            if file_sequence != expected_sequence:
                raise ValueError(
                    f"Event stream ordering gap in {relative_path}: expected sequence "
                    f"{expected_sequence}, found {file_sequence}."
                )
            if str(document["event_type"]) != file_event_type:
                raise ValueError(
                    f"Event stream filename drift in {relative_path}: file event type "
                    f"{file_event_type} does not match document event type "
                    f"{document['event_type']}."
                )
            documents.append(document)
            expected_sequence += 1
        return tuple(documents)


def _normalize_relative_dir(relative_dir: str) -> str:
    return relative_dir.strip().strip("/")


def _parse_event_filename(filename: str) -> tuple[int, str]:
    stem = Path(filename).stem
    sequence_text, separator, event_type = stem.partition("_")
    if not separator or not sequence_text.isdigit() or not event_type:
        raise ValueError(f"Invalid event stream filename: {filename}")
    return int(sequence_text), event_type


__all__ = [
    "EventStreamDescriptor",
    "EventStreamHelper",
    "EventStreamWriteRequest",
    "INITIATIVE_EVENT_STREAM_SCHEMA_ID",
    "TASK_EVENT_STREAM_SCHEMA_ID",
]
