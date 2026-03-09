---
id: "std.metadata.front_matter"
title: "Front Matter Standard"
summary: "This standard defines when repository documents should use front matter, which keys are canonical, and how parsed front matter is validated as structured metadata."
type: "standard"
status: "active"
tags:
  - "standard"
  - "metadata"
  - "front_matter"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
audience: "shared"
authority: "authoritative"
---

# Front Matter Standard

## Summary
This standard defines when repository documents should use front matter, which keys are canonical, and how parsed front matter is validated as structured metadata.

## Purpose
Keep document metadata predictable enough for indexing, ownership tracking, status signaling, retrieval ranking, and machine validation without turning every Markdown file into a metadata-heavy artifact.

## Scope
- Applies to Markdown documents in `docs/**` and other governed document families that adopt front matter.
- Covers front matter placement, required and optional keys, document-family profiles, and machine-validation boundaries.
- Does not define the full repository-wide naming policy for every metadata value.

## Use When
- Adding front matter to a long-lived repository document.
- Defining metadata expectations for a document family.
- Building validation logic for parsed document metadata.

## Related Standards and Sources
- [front_matter_reference.md](/home/j/WatchTowerPlan/docs/references/front_matter_reference.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/schemas/interfaces/README.md)

## Guidance
- Front matter must appear at the top of the Markdown file and must be delimited by opening and closing `---` lines.
- Front matter is YAML metadata for the document, not a substitute for the document body.
- Use front matter when the metadata materially improves routing, indexing, ownership tracking, or lifecycle visibility.
- Do not add front matter to short directory `README.md` files or other small orientation docs unless the metadata has a clear operational use.
- Keep the key set stable across a document family rather than inventing ad hoc keys per file.
- Prefer simple scalar values. Use lists only when the metadata is naturally multi-valued, such as `tags`.
- Quote single-value text fields for consistency.
- Keep `updated_at` as an RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, such as `2026-03-09T05:06:54Z`.
- Use `updated_at` for mutable document metadata. Do not introduce alternate update-timestamp keys such as `updated`, `last_updated`, or `last_synced`.
- Keep `id` values aligned with the repository naming and IDs standard.
- Keep `status` values aligned with the repository status tracking standard.
- When front matter is validated, validate the parsed metadata object rather than the full Markdown file text.
- Use the published documentation front matter schemas under `core/control_plane/schemas/interfaces/documentation/` for machine validation.
- Unknown keys are not allowed in governed front matter profiles unless the relevant schema profile is updated in the same change set.
- Use retrieval-oriented metadata when it materially improves ranking or disambiguation instead of forcing the retriever to infer everything from prose.
- `authority` should indicate whether a document is the source of truth, a supporting explanation, a reference, or historical context.
- `applies_to` should list the concrete repository surfaces or concepts the document governs or explains.
- `aliases` should capture important alternate phrasings, abbreviations, or synonymous terms that users and agents are likely to search for.
- `docs/references/**` documents that use repository-governed reference structure should include front matter and validate against the reference profile.
- `docs/planning/prds/**` documents should include front matter and validate against the PRD profile.
- `docs/planning/decisions/**` documents should include front matter and validate against the decision-record profile.
- `docs/standards/**` standard documents should include front matter and validate against the standard profile. Short directory `README.md` files under `docs/standards/**` remain plain Markdown unless a narrower local rule says otherwise.
- Workflow documents may adopt front matter when status, ownership, or indexing needs justify it. If they do, they should validate against their matching profile.

