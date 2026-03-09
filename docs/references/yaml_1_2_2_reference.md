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
updated_at: "2026-03-09T05:03:16Z"
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
- `https://yaml.org/spec/1.2.2/` - verified 2026-03-09; YAML Ain’t Markup Language (YAML™) revision 1.2.2.

## Related Standards and Sources
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)

## Quick Reference or Distilled Reference
### Practical YAML Rules
| Concern | Preferred approach | Why |
|---|---|---|
| explicit keys and simple scalars | yes | easier cross-parser behavior |
| tabs for indentation | no | indentation should stay space-based |
| advanced YAML features | use sparingly | portability and readability suffer quickly |
| local subset definition | explicit when needed | many parsers behave differently at the edges |

### Core Rules
- Keep YAML usage simple and predictable when interoperability matters.
- Prefer a well-documented local subset over full-YAML assumptions.
- Treat YAML parsing behavior as a contract issue when metadata or configuration is governed.

### Common Pitfalls
- Depending on parser-specific implicit typing or edge behavior.
- Using complex YAML features where JSON-like structure would be clearer.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)

### Why It Matters Here
- Use this reference for any future YAML metadata standards under `docs/standards/metadata/**`.
- Use it when documenting front matter or configuration parsing behavior.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
