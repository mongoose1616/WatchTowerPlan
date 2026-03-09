---
id: "ref.owasp_wstg"
title: "OWASP WSTG Reference"
summary: "This document provides a working reference for the OWASP Web Security Testing Guide."
type: "reference"
status: "active"
tags:
  - "reference"
  - "owasp_wstg"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# OWASP WSTG Reference
## Summary
This document provides a working reference for the OWASP Web Security Testing Guide.

## Purpose
Provide a stable web-application testing baseline for security assessment workflows and findings.

## Scope
- Covers the OWASP WSTG as a testing reference.
- Does not replace repository-specific scope, evidence, or report requirements.

## Canonical Upstream
- `https://owasp.org/www-project-web-security-testing-guide/` - verified 2026-03-09; OWASP Web Security Testing Guide.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### WSTG Coverage Areas
| Area | Typical focus |
|---|---|
| information gathering | discover attack surface and context |
| configuration and deployment | insecure defaults and exposed surfaces |
| identity, auth, and session management | account and session weaknesses |
| input validation and error handling | injection and unsafe processing |
| cryptography and business logic | misuse of trust and control flow |
| client-side testing | browser and front-end behaviors |

### Core Rules
- Use WSTG as structured web-testing guidance, not as the repository's exact workflow by default.
- Select the relevant testing areas explicitly for the target system.
- Keep evidence expectations and report structure explicit even when WSTG provides the methodology.

### Common Pitfalls
- Treating WSTG chapter coverage as proof of real risk prioritization.
- Running a broad checklist without scoping which areas matter.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if security-focused domain packs or reporting standards need a web-testing baseline.
- Pair it with CVSS and pentest-reporting standards where findings need severity and evidence structure.

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
