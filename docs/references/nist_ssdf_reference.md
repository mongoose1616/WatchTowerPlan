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
updated: "2026-03-09"
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
- `https://csrc.nist.gov/publications/detail/sp/800-218/final`
- `https://doi.org/10.6028/NIST.SP.800-218`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use SSDF as a secure-development organizing framework.
- Translate it into explicit repository practices such as validation, review, hardening, and release evidence rules.
- Keep the local control mapping concrete instead of claiming broad alignment without specifics.

## Local Mapping in This Repository
- Use this reference when shaping engineering and release-readiness standards.
- Pair it with supply-chain references when hardening release processes.

## Process or Workflow
1. Read this reference before codifying NIST SSDF Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how secure development and release hardening should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
