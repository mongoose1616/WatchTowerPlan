---
id: "foundation.product_direction"
title: "Product Direction"
summary: "Defines the intended future WatchTower product shape and how that future direction relates to the current repository boundary."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "product"
owner: "repository_maintainer"
updated_at: "2026-03-28T23:55:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/"
  - "core/python/src/watchtower_host/"
  - "core/python/src/watchtower_core/pack_integration/"
  - "first_internal_pack_python"
  - "core/workflows/modules/"
  - "pack_owned_workflows"
  - "live_pack_workspace"
aliases:
  - "product"
  - "product shape"
  - "product direction"
---

# Product Direction

This document defines the intended future WatchTower product shape. For current repository ownership and current implementation scope, [repository_scope.md](repository_scope.md) is authoritative. Read this document when the question is where the broader product is meant to go, not when the question is what the current core-authoring repository owns today.

## Audience

- Primary audience: Product owners and engineering leads defining the future product shape, boundary, and first-wave delivery model.
- Secondary audience: Designers and maintainers who need the governing future-product frame behind workflows, packs, and implementation sequencing.
- Not written for: Contributors looking only for current repository ownership.

## Current Repository Relationship

- The current core-authoring repository owns the governed core substrate, host-composition layer, machine-readable control plane, workflow-routing model, and the currently hosted first-party pack set.
- This repository does not yet own the first operator-facing domain-pack implementation.
- The hosted-pack model is already partially proven here through the current internal pack, hosted-pack scaffolding, and second-pack portability work; future product work should extend that contract rather than re-invent it.
- One supported downstream adoption mode is to copy the canonical shared `core/` tree from this repository and then carry whichever hosted packs the consuming repository actually needs. That may begin with `core/` alone during integration bring-up or with `core/` plus one or more hosted packs.
- The future product model in this document is still relevant because it constrains how the shared core should evolve now.

## Core

Core is the shared system layer of the future product. Its job is to provide the services that every domain needs so domain packs do not have to rebuild them differently each time.

- Provide routing, schema enforcement, standards and contract enforcement, compatibility checks, validation, release evidence, and recovery support.
- Give engineering and governance work a reliable home for proofs, readiness checks, contract publication, and runtime safety.
- Make machine state and operational behavior trustworthy enough that domain workflows can depend on them.
- Prioritize machine-usable structures that help LLMs and agents retrieve context, execute workflows, and stay inside governed boundaries.
- Stay reusable and donor-neutral instead of absorbing challenge-specific, reporting-specific, or other pack-local jobs.
- May host cross-pack external references when those references support shared functions or multiple hosted packs.
- Do not absorb pack-applied guidance, domain templates, domain terminology, or pack-specific artifact conventions unless they are truly cross-domain.
- Remain mostly behind the scenes for operators: strong in product support, thin in direct user-facing workflow language.

## Full Product Shape

The future product promise is not just "automation." It is a local-first environment that helps a user start work quickly, collaborate with an LLM or agent, capture evidence along the way, and close out with reusable outputs. Where practical, important artifacts should exist in both a human-readable form and a machine-usable form so the human can review clearly and the system can operate deterministically.

- Combine planning, execution, knowledge management, validation, and closeout in one coherent system.
- Reduce startup friction while keeping guided execution and clear review points.
- Preserve readable outputs while keeping canonical machine truth in governed surfaces.
- Maintain paired human-readable and machine-usable forms of important artifacts wherever practical.
- Support bounded automation with explicit stop conditions and human oversight.
- Keep product changes traceable through initiative briefs, proposals, tasks, acceptance criteria, and validation artifacts.
- Treat reusable knowledge, templates, workflow modules, and references as product value, not side effects.

## Domain Packs

Domain packs are the future domain-specific operator layer of the product. They are specialized for a domain so the operator experience feels seamless and domain-native instead of generic. In this repository the model is no longer purely theoretical: the current internal pack is the first consumer, hosted-pack portability has been exercised with a second-pack proof, and future external packs should extend that same contract.

- Make packs the main entry point for real operator jobs.
- Use core to help a human achieve a real domain goal efficiently, repeatably, and with clean closeout.
- Let users start quickly, clarify scope, let the agent execute guided workflows, capture evidence, and finish with reusable closeout artifacts.
- Own domain workflows, templates, terminology, references, knowledge surfaces, tool guidance, domain artifact expectations, and pack-local managed state.
- Packs may intentionally duplicate a topic already represented in `core/docs/references/**` when the pack-specific operator mapping, touchpoints, or enforcement posture differ materially from the shared-core reference.
- Shape how the LLM or agent assists the human in that domain instead of forcing the user to translate generic system capabilities into domain process by hand.
- Use shared core contracts instead of reimplementing routing, validation, rule enforcement, traceability, or recovery differently for each domain.
- Support future expansion through the same pack model instead of letting the first domain become the accidental default for all later work.
- Treat the current internal pack as the first internal consumer, treat the second-pack proof as evidence that the contract can travel, and require later external packs to follow the same load, validation, and governance model without importing mismatched domain vocabulary into core.

## Product Delivery Boundary

- Future external operator-facing domain-pack implementation belongs in a later product phase and in a consuming product repository, even though the host-pack contract is already proven here.
- That consuming repository may adopt the shared runtime by copying `core/` and then wiring the hosted pack set it actually owns; shared core must therefore stay donor-neutral even when this repository currently carries one internal proof pack.
- Customer-safe bootstrap for that consuming repository should be a curated export of shared core plus the selected hosted pack set, not a raw donor repository snapshot.
- This repository should prepare the reusable substrate and contracts that product work will consume.
- Product direction should guide current planning, but it should not be mistaken for current repo ownership.
- If a downstream working repository edits `core/**` while implementing that reusable substrate, the authored shared-core change must be reconciled back into the canonical shared-core source before closeout.

## References
- [repository_scope.md](repository_scope.md)
- [engineering_design_principles.md](engineering_design_principles.md)
- [repository_standards_posture.md](repository_standards_posture.md)
- [customer_story.md](customer_story.md)

## Updated At
- `2026-03-28T23:55:00Z`
