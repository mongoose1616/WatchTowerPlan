---
id: "ref.adr_guidance"
title: "ADR Guidance Reference"
summary: "This document provides a working reference for architecture decision records as a durable decision-capture pattern."
type: "reference"
status: "active"
tags:
  - "reference"
  - "adr_guidance"
owner: "repository_maintainer"
updated_at: "2026-03-23T16:50:00Z"
audience: "shared"
authority: "reference"
---

# ADR Guidance Reference
## Summary
This document provides a working reference for architecture decision records as a durable decision-capture pattern.

## Purpose
Provide a focused baseline for recording important architectural or policy decisions without leaving rationale scattered across unrelated docs.

## Scope
- Covers ADRs as a decision-record pattern.
- Does not define this repository's exact ADR format or lifecycle by itself.

## Canonical Upstream
- `https://adr.github.io/` - verified 2026-03-09; Architectural Decision Records (ADRs).

## Related Standards and Sources
- Pack-owned decision-capture standards under `<pack>/docs/standards/governance/`

## Quick Reference or Distilled Reference
### When ADRs Add Value
- Use ADRs for durable architectural or governance choices with real alternatives and downstream consequences.
- Keep one decision per record and keep the current status explicit.
- Push accepted rules back into standards, workflows, or design docs so the ADR does not become hidden policy.

### Minimal ADR Content
| Element | Why It Matters | Notes |
|---|---|---|
| Decision statement | lets readers understand the call quickly | state the outcome in one sentence |
| Alternatives considered | preserves the tradeoff space | record rejected options explicitly enough to preserve why they were not chosen |
| Consequences | shows what changes next | include affected docs, systems, or workflows |
| Status | separates proposal from accepted policy | e.g. proposed, accepted, superseded |

### Common Pitfalls
- Using ADRs for transient meeting notes or issue triage.
- Capturing the rationale but never updating the canonical policy surfaces afterward.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [engineering_design_principles.md](/core/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/core/docs/foundations/repository_standards_posture.md)

### Why It Matters Here
- Use this reference when building ADR templates or decision-capture standards under the owning pack standards root.
- Treat ADRs as supporting decision history, not as the only location of active policy.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- Pack-owned decision-capture standards under `<pack>/docs/standards/governance/`

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-23T16:50:00Z`
