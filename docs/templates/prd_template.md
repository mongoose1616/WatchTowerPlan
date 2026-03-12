---
trace_id: "trace.example_initiative"
id: "prd.example_initiative"
title: "<PRD Title>"
summary: "<One-line description of the product change and why it matters.>"
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
audience: "shared"
authority: "authoritative"
applies_to:
  - "<repo/path/>"
  - "<concept_id>"
aliases:
  - "<helpful search alias>"
---

# <PRD Title>

> Use this template for product requirements documents stored under `docs/planning/prds/`.
> Keep the final document aligned with [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md).
> Keep front matter aligned with the `Record Metadata` block below.
> When `applies_to` uses repo paths, files should omit a trailing slash and directories should end in `/`.
> Start with the required sections below and add optional sections only when they materially reduce ambiguity.

## Record Metadata
- `Trace ID`: `trace.example_initiative`
- `PRD ID`: `prd.example_initiative`
- `Status`: `active`
- `Linked Decisions`: `None`
- `Linked Designs`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `YYYY-MM-DDTHH:MM:SSZ`

## Summary
<One short explanation of the product change and why it matters.>

## Problem Statement
<Describe the problem this PRD exists to solve.>

## Goals
- <Goal>
- <Goal>

## Non-Goals
- <Non-goal>
- <Non-goal>

## Requirements
- `req.example_initiative.001`: <Requirement>
- `req.example_initiative.002`: <Requirement>

## Acceptance Criteria
- `ac.example_initiative.001`: <Acceptance criterion>
- `ac.example_initiative.002`: <Acceptance criterion>

## Risks and Dependencies
- <Risk or dependency>

## References
- <Relevant internal or external source that materially informed this PRD.>

## Optional Sections
Add only when they materially improve the PRD:
- `Target Users or Actors`
- `Key Scenarios`
- `Success Metrics`
- `Open Questions`
- `Foundations References Applied` using `source: implication` bullets
