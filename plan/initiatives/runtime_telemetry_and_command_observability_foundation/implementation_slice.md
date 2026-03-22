# Runtime Telemetry And Command Observability Foundation Implementation Slice

## Summary
Adds default-on local runtime telemetry, timing, and error tracing across host, reusable-core, and plan command paths without adopting OTEL yet.

## Work Breakdown
- `task.runtime_telemetry_and_command_observability_foundation.bootstrap_runtime_telemetry_and_command_observability_foundation`
  - Restore or isolate unrelated worktree drift.
  - Bootstrap the package, author the inputs, confirm them, approve the initiative, and seed the detailed execution tasks.
- `task.runtime_telemetry_and_command_observability_foundation.capture_runtime_telemetry_policy`
  - Add the runtime telemetry standard.
  - Update foundations and pack-authoring guidance.
  - Add ignore rules and pack path guidance for `.wt/runtime/telemetry/`.
- `task.runtime_telemetry_and_command_observability_foundation.build_shared_telemetry_runtime`
  - Add `watchtower_core.telemetry`.
  - Implement config resolution, sink management, run context, nested operations, JSONL writing, and fail-open disablement.
- `task.runtime_telemetry_and_command_observability_foundation.instrument_host_command_lifecycle`
  - Instrument host main parse/dispatch/help/error paths.
  - Integrate telemetry-aware helper hooks in shared CLI emission helpers.
- `task.runtime_telemetry_and_command_observability_foundation.instrument_sync_validation_and_pack_runtime`
  - Add telemetry to sync harness, validation entrypoints, pack contract validation, and pack runtime import and resolution.
- `task.runtime_telemetry_and_command_observability_foundation.instrument_plan_pack_orchestration`
  - Add telemetry to representative plan read and write flows, including sync, initiative lifecycle, and task lifecycle orchestration.
- `task.runtime_telemetry_and_command_observability_foundation.refresh_docs_and_command_contracts`
  - Refresh READMEs, command docs, and pack guidance to explain the new runtime behavior.
- `task.runtime_telemetry_and_command_observability_foundation.validate_benchmark_and_closeout`
  - Run full validation, benchmark representative commands, close execution tasks, and close the initiative.

## Commit Boundaries
- Commit 1: policy and storage contract
  - runtime telemetry standard
  - foundation/authoring guidance updates
  - ignore rules
  - initiative package inputs and task seeds
- Commit 2: shared telemetry runtime and host CLI lifecycle instrumentation
- Commit 3: sync, validation, and pack-runtime instrumentation plus tests
- Commit 4: plan-pack instrumentation, docs refresh, full validation, benchmarks, and closeout

## Validation Strategy
- Narrow validation after Commit 1:
  - front-matter and document-semantics validation for changed standards or foundation docs
  - plan sync/coordination commands required to keep the initiative package aligned
- Narrow validation after Commit 2:
  - targeted `ruff check` on touched telemetry and host CLI modules
  - targeted `mypy` on touched telemetry and host CLI modules
  - targeted unit tests for telemetry runtime and CLI lifecycle behavior
- Narrow validation after Commit 3:
  - targeted `ruff`, `mypy`, and unit or integration tests for sync, validation, and pack runtime
- Final validation after Commit 4:
  - `./core/python/.venv/bin/ruff check core/python/src plan/python/src core/python/tests`
  - `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
  - `./core/python/.venv/bin/mypy plan/python/src/watchtower_plan`
  - `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
  - `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration -q`

## Benchmark Proof
- Capture 5-run median timings before and after the final commit for:
  - `watchtower-core doctor`
  - `watchtower-core pack list --format json`
  - `watchtower-core pack validate --pack plan --format json`
  - one representative plan write command such as `watchtower-core plan approve --initiative-slug <fixture> --write --format json` against a bounded fixture or controlled repo state
- Reject the tranche if telemetry introduces a severe usability regression.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
