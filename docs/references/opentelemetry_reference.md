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
updated_at: "2026-03-09T05:03:16Z"
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
- `https://opentelemetry.io/docs/specs/otel/` - verified 2026-03-09; OpenTelemetry Specification 1.55.0.
- `https://opentelemetry.io/docs/specs/semconv/` - verified 2026-03-09; OpenTelemetry semantic conventions 1.40.0.
- `https://opentelemetry.io/docs/specs/otel/logs/data-model/` - verified 2026-03-09; Logs Data Model.
- `https://opentelemetry.io/docs/specs/otel/metrics/data-model/` - verified 2026-03-09; Metrics Data Model.
- `https://opentelemetry.io/docs/specs/otel/logs/sdk/` - verified 2026-03-09; Logs SDK.
- `https://opentelemetry.io/docs/specs/status/` - verified 2026-03-09; Specification Status Summary.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Core Signals
| Signal | What it captures | Notes |
|---|---|---|
| traces | causal request or operation flow | good for end-to-end correlation |
| metrics | numeric measurements over time | good for rates, counts, and latency |
| logs | event records | still need local structure and handling rules |

### Core Rules
- Separate telemetry schema design from transport or vendor selection.
- Keep semantic attribute names and span or status meanings deliberate and consistent.
- Decide whether you actually need all three signals or only a subset.

### Common Pitfalls
- Adopting the vocabulary without deciding what events or attributes matter locally.
- Mixing trace correlation, business events, and arbitrary log fields without a model.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if future repository telemetry, audit events, or traceable automation surfaces are introduced.
- Pair it with W3C Trace Context when cross-process correlation matters.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.

## Updated At
- `2026-03-09T05:03:16Z`
