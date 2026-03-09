---
id: "ref.nist_sp_800_115"
title: "NIST SP 800-115 Reference"
summary: "This document provides a working reference for NIST SP 800-115 as a testing and assessment methodology baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "nist_sp_800_115"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# NIST SP 800-115 Reference
## Summary
This document provides a working reference for NIST SP 800-115 as a testing and assessment methodology baseline.

## Purpose
Provide a durable planning and assessment baseline for testing programs, especially security assessments.

## Scope
- Covers NIST SP 800-115.
- Does not replace repository-specific workflow or report requirements.

## Canonical Upstream
- `https://csrc.nist.gov/pubs/sp/800/115/final` - verified 2026-03-09; SP 800-115, Technical Guide to Information Security Testing and Assessment.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Testing Lifecycle
| Phase | Main question | Output |
|---|---|---|
| planning | what are we testing and under what rules | scope, rules of engagement, constraints |
| discovery | what exists and how is it exposed | asset and exposure understanding |
| attack or validation | what weaknesses are real and exploitable | validated findings and impact evidence |
| reporting | what matters and what happens next | usable remediation and evidence record |

### Core Rules
- Use SP 800-115 as a methodology skeleton for testing and assessment work.
- Translate the phases into concrete procedures, evidence rules, and reports.
- Keep authorization and scope constraints explicit before testing begins.

### Common Pitfalls
- Quoting the guide as if it were the actual test plan.
- Treating exploitation as required for every assessment.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if security-focused domain packs or validation standards need a formal testing-assessment baseline.
- Pair it with PTES or WSTG when more domain-specific detail is needed.

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
