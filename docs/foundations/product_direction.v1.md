---
id: "foundation.product_direction_v1"
title: "Product Direction v1"
summary: "Comparison draft that reframes the product foundation as a product-direction document for planning and scope decisions."
type: "foundation"
status: "draft"
tags:
  - "foundation"
  - "product"
  - "comparison_draft"
owner: "repository_maintainer"
updated_at: "2026-03-10T00:04:20Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/"
  - "core/control_plane/"
  - "workflows/modules/"
aliases:
  - "product shape"
  - "product audience draft"
---

# Product Direction v1

The product is a two-layer, LLM/agent-driven system. Core is the shared system layer that makes governed execution possible across domains. Domain packs are the domain-specific product layer that use core to turn that shared system into guided operator workflows. Neither layer is enough on its own: core without packs is infrastructure, and packs without core are fragile process documents. The intended operating model is that the agent drives routine execution while the human provides oversight, direction, review, and decisions when judgment is needed.

This comparison draft keeps the original product model but makes the expected reader clearer so the document can function more cleanly as a product-direction surface instead of trying to serve every audience equally.

## Audience
- Primary audience: Product owners and engineering leads defining the product shape, boundary, and first-wave delivery model.
- Secondary audience: Designers and maintainers who need the governing product frame behind workflows, packs, and implementation planning.
- Not written for: End customers looking for narrative value framing rather than product structure.

## Core

Core is the shared system layer. Its job is to provide the services that every domain needs so domain packs do not have to rebuild them differently each time.

- Provide routing, schema enforcement, policy enforcement, compatibility checks, validation, release evidence, and recovery support.
- Give engineering and governance work a reliable home for proofs, readiness checks, contract publication, and runtime safety.
- Make machine state and operational behavior trustworthy enough that domain workflows can depend on them.
- Prioritize machine-usable structures that help LLMs and agents retrieve context, execute workflows, and stay inside governed boundaries.
- Stay domain-agnostic instead of absorbing challenge-specific, reporting-specific, or other pack-local jobs.
- Do not absorb domain templates, domain terminology, or pack-specific artifact conventions unless they are truly cross-domain.
- Remain mostly behind the scenes for operators: strong in product support, thin in direct user-facing workflow language.

## Full Product Shape

The product promise is not just "automation." It is a local-first environment that helps a user start work quickly, collaborate with an LLM or agent, capture evidence along the way, and close out with reusable outputs. Where practical, important artifacts should exist in both a human-readable form and a machine-usable form so the human can review clearly and the system can operate deterministically.

- Combine planning, execution, knowledge management, validation, and closeout in one coherent system.
- Reduce startup friction while keeping guided execution and clear review points.
- Preserve readable outputs while keeping canonical machine truth in governed surfaces.
- Maintain paired human-readable and machine-usable forms of important artifacts wherever practical.
- Support bounded automation with explicit stop conditions and human oversight.
- Keep product changes traceable through PRDs, proposals, tasks, acceptance criteria, and validation artifacts.
- Treat reusable knowledge, templates, workflow modules, and references as product value, not side effects.

## Domain Packs

Domain packs are the domain-specific operator layer of the product. They are specialized for a domain so the operator experience feels seamless and domain-native instead of generic. They are where operators actually experience guided work with an LLM or agent instead of just the shared governance machinery.

- Make packs the main entry point for real operator jobs.
- Use core to help a human achieve a real domain goal efficiently, repeatably, and with clean closeout.
- Let users start quickly, clarify scope, let the agent execute guided workflows, capture evidence, and finish with reusable closeout artifacts.
- Own domain workflows, templates, terminology, references, knowledge surfaces, tool guidance, domain artifact expectations, and pack-local managed state.
- Shape how the LLM or agent assists the human in that domain instead of forcing the user to translate generic system capabilities into domain process by hand.
- Feel like guided workbenches rather than passive archives or thin generic wrappers over shared system capability.
- Use shared core contracts instead of reimplementing routing, validation, policy, traceability, or recovery differently for each domain.
- Support future expansion through the same pack model instead of letting the first domain become the accidental default for all later work.
- Treat offensive security as the first pack, with CTF first and pentest next as the initial delivery path.

## References
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md)
- [product_narrative_brochure.md](/home/j/WatchTowerPlan/docs/foundations/product_narrative_brochure.md)

## Updated At
- `2026-03-10T00:04:20Z`
