---
id: "std.metadata.terminology"
title: "Terminology Standard"
summary: "This standard defines how repository terminology is chosen, stabilized, and used so durable docs and governed artifacts do not drift into competing names for the same concept."
type: "standard"
status: "active"
tags:
  - "standard"
  - "metadata"
  - "terminology"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
audience: "shared"
authority: "authoritative"
---

# Terminology Standard

## Summary
This standard defines how repository terminology is chosen, stabilized, and used so durable docs and governed artifacts do not drift into competing names for the same concept.

## Purpose
Keep retrieval, review, and governance coherent by giving the repository one canonical term set for its recurring concepts and by defining how external or alternate terms should be mapped locally.

## Scope
- Applies to durable documentation, standards, workflows, templates, and governed machine-readable artifacts that introduce or rely on recurring repository terms.
- Covers canonical term choice, synonym handling, and term-boundary rules for the repository's core concepts.
- Does not attempt to control every prose choice or every domain-specific term quoted from external sources.

## Use When
- Introducing a new repeated term in standards, workflows, templates, or control-plane artifacts.
- Reviewing whether multiple docs are using competing terms for the same concept.
- Mapping external terminology into repository-native language.

## Related Standards and Sources
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)

## Guidance
- Prefer one canonical repository term for each recurring concept.
- Keep canonical terms stable across standards, workflows, templates, and machine-readable artifacts.
- When an external source uses a different term, preserve the source term in the reference where needed but map it explicitly to the local canonical term.
- Do not create near-duplicate local terms for the same concept when one existing term already fits.
- Use front matter `aliases` or explicit local-mapping sections for retrieval-relevant alternate terms rather than scattering many synonyms through normal prose.
- Do not reintroduce predecessor-repo language or vague generic labels when a current repository term already exists.

## Structure or Data Model
| Canonical Term | Meaning in This Repository | Notes |
|---|---|---|
| `control plane` | The canonical, versioned, machine-readable authority under `core/control_plane/` | Not mutable runtime state. |
| `workflow module` | A task-execution document under `workflows/modules/**` | Loaded through routing rather than used as a broad narrative doc. |
| `routing table` | The canonical workflow-selection surface at `workflows/ROUTING_TABLE.md` | Handles classification, not execution steps. |
| `standard` | A normative repository rule under `docs/standards/**` | Higher authority than references or templates. |
| `reference` | A supporting lookup document, usually grounded in external source material | Not the same as local policy. |
| `template` | An authoring scaffold for a recurring document shape | Convenience surface, not authority. |
| `index` | A derived lookup artifact that improves retrieval or navigation | Not a source of truth. |
| `registry` | A governed authoritative catalog with stable identifiers | Use when the catalog itself is owned authority. |
| `contract` | An explicit acceptance or compatibility boundary | Used for intake or compatibility expectations. |
| `policy` | A machine-readable guardrail or rule set | Distinct from explanatory standards prose. |
| `README` | A directory-orientation document | Quick reference, not a standards or workflow document. |
| `foundation document` | A durable product, philosophy, standards-context, technology, or narrative document under `docs/foundations/` | Shapes later planning and standards work. |
| `domain pack` | An external operator-facing pack that uses the shared core substrate | Not content owned inside the core control plane. |
| `updated_at` | The last meaningful content update timestamp for a durable document or artifact | Use RFC 3339 UTC in the form `YYYY-MM-DDTHH:MM:SSZ`. |
| `recorded_at` | The timestamp for when an evidence or event-style record was captured | Use RFC 3339 UTC in the form `YYYY-MM-DDTHH:MM:SSZ`. |
| `generated_at` | A distinct generation or build timestamp for a derived artifact | Use only when it differs materially from `updated_at` or `recorded_at`. |

## Validation
- Durable docs and governed artifacts should not use competing terms as if they were equal canonical names.
- New recurring terms should be checked against the existing canonical term set before being introduced broadly.
- Reference docs that keep upstream terminology should still explain the local repository mapping when the difference matters.
- Retrieval metadata should capture important alternate phrasings instead of letting document bodies drift into uncontrolled synonym sprawl.

## Change Control
- Update this standard when the repository adopts a new recurring concept or redefines an existing canonical term.
- Update companion standards, templates, workflows, and retrieval metadata in the same change set when a canonical term changes materially.
- Prefer explicit migration from an old term to a new one rather than leaving both in active use indefinitely.

## References
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)

## Notes
- Canonical terms exist to reduce ambiguity, not to force unnatural prose.
- When a term is unstable or contested, resolve it in a standard or decision artifact before letting it spread through many documents.

## Updated At
- `2026-03-09T05:23:35Z`
