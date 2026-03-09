---
id: "ref.ndjson_spec"
title: "NDJSON Reference"
summary: "This document provides a working reference for NDJSON as a practical newline-delimited JSON stream format."
type: "reference"
status: "active"
tags:
  - "reference"
  - "ndjson_spec"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# NDJSON Reference

## Summary
This document provides a working reference for NDJSON as a practical newline-delimited JSON stream format.

## Purpose
Provide a simple operational stream format baseline for append-only records, logs, indexes, or task state streams.

## Scope
- Covers NDJSON as a newline-delimited JSON convention.
- Does not define every repository stream schema or event model.

## Canonical Upstream
- `https://github.com/ndjson/ndjson-spec`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use NDJSON when append-only, line-oriented processing matters more than nested document structure.
- Keep one valid JSON object per line.
- Treat schema and event semantics as separate concerns from the NDJSON container format.

## Local Mapping in This Repository
- Use this reference for any future operational streams or task/event logs in the repository.
- Pair it with schema and timestamp standards when designing durable event records.

## Process or Workflow
1. Read this reference before codifying NDJSON Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how line-oriented JSON streams should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
