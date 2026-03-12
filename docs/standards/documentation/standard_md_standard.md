---
id: "std.documentation.standard_md"
title: "Standard Document Standard"
summary: "This standard defines the expected document shape for governed standard and best-practice documents stored under `docs/standards/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "standard_md"
owner: "repository_maintainer"
updated_at: "2026-03-12T02:06:54Z"
audience: "shared"
authority: "authoritative"
---

# Standard Document Standard

## Summary
This standard defines the expected document shape for governed standard and best-practice documents stored under `docs/standards/`.

## Purpose
Keep standards structured enough that internal and external authority is not only cited but auditable as concrete local guidance.

## Scope
- Applies to governed standard and best-practice documents stored under `docs/standards/` other than short directory `README.md` files.
- Covers required sections, reference usage, and the difference between cited sources and applied implications.
- Does not replace narrower content rules in individual standard families.

## Use When
- Creating a new governed standard or best-practice document.
- Refreshing an existing standard after its source authorities or local implications change materially.
- Reviewing whether a standard captures the concrete local effect of the authorities it cites.

## Related Standards and Sources
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): governed standards inherit the shared semantic guardrails for repo-local links and list-to-heading spacing.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): governed standards must use the standard front matter profile.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): external authority should be normalized through local reference docs when practical.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): standard docs must remain structured enough for the governed standard index to capture citation and application signals.
- [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md): authoring scaffold that should stay aligned with this standard.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): standard docs must use UTC `updated_at` values consistently.

## Guidance
- Use governed front matter on standards and validate it against the standard front matter profile.
- Keep one primary standard concern per document.
- Use the standard-document template when creating or materially refreshing a governed standard unless a narrower family scaffold is intentionally more specific.
- Use `Related Standards and Sources` for the authorities that materially shape the standard, not for loose “nice to read” links.
- Every bullet in `Related Standards and Sources` should use `source: implication` form so the repo-local consequence of the cited authority is explicit.
- Repo-local Markdown links should resolve to existing repository targets and should fail validation when they drift.
- Leave one blank line between the last item in a bullet or numbered list and the next heading.
- Keep `References` for companion docs, examples, and supporting material that help the reader navigate the repo or verify implementation.
- When an external topic already has a governed local reference under `docs/references/**`, cite that local reference instead of scattering raw external URLs.
- Publish an `Operationalization` section using compact metadata bullets so maintainers can see which modes and repository surfaces actively enforce or embody the standard, using exact repo-relative file paths, repo-relative directory paths ending in `/`, or bounded repo-relative glob patterns when the governed surface is a repeating file family.
- Do not publish semantically duplicate operationalization surfaces. Use one canonical path form for each governed file or directory so the standard index does not carry redundant entries.
- Keep `Updated At` aligned with front matter `updated_at`.

## Operationalization
- `Modes`: `validation`; `sync`; `query`; `documentation`
- `Operational Surfaces`: `docs/standards/*/*_standard.md`; `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`; `core/python/src/watchtower_core/repo_ops/sync/standard_index.py`; `core/python/src/watchtower_core/repo_ops/query/standards.py`; `docs/commands/core_python/watchtower_core_query_standards.md`; `docs/templates/standard_document_template.md`

## Structure or Data Model
### Required sections
| Section | Requirement | Notes |
|---|---|---|
| `Summary` | Required | One short explanation of the standard and what it governs. |
| `Purpose` | Required | Explain why the rule exists. |
| `Scope` | Required | Define where the rule applies and what it does not cover. |
| `Use When` | Required | Explain when maintainers should consult the standard. |
| `Related Standards and Sources` | Required | Use `source: implication` bullets. Bare link lists are insufficient. |
| `Guidance` | Required | Publish the actual normative or best-practice guidance. |
| `Operationalization` | Required | Use metadata bullets for `Modes` and `Operational Surfaces` so operational enforcement is discoverable without code spelunking; directory surfaces should use repo-relative paths ending in `/`. |
| `Validation` | Required | Describe how compliance is checked. |
| `Change Control` | Required | Describe what companion surfaces change with the standard. |
| `References` | Required | Link supporting companion docs, artifacts, or examples. |
| `Updated At` | Required | Record the last meaningful content update as an RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`. |

## Validation
- Standard-doc front matter should validate against `standard_front_matter.v1.schema.json`.
- `Related Standards and Sources` should use explained `source: implication` bullets rather than bare link lists.
- `Operationalization` should include metadata bullets for `Modes` and `Operational Surfaces`, and each operational surface should resolve to a real repository path or be a bounded repo-relative glob pattern that matches one or more live repository surfaces.
- Exact file surfaces should use repo-relative file paths without a trailing slash, and directory surfaces should use repo-relative directory paths ending in `/`.
- Repo-local Markdown links should resolve to existing files or directories under the repository root.
- Headings should not appear immediately after a bullet or numbered list item without a blank separator line.
- `References` should remain present and should not silently absorb the applied-implication role.
- `updated_at` in front matter and the `Updated At` body section should match.

## Change Control
- Update this standard when the repository changes the expected document shape for standards.
- Update the standards template, standard index, and affected live standards in the same change set when this family changes structurally.

## References
- [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md)
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/standards/README.md)

## Updated At
- `2026-03-12T02:06:54Z`
