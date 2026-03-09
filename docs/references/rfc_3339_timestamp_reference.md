---
id: "ref.rfc_3339_timestamp"
title: "RFC 3339 Timestamp Reference"
summary: "This document provides a working reference for RFC 3339 as a timestamp format baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "rfc_3339_timestamp"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:06:54Z"
audience: "shared"
authority: "reference"
---

# RFC 3339 Timestamp Reference
## Summary
This document provides a working reference for RFC 3339 as a timestamp format baseline.

## Purpose
Provide a stable timestamp format baseline for logs, records, manifests, and structured metadata.

## Scope
- Covers RFC 3339 timestamps.
- Does not define repository-specific timezone or precision policy beyond the baseline format, though repository standards may adopt a narrower subset.

## Canonical Upstream
- `https://www.rfc-editor.org/rfc/rfc3339` - verified 2026-03-09; RFC 3339: Date and Time on the Internet: Timestamps.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Core Format Rules
| Part | Meaning | Notes |
|---|---|---|
| full date and time | `YYYY-MM-DDThh:mm:ss` | `T` separator is the standard textual form |
| offset | `Z` or numeric UTC offset | do not leave timezone implicit |
| fractional seconds | optional | define precision locally if it matters |

### Core Rules
- Use RFC 3339 when a portable textual timestamp is needed.
- Make UTC-versus-offset expectations explicit at the repository boundary.
- Keep timestamp format policy separate from semantic meaning such as creation time, event time, or expiry.

### Common Pitfalls
- Treating naive local times as if they were RFC 3339 timestamps.
- Leaving precision or timezone interpretation to guesswork.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference when timestamp rules appear in metadata or data-contract standards.
- Repository standards narrow ordinary governed timestamps to UTC with a trailing `Z` and whole-second precision.
- Pair it with identifier and serialization references when designing structured records.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.
- The current repository timestamp baseline is defined in [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md).

## Updated At
- `2026-03-09T05:06:54Z`
