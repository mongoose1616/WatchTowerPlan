---
id: "std.engineering.performance_benchmarking"
title: "Performance Benchmarking Standard"
summary: "This standard defines the deliberate fail-closed benchmarking contract for reusable-core performance measurement and retained benchmark evidence."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "performance_benchmarking"
owner: "repository_maintainer"
updated_at: "2026-03-30T18:30:00Z"
audience: "shared"
authority: "authoritative"
---

# Performance Benchmarking Standard

## Summary
This standard defines the deliberate fail-closed benchmarking contract for reusable-core performance measurement and retained benchmark evidence.

## Purpose
Give the repository one explicit methodology for repeatable performance measurement so contributors can compare current behavior against an owned baseline without mixing ad hoc timings, transient telemetry files, and durable benchmark evidence.

## Scope
- Applies to reusable-core benchmark suite declarations, benchmark runner code, retained benchmark records, and benchmark-focused command surfaces.
- Applies to benchmark suites and retained benchmark records owned under `core/control_plane/**`.
- Covers warmup and measured-run rules, subprocess isolation, environment capture, telemetry-on and telemetry-off comparison, retained benchmark evidence, and baseline comparison behavior.
- Does not define default-on runtime telemetry behavior, remote metrics collection, or general logging policy.

## Use When
- Adding or changing reusable-core benchmark suites or benchmark runner behavior.
- Capturing a new shared-core performance baseline or comparing current behavior against a prior retained benchmark record.
- Reviewing whether a performance result is strong enough to retain as governed benchmark evidence.

## Related Standards and Sources
- [runtime_telemetry_standard.md](/core/docs/standards/engineering/runtime_telemetry_standard.md): governs default-on operational telemetry and explicitly does not own deliberate benchmark methodology or retained benchmark evidence.
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md): establishes the active local observability direction that benchmarking should use without widening the dependency boundary.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): constrains where the reusable benchmark runtime, tests, and CLI surfaces live.
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md): constrains why retained benchmark records are internal history rather than portable customer-bootstrap content.

## Guidance
- Benchmarking must be deliberate and fail-closed.
- Benchmark commands must run in fresh serialized subprocesses rather than as in-process timers around already-imported Python modules.
- Publish the benchmark suite definition in the authored benchmark-suite registry instead of hard-coding suite shape in Python.
- Use warmup runs to absorb obvious first-run effects and exclude those warmup timings from retained measured samples.
- Use median runtime as the primary reported summary for each telemetry mode.
- Benchmark both telemetry-on and telemetry-off modes when the suite contract says telemetry overhead is part of the measurement question.
- Treat runtime telemetry JSONL as supporting input to hotspot extraction, not as retained benchmark evidence by itself.
- Capture environment context with each retained benchmark record, including Python version, Python executable label, platform, CPU count when available, and current git context when available.
- Do not retain machine-local absolute paths inside benchmark environment context fields when an executable label or repo-logical path is sufficient for interpretation.
- Require suite-ID and command-ID parity before comparing a current benchmark run against a retained baseline record.
- Keep the benchmark runner stdlib-only unless a later approved change explicitly widens the dependency boundary.

## Structure or Data Model
### Execution contract
| Surface | Rule |
|---|---|
| execution mode | serialized subprocess execution |
| failure posture | fail closed |
| warmup runs | declared by the suite and excluded from retained measured samples |
| measured runs | declared by the suite and retained as raw timing samples |
| primary summary | median duration per command per mode |

### Telemetry mode contract
| Mode | Required environment |
|---|---|
| telemetry on | `WATCHTOWER_TELEMETRY=on`, `WATCHTOWER_TELEMETRY_STDERR=off`, `WATCHTOWER_TELEMETRY_DIR=<temp benchmark dir>` |
| telemetry off | `WATCHTOWER_TELEMETRY=off`, `WATCHTOWER_TELEMETRY_STDERR=off` |

### Retained benchmark evidence contract
| Surface | Requirement |
|---|---|
| benchmark suite registry | authored under `core/control_plane/registries/benchmark_suite_registry.json` |
| retained benchmark records | stored under `core/control_plane/records/benchmarks/` |
| schema contract | validate against the published benchmark-record schema before writing retained output |
| environment context | retain portable runtime labels and repo context, not machine-local absolute interpreter paths |
| command evidence | retain raw telemetry-on and telemetry-off measured timing samples plus medians, delta, ratio, and top nested operations |
| baseline comparison | optional, but only when suite ID and command IDs match exactly |

## Operationalization
- `Modes`: `benchmarking`; `documentation`; `validation`
- `Operational Surfaces`: `core/python/src/watchtower_core/benchmarking/`; `core/python/src/watchtower_host/cli/benchmark_family.py`; `core/control_plane/registries/benchmark_suite_registry.json`; `core/control_plane/records/benchmarks/`

## Validation
- Reviewers should reject benchmark changes that bypass the governed benchmark-suite registry for reusable-core suite definition.
- Reviewers should reject benchmark runners that silently continue after non-zero subprocess exits, missing telemetry files, suite mismatch, or schema-invalid output.
- Representative benchmark coverage should prove warmup exclusion, telemetry-on/off env handling, retained record validation, and baseline comparison behavior.
- Retained benchmark records should validate through the benchmark-record validator and remain excluded from portable exports.

## Change Control
- Update this standard when benchmark execution methodology, retained record ownership, failure posture, or baseline comparison rules change materially.
- Update the benchmark suite registry, benchmark record schema, benchmark runner docs, and command docs in the same change set when the benchmark contract changes materially.
- Keep telemetry policy changes in the runtime telemetry standard rather than silently widening this benchmark standard into an observability catch-all.

## References
- [runtime_telemetry_standard.md](/core/docs/standards/engineering/runtime_telemetry_standard.md)
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md)

## Updated At
- `2026-03-30T18:30:00Z`
