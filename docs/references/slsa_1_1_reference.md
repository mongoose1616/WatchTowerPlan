---
id: "ref.slsa_1_1"
title: "SLSA 1.1 Reference"
summary: "This document provides a working reference for SLSA 1.1 as a supply-chain security baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "slsa_1_1"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# SLSA 1.1 Reference
## Summary
This document provides a working reference for SLSA 1.1 as a supply-chain security baseline.

## Purpose
Provide a provenance and build-integrity framework when repository release or artifact controls need a supply-chain baseline.

## Scope
- Covers SLSA 1.1 as selected in the MVP material.
- Does not by itself define the repository's full provenance or attestation process.

## Canonical Upstream
- `https://slsa.dev/spec/` - verified 2026-03-09; SLSA specification entrypoint.
- `https://slsa.dev/blog/2025/04/slsa-v1.1` - verified 2026-03-09; SLSA v1.1 approval announcement and release context.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What SLSA Organizes
| Question | Why it matters |
|---|---|
| who built the artifact | establishes trust and accountability |
| from what source | ties artifacts back to versioned inputs |
| under what build controls | shows tamper-resistance and isolation expectations |
| what provenance is available | supports downstream verification |

### Core Rules
- Use SLSA as a staged supply-chain assurance model, not as a vague marketing label.
- Pick the target requirements explicitly and version-lock the SLSA baseline you mean.
- Translate that target into concrete repository release, build, and evidence controls.

### Common Pitfalls
- Claiming a SLSA level or alignment without naming the implemented controls.
- Treating provenance generation as sufficient without downstream verification.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if future release-hardening or provenance standards are added.
- Pair it with Sigstore, in-toto, and CycloneDX when building a fuller supply-chain model.

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
