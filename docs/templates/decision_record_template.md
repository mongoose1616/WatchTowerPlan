---
trace_id: "trace.example_initiative"
id: "decision.example_decision"
title: "<Decision Title>"
summary: "<One-line description of the decision boundary.>"
type: "decision_record"
status: "active"
owner: "repository_maintainer"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
audience: "shared"
authority: "supporting"
applies_to:
  - "<repo/path/>"
  - "<concept_id>"
aliases:
  - "<helpful search alias>"
---

# <Decision Title>

> Use this template for durable decision records stored under `docs/planning/decisions/`.
> Keep the final document aligned with [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md) and [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md).
> Keep front matter aligned with the `Record Metadata` block below.
> When `applies_to` uses repo paths, files should omit a trailing slash and directories should end in `/`.
> Keep one primary decision per file.

## Record Metadata
- `Trace ID`: `trace.example_initiative`
- `Decision ID`: `decision.example_decision`
- `Record Status`: `active`
- `Decision Status`: `proposed`
- `Linked PRDs`: `None`
- `Linked Designs`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `YYYY-MM-DDTHH:MM:SSZ`

## Summary
<One short explanation of the decision boundary.>

## Decision Statement
<State the decision in one clear sentence.>

## Trigger or Source Request
<Describe what prompted the decision.>

## Current Context and Constraints
- <Constraint or current-state fact>

## Applied References and Implications
- <Reference or authority>: <Why it affects this decision.>

## Affected Surfaces
- <PRD, design, plan, standard, workflow, or implementation path affected>

## Options Considered
### Option 1
- <Description>
- <Strength>
- <Tradeoff>

### Option 2
- <Description>
- <Strength>
- <Tradeoff>

## Chosen Outcome
<Describe the recommended or accepted outcome.>

## Rationale and Tradeoffs
- <Why this outcome was chosen>

## Consequences and Follow-Up Impacts
- <What changes next>

## Risks, Dependencies, and Assumptions
- <Risk, dependency, or assumption>

## References
- <Companion document or source>

## Optional Sections
Add only when they materially improve the decision record:
- `Open Questions`
- `Supersession`
