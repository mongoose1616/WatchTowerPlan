---
id: "ref.first_tlp_2_0"
title: "FIRST TLP 2.0 Reference"
summary: "This document provides a working reference for FIRST TLP 2.0 as an information-sharing sensitivity taxonomy."
type: "reference"
status: "active"
tags:
  - "reference"
  - "first_tlp_2_0"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# FIRST TLP 2.0 Reference

## Summary
This document provides a working reference for FIRST TLP 2.0 as an information-sharing sensitivity taxonomy.

## Purpose
Provide a clear baseline for labeling and handling information with different sharing constraints.

## Scope
- Covers FIRST Traffic Light Protocol 2.0.
- Does not define a complete repository incident or disclosure policy by itself.

## Canonical Upstream
- `https://www.first.org/tlp/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use TLP labels when sharing constraints need to be made explicit.
- Keep operational handling rules aligned with the chosen TLP level.
- Do not apply TLP labels casually without defining who the intended audience actually is.

## Local Mapping in This Repository
- Use this reference if future incident, evidence-handling, or disclosure standards need a sharing taxonomy.
- Pair it with incident-response and logging guidance when handling sensitive operational information.

## Process or Workflow
1. Read this reference before codifying FIRST TLP 2.0 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how information-sharing labels and handling rules should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
