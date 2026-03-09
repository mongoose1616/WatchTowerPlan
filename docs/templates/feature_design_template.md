---
trace_id: "trace.example_feature"
id: "design.features.example_feature"
title: "<Feature Design Title>"
summary: "<One-line description of the design and intended outcome.>"
type: "feature_design"
status: "draft"
owner: "repository_maintainer"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
audience: "shared"
authority: "authoritative"
applies_to:
  - "<repo/path/or/concept>"
aliases:
  - "<helpful search alias>"
---

# <Feature Design Title>

> Use this template for feature-level technical designs that should be specific enough for implementation planning.
> Store the finished document under `docs/planning/design/features/` and keep it aligned with [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md).
> Keep front matter valid against the governed feature-design front matter profile and keep `updated_at` aligned with the `Updated At` section below.
> Keep the document focused on one feature or narrowly related capability.
> Record the recommended design, its tradeoffs, and the implementation guardrails without turning the document into a task checklist.

## Record Metadata
- `Trace ID`: `trace.example_feature`
- `Design ID`: `design.features.example_feature`
- `Design Status`: `draft`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `YYYY-MM-DDTHH:MM:SSZ`

## Summary
<Short explanation of the feature and the intended design outcome.>

## Source Request
- <Feature request, planning brief, issue, or user request that triggered this design.>

## Scope and Feature Boundary
- <What the design covers.>
- <What the design intentionally does not cover.>

## Current-State Context
- <Relevant codebase, control-plane, workflow, or documentation context.>
- <Current gaps or constraints that shape the design.>

## Foundations References Applied
- <Relevant docs/foundations document>: <Design implication, constraint, or rule adopted from it.>
- <Relevant docs/foundations document>: <Design implication, constraint, or rule adopted from it.>

## Internal Standards and Canonical References Applied
- <Relevant standard, template, schema, registry, contract, or canonical internal doc>: <What this authority requires or changes in the design.>
- <Relevant standard, template, schema, registry, contract, or canonical internal doc>: <What this authority requires or changes in the design.>

## External Sources Consulted
- <Primary external source>: <What it clarified, constrained, or justified in this design. Delete if none were needed.>

## Design Goals and Constraints
- <Primary design goal.>
- <Key constraint or non-goal.>
- <Key invariant the implementation must preserve.>

## Options Considered
### Option 1
- <Short description.>
- <Strengths.>
- <Tradeoffs or reasons not chosen.>

### Option 2
- <Short description.>
- <Strengths.>
- <Tradeoffs or reasons not chosen.>

## Recommended Design
### Architecture
- <Core components and responsibilities.>

### Data and Interface Impacts
- <Artifacts, schemas, registries, contracts, or interfaces affected.>

### Execution Flow
1. <Step in the recommended flow.>
2. <Step in the recommended flow.>
3. <Step in the recommended flow.>

### Invariants and Failure Cases
- <Invariant or fail-closed behavior.>
- <Failure mode that the implementation must handle explicitly.>

## Affected Surfaces
- <Docs, code paths, schemas, registries, contracts, tests, or policies that will change.>

## Design Guardrails
- <Rule that implementation planning must preserve.>
- <Rule that implementation planning must preserve.>

## Implementation-Planning Handoff Notes
- <What implementation planning should break down next.>
- <Dependencies or prerequisites implementation planning must account for.>

## Dependencies
- <Internal or external dependency.>

## Risks
- <Concrete risk or uncertainty.>

## Open Questions
- <Unresolved design question. Delete if none remain.>

## References
- <Relevant internal or external document.>

## Updated At
- `YYYY-MM-DDTHH:MM:SSZ`
