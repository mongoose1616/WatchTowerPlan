---
id: "std.documentation.foundation_md"
title: "Foundation Document Standard"
summary: "This standard defines the minimum governed shape for foundation documents stored under `docs/foundations/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "foundation_md"
owner: "repository_maintainer"
updated_at: "2026-03-12T23:43:00Z"
audience: "shared"
authority: "authoritative"
---

# Foundation Document Standard

## Summary
This standard defines the minimum governed shape for foundation documents stored under `docs/foundations/`.

## Purpose
Keep the repository's product, philosophy, standards-posture, and technology-direction documents structured enough that they can be indexed, queried, and audited as first-class intent surfaces.

## Scope
- Applies to governed foundation documents stored under `docs/foundations/` other than the short directory `README.md`.
- Covers front matter, minimum body requirements, and the role of foundation documents as intent-setting authority.
- Does not force one narrative template across all foundation documents.

## Use When
- Creating a new governed foundation document.
- Refreshing an existing foundation document after product, philosophy, standards, or technology-direction intent changes materially.
- Reviewing whether the foundation layer is structured enough to remain queryable and auditable.

## Related Standards and Sources
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): foundation docs must publish governed metadata so the intent layer is indexable and traceable.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): external authority that materially shapes foundations should be normalized through local reference docs when practical.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): foundation docs must use UTC `updated_at` values consistently.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): foundation documents are the intent layer that should stay auditable instead of only implicit.

## Guidance
- Store governed foundation documents under `docs/foundations/`.
- Use governed front matter on foundation documents and validate it against the published foundation front matter profile.
- Keep front-matter `audience` accurate so intent-layer retrieval can route human and agent readers effectively.
- Keep each foundation document centered on one primary intent surface, such as product shape, design philosophy, standards posture, or technology direction.
- Keep foundation docs durable and repo-native. They should explain current repository intent, not historical lineage.
- When external guidance materially shapes a foundation doc, prefer citing a governed local reference under `docs/references/**` instead of only raw external URLs.
- Publish a `References` section so internal and external source use remains explicit.
- Publish an `Updated At` section and keep it aligned with front matter `updated_at`.
- Operationalization for this standard should publish only governed foundation
  documents, not the family `README.md`, so standards lookup stays aligned with
  the documented scope boundary.
- Foundation documents may remain narrative and do not need a rigid shared body-heading set beyond the minimum governed sections.

## Structure or Data Model
### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Foundation document | `docs/foundations/<topic>.md` | Use stable snake_case filenames derived from the governed topic. |
| Foundation directory README | `docs/foundations/README.md` | Directory orientation and inventory only. |

### Minimum governed requirements
| Surface | Requirement | Notes |
|---|---|---|
| Front matter | Required | Use the foundation front matter profile. |
| Visible H1 title | Required | Must align with front matter `title`. |
| `References` | Required | Record internal companion docs and any material external authority. |
| `Updated At` | Required | Record the last meaningful content update as an RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`. |

## Operationalization
- `Modes`: `documentation`; `sync`; `query`
- `Operational Surfaces`: `docs/foundations/customer_story.md`; `docs/foundations/engineering_design_principles.md`; `docs/foundations/engineering_stack_direction.md`; `docs/foundations/product_direction.md`; `docs/foundations/repository_scope.md`; `docs/foundations/repository_standards_posture.md`; `docs/templates/foundation_document_template.md`; `core/python/src/watchtower_core/repo_ops/sync/foundation_index.py`; `core/python/src/watchtower_core/repo_ops/query/foundations.py`

## Validation
- Foundation-doc front matter should validate against `foundation_front_matter.v1.schema.json`.
- Foundation docs should publish `References` and `Updated At`.
- `updated_at` in front matter and the `Updated At` body section should match.
- Standards lookup should resolve this standard for the governed foundation
  documents but not for `docs/foundations/README.md`, which is governed by the
  README standard instead.
- Reviewers should reject foundation docs that materially govern the repo but remain structurally invisible to indexes and retrieval.

## Change Control
- Update this standard when the repository changes how foundation documents are governed or indexed.
- Update the operationalization list in this standard when the governed
  foundation-document corpus gains, renames, or removes a foundation doc so
  standards lookup stays fail-closed on family-boundary drift.
- Update the foundation front matter schema, templates, and foundation index surfaces in the same change set when this document family changes structurally.

## References
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)

## Updated At
- `2026-03-12T23:43:00Z`
