---
id: "ref.diataxis_local"
title: "Diataxis Local Reference"
summary: "This document captures a local distilled reference for Diataxis so documentation in this repository can be written consistently without depending on external browsing during normal authoring work."
type: "reference"
status: "active"
tags:
  - "reference"
  - "diataxis_local"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Diataxis Local Reference

## Summary
This document captures a local distilled reference for Diataxis so documentation in this repository can be written consistently without depending on external browsing during normal authoring work.

## Purpose
Provide an in-repo, offline-friendly reference for Diataxis so planning docs, standards docs, workflow docs, and templates can be authored with clearer document intent and less accidental mode-mixing.

## Scope
- This document covers the four Diataxis documentation modes, the compass model, basic quality signals, and how those ideas map into this repository.
- This document is a local distilled reference, not a replacement for the canonical Diataxis source material.

## Canonical Upstream
- `https://diataxis.fr/` - verified 2026-03-09; Diataxis overview.
- `https://diataxis.fr/foundations/` - verified 2026-03-09; foundations guidance.
- `https://diataxis.fr/quality/` - verified 2026-03-09; documentation quality guidance.
- `https://diataxis.fr/compass/` - verified 2026-03-09; compass model guidance.

## Related Standards and Sources
- [documentation_template.md](/home/j/WatchTowerPlan/docs/templates/documentation_template.md)
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)

## Quick Reference or Distilled Reference
### The Four Documentation Modes

| Mode | Primary User Need | Typical Prompt | Output Shape |
|---|---|---|---|
| Tutorial | Learning through guided practice | "Teach me step-by-step" | Structured lesson with expected milestones |
| How-to Guide | Completing a task | "How do I do X now?" | Procedural sequence for a concrete objective |
| Reference | Looking up facts quickly | "What is the exact syntax, contract, or structure?" | Dense factual lookup with stable terms, tables, and rules |
| Explanation | Building conceptual understanding | "Why does it work this way?" | Narrative rationale, tradeoffs, and decision context |

### Compass Model
- The action axis separates practical action guidance from conceptual understanding.
- The cognition axis separates immediate execution needs from broader study and reasoning needs.
- A document should usually live in one dominant quadrant even when related documents exist in the other modes.
- If a document starts trying to teach, instruct, define syntax, and explain theory all at once, it should usually be split or clearly sectioned.

### Quality Signals
- Each document should primarily serve one user need at a time.
- Clarity is usually more valuable than trying to make one file cover every possible question.
- A good doc states its boundaries honestly and links to companion artifacts instead of pretending to do everything.
- Reference docs should optimize for fast lookup.
- How-to docs should optimize for action.
- Explanation docs should optimize for understanding.
- Tutorial docs should optimize for learning through guided progression.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)

### Why It Matters Here
- `workflows/**` primarily map to how-to guidance because they define procedural steps for planning tasks and operational flows.
- `docs/standards/**` primarily map to reference because they define structures, rules, naming, contracts, and documentation expectations.
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md), [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md), and [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md) primarily map to explanation because they describe rationale, interpretation, and layered application rather than serving as strict lookup-only artifacts.
- `docs/templates/**` support how-to and tutorial-style authoring depending on whether a template is being used as a scaffold, a teaching aid, or a repeatable documentation starting point.
- `README.md` files should usually act as orientation or navigation docs and should stay concise instead of absorbing full standards, workflows, or deep explanation content.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## Tooling and Automation
- No repository-local documentation classifier or validator exists yet.
- If documentation validation tooling is added later, this document should become one of the reference inputs for classification guidance rather than an isolated prose note.

## References
- [documentation_template.md](/home/j/WatchTowerPlan/docs/templates/documentation_template.md)
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)

## Notes
- This document is intentionally short and operational.
- When interpretation becomes ambiguous, re-evaluate the document against the Diataxis model rather than extending this local distillation by guesswork.
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- The prior `https://diataxis.fr/workflow/` link returned `404` during the refresh and was removed from the canonical upstream list.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
