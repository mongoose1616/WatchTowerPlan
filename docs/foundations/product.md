# Product

The product is a two-layer, LLM/agent-driven system. Core provides the shared runtime and governance substrate, while domain packs turn that substrate into guided operator workflows. Neither layer is enough on its own: core without packs is infrastructure, and packs without core are fragile process documents. The intended operating model is that the agent drives routine execution while the human provides oversight, direction, review, and decisions when judgment is needed.

## Core

Core is the reusable product layer. Its job is to provide the services that every domain needs so domain packs do not have to rebuild them differently each time.

- Provide routing, schema enforcement, policy enforcement, compatibility checks, validation, release evidence, and recovery support.
- Give engineering and governance work a reliable home for proofs, readiness checks, contract publication, and runtime safety.
- Make machine state and operational behavior trustworthy enough that domain workflows can depend on them.
- Prioritize machine-usable structures that help LLMs and agents retrieve context, execute workflows, and stay inside governed boundaries.
- Stay domain-agnostic instead of absorbing challenge-specific, reporting-specific, or other pack-local jobs.
- Remain thin in product language and strong in product support.

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

Domain packs are the customer-facing part of the product. They are where operators actually experience guided work with an LLM or agent instead of just the shared governance machinery.

- Make packs the main entry point for real operator jobs.
- Let users start quickly, clarify scope, let the agent execute guided workflows, capture evidence, and finish with reusable closeout artifacts.
- Own domain workflows, templates, knowledge surfaces, tool guidance, and pack-local managed state.
- Feel like guided workbenches rather than passive archives.
- Support future expansion through the same pack model instead of letting the first domain become the accidental default for all later work.
- Treat offensive security as the first pack, with CTF first and pentest next as the initial delivery path.
