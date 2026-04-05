"""Routing overlay and merge-policy catalog models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RouteOverlayDefinition:
    """One governed route-overlay entry."""

    overlay_id: str
    entry_status: str
    title: str
    trigger_terms: tuple[str, ...]
    trigger_mode: str
    anchor_terms: tuple[str, ...] = ()
    compatible_task_types: tuple[str, ...] = ()
    excluded_task_types: tuple[str, ...] = ()
    attached_workflow_ids: tuple[str, ...] = ()
    attached_route_task_types: tuple[str, ...] = ()
    retain_dominant_compatible_route: bool = False
    minimum_route_score: int = 0
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RouteOverlayDefinition:
        return cls(
            overlay_id=document["overlay_id"],
            entry_status=document["entry_status"],
            title=document["title"],
            trigger_terms=tuple(document["trigger_terms"]),
            trigger_mode=document["trigger_mode"],
            anchor_terms=tuple(document.get("anchor_terms", ())),
            compatible_task_types=tuple(document.get("compatible_task_types", ())),
            excluded_task_types=tuple(document.get("excluded_task_types", ())),
            attached_workflow_ids=tuple(document.get("attached_workflow_ids", ())),
            attached_route_task_types=tuple(document.get("attached_route_task_types", ())),
            retain_dominant_compatible_route=bool(
                document.get("retain_dominant_compatible_route", False)
            ),
            minimum_route_score=int(document.get("minimum_route_score", 0)),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class RouteOverlayRegistry:
    """Typed route-overlay registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[RouteOverlayDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RouteOverlayRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                RouteOverlayDefinition.from_document(item) for item in document["entries"]
            ),
            notes=document.get("notes"),
        )

    def get(self, overlay_id: str) -> RouteOverlayDefinition:
        """Return one route-overlay entry by identifier."""

        for entry in self.entries:
            if entry.overlay_id == overlay_id:
                return entry
        raise KeyError(overlay_id)

    @classmethod
    def merge(cls, *registries: RouteOverlayRegistry) -> RouteOverlayRegistry:
        """Return one merged route-overlay registry."""

        if not registries:
            raise ValueError("At least one route overlay registry is required.")
        schema_id = registries[0].schema_id
        artifact_id = registries[0].artifact_id
        title = registries[0].title
        status = registries[0].status
        notes = registries[0].notes
        merged_entries: dict[str, RouteOverlayDefinition] = {}
        for registry in registries:
            if registry.schema_id != schema_id:
                raise ValueError(
                    "Route overlay registries must share the same schema_id: "
                    f"{registry.schema_id} != {schema_id}"
                )
            if registry.artifact_id != artifact_id:
                raise ValueError(
                    "Route overlay registries must share the same artifact_id: "
                    f"{registry.artifact_id} != {artifact_id}"
                )
            for entry in registry.entries:
                existing = merged_entries.get(entry.overlay_id)
                if existing is None:
                    merged_entries[entry.overlay_id] = entry
                    continue
                if existing != entry:
                    raise ValueError(
                        "Route overlay registries declare conflicting entries for "
                        f"{entry.overlay_id}"
                    )
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=tuple(merged_entries[key] for key in sorted(merged_entries)),
            notes=notes,
        )


@dataclass(frozen=True, slots=True)
class RouteMergePolicyDefinition:
    """One governed route-merge policy entry."""

    rule_id: str
    entry_status: str
    title: str
    priority: int
    suppress_task_types: tuple[str, ...]
    when_any_task_types_present: tuple[str, ...] = ()
    when_all_task_types_present: tuple[str, ...] = ()
    when_request_terms_present_any: tuple[str, ...] = ()
    unless_request_terms_present_any: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RouteMergePolicyDefinition:
        return cls(
            rule_id=document["rule_id"],
            entry_status=document["entry_status"],
            title=document["title"],
            priority=int(document["priority"]),
            suppress_task_types=tuple(document["suppress_task_types"]),
            when_any_task_types_present=tuple(document.get("when_any_task_types_present", ())),
            when_all_task_types_present=tuple(document.get("when_all_task_types_present", ())),
            when_request_terms_present_any=tuple(
                document.get("when_request_terms_present_any", ())
            ),
            unless_request_terms_present_any=tuple(
                document.get("unless_request_terms_present_any", ())
            ),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class RouteMergePolicyRegistry:
    """Typed route-merge policy registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[RouteMergePolicyDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RouteMergePolicyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                RouteMergePolicyDefinition.from_document(item) for item in document["entries"]
            ),
            notes=document.get("notes"),
        )

    def get(self, rule_id: str) -> RouteMergePolicyDefinition:
        """Return one route-merge policy entry by identifier."""

        for entry in self.entries:
            if entry.rule_id == rule_id:
                return entry
        raise KeyError(rule_id)

    @classmethod
    def merge(cls, *registries: RouteMergePolicyRegistry) -> RouteMergePolicyRegistry:
        """Return one merged route-merge policy registry."""

        if not registries:
            raise ValueError("At least one route merge policy registry is required.")
        schema_id = registries[0].schema_id
        artifact_id = registries[0].artifact_id
        title = registries[0].title
        status = registries[0].status
        notes = registries[0].notes
        merged_entries: dict[str, RouteMergePolicyDefinition] = {}
        for registry in registries:
            if registry.schema_id != schema_id:
                raise ValueError(
                    "Route merge policy registries must share the same schema_id: "
                    f"{registry.schema_id} != {schema_id}"
                )
            if registry.artifact_id != artifact_id:
                raise ValueError(
                    "Route merge policy registries must share the same artifact_id: "
                    f"{registry.artifact_id} != {artifact_id}"
                )
            for entry in registry.entries:
                existing = merged_entries.get(entry.rule_id)
                if existing is None:
                    merged_entries[entry.rule_id] = entry
                    continue
                if existing != entry:
                    raise ValueError(
                        "Route merge policy registries declare conflicting entries for "
                        f"{entry.rule_id}"
                    )
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=tuple(merged_entries[key] for key in sorted(merged_entries)),
            notes=notes,
        )
