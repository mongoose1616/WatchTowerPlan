---
id: "ref.rfc_9562_uuid"
title: "RFC 9562 UUID Reference"
summary: "This document provides a working reference for RFC 9562 as the current UUID standard."
type: "reference"
status: "active"
tags:
  - "reference"
  - "rfc_9562_uuid"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# RFC 9562 UUID Reference
## Summary
This document provides a working reference for RFC 9562 as the current UUID standard.

## Purpose
Provide a standard identifier baseline when UUIDs are used in structured records or system contracts.

## Scope
- Covers UUIDs as standardized by RFC 9562.
- Does not require UUIDs as the only identifier strategy in the repository.

## Canonical Upstream
- `https://www.rfc-editor.org/info/rfc9562` - verified 2026-03-09; Information on RFC 9562 » RFC Editor.

## Related Standards and Sources
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)

## Quick Reference or Distilled Reference
### Common UUID Version Choices
| Version | Good default use | Notes |
|---|---|---|
| 4 | random identifiers | simple and widely understood |
| 7 | time-ordered identifiers | often better for sortability and newer systems |
| 5 | name-based deterministic identifiers | use only when stable namespace and name mapping is wanted |
| 1, 6, or 8 | specialized cases | choose intentionally with clear constraints |

### Core Rules
- Use RFC 9562 as the current UUID reference baseline.
- Choose UUID versions intentionally based on randomness, ordering, or determinism needs.
- Document where UUIDs are required and where simpler IDs are enough.

### Common Pitfalls
- Defaulting to an older version by habit without checking the actual need.
- Treating UUID format choice as irrelevant to storage, ordering, or privacy concerns.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)

### Why It Matters Here
- Use this reference when identifier standards are added under `docs/standards/metadata/**` or `docs/standards/data_contracts/**`.
- Pair it with timestamp and serialization references when designing event or artifact records.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
