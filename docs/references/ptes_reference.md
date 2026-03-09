---
id: "ref.ptes"
title: "PTES Reference"
summary: "This document provides a working reference for PTES as a penetration-testing lifecycle baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "ptes"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# PTES Reference
## Summary
This document provides a working reference for PTES as a penetration-testing lifecycle baseline.

## Purpose
Provide a lifecycle model for penetration-testing planning, execution, and reporting.

## Scope
- Covers PTES as a methodology reference.
- Does not force the repository into a pentest-only operating model.

## Canonical Upstream
- `https://www.pentest-standard.org/index.php/Main_Page` - canonical PTES home preserved; the official site was unreachable from this environment during the 2026-03-09 refresh.
- `https://www.pentest-standard.org/index.php/PTES_Technical_Guidelines` - canonical PTES technical-guidelines URL preserved; the official site was unreachable from this environment during the 2026-03-09 refresh.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### PTES Phases
| Phase | Main goal |
|---|---|
| pre-engagement interactions | scope, authorization, constraints |
| intelligence gathering | collect context and target information |
| threat modeling | prioritize realistic attack paths |
| vulnerability analysis | identify weaknesses worth validating |
| exploitation | prove impact where authorized |
| post-exploitation | understand depth and consequences |
| reporting | deliver actionable evidence and findings |

### Core Rules
- Use PTES to structure lifecycle coverage, not to replace local safety or authorization rules.
- Keep reporting and evidence expectations explicit.
- Decide up front whether exploitation and post-exploitation are actually in scope.

### Common Pitfalls
- Treating PTES as permission to test beyond the agreed scope.
- Using phase names without defining the concrete deliverables for each one.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if offensive-security planning or domain-pack standards need a pentest lifecycle baseline.
- Pair it with OWASP WSTG, CVSS, and reporting standards when formalizing pentest deliverables.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- The official PTES site was unreachable from this environment during the refresh, so the canonical URLs were preserved with an availability note rather than replaced with a secondary mirror.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.

## Updated At
- `2026-03-09T05:03:16Z`
