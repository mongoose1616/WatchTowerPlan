---
id: "ref.mitre_attack"
title: "MITRE ATT&CK Reference"
summary: "This document provides a working reference for MITRE ATT&CK as a tactic-and-technique taxonomy for offensive-security knowledge."
type: "reference"
status: "active"
tags:
  - "reference"
  - "mitre_attack"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# MITRE ATT&CK Reference
## Summary
This document provides a working reference for MITRE ATT&CK as a tactic-and-technique taxonomy for offensive-security knowledge.

## Purpose
Provide a shared vocabulary for structuring offensive-security techniques, mappings, and reusable knowledge.

## Scope
- Covers MITRE ATT&CK as a knowledge and classification framework.
- Does not replace repository-specific workflows or reporting requirements.

## Canonical Upstream
- `https://attack.mitre.org/` - verified 2026-03-09; MITRE ATT&CK®.
- `https://attack.mitre.org/resources/versions/` - verified 2026-03-09; Version History.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What ATT&CK Is Good For
- Use ATT&CK as a shared taxonomy for adversary behavior, detection mapping, and control coverage.
- Pin the ATT&CK version when reproducibility or stable IDs matter.
- Keep the local purpose explicit: planning, mapping, reporting, or gap analysis.

### Core ATT&CK Terms
| Term | Meaning | Notes |
|---|---|---|
| tactic | attacker goal or objective | higher-level behavior category |
| technique | how the goal is achieved | stable IDs matter here |
| sub-technique | narrower technique variant | useful for precise mapping |
| mitigation / detection | defensive context | not the same as workflow procedure |

### Common Pitfalls
- Treating ATT&CK as a complete testing methodology or incident workflow.
- Citing tactics or techniques without IDs or version context.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if domain packs or future security knowledge surfaces need tactic mapping.
- Pair it with domain-specific workflows or tagging standards rather than using it as free-form decoration.

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
