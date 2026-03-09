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
updated_at: "2026-03-09T23:02:08Z"
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
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): governed standards must use the standard front matter profile.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): external authority should be normalized through local reference docs when practical.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): standard docs must remain structured enough for the governed standard index to capture citation and application signals.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): standard docs must use UTC `updated_at` values consistently.

## Guidance
- Use governed front matter on standards and validate it against the standard front matter profile.
- Keep one primary standard concern per document.
- Use `Related Standards and Sources` for the authorities that materially shape the standard, not for loose “nice to read” links.
- Every bullet in `Related Standards and Sources` should use `source: implication` form so the repo-local consequence of the cited authority is explicit.
- Keep `References` for companion docs, examples, and supporting material that help the reader navigate the repo or verify implementation.
- When an external topic already has a governed local reference under `docs/references/**`, cite that local reference instead of scattering raw external URLs.
- Keep `Updated At` aligned with front matter `updated_at`.

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
| `Validation` | Required | Describe how compliance is checked. |
| `Change Control` | Required | Describe what companion surfaces change with the standard. |
| `References` | Required | Link supporting companion docs, artifacts, or examples. |
| `Updated At` | Required | Record the last meaningful content update as an RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`. |

## Validation
- Standard-doc front matter should validate against `standard_front_matter.v1.schema.json`.
- `Related Standards and Sources` should use explained `source: implication` bullets rather than bare link lists.
- `References` should remain present and should not silently absorb the applied-implication role.
- `updated_at` in front matter and the `Updated At` body section should match.

## Change Control
- Update this standard when the repository changes the expected document shape for standards.
- Update the standards template, standard index, and affected live standards in the same change set when this family changes structurally.

## References
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/standards/README.md)

## Updated At
- `2026-03-09T23:02:08Z`
