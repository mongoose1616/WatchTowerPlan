---
id: "ref.owasp_wstg"
title: "OWASP WSTG Reference"
summary: "This document provides a working reference for the OWASP Web Security Testing Guide."
type: "reference"
status: "active"
tags:
  - "reference"
  - "owasp_wstg"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# OWASP WSTG Reference

## Summary
This document provides a working reference for the OWASP Web Security Testing Guide.

## Purpose
Provide a stable web-application testing baseline for security assessment workflows and findings.

## Scope
- Covers the OWASP WSTG as a testing reference.
- Does not replace repository-specific scope, evidence, or report requirements.

## Canonical Upstream
- `https://owasp.org/www-project-web-security-testing-guide/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use WSTG as structured web-testing guidance rather than as a direct repository workflow.
- Translate relevant tests into scoped checklists or procedures.
- Keep report structure and evidence rules explicit even when WSTG is the methodology baseline.

## Local Mapping in This Repository
- Use this reference if security-focused domain packs or reporting standards need a web-testing baseline.
- Pair it with CVSS and pentest-reporting standards where findings need severity and evidence structure.

## Process or Workflow
1. Read this reference before codifying OWASP WSTG Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how web security testing methodology should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
