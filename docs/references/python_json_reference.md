---
id: "ref.python_json"
title: "Python json Library Reference"
summary: "This document provides a working reference for Python's standard `json` library documentation."
type: "reference"
status: "active"
tags:
  - "reference"
  - "python_json"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Python json Library Reference
## Summary
This document provides a working reference for Python's standard `json` library documentation.

## Purpose
Provide a baseline for JSON handling in repository Python code when the standard library is sufficient.

## Scope
- Covers Python's built-in `json` module.
- Does not replace broader JSON standards or canonicalization rules.

## Canonical Upstream
- `https://docs.python.org/3/library/json.html` - verified 2026-03-09; json.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Common Stdlib Operations
| Function | Use For | Notes |
|---|---|---|
| `load` / `loads` | parse JSON text into Python objects | use text or bytes input deliberately |
| `dump` / `dumps` | serialize Python objects to JSON | choose formatting and ordering explicitly |
| encoder hooks | custom serialization | use only when the contract really needs it |

### Core Rules
- Use the stdlib when simple JSON parsing or emission is enough.
- Treat formatting choices such as indentation, separators, and key sorting as deliberate artifact decisions.
- Remember that Python defaults can be more permissive than strict interoperability expectations.

### Common Pitfalls
- Assuming stdlib output is canonical or reproducible without explicit settings.
- Forgetting that non-standard numeric values or custom types need policy, not just code.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference for future Python automation that reads or writes repository JSON artifacts.
- Pair it with JSON, schema, and canonicalization references when building durable machine-readable outputs.

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
