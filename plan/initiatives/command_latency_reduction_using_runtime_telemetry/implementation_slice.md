# Command Latency Reduction Using Runtime Telemetry Implementation Slice

## Summary
Uses the new local runtime telemetry to profile, prioritize, and reduce command latency across host, reusable core, and pack-owned paths.

## Work Breakdown
- `task.command_latency_reduction_using_runtime_telemetry.bootstrap_command_latency_reduction_using_runtime_telemetry`
  - Author the initiative package.
  - Confirm and approve the authored inputs.
  - Seed the detailed execution tasks.
- `task.command_latency_reduction_using_runtime_telemetry.capture_latency_baseline_and_hotspot_inventory`
  - Define the stable benchmark set.
  - Capture telemetry-on and telemetry-off medians.
  - Produce the first ranked hotspot inventory.
- `task.command_latency_reduction_using_runtime_telemetry.reduce_host_and_loader_startup_latency`
  - Reduce parser-build, command-group discovery, selected-pack activation, or loader startup cost where the telemetry proves it is material.
  - Add focused regression checks for any new cache or startup-path optimization.
- `task.command_latency_reduction_using_runtime_telemetry.reduce_plan_command_latency`
  - Reduce the slowest pack-owned `plan` command paths, especially coordination refresh, closeout, query, and task write orchestration.
  - Keep `watchtower_plan` changes bounded and push reusable optimizations back into `watchtower_core` when possible.
- `task.command_latency_reduction_using_runtime_telemetry.reduce_validation_and_pack_runtime_latency`
  - Reduce validation and pack-runtime work that still dominates common operator commands after the earlier slices land.
  - Keep contract behavior unchanged while cutting repeated work or unnecessary reloads.
- `task.command_latency_reduction_using_runtime_telemetry.add_latency_regression_guards`
  - Add or refine targeted tests, benchmark helpers, or telemetry-based assertions for the optimized paths.
  - Document the benchmark workflow and expected command set.
- `task.command_latency_reduction_using_runtime_telemetry.validate_benchmark_and_closeout`
  - Run the repo-wide validation gate.
  - Refresh the final benchmark set.
  - Capture the delta summary and close the initiative.

## Commit Boundaries
- Commit 1: initiative bootstrap, authored inputs, machine confirmation, approval, and task seeding.
- Commit 2: latency baseline capture plus hotspot inventory and any helper scaffolding needed for repeatable benchmarks.
- Commit 3: host and reusable-core startup latency reductions.
- Commit 4: plan command latency reductions.
- Commit 5: validation or pack-runtime latency reductions plus regression guards.
- Commit 6: final validation, benchmark refresh, and initiative closeout.

## Validation Strategy
- Before execution:
  - `./core/python/.venv/bin/watchtower-core plan confirm-inputs --initiative-slug command_latency_reduction_using_runtime_telemetry --write --format json`
  - `./core/python/.venv/bin/watchtower-core plan approve --initiative-slug command_latency_reduction_using_runtime_telemetry --write --format json`
- After each optimization slice:
  - targeted `ruff`
  - targeted `mypy`
  - targeted unit or integration tests for the changed seam
  - rerun the affected benchmark subset
- Final gate:
  - `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/tests/unit`
  - `./core/python/.venv/bin/ruff check plan/python/src/watchtower_plan core/python/tests/integration`
  - `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
  - `./core/python/.venv/bin/mypy plan/python/src/watchtower_plan`
  - `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
  - `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration -q`

## Benchmark Protocol
- Record 5-run medians with telemetry enabled and disabled.
- Keep `WATCHTOWER_TELEMETRY_STDERR=off` during timing captures so the benchmark focuses on runtime cost rather than console noise.
- Store the benchmark summary in initiative-local notes or closeout evidence before closing the tranche.
- Reject any optimization that makes the common command set slower without a stronger compensating gain elsewhere.

## Exit Conditions
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
- The initiative closes only after the benchmark set is rerun on the final tree and the remaining hotspots are either reduced or explicitly deferred.
