---
id: "ref.owasp_genai_security_project"
title: "OWASP GenAI Security Project Reference"
summary: "This document provides a working reference for the OWASP GenAI Security Project."
type: "reference"
status: "active"
tags:
  - "reference"
  - "owasp_genai_security_project"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# OWASP GenAI Security Project Reference

## Summary
This document provides a working reference for the OWASP GenAI Security Project.

## Purpose
Provide an external security baseline for AI- and LLM-related system risks, controls, and design review.

## Scope
- Covers the OWASP GenAI Security Project as a reference source.
- Does not by itself define the repository's AI governance policy.

## Canonical Upstream
- `https://genai.owasp.org/home/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use it as a risk and control reference for GenAI-specific concerns.
- Translate the guidance into repository-specific safety, oversight, and misuse controls.
- Do not assume generic AI security guidance automatically fits this repository without interpretation.

## Local Mapping in This Repository
- Use this reference if the repository later formalizes AI governance or bounded-agency standards.
- Pair it with NIST AI RMF and AI 600-1 when building governance-oriented policy.

## Process or Workflow
1. Read this reference before codifying OWASP GenAI Security Project Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how GenAI and agent security governance should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
