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
updated: "2026-03-09"
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
- `https://www.first.org/cvss/v4-0/`
- `https://www.first.org/cvss/specification-document%E3%80%82`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use CVSS when a shared scoring vocabulary helps prioritization and communication.
- Keep vector strings and scoring rationale explicit when scores are recorded.
- Do not use CVSS as a substitute for contextual business or operational judgment.

## Local Mapping in This Repository
- Use this reference if repository outputs later include scored security findings.
- Pair it with methodology and reporting standards rather than applying it in isolation.

## Process or Workflow
1. Read this reference before codifying CVSS v4.0 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how vulnerability severity scoring should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
