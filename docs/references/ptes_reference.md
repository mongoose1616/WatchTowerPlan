---
id: "ref.ptes"
title: "PTES Reference"
summary: "This document provides a working reference for PTES as a penetration-testing lifecycle baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "ptes"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# PTES Reference

## Summary
This document provides a working reference for PTES as a penetration-testing lifecycle baseline.

## Purpose
Provide a lifecycle model for penetration-testing planning, execution, and reporting.

## Scope
- Covers PTES as a methodology reference.
- Does not force the repository into a pentest-only operating model.

## Canonical Upstream
- `https://www.pentest-standard.org/index.php/Main_Page`
- `https://www.pentest-standard.org/index.php/PTES_Technical_Guidelines`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use PTES to frame phases and coverage expectations.
- Translate methodology guidance into concrete workflow and reporting rules instead of citing PTES abstractly.
- Do not let methodology references override repository-specific safety or governance constraints.

## Local Mapping in This Repository
- Use this reference if offensive-security planning or domain-pack standards need a pentest lifecycle baseline.
- Pair it with OWASP WSTG, CVSS, and reporting standards when formalizing pentest deliverables.

## Process or Workflow
1. Read this reference before codifying PTES Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how pentest lifecycle design should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
