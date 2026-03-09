---
id: "ref.nist_sp_800_61_rev_3"
title: "NIST SP 800-61 Rev. 3 Reference"
summary: "This document provides a working reference for NIST SP 800-61 Rev. 3 as an incident-response baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "nist_sp_800_61_rev_3"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# NIST SP 800-61 Rev. 3 Reference
## Summary
This document provides a working reference for NIST SP 800-61 Rev. 3 as an incident-response baseline.

## Purpose
Provide a recognized baseline for incident response planning, handling, recovery, and communication.

## Scope
- Covers NIST SP 800-61 Rev. 3.
- Does not define the repository's full incident-response runbook by itself.

## Canonical Upstream
- `https://csrc.nist.gov/pubs/sp/800/61/r3/final` - verified 2026-03-09; SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile.
- `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf` - verified 2026-03-09; official publication PDF.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Incident Lifecycle
| Phase | Focus | Notes |
|---|---|---|
| preparation | readiness before incidents | roles, tooling, evidence handling, communications |
| detection and analysis | confirm and understand the event | triage, scope, severity, evidence |
| containment, eradication, and recovery | stop impact and restore operations | often iterative rather than strictly linear |
| post-incident activity | learn and improve | updates to controls, playbooks, and tracking |

### Core Rules
- Use the lifecycle to shape local incident-response expectations.
- Define evidence handling, ownership, and escalation paths explicitly.
- Keep response recommendations grounded in the repository's actual operational context.

### Common Pitfalls
- Treating the lifecycle as rigidly sequential.
- Leaving lessons learned outside the controlled remediation surfaces.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repository later formalizes incident or operational recovery standards.
- Pair it with FIRST TLP and logging guidance when incident evidence and sharing rules matter.

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
