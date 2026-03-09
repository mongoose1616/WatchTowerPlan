---
id: "ref.ndjson_spec"
title: "NDJSON Reference"
summary: "This document provides a working reference for NDJSON as a practical newline-delimited JSON stream format."
type: "reference"
status: "active"
tags:
  - "reference"
  - "ndjson_spec"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# NDJSON Reference
## Summary
This document provides a working reference for NDJSON as a practical newline-delimited JSON stream format.

## Purpose
Provide a simple operational stream format baseline for append-only records, logs, indexes, or task state streams.

## Scope
- Covers NDJSON as a newline-delimited JSON convention.
- Does not define every repository stream schema or event model.

## Canonical Upstream
- `https://github.com/ndjson/ndjson-spec` - verified 2026-03-09; GitHub.

## Related Standards and Sources
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)

## Quick Reference or Distilled Reference
### Container Rules
- Write one complete JSON text per line and use newline separation.
- Keep UTF-8 encoding and line-oriented processing explicit.
- Treat NDJSON as a streaming container format, not as the schema for the records themselves.

### Common Decisions
| Question | Preferred answer | Why |
|---|---|---|
| one record or many per line | one per line | preserves stream and append behavior |
| empty lines | decide explicitly whether to allow or ignore them | consumers differ |
| schema enforcement | separate layer | NDJSON does not define record semantics |

### Common Pitfalls
- Mixing pretty-printed multi-line JSON with NDJSON.
- Assuming the line format by itself defines event meaning or validation.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)

### Why It Matters Here
- Use this reference for any future operational streams or task/event logs in the repository.
- Pair it with schema and timestamp standards when designing durable event records.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
