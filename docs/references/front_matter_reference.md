---
id: "ref.front_matter"
title: "Front Matter Reference"
summary: "Working reference for when and how to use front matter in repository documents."
type: "reference"
status: "active"
tags:
  - "reference"
  - "front_matter"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
applies_to:
  - "docs/standards/metadata/front_matter_standard.md"
  - "core/control_plane/schemas/interfaces/documentation"
aliases:
  - "yaml_header"
  - "document_metadata"
---

# Front Matter Reference

## Summary
This document provides a working reference for front matter so repository documents use metadata consistently when metadata is needed.

## Purpose
Provide a practical guide for deciding when to use front matter, which fields are useful, and how to keep metadata predictable across docs.

## Scope
- Covers when front matter is useful, common metadata fields, and basic authoring expectations.
- Does not by itself create a mandatory repository-wide metadata schema.

## Canonical Upstream
- `https://spec.yaml.io/main/spec/1.2.2/`
- `https://jekyllrb.com/docs/front-matter/`
- `https://gohugo.io/content-management/front-matter/`

## Related Standards and Sources
- [documentation_template.md](/home/j/WatchTowerPlan/docs/templates/documentation_template.md)
- [yaml_1_2_2_reference.md](/home/j/WatchTowerPlan/docs/references/yaml_1_2_2_reference.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)

## Quick Reference or Distilled Reference
### Use Front Matter When
- The document needs stable metadata for routing, status tracking, ownership, indexing, or filtering.
- The document is part of a repeated document family such as references, standards, workflows, or other governed docs.
- The same metadata fields need to be applied consistently across a set of related files.

### Do Not Use Front Matter When
- The document is a tiny one-off note, scratch doc, or short directory README with no meaningful metadata needs.
- The metadata would duplicate the visible content without improving routing or maintenance.
- The keys are speculative, temporary, or likely to vary from one file to the next without a stable meaning.

### Common Fields
| Field | Use For | Typical Shape | Notes |
|---|---|---|---|
| `title` | Stable human-readable document name | quoted string | Usually matches the visible title closely. |
| `summary` | One-line description for indexes or listings | quoted string | Keep it short and specific. |
| `type` | Broad document class | quoted string | Examples: `reference`, `standard`, `workflow`, `guide`. |
| `status` | Lifecycle state | quoted string | Examples: `active`, `draft`, `deprecated`. |
| `tags` | Search or grouping labels | YAML list | Keep tags controlled and reusable. |
| `owner` | Responsible maintainer or role | quoted string | Prefer stable role-like values over personal notes. |
| `updated` | Last meaningful content update | quoted string date | Use ISO-style dates for consistency. |
| `audience` | Intended readership | quoted string | Examples: `shared`, `maintainers`, `contributors`. |
| `authority` | Retrieval precedence signal | quoted string | Examples: `authoritative`, `supporting`, `reference`, `historical`. |
| `applies_to` | Concrete repository surfaces or concepts | YAML list | Prefer real paths or stable concept identifiers. |
| `aliases` | Alternate search terms | YAML list | Keep this short and intentional. |

### Authoring Rules
- Keep keys stable across similar document types instead of inventing near-duplicates.
- Prefer simple scalar values unless the field is naturally multi-valued, such as `tags`.
- Quote single-value text fields for consistency.
- Keep dates in a consistent ISO-style format such as `2026-03-08`.
- Treat front matter as support metadata; the document body is still the primary reader-facing content.

### Minimal Example

```yaml
---
title: "Document Title"
summary: "One-sentence description."
type: "reference"
status: "active"
tags:
  - "docs"
owner: "repository_maintainer"
updated: "2026-03-08"
audience: "shared"
authority: "reference"
applies_to:
  - "docs/references/**"
aliases:
  - "yaml_header"
---
```

### Common Pitfalls
- Adding front matter because it feels formal rather than because the metadata is actually useful.
- Creating ad hoc keys when an existing key already expresses the intent.
- Letting tags drift into free-form prose instead of controlled labels.
- Treating front matter as a substitute for a clear title, summary, or body structure.

## Local Mapping in This Repository
- Use front matter mainly on longer-lived references, standards, workflows, and other documents where indexing, ownership, or status need to be explicit.
- Small orientation docs such as many `README.md` files can usually stay plain Markdown unless metadata becomes operationally useful.
- Repository-front-matter policy now lives in [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md), while this reference remains the supporting working reference.

## Examples
- A long-lived reference doc under `docs/references/**` is a good candidate for front matter because summary, status, audience, and tags help indexing and maintenance.
- A short directory README that only explains folder purpose usually does not need front matter.
- A workflow or standard doc may justify front matter when status, owner, or audience materially affect how the file is used.

## References
- [documentation_template.md](/home/j/WatchTowerPlan/docs/templates/documentation_template.md)

## Notes
- This document is a working reference, not a mandatory metadata policy by itself.
- Front matter is a convention rather than one single universal standard, so this reference uses the YAML specification plus widely adopted documentation-system implementations as its upstream basis.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md) is now the authority for repository front matter policy.

## Last Synced
- `2026-03-09`
