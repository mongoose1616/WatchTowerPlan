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
updated_at: "2026-03-11T01:34:31Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/"
  - "core/control_plane/"
  - "workflows/modules/"
aliases:
  - "product"
  - "product shape"
  - "product direction"
---

# Product Direction

This document defines the intended future WatchTower product shape. For current repository ownership and current implementation scope, [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md) is authoritative. Read this document when the question is where the broader product is meant to go, not when the question is what `WatchTowerPlan` owns today.

## Audience

- Primary audience: Product owners and engineering leads defining the future product shape, boundary, and first-wave delivery model.
- Secondary audience: Designers and maintainers who need the governing future-product frame behind workflows, packs, and implementation planning.
- Not written for: Contributors looking only for current repository ownership.

## Current Repository Relationship

- `WatchTowerPlan` currently owns the governed core substrate, planning system, workflow-routing model, and machine-readable control plane.
- This repository does not yet own the first operator-facing domain-pack implementation.
- The future product model in this document is still relevant because it constrains how the shared core should evolve now.

## Core

Core is the shared system layer of the future product. Its job is to provide the services that every domain needs so domain packs do not have to rebuild them differently each time.

- Provide routing, schema enforcement, policy enforcement, compatibility checks, validation, release evidence, and recovery support.
- Give engineering and governance work a reliable home for proofs, readiness checks, contract publication, and runtime safety.
- Make machine state and operational behavior trustworthy enough that domain workflows can depend on them.
- Prioritize machine-usable structures that help LLMs and agents retrieve context, execute workflows, and stay inside governed boundaries.
- Stay domain-agnostic instead of absorbing challenge-specific, reporting-specific, or other pack-local jobs.
- Do not absorb domain templates, domain terminology, or pack-specific artifact conventions unless they are truly cross-domain.
- Remain mostly behind the scenes for operators: strong in product support, thin in direct user-facing workflow language.

## Full Product Shape

The future product promise is not just "automation." It is a local-first environment that helps a user start work quickly, collaborate with an LLM or agent, capture evidence along the way, and close out with reusable outputs. Where practical, important artifacts should exist in both a human-readable form and a machine-usable form so the human can review clearly and the system can operate deterministically.

- Combine planning, execution, knowledge management, validation, and closeout in one coherent system.
- Reduce startup friction while keeping guided execution and clear review points.
- Preserve readable outputs while keeping canonical machine truth in governed surfaces.
- Maintain paired human-readable and machine-usable forms of important artifacts wherever practical.
- Support bounded automation with explicit stop conditions and human oversight.
- Keep product changes traceable through PRDs, proposals, tasks, acceptance criteria, and validation artifacts.
- Treat reusable knowledge, templates, workflow modules, and references as product value, not side effects.

## Domain Packs

Domain packs are the future domain-specific operator layer of the product. They are specialized for a domain so the operator experience feels seamless and domain-native instead of generic.

- Make packs the main entry point for real operator jobs.
- Use core to help a human achieve a real domain goal efficiently, repeatably, and with clean closeout.
- Let users start quickly, clarify scope, let the agent execute guided workflows, capture evidence, and finish with reusable closeout artifacts.
- Own domain workflows, templates, terminology, references, knowledge surfaces, tool guidance, domain artifact expectations, and pack-local managed state.
- Shape how the LLM or agent assists the human in that domain instead of forcing the user to translate generic system capabilities into domain process by hand.
- Use shared core contracts instead of reimplementing routing, validation, policy, traceability, or recovery differently for each domain.
- Support future expansion through the same pack model instead of letting the first domain become the accidental default for all later work.
- Treat offensive security as the first pack, with CTF first and pentest next as the initial delivery path.

## Product Delivery Boundary

- Future domain-pack implementation belongs in a later product phase and likely in a consuming repository such as `/home/j/WatchTower`.
- This repository should prepare the reusable substrate and contracts that product work will consume.
- Product direction should guide current planning, but it should not be mistaken for current repo ownership.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md)

## Updated At
- `2026-03-11T01:34:31Z`
