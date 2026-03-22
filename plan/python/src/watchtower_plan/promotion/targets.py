"""Promotion target-kind and path selection helpers."""

from __future__ import annotations

import re
from pathlib import Path

_SOURCE_ARTIFACT_KIND_BY_FILENAME = {
    "initiative_brief.md": "initiative_brief",
    "design_record.md": "design_record",
    "implementation_slice.md": "implementation_slice",
    "decision_notes.md": "decision_notes",
}
_DEFAULT_TARGET_FAMILY_BY_SOURCE_KIND = {
    "initiative_brief": "reference",
    "design_record": "decision_record",
    "implementation_slice": "pattern",
    "decision_notes": "standard",
}
_GUIDANCE_ID_PREFIX_BY_FAMILY = {
    "decision_record": "decision",
}


def source_artifact_kind_for_path(source_path: str) -> str:
    """Resolve the initiative-local source artifact kind for one authored input path."""

    filename = Path(source_path).name
    try:
        return _SOURCE_ARTIFACT_KIND_BY_FILENAME[filename]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported promotion source artifact: {source_path}"
        ) from exc


def default_target_family_for_source_kind(source_artifact_kind: str) -> str:
    """Return the default target family for one source artifact kind."""

    try:
        return _DEFAULT_TARGET_FAMILY_BY_SOURCE_KIND[source_artifact_kind]
    except KeyError as exc:
        raise ValueError(
            f"No default target family exists for source artifact kind {source_artifact_kind}."
        ) from exc


def default_target_path(
    *,
    initiative_slug: str,
    source_path: str,
    target_family: str,
    target_root: str,
) -> str:
    """Return the default target path for one promoted guidance output."""

    source_stem = Path(source_path).stem
    filename = f"{initiative_slug}_{source_stem}.md"
    if target_family == "standard" and Path(target_root).name == "standards":
        return f"{target_root}/governance/{filename}"
    return f"{target_root}/{filename}"


def default_mirror_target_paths(
    *,
    target_path: str,
    target_root: str,
    mirror_roots: tuple[str, ...],
) -> tuple[str, ...]:
    """Return deterministic mirror targets for one promoted guidance output."""

    relative_suffix = target_path.removeprefix(f"{target_root}/")
    return tuple(
        f"{root}/{relative_suffix}" for root in mirror_roots if root != target_root
    )


def guidance_id_for_target_path(target_family: str, target_path: str) -> str:
    """Return the default guidance identifier for one promoted target path."""

    stem = Path(target_path).stem
    prefix = _GUIDANCE_ID_PREFIX_BY_FAMILY.get(target_family, target_family)
    return f"{prefix}.{stem}"


def guidance_trace_id_for_target_path(target_path: str) -> str:
    """Return the durable trace identifier for one promoted guidance target."""

    stem = Path(target_path).stem
    normalized_stem = (
        re.sub(r"[^a-z0-9]+", "_", stem.casefold()).strip("_") or "guidance"
    )
    return f"trace.guidance.{normalized_stem}"
