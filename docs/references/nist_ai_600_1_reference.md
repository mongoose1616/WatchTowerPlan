---
id: "ref.nist_ai_600_1"
title: "NIST AI 600-1 Reference"
summary: "This document provides a working reference for NIST AI 600-1, the Generative AI Profile for the AI RMF."
type: "reference"
status: "active"
tags:
  - "reference"
  - "nist_ai_600_1"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# NIST AI 600-1 Reference

## Summary
This document provides a working reference for NIST AI 600-1, the Generative AI Profile for the AI RMF.

## Purpose
Provide a GenAI-specific governance overlay when AI policy needs more specific controls than the base AI RMF alone.

## Scope
- Covers NIST AI 600-1.
- Does not by itself define repository-local AI guardrails or workflows.

## Canonical Upstream
- `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence`
- `https://doi.org/10.6028/NIST.AI.600-1`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use AI 600-1 when GenAI-specific risk patterns need more concrete treatment than a general AI framework provides.
- Treat it as a profile layered on the AI RMF, not a replacement for core governance.
- Translate profile guidance into repository-specific controls and review criteria.

## Local Mapping in This Repository
- Use this reference if the repository later formalizes GenAI-specific governance or misuse controls.
- Pair it with AI RMF and OWASP GenAI guidance when building policy.

## Process or Workflow
1. Read this reference before codifying NIST AI 600-1 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how GenAI-specific governance design should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
