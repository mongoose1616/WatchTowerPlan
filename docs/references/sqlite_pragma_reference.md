---
id: "ref.sqlite_pragma"
title: "SQLite PRAGMA Reference"
summary: "This document provides a working reference for SQLite PRAGMA settings and behavior."
type: "reference"
status: "active"
tags:
  - "reference"
  - "sqlite_pragma"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# SQLite PRAGMA Reference
## Summary
This document provides a working reference for SQLite PRAGMA settings and behavior.

## Purpose
Provide a baseline for understanding and documenting SQLite configuration switches that affect storage behavior.

## Scope
- Covers SQLite PRAGMA documentation as a configuration reference.
- Does not prescribe a local PRAGMA profile by itself.

## Canonical Upstream
- `https://www.sqlite.org/pragma.html` - verified 2026-03-09; Pragma statements supported by SQLite.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### High-Impact PRAGMAs
| PRAGMA area | Why it matters | Common concern |
|---|---|---|
| journal or WAL mode | durability and concurrency behavior | affects file layout and recovery |
| synchronous | write safety versus performance | should be deliberate |
| foreign_keys | relational integrity enforcement | often needs explicit enabling |
| busy timeout or locking | contention behavior | affects operational correctness |

### Core Rules
- Treat PRAGMAs as deliberate configuration, not hidden defaults.
- Distinguish persistent database settings from connection-scoped settings.
- Document performance, integrity, and recovery tradeoffs for any high-impact PRAGMA.

### Common Pitfalls
- Assuming a PRAGMA change persists when it is actually connection-scoped.
- Tuning performance PRAGMAs without explaining the safety tradeoff.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if future SQLite adoption requires documented configuration choices.
- Pair it with WAL and backup references when defining operational storage behavior.

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
