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
updated: "2026-03-09"
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
- `https://in-toto.io/`
- `https://in-toto.io/docs/specs/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use in-toto when the order, actor, and integrity of build or release steps need verifiable expression.
- Keep attestation scope explicit.
- Pair attestation design with release, signing, and evidence rules rather than isolating it.

## Local Mapping in This Repository
- Use this reference if the repository later adopts attestation-based release evidence.
- Pair it with SLSA and Sigstore rather than treating it as an isolated control.

## Process or Workflow
1. Read this reference before codifying in-toto v1.0 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how supply-chain attestations and provenance metadata should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
