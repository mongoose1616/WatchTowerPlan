"""Promotion front-matter and durable markdown rendering helpers."""

# ruff: noqa: E501

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from watchtower_core.adapters.front_matter import render_front_matter
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.promotion.targets import (
    guidance_id_for_target_path,
    guidance_trace_id_for_target_path,
)

_AUTHORITY_BY_FAMILY = {
    "reference": "reference",
    "decision_record": "authoritative",
    "pattern": "authoritative",
    "standard": "authoritative",
    "foundation": "authoritative",
}


def build_guidance_front_matter(
    *,
    initiative_document: dict[str, Any],
    promotion_document: dict[str, Any],
    source_path: str,
    source_artifact_kind: str,
    target_family: str,
    target_path: str,
    mirror_target_paths: tuple[str, ...],
    updated_at: str,
    source_title: str | None,
    source_summary: str | None,
) -> dict[str, Any]:
    """Build front matter for one promoted guidance document."""

    initiative_title = str(initiative_document["title"])
    _ = source_path
    _ = promotion_document
    title = guidance_title(
        initiative_title=initiative_title,
        target_family=target_family,
        source_artifact_kind=source_artifact_kind,
        source_title=source_title,
    )
    summary = guidance_summary(
        initiative_title=initiative_title,
        initiative_summary=str(initiative_document["summary"]),
        target_family=target_family,
        source_artifact_kind=source_artifact_kind,
        source_summary=source_summary,
    )
    promoted_paths = list(dict.fromkeys((target_path, *mirror_target_paths)))
    front_matter: dict[str, Any] = {
        "trace_id": guidance_trace_id_for_target_path(target_path),
        "id": guidance_id_for_target_path(target_family, target_path),
        "title": title,
        "summary": summary,
        "type": target_family,
        "status": "active",
        "owner": str(initiative_document["owner"]),
        "updated_at": updated_at,
        "audience": "shared",
        "authority": _AUTHORITY_BY_FAMILY[target_family],
        "applies_to": [
            *promoted_paths,
            "plan/python/src/watchtower_plan/promotion/service.py",
            "plan/.wt/registries/promotion_policy_registry.json",
            "plan/.wt/indexes/guidance_index.json",
            "plan/.wt/indexes/promotion_index.json",
        ],
    }
    if target_family == "reference":
        front_matter["tags"] = [
            "promoted_guidance",
            target_family,
            "guidance_promotion",
            source_artifact_kind,
        ]
    return front_matter


def render_guidance_document(
    *,
    initiative_document: dict[str, Any],
    promotion_document: dict[str, Any],
    source_path: str,
    source_artifact_kind: str,
    target_family: str,
    target_path: str,
    mirror_target_paths: tuple[str, ...],
    template_path: Path,
    updated_at: str,
    source_title: str | None,
    source_summary: str | None,
    documentation_helper: Any,
    pack_loader: ControlPlaneLoader,
) -> str:
    """Render one governed markdown guidance document with validated front matter."""

    front_matter = build_guidance_front_matter(
        initiative_document=initiative_document,
        promotion_document=promotion_document,
        source_path=source_path,
        source_artifact_kind=source_artifact_kind,
        target_family=target_family,
        target_path=target_path,
        mirror_target_paths=mirror_target_paths,
        updated_at=updated_at,
        source_title=source_title,
        source_summary=source_summary,
    )
    family = documentation_helper.family(target_family)
    pack_loader.schema_store.validate_instance(
        front_matter,
        schema_id=family.front_matter_schema_id,
    )
    body = render_guidance_body(
        initiative_document=initiative_document,
        promotion_document=promotion_document,
        source_path=source_path,
        source_artifact_kind=source_artifact_kind,
        source_title=source_title,
        source_summary=source_summary,
        target_family=target_family,
        target_path=target_path,
        template_path=template_path,
        document_title=str(front_matter["title"]),
        document_summary=str(front_matter["summary"]),
        updated_at=updated_at,
    )
    return f"---\n{render_front_matter(front_matter)}\n---\n\n{body}"