## Structure or Data Model
### Canonical keys
| Key | Purpose | Typical Shape | Notes |
|---|---|---|---|
| `id` | Stable machine-usable document identifier | quoted string | Required for governed document families that need stable identity. |
| `trace_id` | Shared traceability identifier | quoted string | Required for planning families that participate in end-to-end traceability. |
| `title` | Stable human-readable document name | quoted string | Usually matches the visible title closely. |
| `summary` | One-line description for listings and indexes | quoted string | Keep it short and specific. |
| `type` | Document family | quoted string | Examples include `reference`, `standard`, and `workflow`. |
| `status` | Lifecycle state | quoted string | Keep the value controlled and stable. |
| `tags` | Search or grouping labels | YAML list | Use reusable labels, not prose. |
| `owner` | Responsible maintainer or role | quoted string | Prefer stable role-like values. |
| `updated_at` | Last meaningful content update | quoted UTC timestamp | Use the repository timestamp baseline `YYYY-MM-DDTHH:MM:SSZ`. |
| `audience` | Intended readership | quoted string | Keep values concise and reusable. |
| `authority` | Retrieval and precedence signal | quoted string | Use controlled values such as `authoritative`, `supporting`, `reference`, or `historical`. |
| `applies_to` | Concrete repository surfaces or governed concepts | YAML list | Prefer real paths or stable concept identifiers over vague prose. |
| `aliases` | Important alternate search terms | YAML list | Use only terms that improve retrieval or disambiguation. |

### Current profile rules
| Document Family | Front Matter Rule | Validation Profile |
|---|---|---|
| `docs/references/**` | Required for governed reference docs | `reference_front_matter.v1.schema.json` |
| `docs/planning/prds/**` | Required | `prd_front_matter.v1.schema.json` |
| `docs/planning/decisions/**` | Required | `decision_record_front_matter.v1.schema.json` |
| `docs/standards/**` | Required for governed standard docs other than short directory `README.md` files | `standard_front_matter.v1.schema.json` |
| `workflows/**` | Optional but approved when metadata is operationally useful | `workflow_front_matter.v1.schema.json` |
| short directory `README.md` files | Not required by default | none |

### Validation boundary
- Parse YAML front matter into a metadata object first.
- Validate that metadata object against the appropriate schema profile.
- Treat the Markdown body and the parsed metadata as related but separate validation surfaces.

### Retrieval guidance
- Prefer `authority` over free-form wording when one document should outrank related supporting material.
- Use `applies_to` to connect a document to real repository paths, modules, schemas, or governed concepts.
- Use `aliases` sparingly to capture search synonyms that would otherwise be easy to miss.
- Do not use these fields as a substitute for a clear title, summary, or path structure.

## Process or Workflow
1. Decide whether the document family benefits from governed metadata.
2. If front matter is needed, choose the matching profile under `core/control_plane/schemas/interfaces/documentation/`.
3. Add only the canonical keys that the selected profile permits.
4. Keep visible title, summary, and metadata values aligned so the document does not present conflicting identity or lifecycle signals.
5. Validate the parsed metadata object before treating the document change as complete.

## Examples
- A long-lived reference under `docs/references/**` should use the reference front matter profile.
- A PRD under `docs/planning/prds/**` should use the PRD front matter profile and carry a shared `trace_id`.
- A decision record under `docs/planning/decisions/**` should use the decision-record front matter profile and carry a shared `trace_id`.
- A standard under `docs/standards/**` should use the standard front matter profile.
- A front matter document can add `aliases` such as `yaml_header` and `document_metadata` when those terms are likely retrieval entrypoints.
- A short `README.md` that only explains directory purpose should usually stay plain Markdown with no front matter.

## Validation
- Front matter should parse cleanly as YAML.
- Documents that claim a governed front matter profile should validate against the matching schema under `core/control_plane/schemas/interfaces/documentation/`.
- Reviewers should reject unexpected keys, conflicting title or type signals, and stale `updated_at` values when the metadata was materially changed.
- Front matter rules and schema profiles should be updated together when the permitted key set changes.

## Change Control
- Update this standard when the repository changes which document families require front matter or which keys are canonical.
- Update the matching schema profiles in the same change set when front matter rules change.
- Update companion references or document-family standards in the same change set when their metadata expectations change.

## References
- [front_matter_reference.md](/home/j/WatchTowerPlan/docs/references/front_matter_reference.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/schemas/interfaces/README.md)

## Notes
- This standard intentionally does not require front matter on every document in `docs/**`.
- The exact allowed values for identifiers, statuses, owners, and audiences can be tightened later by companion metadata standards without changing the basic front matter structure.
- Retrieval-oriented keys should stay small and intentional. If they become broad keyword dumps, they will reduce rather than improve retrieval quality.

## Updated At
- `2026-03-09T05:23:35Z`
