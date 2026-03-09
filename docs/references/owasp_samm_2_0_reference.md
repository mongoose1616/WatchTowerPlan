---
id: "ref.owasp_samm_2_0"
title: "OWASP SAMM 2.0 Reference"
summary: "This document provides a working reference for OWASP SAMM 2.0 as a software-security maturity model."
type: "reference"
status: "active"
tags:
  - "reference"
  - "owasp_samm_2_0"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# OWASP SAMM 2.0 Reference
## Summary
This document provides a working reference for OWASP SAMM 2.0 as a software-security maturity model.

## Purpose
Provide a maturity and improvement-model baseline when the repository needs phased security program evolution guidance.

## Scope
- Covers OWASP SAMM 2.0.
- Does not by itself define a repository maturity roadmap.

## Canonical Upstream
- `https://owasp.org/www-project-samm/` - verified 2026-03-09; OWASP SAMM.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### SAMM Structure
| Business function | Focus | Local use |
|---|---|---|
| Governance | strategy and management | ownership, policy, measurement |
| Design | secure architecture and requirements | design-time controls |
| Implementation | build-time practices | coding, dependencies, pipelines |
| Verification | assurance activities | testing, review, evidence |
| Operations | running and maintaining securely | deployment and incident readiness |

### Core Rules
- Use SAMM as a maturity and improvement-planning lens.
- Convert target maturity outcomes into measurable local actions.
- Keep the chosen scope explicit: repo, team, product, or program.

### Common Pitfalls
- Using maturity labels without defining the concrete practices underneath.
- Treating SAMM as a replacement for immediate control decisions.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repository later formalizes phased capability improvement standards.
- Pair it with SSDF or ASVS when maturity needs to connect to specific controls.

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
