---
id: "ref.nist_ssdf"
title: "NIST SSDF Reference"
summary: "This document provides a working reference for NIST SP 800-218, the Secure Software Development Framework (SSDF)."
type: "reference"
status: "active"
tags:
  - "reference"
  - "nist_ssdf"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# NIST SSDF Reference
## Summary
This document provides a working reference for NIST SP 800-218, the Secure Software Development Framework (SSDF).

## Purpose
Provide a software-development and release-hardening baseline when repository standards need a recognized secure-development model.

## Scope
- Covers NIST SP 800-218 SSDF v1.1.
- Does not by itself define all repository engineering rules.

## Canonical Upstream
- `https://csrc.nist.gov/pubs/sp/800/218/final` - verified 2026-03-09; SP 800-218, Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities.
- `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf` - verified 2026-03-09; official publication PDF.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### SSDF Practice Groups
| Group | Focus | Local translation |
|---|---|---|
| PO | prepare the organization | policy, roles, training, tooling readiness |
| PS | protect the software | integrity, access, environments, dependencies |
| PW | produce well-secured software | secure design, implementation, validation |
| RV | respond to vulnerabilities | intake, triage, remediation, disclosure |

### Core Rules
- Use SSDF as a secure-development organizing model, not a substitute for local controls.
- Map practices to explicit repository behaviors such as review, validation, hardening, and release evidence.
- Keep the local control mapping concrete and auditable.

### Common Pitfalls
- Claiming SSDF alignment without naming which practices are actually implemented.
- Treating the framework as complete execution guidance.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference when shaping engineering and release-readiness standards.
- Pair it with supply-chain references when hardening release processes.

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
