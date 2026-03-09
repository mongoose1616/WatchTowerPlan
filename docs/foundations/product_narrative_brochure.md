---
id: "foundation.product_narrative_brochure"
title: "Product Narrative Brochure"
summary: "Provides a customer-facing narrative summary of the product story, value, and intended operator experience."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "product_narrative"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/foundations/"
  - "docs/planning/"
aliases:
  - "product narrative"
  - "product brochure"
---

# Product Narrative Brochure

## Purpose and Audience

This document provides a customer-facing narrative summary of the product for operators, buyers, reviewers, and implementation stakeholders. It consolidates the product story, value, and intended experience in one place for presentation and alignment use.

This document summarizes the governed product model. It does not override authoritative policy, architecture, standards, workflow, or data-contract surfaces.

## Executive Narrative

WatchTower is a local-first, deterministic operating environment for LLM- and agent-driven work. It combines a stable shared core with domain packs that turn the core into guided operator workflows. The product is designed for people who need fast execution without giving up governance, evidence quality, or repeatability.

Instead of relying on scattered notes, ad hoc scripts, and operator memory, WatchTower turns work into governed workflows with explicit routing, machine-validated artifacts, and evidence-linked outcomes. The agent handles the routine structured execution. Python helpers and harnesses improve agent efficiency, validation, and orchestration. The human remains responsible for goals, oversight, review, blocker resolution, and final decisions.

The result is lower context loss, better handoffs, clearer execution, and stronger closeout quality across planning, execution, and delivery.

## What Customers Get

1. Clarify-first routing that reduces ambiguous execution.
2. Deterministic workflow behavior with explicit boundaries and stop conditions.
3. Trace-linked evidence for material actions and decisions.
4. Reusable domain knowledge that improves over time.
5. Closeout artifacts that are easier to review, reuse, and defend.

## Customer Experience Promise

1. Customers experience WatchTower primarily as a domain-specific assistant and knowledge manager.
2. That experience is delivered through LLM- and agent-driven workflows, not through routine manual control of hidden system state.
3. Python code and other implementation surfaces exist mainly as helper and harness layers that improve agent efficiency, validation, retrieval, and control.
4. Human-facing interactions center on domain workflows, domain artifacts, and domain knowledge retrieval.
5. Humans stay in the loop as reviewers, idea generators, blocker resolvers, and decision makers when judgment is needed.
6. Wherever practical, important artifacts exist in both a human-readable form and a machine-usable form.

## Core Platform Value

Core platform outcomes:

1. Policy-safe execution guardrails.
2. Schema-first validation across governed artifacts.
3. Machine-usable registries, indexes, and state surfaces for continuity.
4. Clear authority boundaries between human-readable outputs and canonical machine truth.
5. Structured traceability and audit-ready evidence.

Why this matters:

1. Runtime quality stays consistent across operators and domains.
2. Governance integrity survives delivery pressure.
3. Onboarding, handoff, and restart effort go down.
4. The agent can move faster without becoming opaque or unreviewable.

## Shared Capability Model

Information intake:

1. Normalize incoming context into governed structures.
2. Reject malformed or unsafe writes before persistence.
3. Preserve source, intent, and constraint linkage.

Tracking and continuity:

1. Track tasks, decisions, execution state, and evidence with stable identifiers.
2. Maintain run-level continuity across sessions and handoffs.
3. Make blockers, ambiguity, and risk explicit instead of burying them in notes.

Consolidation and reuse:

1. Keep run-specific details scoped to the active workflow.
2. Promote validated reusable insights into shared knowledge.
3. Keep reusable knowledge aligned with domain contracts and workflow structure.

Retrieval and analysis:

1. Prefer route-first, index-first, machine-usable retrieval.
2. Give the agent and the human access to the same governed context from different views.
3. Reduce restart cost for interrupted or handed-off work.

Projection and closeout:

1. Project readable notes, findings, reports, solutions, and recaps from governed state.
2. Preserve the machine-usable state behind those outputs for validation and replay.
3. Produce reusable closeout artifacts tied back to evidence and workflow history.

## Example Operator Experience

1. The operator starts a new challenge, engagement, or other domain run.
2. The operator provides goals, scope, constraints, and operating context.
3. The system resolves the correct route or asks for clarification before execution.
4. The agent performs the next bounded workflow step and updates governed state.
5. Helper and harness code support retrieval, validation, orchestration, and evidence capture.
6. Human-readable artifacts stay current so the operator can review progress without managing hidden internals directly.
7. The human steps in to redirect, approve, unblock, or decide when judgment is required.
8. Closeout produces reusable, trace-linked outputs and clear next-step options.

## First-Wave Product Shape

1. Core provides the reusable runtime, governance, validation, and traceability substrate.
2. Domain packs provide the operator-facing workflow experience.
3. The first shipping domain pack is offensive security.
4. Within that pack, CTF ships first and pentest follows.
5. Future domains can be added through the same pack model without turning the first domain into the hidden baseline for everything else.

## Product Boundaries

WatchTower is not intended to be:

1. A passive note archive.
2. A human-only documentation workflow with no governed machine state.
3. A code-first product where Python helpers become the primary user experience.
4. A system that depends on routine manual editing of hidden internals.
5. A product that removes human oversight from consequential decisions.

## Success Signals

1. Operators start work with less friction and less context rebuilding.
2. Guided execution stays fast without bypassing governance.
3. Handoffs preserve intent, evidence, and current state more reliably.
4. Customer-facing outputs are cleaner and more reproducible.
5. The product becomes more useful over time because validated knowledge compounds.

## References
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)

## Updated At
- `2026-03-09T23:02:08Z`
