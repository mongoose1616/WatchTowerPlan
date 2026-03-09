---
id: "ref.rfc_7464_json_text_sequences"
title: "RFC 7464 JSON Text Sequences Reference"
summary: "This document provides a working reference for RFC 7464 as the standard for JSON text sequences."
type: "reference"
status: "active"
tags:
  - "reference"
  - "rfc_7464_json_text_sequences"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# RFC 7464 JSON Text Sequences Reference
## Summary
This document provides a working reference for RFC 7464 as the standard for JSON text sequences.

## Purpose
Provide a baseline when newline-delimited or stream-oriented JSON needs a formal sequence model.

## Scope
- Covers RFC 7464 JSON text sequences.
- Does not replace NDJSON guidance where the repository prefers that simpler convention.

## Canonical Upstream
- `https://www.rfc-editor.org/info/rfc7464` - verified 2026-03-09; Information on RFC 7464 » RFC Editor.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Sequence Format
| Element | Role | Notes |
|---|---|---|
| record separator (`RS`, `0x1E`) | marks the start of each JSON text | key difference from NDJSON |
| JSON text | the actual payload | can be parsed as normal JSON |
| line feed (`LF`) | terminator after each text | helps stream framing |

### Core Rules
- Use RFC 7464 when framed JSON streaming matters more than newline-only conventions.
- Prefer it over ad hoc delimiters when consumers need an explicit standard.
- Keep producer and consumer agreement explicit because many tools assume NDJSON instead.

### Common Pitfalls
- Confusing JSON text sequences with NDJSON.
- Assuming plain line-based readers will understand `RS` framing.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if future event streams or append-only logs need a formal streamed-JSON standard.
- Compare it against NDJSON before choosing a stream format standard.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.

## Updated At
- `2026-03-09T05:03:16Z`
