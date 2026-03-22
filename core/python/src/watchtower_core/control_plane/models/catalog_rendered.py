"""Rendered-surface registry models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RenderedSurfaceColumnDefinition:
    """Rendered-surface column definition."""

    header: str
    field: str
    formatter: str
    path_field: str | None = None
    label_field: str | None = None
    empty_value: str | None = None
    enabled_when_key: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceColumnDefinition:
        return cls(
            header=document["header"],
            field=document["field"],
            formatter=document["formatter"],
            path_field=document.get("path_field"),
            label_field=document.get("label_field"),
            empty_value=document.get("empty_value"),
            enabled_when_key=document.get("enabled_when_key"),
        )


@dataclass(frozen=True, slots=True)
class RenderedSurfaceSectionDefinition:
    """Rendered-surface section definition."""

    section_id: str
    kind: str
    source_key: str
    title: str | None = None
    empty_message: str | None = None
    columns: tuple[RenderedSurfaceColumnDefinition, ...] = ()
    label_field: str | None = None
    count_field: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceSectionDefinition:
        return cls(
            section_id=document["section_id"],
            kind=document["kind"],
            source_key=document["source_key"],
            title=document.get("title"),
            empty_message=document.get("empty_message"),
            columns=tuple(
                RenderedSurfaceColumnDefinition.from_document(item)
                for item in document.get("columns", ())
            ),
            label_field=document.get("label_field"),
            count_field=document.get("count_field"),
        )


@dataclass(frozen=True, slots=True)
class RenderedSurfaceDefinition:
    """Rendered-surface registry entry."""

    surface_id: str
    title: str
    output_path: str
    sections: tuple[RenderedSurfaceSectionDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceDefinition:
        return cls(
            surface_id=document["surface_id"],
            title=document["title"],
            output_path=document["output_path"],
            sections=tuple(
                RenderedSurfaceSectionDefinition.from_document(item)
                for item in document["sections"]
            ),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class RenderedSurfaceRegistry:
    """Typed rendered-surface registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    surfaces: tuple[RenderedSurfaceDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            surfaces=tuple(
                RenderedSurfaceDefinition.from_document(item) for item in document["surfaces"]
            ),
        )

    def get(self, surface_id: str) -> RenderedSurfaceDefinition:
        """Return one rendered-surface definition by identifier."""
        for surface in self.surfaces:
            if surface.surface_id == surface_id:
                return surface
        raise KeyError(surface_id)
