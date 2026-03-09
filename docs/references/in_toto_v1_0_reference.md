---
id: "ref.in_toto_v1_0"
title: "in-toto v1.0 Reference"
summary: "This document provides a working reference for in-toto v1.0 as an attestation and supply-chain metadata framework."
type: "reference"
status: "active"
tags:
  - "reference"
  - "in_toto_v1_0"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# in-toto v1.0 Reference
## Summary
This document provides a working reference for in-toto v1.0 as an attestation and supply-chain metadata framework.

## Purpose
Provide an attestation framework baseline when the repository needs verifiable build-step provenance.

## Scope
- Covers in-toto v1.0.
- Does not define the repository's complete attestation model by itself.

## Canonical Upstream
- `https://in-toto.io/` - verified 2026-03-09; in-toto.
- `https://in-toto.io/docs/specs/` - verified 2026-03-09; Specifications.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What in-toto Gives You
- Use in-toto when you need verifiable statements about who performed which supply-chain step and what inputs and outputs were involved.
- Keep step boundaries, functionary identity, and expected materials and products explicit.
- Pair attestation design with signing and provenance strategy rather than adopting it in isolation.

### Core Concepts
| Concept | Why it matters | Notes |
|---|---|---|
| layout or policy | defines the expected supply-chain steps | establishes the trust model |
| link or attestation | records what a step did | should be signed by the functionary |
| materials and products | tie inputs to outputs | needed for traceability and tamper evidence |

### Common Pitfalls
- Recording attestations without a clear policy about which steps are trusted.
- Treating attestation presence as equivalent to safe release policy.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repository later adopts attestation-based release evidence.
- Pair it with SLSA and Sigstore rather than treating it as an isolated control.

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
