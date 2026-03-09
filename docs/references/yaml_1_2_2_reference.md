---
id: "ref.yaml_1_2_2"
title: "YAML 1.2.2 Reference"
summary: "This document provides a working reference for YAML 1.2.2 when repository metadata or configuration relies on YAML."
type: "reference"
status: "active"
tags:
  - "reference"
  - "yaml_1_2_2"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# YAML 1.2.2 Reference

## Summary
This document provides a working reference for YAML 1.2.2 when repository metadata or configuration relies on YAML.

## Purpose
Provide a format baseline for YAML-backed metadata or configuration so parsers and writers stay consistent.

## Scope
- Covers YAML 1.2.2 as a source format.
- Does not define the repository's allowed YAML subset by itself.

## Canonical Upstream
- `https://yaml.org/spec/1.2.2/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Keep YAML usage simple and predictable when interoperability matters.
- Document any local subset restrictions explicitly.
- Prefer explicit keys and straightforward scalar values over clever YAML features.

## Local Mapping in This Repository
- Use this reference for any future YAML metadata standards under `docs/standards/metadata/**`.
- Use it when documenting front matter or configuration parsing behavior.

## Process or Workflow
1. Read this reference before codifying YAML 1.2.2 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how YAML metadata and configuration rules should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
