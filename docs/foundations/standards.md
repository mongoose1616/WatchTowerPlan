---
id: "foundation.standards"
title: "Standards"
summary: "Explains the repository-wide standards posture and why governed standards matter."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "standards"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/standards/"
  - "core/control_plane/"
  - "workflows/modules/"
aliases:
  - "standards posture"
---

# Standards

Standards in this repository exist to protect coherence in an LLM/agent-driven system. They are not decoration and they are not optional cleanup work. The point is to keep product intent, machine state, workflows, human-readable outputs, and evidence aligned so the system remains trustworthy as it grows.

## Core

Core standards define how shared machine-facing surfaces behave. If these rules are loose, every domain pack becomes harder to validate and easier to break.

- Keep one canonical source for each important machine-facing fact, policy rule, command contract, schema, and lifecycle state.
- Use a clear authority and precedence model so specs, workflows, registries, indexes, and references do not compete as equal truth.
- Make machine-facing surfaces schema-first, versioned, and fail-closed.
- Keep paired human-readable and machine-usable forms of durable artifacts wherever practical, with a defined relationship between them.
- Require synchronized updates across related governed artifacts.
- Make validation mandatory for governed changes.
- Prefer local, deterministic command surfaces for setup, QA, validation, and verification.
- Gate risky or high-impact operations explicitly.
- Treat mutable runtime state, generated reports, and release evidence as governed artifacts with clear storage rules.

## Across Both Layers

Core and domain packs should share the same discipline. The operating model depends on loading the right context, using small composable workflow units, and keeping narrative changes tied to traceable governed updates. The default assumption should be that the LLM or agent performs the routine work, while the human reviews, redirects, resolves blockers, and makes the calls that should not be delegated.

- Use route-first and index-first retrieval instead of broad scans.
- Keep human and agent entrypoints thin, modular, and easy to inspect.
- Design workflow modules as single-objective units with explicit triggers, inputs, steps, outputs, validation, and handoff rules.
- Design durable artifacts so both humans and machines can use them without inventing parallel undocumented state.
- Update traceability, acceptance, validation, and registry surfaces alongside product, planning, or workflow changes.
- Favor readable, deterministic code and behavior-oriented tests.
- Use governed templates for recurring artifacts such as workflows, ADRs, intake packets, release decisions, and implementation reports.
- Mark historical, legacy, and reference-only material as non-authoritative by default.
- Require explicit justification for exceptions.
- Use disciplined commits that represent one logical change in a parseable format.

## Domain Packs

Domain pack standards should keep packs expressive for their domain without letting them drift away from the shared control model.

- Keep packs portable and primarily declarative.
- Maintain a clear boundary between user-editable surfaces and managed pack state.
- Do not allow pack-local hidden state to become the operator-authored source of truth.
- Require pack workflows, templates, knowledge assets, and tool guidance to follow shared structural contracts.
- Require pack artifacts to remain usable by both the human reviewer and the agent executor wherever practical.
- Fail closed when manifests, registries, schemas, or compatibility contracts are invalid.
- Keep outputs as governed projections from managed state rather than ad hoc standalone documents.
- Allow domain-specific expression without bypassing shared core contracts.

## References
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md)

## Updated At
- `2026-03-09T23:02:08Z`
