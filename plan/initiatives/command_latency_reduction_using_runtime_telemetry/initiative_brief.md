# Command Latency Reduction Using Runtime Telemetry

## Summary
Uses the new local runtime telemetry to profile, prioritize, and reduce command latency across host, reusable core, and pack-owned paths.

## Identity
- `initiative_id`: `initiative.command_latency_reduction_using_runtime_telemetry`
- `trace_id`: `trace.command_latency_reduction_using_runtime_telemetry`
- `scope_type`: `pack_wide`

## Problem
- The repository now has usable local runtime telemetry, but it is not yet being used as the primary source of evidence for command-latency reduction.
- Operator-facing commands still have a long-tail latency problem even after the earlier sync and task-tracking performance work.
- The remaining slow paths are likely distributed across host startup, reusable-core loading and validation seams, and pack-owned orchestration rather than one single hotspot.
- Future optimization work will drift or regress unless one initiative captures a stable benchmark set, a ranked hotspot inventory, and explicit regression guards.

## Desired Outcome
- Produce one telemetry-backed latency baseline for the highest-value operator command set.
- Reduce median latency for the slowest real commands without changing stdout payloads, exit codes, or hosted-pack boundaries.
- Leave behind one repeatable optimization workflow: collect telemetry, identify hotspots, apply bounded refactors, rerun the same measurements, and reject regressions.

## In Scope
- Host CLI startup and dispatch overhead, including parser construction and selected-pack loading.
- Reusable-core loading, validation, sync, query, and artifact or schema access paths that show up in telemetry traces for slow commands.
- Pack-owned `watchtower_plan` command paths whose latency is materially visible to operators, especially sync, query, closeout, and task lifecycle flows.
- Measurement discipline, benchmark commands, telemetry evidence capture, and targeted regression coverage for latency-sensitive paths.

## Out Of Scope
- OpenTelemetry exporters, remote collectors, or distributed tracing.
- Broad algorithmic rewrites without telemetry evidence that they are on the hot path.
- Multi-user concurrency control, database migration, or state-model redesign unless telemetry proves one of those is the immediate latency driver.
- Cosmetic CLI changes that do not materially improve runtime behavior.

## Operator Requirements
- Use the existing runtime telemetry contract as the primary profiling input instead of ad hoc guesswork.
- Keep commands operational during the optimization tranche; performance work must not break standard CLI behavior.
- Prefer changes that improve the common operator flows first: `doctor`, `pack` inspection and validation, `plan` sync and query, and plan closeout and task mutations.
- Preserve clear before-versus-after evidence for each performance slice so later contributors can see which optimizations actually mattered.

## Acceptance Criteria
- A baseline command set is documented and benchmarked with telemetry-on and telemetry-off medians.
- The initiative produces a ranked hotspot inventory tied to actual telemetry evidence, not only intuition.
- At least the highest-value latency hotspots in host startup, reusable core, and pack-owned orchestration are either reduced or explicitly deferred with evidence-backed rationale.
- The repo-wide validation gate remains green after every landed optimization slice.
- The final summary captures the benchmark deltas, the hotspots addressed, the remaining slow paths, and the next recommended optimization tranche if one remains.

## Non-Goals
- This initiative does not try to make every command instantaneous.
- This initiative does not add a new observability backend.
- This initiative does not collapse core, host, and pack boundaries in the name of speed.

## Planned Task Set
- `task.command_latency_reduction_using_runtime_telemetry.bootstrap_command_latency_reduction_using_runtime_telemetry`: Finish bootstrap, author the detailed plan, confirm inputs, approve the initiative, and seed the execution tasks.
- `task.command_latency_reduction_using_runtime_telemetry.capture_latency_baseline_and_hotspot_inventory`: Collect the benchmark baseline, rank the command hotspots, and capture the first optimization inventory.
- `task.command_latency_reduction_using_runtime_telemetry.reduce_host_and_loader_startup_latency`: Reduce host startup, parser-build, selected-pack load, and loader activation overhead where telemetry proves it matters.
- `task.command_latency_reduction_using_runtime_telemetry.reduce_plan_command_latency`: Reduce pack-owned `plan` command latency in the highest-value orchestration paths.
- `task.command_latency_reduction_using_runtime_telemetry.reduce_validation_and_pack_runtime_latency`: Reduce validation, pack-runtime, and contract-evaluation latency that still dominates common operator flows.
- `task.command_latency_reduction_using_runtime_telemetry.add_latency_regression_guards`: Add targeted regression checks and benchmark guidance so the optimized paths do not silently drift back.
- `task.command_latency_reduction_using_runtime_telemetry.validate_benchmark_and_closeout`: Rerun the full gate, refresh the benchmark evidence, capture the final delta summary, and close the initiative.
