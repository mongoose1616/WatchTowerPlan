"""Helpers for governed actor lookup and actor-policy enforcement."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import ActorEntry, ActorRegistry


@dataclass(frozen=True, slots=True)
class ActorRegistryIssue:
    """One actor-reference validation issue."""

    issue_code: str
    actor_id: str
    message: str


class ActorRegistryHelper:
    """Resolve governed actors and enforce actor-policy expectations."""

    def __init__(self, registry: ActorRegistry) -> None:
        self._registry = registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> ActorRegistryHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        return cls(context.actor_registry)

    def actor(self, actor_id: str) -> ActorEntry:
        """Return one actor entry by identifier."""

        return self._registry.get(actor_id)

    def has_actor(self, actor_id: str) -> bool:
        """Return whether one actor id is declared."""

        try:
            self.actor(actor_id)
        except KeyError:
            return False
        return True

    def actors_for_type(self, actor_type: str) -> tuple[ActorEntry, ...]:
        """Return declared actors of one actor type."""

        return tuple(entry for entry in self._registry.actors if entry.actor_type == actor_type)

    def validate_actor_reference(
        self,
        actor_id: str,
        *,
        allowed_types: tuple[str, ...] = (),
        allowed_roles: tuple[str, ...] = (),
        allowed_scopes: tuple[str, ...] = (),
    ) -> tuple[ActorRegistryIssue, ...]:
        """Validate one actor id against governed type, role, and scope expectations."""

        try:
            actor = self.actor(actor_id)
        except KeyError:
            return (
                ActorRegistryIssue(
                    issue_code="unknown_actor_id",
                    actor_id=actor_id,
                    message=f"Unknown actor_id: {actor_id}.",
                ),
            )

        issues: list[ActorRegistryIssue] = []
        if allowed_types and actor.actor_type not in allowed_types:
            issues.append(
                ActorRegistryIssue(
                    issue_code="actor_type_mismatch",
                    actor_id=actor_id,
                    message=(
                        f"Actor {actor_id} has actor_type {actor.actor_type}, expected one of "
                        f"{', '.join(allowed_types)}."
                    ),
                )
            )
        if allowed_roles and actor.role not in allowed_roles:
            issues.append(
                ActorRegistryIssue(
                    issue_code="actor_role_mismatch",
                    actor_id=actor_id,
                    message=(
                        f"Actor {actor_id} has role {actor.role or '<unset>'}, expected one of "
                        f"{', '.join(allowed_roles)}."
                    ),
                )
            )
        if allowed_scopes and actor.scope not in allowed_scopes:
            issues.append(
                ActorRegistryIssue(
                    issue_code="actor_scope_mismatch",
                    actor_id=actor_id,
                    message=(
                        f"Actor {actor_id} has scope {actor.scope or '<unset>'}, expected one of "
                        f"{', '.join(allowed_scopes)}."
                    ),
                )
            )
        return tuple(issues)

    def require_actor(
        self,
        actor_id: str,
        *,
        allowed_types: tuple[str, ...] = (),
        allowed_roles: tuple[str, ...] = (),
        allowed_scopes: tuple[str, ...] = (),
    ) -> ActorEntry:
        """Return one actor entry or raise when the reference violates policy."""

        issues = self.validate_actor_reference(
            actor_id,
            allowed_types=allowed_types,
            allowed_roles=allowed_roles,
            allowed_scopes=allowed_scopes,
        )
        if issues:
            raise ValueError(issues[0].message)
        return self.actor(actor_id)


__all__ = ["ActorRegistryHelper", "ActorRegistryIssue"]
