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
updated: "2026-03-09"
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
- `https://diataxis.fr/`
- `https://diataxis.fr/foundations/`
- `https://diataxis.fr/quality/`
- `https://diataxis.fr/compass/`
- `https://diataxis.fr/workflow/`

## Related Standards and Sources
- `Diataxis documentation framework`
- [documentation_template.md](/home/j/WatchTowerPlan/docs/templates/documentation_template.md)
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)

This document is a local working reference for applying Diataxis in this repository.

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
- `workflows/**` primarily map to how-to guidance because they define procedural steps for planning tasks and operational flows.
- `docs/standards/**` primarily map to reference because they define structures, rules, naming, contracts, and documentation expectations.
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md), [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md), and [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md) primarily map to explanation because they describe rationale, interpretation, and layered application rather than serving as strict lookup-only artifacts.
- `docs/templates/**` support how-to and tutorial-style authoring depending on whether a template is being used as a scaffold, a teaching aid, or a repeatable documentation starting point.
- `README.md` files should usually act as orientation or navigation docs and should stay concise instead of absorbing full standards, workflows, or deep explanation content.

## Process or Workflow
1. Identify the dominant user intent before drafting: learn, perform, look up, or understand.
2. Choose the target document type and destination path before writing content.
3. Write the document in the shape that best serves that dominant intent.
4. Link to companion documents instead of mixing multiple documentation modes into one file when that would reduce clarity.
5. Re-check the document after drafting and ask whether it still serves one primary need well.

## Examples
- A workflow document such as [prd_generation.md](/home/j/WatchTowerPlan/workflows/modules/prd_generation.md) is primarily a how-to document because it gives ordered steps to complete a planning task.
- A standard such as [docs/standards/documentation/workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md) is primarily a reference document because the reader needs stable structural rules and required sections.
- A repo-level explanation document such as [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md) is primarily an explanation document because it explains the intended shape and meaning of the system rather than giving step-by-step instructions.

## References
- [documentation_template.md](/home/j/WatchTowerPlan/docs/templates/documentation_template.md)
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)

## Tooling and Automation
- No repository-local documentation classifier or validator exists yet.
- If documentation validation tooling is added later, this document should become one of the reference inputs for classification guidance rather than an isolated prose note.

## Notes
- This document is intentionally short and operational.
- When interpretation becomes ambiguous, re-evaluate the document against the Diataxis model rather than extending this local distillation by guesswork.

## Last Synced
- `2026-03-09`
