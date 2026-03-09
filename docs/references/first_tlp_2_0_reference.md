---
id: "ref.first_tlp_2_0"
title: "FIRST TLP 2.0 Reference"
summary: "This document provides a working reference for FIRST TLP 2.0 as an information-sharing sensitivity taxonomy."
type: "reference"
status: "active"
tags:
  - "reference"
  - "first_tlp_2_0"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# FIRST TLP 2.0 Reference
## Summary
This document provides a working reference for FIRST TLP 2.0 as an information-sharing sensitivity taxonomy.

## Purpose
Provide a clear baseline for labeling and handling information with different sharing constraints.

## Scope
- Covers FIRST Traffic Light Protocol 2.0.
- Does not define a complete repository incident or disclosure policy by itself.

## Canonical Upstream
- `https://www.first.org/tlp/` - verified 2026-03-09; Traffic Light Protocol (TLP).

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### TLP Meanings
| Label | Sharing expectation | Typical use |
|---|---|---|
| `TLP:CLEAR` | no sharing restrictions | public guidance |
| `TLP:GREEN` | limited community sharing | peer or community coordination |
| `TLP:AMBER` | restricted sharing on a need-to-know basis | sensitive operational details |
| `TLP:RED` | named recipients only | highly sensitive coordination |

### Core Rules
- Pick a TLP label only when you also know the audience and the intended sharing boundary.
- Pair the label with handling expectations in procedures or reports.
- Review whether a document really needs a restriction before applying one.

### Common Pitfalls
- Using TLP as a vague "sensitive" sticker.
- Assuming all readers interpret the label the same way without local handling rules.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if future incident, evidence-handling, or disclosure standards need a sharing taxonomy.
- Pair it with incident-response and logging guidance when handling sensitive operational information.

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