def render_guidance_body(
    *,
    initiative_document: dict[str, Any],
    promotion_document: dict[str, Any],
    source_path: str,
    source_artifact_kind: str,
    source_title: str | None,
    source_summary: str | None,
    target_family: str,
    target_path: str,
    template_path: Path,
    document_title: str,
    document_summary: str,
    updated_at: str,
) -> str:
    """Render the markdown body for one promoted guidance output."""

    _ = template_path
    _ = promotion_document
    source_label = source_title or readable_source_artifact_kind(source_artifact_kind)
    source_summary_line = source_summary or str(initiative_document["summary"])
    if target_family == "reference":
        return (
            f"# {document_title}\n\n"
            "## Subject Summary\n\n"
            f"This reference captures the durable operating model for governed guidance promotion. "
            f"{source_summary_line}\n\n"
            "## Usage Guidance\n\n"
            "- Use this reference when implementing or reviewing promotion of initiative-local inputs into `plan/docs/**`.\n"
            "- Treat `plan/.wt/registries/promotion_policy_registry.json`, `plan/.wt/indexes/guidance_index.json`, and `plan/.wt/indexes/promotion_index.json` as the machine companions for this document.\n\n"
            "## Boundaries\n\n"
            "- Durable guidance belongs in `plan/docs/**`.\n"
            "- Live execution state, closeout artifacts, and evidence bundles remain under initiative-local `plan/**` roots.\n\n"
            "## Related Surfaces\n\n"
            f"- `{target_path}`\n"
            "- `plan/python/src/watchtower_plan/promotion/service.py`\n"
            "- `plan/.wt/indexes/guidance_index.json`\n"
            "- `plan/.wt/indexes/promotion_index.json`\n\n"
            "## Notes\n\n"
            "- Keep this document durable; initiative-local authored inputs are temporary proof surfaces, not long-term guidance roots.\n"
        )
    if target_family == "decision_record":
        return (
            f"# {document_title}\n\n"
            "## Context\n\n"
            "This decision defines how validated initiative-local outputs become durable plan guidance. "
            f"{source_summary_line}\n\n"
            "## Decision\n\n"
            "- Durable guidance must be promoted through governed policy, family, and template contracts rather than being copied ad hoc from live initiative inputs.\n"
            "- Machine-readable promotion and guidance indexes must preserve provenance without forcing durable docs to retain live initiative package references.\n\n"
            "## Consequences\n\n"
            "- Promotion output stays aligned with machine-readable policy and indexing surfaces.\n"
            "- Durable guidance can move out of initiative-local planning state without blocking purge of closed initiative packages.\n"
            "- Future closeout and retention flows can treat promoted docs as authority and initiative artifacts as temporary state.\n\n"
            "## Current Status or Supersession Notes\n\n"
            "- Active as durable guidance under `plan/docs/**`.\n"
            "- Promotion policy and promotion-index records carry the machine-readable provenance for this guidance family.\n"
        )
    if target_family == "pattern":
        return (
            f"# {document_title}\n\n"
            "## Scenario\n\n"
            "Use this pattern when one initiative-local authored input needs to become durable shared guidance without turning `plan/docs/` into a second live workspace. "
            f"{source_summary_line}\n\n"
            "## Recommended Structure\n\n"
            "- Resolve the promotion policy from source artifact kind and target family.\n"
            "- Write the durable document under the governed target root with valid front matter and template headings.\n"
            "- Rebuild the guidance and promotion indexes in the same change.\n\n"
            "## Boundaries or Constraints\n\n"
            "- Promotion is not a substitute for live initiative state or rendered plan views.\n"
            "- Mirrored foundations must update all required roots in the same change set.\n\n"
            "## Usage Notes\n\n"
            f"- Use this pattern for `{source_label}` promotion into durable guidance families.\n"
            "- Keep durable guidance self-contained and rely on machine indexes for provenance.\n\n"
            "## Illustrative Example\n\n"
            f"- Promote a validated initiative-local `{source_artifact_kind.replace('_', ' ')}` into `{target_path}` and keep the guidance and promotion indexes synchronized with the result.\n"
        )
    if target_family == "standard":
        return (
            f"# {document_title}\n\n"
            "## Summary\n\n"
            f"{document_summary}\n\n"
            "## Purpose\n\n"
            "Define the rule-bearing obligations for governed promotion of initiative-local authored inputs into durable plan guidance.\n\n"
            "## Scope\n\n"
            "- Applies to pack-wide and project-scoped initiatives that promote implementation slices or decision notes into durable plan-domain standards.\n"
            "- Applies to the promotion runtime, policy registry, guidance index, promotion index, and the promoted standard documents written under `plan/docs/standards/**`.\n"
            "- Does not replace the live initiative package as the execution workspace before promotion approval.\n\n"
            "## Use When\n\n"
            "- Promoting initiative-local authored inputs into durable plan-domain standards.\n"
            "- Reviewing whether a promoted standard remains authoritative after the source initiative package is closed and purged.\n"
            "- Auditing whether the machine-readable promotion policy and index surfaces still match the promoted standard outputs.\n\n"
            "## Related Standards and Sources\n\n"
            "- [standard_md_standard.md](/core/docs/standards/documentation/standard_md_standard.md): promoted standards under `plan/docs/standards/**` must satisfy the governed standard-document contract instead of using a reduced template-only shape.\n"
            "- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md): durable guidance must remain authoritative after initiative packages are eligible for purge.\n"
            "- [promotion/service.py](/plan/python/src/watchtower_plan/promotion/service.py): the promotion runtime must route outputs into governed roots and keep rendered documents aligned with the active validators.\n"
            "- [promotion_policy_registry.json](/plan/.wt/registries/promotion_policy_registry.json): the promotion policy registry defines the sanctioned target family, root, review path, provenance, and mirror behavior.\n\n"
            "## Guidance\n\n"
            "- Require one governed promotion record with source, evidence, approval, and target-path metadata before durable promotion writes occur.\n"
            "- Require promoted standards to land under a governed standards category path instead of directly under the `plan/docs/standards/` root.\n"
            "- Require promoted standards to remain self-contained and validator-compliant so they can outlive the source initiative package cleanly.\n"
            "- Do not promote durable standards directly into `plan/docs/**` without a recorded initiative-local promotion artifact and synchronized machine indexes.\n\n"
            "## Operationalization\n\n"
            f"- `Modes`: `documentation`; `sync`; `validation`\n"
            f"- `Operational Surfaces`: `{target_path}`; `plan/python/src/watchtower_plan/promotion/service.py`; `plan/.wt/registries/promotion_policy_registry.json`; `plan/.wt/indexes/guidance_index.json`; `plan/.wt/indexes/promotion_index.json`\n\n"
            "## Validation\n\n"
            "- Promotion records and promoted standard docs should pass schema-backed validation before closeout.\n"
            "- Promoted standards should rebuild the guidance and promotion indexes cleanly in the same change set.\n"
            "- Reviewers should reject promoted standards that bypass the governed category structure or fail the standard-document contract.\n\n"
            "## Change Control\n\n"
            "- Update this standard when promotion policy, durable target roots, or standard-document requirements change materially.\n"
            "- Update the promotion runtime, promotion policy registry, guidance index, promotion index, and affected promoted docs in the same change set when this contract changes.\n\n"
            "## References\n\n"
            "- [standard_md_standard.md](/core/docs/standards/documentation/standard_md_standard.md)\n"
            "- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md)\n"
            "- [promotion_policy_registry.json](/plan/.wt/registries/promotion_policy_registry.json)\n"
            "- [guidance_index.json](/plan/.wt/indexes/guidance_index.json)\n"
            "- [promotion_index.json](/plan/.wt/indexes/promotion_index.json)\n\n"
            "## Updated At\n\n"
            f"- `{updated_at}`\n"
        )
    if target_family == "foundation":
        return (
            f"# {document_title}\n\n"
            "## Purpose or Context\n\n"
            "This foundation captures the durable boundary for promotion-authority separation. "
            f"{source_summary_line}\n\n"
            "## Scope Boundary\n\n"
            "- In scope: governed extraction of durable guidance out of live initiative state.\n"
            "- Out of scope: treating live initiative folders as long-term guidance roots.\n\n"
            "## Guiding Principles or Rules\n\n"
            "- Durable guidance promotion is policy-governed and traceable.\n"
            "- Mirrored foundations must remain byte-identical across required roots.\n\n"
            "## Implications for Behavior\n\n"
            "- Operators and agents can rely on promoted guidance as a durable surface without treating initiative-local authored inputs as permanent docs.\n\n"
            "## Related Surfaces\n\n"
            f"- `{target_path}`\n"
            "- `plan/python/src/watchtower_plan/promotion/service.py`\n"
            "- `plan/.wt/registries/promotion_policy_registry.json`\n\n"
            "## Notes\n\n"
            "- Promotion and guidance indexes retain the machine-readable provenance for these mirrored foundations.\n\n"
            "## References\n\n"
            "- [foundation_md_standard.md](/core/docs/standards/documentation/foundation_md_standard.md)\n"
            "- [promotion_policy_registry.json](/plan/.wt/registries/promotion_policy_registry.json)\n"
            "- [guidance_index.json](/plan/.wt/indexes/guidance_index.json)\n\n"
            "## Updated At\n\n"
            f"- `{updated_at}`\n"
        )
    raise ValueError(f"Unsupported promotion target family: {target_family}")


