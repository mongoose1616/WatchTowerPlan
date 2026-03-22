"""Deterministic helpers for finding hosted-pack settings manifests."""

from __future__ import annotations

from pathlib import Path

_PACK_SETTINGS_DISCOVERY_PATTERNS: tuple[str, ...] = (
    "*/.wt/manifests/pack_settings.json",
    "packs/*/.wt/manifests/pack_settings.json",
)


def discover_pack_settings_paths(repo_root: Path) -> tuple[str, ...]:
    """Return discoverable hosted-pack settings paths in deterministic order.

    Direct first-party/root packs such as `plan/` or `oversight/` are preferred
    ahead of nested `packs/<slug>/` layouts. The manifest path remains the real
    discovery marker; directory shape only affects fallback ordering.
    """

    discovered: list[str] = []
    seen: set[str] = set()
    for pattern in _PACK_SETTINGS_DISCOVERY_PATTERNS:
        for candidate in sorted(repo_root.glob(pattern)):
            if not candidate.is_file():
                continue
            relative_path = candidate.relative_to(repo_root).as_posix()
            if relative_path in seen:
                continue
            discovered.append(relative_path)
            seen.add(relative_path)
    return tuple(discovered)


__all__ = ["discover_pack_settings_paths"]
