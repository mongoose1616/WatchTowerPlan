---
id: "ref.opentelemetry"
title: "OpenTelemetry Reference"
summary: "This document provides a working reference for OpenTelemetry as an observability baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "opentelemetry"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# OpenTelemetry Reference

## Summary
This document provides a working reference for OpenTelemetry as an observability baseline.

## Purpose
Provide a coherent observability baseline for traces, metrics, logs, and semantic conventions when the repository needs structured telemetry.

## Scope
- Covers OpenTelemetry specs, semantic conventions, logs, metrics, logs SDK guidance, and status guidance.
- Does not define this repository's full telemetry policy by itself.

## Canonical Upstream
- `https://opentelemetry.io/docs/specs/otel/`
- `https://opentelemetry.io/docs/specs/semconv/`
- `https://opentelemetry.io/docs/specs/otel/logs/data-model/`
- `https://opentelemetry.io/docs/specs/otel/metrics/data-model/`
- `https://opentelemetry.io/docs/specs/otel/logs/sdk/`
- `https://opentelemetry.io/docs/specs/status/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use OpenTelemetry as a conceptual baseline when portable observability semantics matter.
- Separate telemetry schema design from transport or vendor choices.
- Keep semantic attribute names and status meanings deliberate rather than ad hoc.

## Local Mapping in This Repository
- Use this reference if future repository telemetry, audit events, or traceable automation surfaces are introduced.
- Pair it with W3C Trace Context when cross-process correlation matters.

## Process or Workflow
1. Read this reference before codifying OpenTelemetry Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how telemetry and observability contracts should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
