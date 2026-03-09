---
id: "ref.sqlite_fts5"
title: "SQLite FTS5 Reference"
summary: "This document provides a working reference for SQLite FTS5 full-text search."
type: "reference"
status: "active"
tags:
  - "reference"
  - "sqlite_fts5"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# SQLite FTS5 Reference
## Summary
This document provides a working reference for SQLite FTS5 full-text search.

## Purpose
Provide a search-indexing baseline if the repository later needs local full-text retrieval over SQLite data.

## Scope
- Covers SQLite FTS5.
- Does not imply that full-text search is required in the repository.

## Canonical Upstream
- `https://www.sqlite.org/fts5.html` - verified 2026-03-09; SQLite FTS5 Extension.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### FTS5 Building Blocks
| Item | Role | Notes |
|---|---|---|
| virtual table | stores searchable index data | central FTS5 abstraction |
| tokenizer | splits text into searchable terms | affects search behavior and language handling |
| `MATCH` queries | full-text search expression | different from ordinary `LIKE` |
| content strategy | inline, external-content, or contentless | storage and sync tradeoffs matter |

### Core Rules
- Use FTS5 only when SQLite-backed full-text search is a real requirement.
- Choose tokenizer and content strategy deliberately.
- Keep ranking and query semantics explicit in the local contract.

### Common Pitfalls
- Treating FTS5 as a drop-in replacement for ordinary indexed lookup.
- Ignoring index-maintenance cost or tokenizer behavior.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference only if the repo adopts SQLite-backed retrieval or indexing.
- Pair it with schema and storage standards when documenting search behavior.

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
