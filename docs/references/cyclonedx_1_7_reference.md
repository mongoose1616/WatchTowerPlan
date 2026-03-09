---
id: "ref.cyclonedx_1_7"
title: "CycloneDX 1.7 Reference"
summary: "This document provides a working reference for CycloneDX 1.7 as an SBOM and supply-chain inventory standard."
type: "reference"
status: "active"
tags:
  - "reference"
  - "cyclonedx_1_7"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# CycloneDX 1.7 Reference
## Summary
This document provides a working reference for CycloneDX 1.7 as an SBOM and supply-chain inventory standard.

## Purpose
Provide a standard bill-of-materials baseline when the repository needs machine-readable inventory or vulnerability-exchange artifacts.

## Scope
- Covers CycloneDX 1.7.
- Does not require SBOM generation unless the repository adopts it.

## Canonical Upstream
- `https://cyclonedx.org/` - verified 2026-03-09; CycloneDX Bill of Materials Standard.
- `https://cyclonedx.org/specification/overview/` - verified 2026-03-09; Specification Overview.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### When CycloneDX Is Useful
- Use CycloneDX for machine-readable software inventory, dependency, or supply-chain exchange artifacts.
- Keep the CycloneDX version explicit in generated artifacts.
- Define artifact scope clearly: repository, package, image, build, or release.

### Common Scoping Decisions
| Question | Decide explicitly | Why |
|---|---|---|
| artifact boundary | what the SBOM covers | the format does not choose this for you |
| component granularity | top-level only or full dependency graph | affects noise and reuse |
| evidence linkage | whether you also need vulnerabilities, attestations, or licenses | may require companion artifacts |

### Common Pitfalls
- Generating an SBOM without saying what build or release it represents.
- Assuming the format alone answers provenance or policy questions.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if release or supply-chain standards later require SBOM artifacts.
- Pair it with SLSA, Sigstore, and in-toto when designing release evidence.

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
