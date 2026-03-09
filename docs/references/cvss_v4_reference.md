---
id: "ref.cvss_v4"
title: "CVSS v4.0 Reference"
summary: "This document provides a working reference for CVSS v4.0 as a vulnerability-severity scoring baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "cvss_v4"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# CVSS v4.0 Reference
## Summary
This document provides a working reference for CVSS v4.0 as a vulnerability-severity scoring baseline.

## Purpose
Provide a standardized scoring baseline when findings or vulnerabilities need normalized severity.

## Scope
- Covers CVSS v4.0.
- Does not require every finding to be scoreable if the repository defines valid exceptions.

## Canonical Upstream
- `https://www.first.org/cvss/v4.0/` - verified 2026-03-09; FIRST CVSS v4.0 landing page.
- `https://www.first.org/cvss/v4.0/specification-document` - verified 2026-03-09; CVSS v4.0 specification document.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What CVSS Answers
- Use CVSS to normalize technical severity across findings when a shared scoring vocabulary helps prioritization.
- Record the vector string with the score so the reasoning is reviewable.
- Keep business impact and local exploit context separate from the base score.

### Common Score Components
| Component family | What it captures | Why it matters |
|---|---|---|
| base | intrinsic technical severity | gives the shared baseline |
| threat / environmental | context that changes by deployment or threat landscape | explains why local priority may differ |
| supplemental | extra context | useful for communication but not a substitute for rationale |

### Common Pitfalls
- Comparing raw scores without the underlying vector or local context.
- Treating CVSS as the whole prioritization model rather than one input.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if repository outputs later include scored security findings.
- Pair it with methodology and reporting standards rather than applying it in isolation.

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
