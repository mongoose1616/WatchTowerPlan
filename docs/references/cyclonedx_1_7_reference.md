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
updated: "2026-03-09"
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
- `https://cyclonedx.org/`
- `https://cyclonedx.org/specification/overview`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use CycloneDX when machine-readable software inventory matters.
- Keep the chosen specification version explicit.
- Define what scope the SBOM covers instead of assuming the format answers that automatically.

## Local Mapping in This Repository
- Use this reference if release or supply-chain standards later require SBOM artifacts.
- Pair it with SLSA, Sigstore, and in-toto when designing release evidence.

## Process or Workflow
1. Read this reference before codifying CycloneDX 1.7 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how SBOM and inventory artifact design should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
