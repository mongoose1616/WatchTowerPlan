---
id: "ref.mitre_attack"
title: "MITRE ATT&CK Reference"
summary: "This document provides a working reference for MITRE ATT&CK as a tactic-and-technique taxonomy for offensive-security knowledge."
type: "reference"
status: "active"
tags:
  - "reference"
  - "mitre_attack"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# MITRE ATT&CK Reference

## Summary
This document provides a working reference for MITRE ATT&CK as a tactic-and-technique taxonomy for offensive-security knowledge.

## Purpose
Provide a shared vocabulary for structuring offensive-security techniques, mappings, and reusable knowledge.

## Scope
- Covers MITRE ATT&CK as a knowledge and classification framework.
- Does not replace repository-specific workflows or reporting requirements.

## Canonical Upstream
- `https://attack.mitre.org/`
- `https://attack.mitre.org/resources/versions/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use ATT&CK as a shared taxonomy, not as a substitute for task-specific procedures.
- Keep mappings explicit rather than implied.
- Version-lock the ATT&CK release when reproducibility matters.

## Local Mapping in This Repository
- Use this reference if domain packs or future security knowledge surfaces need tactic mapping.
- Pair it with domain-specific workflows or tagging standards rather than using it as free-form decoration.

## Process or Workflow
1. Read this reference before codifying MITRE ATT&CK Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how offensive-security taxonomy and tagging should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
