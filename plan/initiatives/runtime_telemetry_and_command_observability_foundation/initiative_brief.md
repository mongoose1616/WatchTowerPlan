# Runtime Telemetry And Command Observability Foundation

## Summary
Adds default-on local runtime telemetry, timing, and error tracing across host, reusable-core, and plan command paths without adopting OTEL yet.

## Identity
- `initiative_id`: `initiative.runtime_telemetry_and_command_observability_foundation`
- `trace_id`: `trace.runtime_telemetry_and_command_observability_foundation`
- `scope_type`: `pack_wide`

## Problem
- The current CLI and runtime paths provide almost no consistent machine-readable runtime timing or failure tracing.
- Recent performance and failure-isolation work had to rely on ad hoc profiling, targeted test reproduction, and manual code inspection because there is no stable local telemetry layer for normal operator commands.
- The repository now has enough command, sync, validation, and pack-runtime surface area that missing runtime observability materially slows debugging, performance work, and fault isolation.
- Existing planning `trace_id` usage covers planning and governance state only. It does not provide runtime command correlation, nested operation timing, or command-failure telemetry.
- The current standards posture still treats observability as a candidate future capability. That is now behind the actual operational need.

## Desired Outcome
- Every normal host-owned CLI invocation emits one local telemetry run record set and one concise stderr summary by default.
- Telemetry remains local-only, dependency-free, and fail-open in this tranche.
- Core, host, and plan code paths emit bounded nested operation records at public service boundaries rather than arbitrary low-level tracing noise.
- The default sink is pack-local runtime state under `<machine_root>/runtime/telemetry/`, with `plan/.wt/runtime/telemetry/` as the proof-pack path in this repository.
- Operators can disable or quiet telemetry through environment variables without changing command syntax.

## Scope
- Reusable-core telemetry runtime under `core/python/src/watchtower_core/`.
- Host CLI lifecycle instrumentation under `core/python/src/watchtower_host/cli/`.
- Reusable sync, validation, and pack-integration runtime instrumentation under `core/python/src/watchtower_core/`.
- Plan-pack orchestration instrumentation under `plan/python/src/watchtower_plan/`.
- Shared standards, foundations, README guidance, pack authoring reference updates, and ignore rules required to make the new runtime state contract explicit.
- Initiative-local tracking, task breakdown, validation evidence, commit sequencing, and closeout for this work.

## Out Of Scope
- OpenTelemetry SDK adoption, exporters, collectors, remote sinks, or vendor integrations.
- W3C Trace Context propagation across processes or network hops.
- Metrics aggregation, dashboards, or durable promoted telemetry-analysis guidance.
- Converting runtime telemetry JSONL into a governed durable artifact family in this tranche.
- Redesigning stdout payload contracts, CLI synopsis structure, or exit-code semantics.

## Operator Requirements
- Telemetry must not break command execution when sink creation, file writes, or serialization fails.
- Human-readable command output and JSON command output must remain unchanged on stdout.
- Telemetry summaries must go to stderr only and remain concise enough for interactive use.
- The runtime sink must be easy to ignore, delete, or relocate with the pack workspace.
- The implementation must not add new third-party Python dependencies.

## Acceptance Criteria
- `watchtower-core doctor`, `watchtower-core pack list`, `watchtower-core pack describe --pack plan`, `watchtower-core pack validate --pack plan`, one representative sync command, and one representative plan command emit telemetry by default without changing stdout contracts.
- Telemetry files are written under `plan/.wt/runtime/telemetry/` by default and are ignored by Git.
- `WATCHTOWER_TELEMETRY=off` disables file and stderr telemetry output without disabling the command itself.
- `WATCHTOWER_TELEMETRY_STDERR=off` suppresses stderr summaries while preserving JSONL telemetry when telemetry is otherwise enabled.
- Telemetry failures degrade silently or to internal disablement; they do not change command exit codes or raise user-facing telemetry exceptions.
- The full repo validation gate passes after the tranche lands.

## Non-Goals
- Do not turn runtime telemetry into a second planning or evidence system.
- Do not propagate planning terminology into the reusable telemetry contract beyond optional context attributes.
- Do not add per-function instrumentation across the entire codebase.
- Do not optimize every slow command in the same tranche; this initiative is for visibility first, not another full performance sweep.

## Initial Task Set
- `task.runtime_telemetry_and_command_observability_foundation.bootstrap_runtime_telemetry_and_command_observability_foundation`: Bootstrap, author, confirm, approve, and initialize the telemetry initiative package.
- `task.runtime_telemetry_and_command_observability_foundation.capture_runtime_telemetry_policy`: Publish the storage, ownership, enablement, and documentation rules for runtime telemetry before code lands.
- `task.runtime_telemetry_and_command_observability_foundation.build_shared_telemetry_runtime`: Add the reusable-core telemetry runtime, configuration resolution, sink management, and fail-open guard.
- `task.runtime_telemetry_and_command_observability_foundation.instrument_host_command_lifecycle`: Instrument root command parse, dispatch, help, error, and handler execution paths in the host CLI.
- `task.runtime_telemetry_and_command_observability_foundation.instrument_sync_validation_and_pack_runtime`: Instrument sync harness, validation entrypoints, and pack runtime resolution boundaries.
- `task.runtime_telemetry_and_command_observability_foundation.instrument_plan_pack_orchestration`: Instrument plan-owned read and write orchestration paths that operators use daily.
- `task.runtime_telemetry_and_command_observability_foundation.refresh_docs_and_command_contracts`: Update READMEs, standards, references, authoring guidance, and command docs to describe the new runtime contract.
- `task.runtime_telemetry_and_command_observability_foundation.validate_benchmark_and_closeout`: Run the full gate, benchmark representative commands, close completed tasks, and close the initiative.
