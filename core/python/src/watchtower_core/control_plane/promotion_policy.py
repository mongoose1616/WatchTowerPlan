"""Helpers for governed promotion-policy resolution and alignment checks."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.documentation_family import DocumentationFamilyHelper
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import PromotionPolicyEntry, PromotionPolicyRegistry


@dataclass(frozen=True, slots=True)
class PromotionPolicyIssue:
    """One promotion-policy issue discovered against registry state."""

    issue_code: str
    policy_id: str
    message: str


class PromotionPolicyHelper:
    """Resolve promotion-policy behavior for initiative-local guidance extraction."""

    def __init__(self, registry: PromotionPolicyRegistry) -> None:
        self._registry = registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> PromotionPolicyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("promotion_policy_registry")
        if not isinstance(registry, PromotionPolicyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed promotion_policy_registry."
            )
        return cls(registry)

    def policy(self, policy_id: str) -> PromotionPolicyEntry:
        """Return one policy entry by identifier."""

        return self._registry.get(policy_id)

    def policies_for_source_kind(
        self,
        source_artifact_kind: str,
    ) -> tuple[PromotionPolicyEntry, ...]:
        """Return active policies that allow one source artifact kind."""

        return tuple(
            entry
            for entry in self._registry.entries
            if entry.entry_status == "active"
            and source_artifact_kind in entry.source_artifact_kinds
        )

    def resolve(
        self,
        *,
        source_artifact_kind: str,
        target_family: str,
    ) -> PromotionPolicyEntry:
        """Resolve one active promotion policy for a source-kind/family pair."""

        matches = tuple(
            entry
            for entry in self.policies_for_source_kind(source_artifact_kind)
            if entry.target_family == target_family
        )
        if not matches:
            raise KeyError(f"{source_artifact_kind}:{target_family}")
        if len(matches) > 1:
            raise ValueError(
                "Multiple active promotion policies match "
                f"{source_artifact_kind}:{target_family}."
            )
        return matches[0]

    def validate_alignment(
        self,
        documentation_helper: DocumentationFamilyHelper,
    ) -> tuple[PromotionPolicyIssue, ...]:
        """Validate that promotion policies point at allowed documentation-family roots."""

        issues: list[PromotionPolicyIssue] = []
        for entry in self._registry.entries:
            if entry.entry_status != "active":
                continue
            family = documentation_helper.family(entry.target_family)
            normalized_root = entry.target_root.strip().strip("/")
            if normalized_root not in family.allowed_roots:
                issues.append(
                    PromotionPolicyIssue(
                        issue_code="target_root_not_allowed",
                        policy_id=entry.policy_id,
                        message=(
                            f"Promotion policy {entry.policy_id} targets {normalized_root}, "
                            f"which is not an allowed root for documentation family "
                            f"{entry.target_family}."
                        ),
                    )
                )
            if entry.mirror_update_mode != "none":
                missing_roots = tuple(
                    root for root in entry.mirror_roots if root not in family.allowed_roots
                )
                if missing_roots:
                    issues.append(
                        PromotionPolicyIssue(
                            issue_code="mirror_root_not_allowed",
                            policy_id=entry.policy_id,
                            message=(
                                f"Promotion policy {entry.policy_id} declares mirror roots "
                                f"{', '.join(missing_roots)} that are not allowed roots for "
                                f"documentation family {entry.target_family}."
                            ),
                        )
                    )
        return tuple(issues)


__all__ = ["PromotionPolicyHelper", "PromotionPolicyIssue"]
