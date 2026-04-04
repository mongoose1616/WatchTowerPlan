---
id: "std.engineering.runtime_telemetry"
title: "Runtime Telemetry Standard"
summary: "This standard defines the baseline local runtime telemetry contract for command timing, error tracing, and pack-local telemetry sinks."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "runtime_telemetry"
owner: "repository_maintainer"
updated_at: "2026-04-04T03:05:00Z"
audience: "shared"
authority: "authoritative"
---

# Runtime Telemetry Standard

## Summary
This standard defines the baseline local runtime telemetry contract for command timing, error tracing, and pack-local telemetry sinks.

## Purpose
Give the repository one deliberate runtime-observability baseline so operators and contributors can diagnose slow or failing command paths without inventing ad hoc profiling or logging behavior each time.

## Scope
- Applies to reusable-core telemetry runtime code, host-owned CLI lifecycle instrumentation, and pack-owned command or orchestration paths that emit runtime telemetry.
- Applies to runtime telemetry storage under pack machine roots such as `<pack-root>/.wt/runtime/telemetry/`.
- Covers enablement defaults, environment-variable control, stderr summaries, JSONL event records, failure posture, and dry-run-first cleanup of retained telemetry sinks.
- Does not define OTEL exporters, cross-process trace propagation, deliberate benchmark methodology, retained benchmark evidence, or performance-regression policy.

## Use When
- Adding or changing runtime timing or error tracing behavior.
- Choosing where runtime telemetry files should live.
- Instrumenting CLI, sync, validation, pack-runtime, or pack-owned orchestration code.
- Cleaning retained telemetry JSONL files without using ad hoc filesystem deletion.

## Related Standards and Sources
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md): establishes that local runtime telemetry is now an active implementation baseline while OTEL remains a later candidate.
- [performance_benchmarking_standard.md](/core/docs/standards/engineering/performance_benchmarking_standard.md): governs deliberate retained performance measurement and keeps that contract separate from default-on telemetry.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): constrains where runtime implementation and local tooling live.
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md): constrains how hosted packs own machine-root storage and runtime integration surfaces.
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md): explains how pack authors should carry the runtime sink contract into copied or newly created packs.
- [python_logging_reference.md](/core/docs/references/python_logging_reference.md): reference baseline for structured Python logging decisions.
- [ndjson_spec_reference.md](/core/docs/references/ndjson_spec_reference.md): reference baseline for one-record-per-line JSON event streams.
- [opentelemetry_reference.md](/core/docs/references/opentelemetry_reference.md): future-facing reference for later OTEL mapping or exporter work.
- [w3c_trace_context_reference.md](/core/docs/references/w3c_trace_context_reference.md): future-facing reference for later cross-process trace propagation.

## Guidance
- Telemetry must be local and fail-open in the current baseline.
- Emit runtime telemetry by default unless `WATCHTOWER_TELEMETRY=off`.
- Emit one concise command summary to stderr by default unless `WATCHTOWER_TELEMETRY_STDERR=off`.
- Keep normal human-readable and JSON command results on stdout. Do not mix telemetry records into stdout payloads.
- Use environment variables rather than global CLI flags for cross-cutting telemetry control in this baseline.
- Use only standard-library facilities for timing, JSONL writing, ID generation, sink management, and stderr summaries unless a later approved change explicitly widens the dependency boundary.
- Keep runtime telemetry identifiers separate from planning `trace_id`. When planning identity is already available, attach it only as optional context.
- Instrument public service or orchestration boundaries rather than every low-level helper.
- Treat runtime telemetry JSONL as operational runtime state, not as a governed durable artifact family.
- Use a dry-run-first cleanup path that stays inside the resolved telemetry root and only deletes matched telemetry JSONL files plus any now-empty dated directories beneath that root.
- Do not treat telemetry JSONL as retained benchmark evidence. Use the performance benchmarking standard and retained benchmark-record family for deliberate repeatable performance measurement.

## Structure or Data Model
### Enablement contract
| Surface | Rule |
|---|---|
| `WATCHTOWER_TELEMETRY` | `on` by default; `off` disables runtime telemetry for the invocation |
| `WATCHTOWER_TELEMETRY_STDERR` | `on` by default; `off` suppresses stderr summaries while leaving file telemetry enabled |
| `WATCHTOWER_TELEMETRY_DIR` | optional explicit sink root override |

### Default sink contract
| Rule | Requirement |
|---|---|
| default sink root | `<machine_root>/runtime/telemetry/` |
| example pack path | `<pack-root>/.wt/runtime/telemetry/` |
| sink layout | dated subdirectories are allowed and preferred |
| file format | JSONL / NDJSON |
| file ownership | pack-local operational runtime state |
| git behavior | ignored |
| cleanup command | `watchtower-core telemetry delete` |

### Event contract
| Record type | Purpose |
|---|---|
| `run_started` | start of one top-level command invocation |
| `operation_result` | completion record for one nested operation or boundary span |
| `run_finished` | end of one top-level command invocation |

### Failure posture
| Condition | Required behavior |
|---|---|
| sink creation fails | disable telemetry for the invocation and continue the command |
| record serialization fails | disable telemetry for the invocation and continue the command |
| JSONL write fails | disable telemetry for the invocation and continue the command |
| command itself fails | preserve existing exit code and emit telemetry only if still available |

## Operationalization
- `Modes`: `runtime`; `documentation`; `validation`
- `Operational Surfaces`: `core/python/src/watchtower_core/telemetry/`; `core/python/src/watchtower_host/cli/`; `core/docs/commands/core_python/watchtower_core_telemetry.md`; `core/docs/references/domain_pack_authoring_reference.md`; `.gitignore`

## Validation
- Reviewers should reject runtime telemetry changes that alter existing stdout payload contracts without an explicit separately approved command-contract change.
- Reviewers should reject runtime telemetry sinks that escape the active pack machine root by default.
- Reviewers should reject telemetry failures that can break normal command execution.
- Reviewers should reject cleanup paths that reach outside the resolved telemetry root or delete non-telemetry governed artifacts.
- Reviewers should reject telemetry changes that silently widen this surface into benchmark methodology or retained performance evidence ownership.
- Representative commands should prove both enabled and disabled paths through unit or integration coverage.

## Change Control
- Update this standard when the runtime telemetry enablement contract, sink placement rule, event model, or failure posture changes materially.
- Update companion READMEs, host or pack authoring guidance, and affected command docs in the same change set when telemetry behavior changes materially.
- Keep deliberate benchmarking methodology and retained benchmark evidence in `performance_benchmarking_standard.md` rather than silently widening this telemetry baseline.
- If OTEL, W3C propagation, or durable promoted telemetry analysis becomes active policy later, capture that as a separate approved change rather than silently widening this baseline.

## References
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md)
- [performance_benchmarking_standard.md](/core/docs/standards/engineering/performance_benchmarking_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md)
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [python_logging_reference.md](/core/docs/references/python_logging_reference.md)
- [ndjson_spec_reference.md](/core/docs/references/ndjson_spec_reference.md)
- [opentelemetry_reference.md](/core/docs/references/opentelemetry_reference.md)
- [w3c_trace_context_reference.md](/core/docs/references/w3c_trace_context_reference.md)

## Updated At
- `2026-04-04T03:05:00Z`