def extract_markdown_title(path: Path) -> str | None:
    """Extract the first markdown H1 title from one source document."""

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip() or None
    return None


def extract_markdown_summary(path: Path) -> str | None:
    """Extract the first short summary line from a `## Summary` section when present."""

    lines = path.read_text(encoding="utf-8").splitlines()
    summary_started = False
    collected: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == "## Summary":
            summary_started = True
            continue
        if summary_started and stripped.startswith("#"):
            break
        if summary_started and stripped:
            collected.append(stripped)
    if not collected:
        return None
    return " ".join(collected)


def readable_source_artifact_kind(source_artifact_kind: str) -> str:
    """Return a human-readable label for one source artifact kind."""

    return source_artifact_kind.replace("_", " ")


def guidance_title(
    *,
    initiative_title: str,
    target_family: str,
    source_artifact_kind: str,
    source_title: str | None,
) -> str:
    """Build a durable guidance title for one promoted output."""

    _ = initiative_title
    family_label = target_family.replace("_", " ").title()
    source_label = (
        source_title or readable_source_artifact_kind(source_artifact_kind).title()
    )
    return f"Guidance Promotion {family_label}: {source_label}"


def guidance_summary(
    *,
    initiative_title: str,
    initiative_summary: str,
    target_family: str,
    source_artifact_kind: str,
    source_summary: str | None,
) -> str:
    """Build a one-line summary for one promoted output."""

    _ = initiative_title
    fragment = source_summary or initiative_summary
    compact = re.sub(r"\s+", " ", fragment).strip()
    family_label = target_family.replace("_", " ")
    return f"Durable {family_label} for governed guidance promotion. {compact}"
