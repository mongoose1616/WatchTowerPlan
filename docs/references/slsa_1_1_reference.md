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
updated: "2026-03-09"
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
- `https://slsa.dev/`
- `https://slsa.dev/blog/2025/04/slsa-v1.1`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use SLSA when supply-chain guarantees need a staged model.
- Translate SLSA goals into concrete repository release and evidence requirements.
- Keep the chosen version explicit because SLSA evolves.

## Local Mapping in This Repository
- Use this reference if future release-hardening or provenance standards are added.
- Pair it with Sigstore, in-toto, and CycloneDX when building a fuller supply-chain model.

## Process or Workflow
1. Read this reference before codifying SLSA 1.1 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how supply-chain integrity and provenance planning should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
