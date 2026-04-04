# Performance Benchmarking Workflow

## Purpose
Use this workflow to run deliberate, fail-closed reusable-core performance benchmarks and interpret or retain the resulting benchmark evidence without mixing it with default runtime telemetry or ad hoc local profiling.

## Use When
- A task needs a repeatable shared-core performance baseline for one governed benchmark suite.
- A contributor needs to compare current benchmark results against a prior retained benchmark record.
- A performance-sensitive change needs benchmark evidence rather than only tests, telemetry, or informal timing notes.
- Choose this route when the main question is deliberate benchmarking or retained benchmark evidence, not test-runtime cleanup or default operational telemetry behavior.

## Inputs
- Scoped benchmark objective, including the suite or command path under review and whether the task is baseline capture, baseline comparison, or regression investigation
- Relevant benchmark suite ID, retained benchmark record ID or path when comparison is requested, and any explicitly requested run overrides
- Current code or governed-artifact changes in scope when the benchmark task is evidence for a broader engineering change
- Environment constraints or caveats that could affect comparability, such as platform drift or intentionally changed workload shape

## Additional Files to Load
- [performance_benchmarking_standard.md](/core/docs/standards/engineering/performance_benchmarking_standard.md): defines the deliberate benchmark contract, telemetry-mode expectations, subprocess isolation rules, and retained-record boundary this workflow must preserve.
- [watchtower_core_benchmark_run.md](/core/docs/commands/core_python/watchtower_core_benchmark_run.md): documents the executable benchmark runner, suite-selection flags, baseline comparison behavior, and retained-record write path.
- [watchtower_core_query_benchmarks.md](/core/docs/commands/core_python/watchtower_core_query_benchmarks.md): documents how to find prior retained benchmark records before comparison and how to confirm that a new retained record landed in the canonical family.
- [benchmark_suite_registry.json](/core/control_plane/registries/benchmark_suite_registry.json): publishes the governed suite IDs, working directory, warmup and measured-run defaults, and the exact command set that the benchmark runner will execute.

## Workflow
1. Define the benchmark boundary.
   - Confirm whether the task is capturing a fresh baseline, comparing against a retained baseline, or checking a suspected regression after a code or artifact change.
   - Confirm that deliberate benchmarking is the right surface. If the task is about default operational timings, use the runtime telemetry guidance instead. If the task is about reducing test cost, route to test-suite optimization instead of treating benchmark evidence as a substitute.
   - If the canonical benchmark authority is unclear, resolve it with `watchtower-core query authority` before opening raw files or inventing a local measurement contract.
2. Load the governed benchmark contract.
   - Read the selected suite definition from the benchmark-suite registry and confirm the suite ID, command IDs, working directory, warmup rules, and measured-run defaults.
   - Confirm the fail-closed rules from the benchmark standard, especially fresh serialized subprocess execution, telemetry-on versus telemetry-off handling, median summary expectations, and retained-record portability boundaries.
   - If the task changes benchmark-suite or benchmark-runner behavior rather than only running an existing suite, identify the companion registry, schema, index, and command-doc surfaces that must stay aligned and merge the governed-artifact or documentation reconciliation workflows when needed.
3. Select the comparison baseline and execution plan.
   - Use `watchtower-core query benchmarks` to locate the prior retained benchmark record when comparison continuity matters.
   - Require exact suite-ID and command-ID parity before using a retained record as a valid comparison baseline.
   - Keep the registry defaults for warmup and measured runs unless the task explicitly needs an override and the resulting comparability tradeoff is acceptable.
   - Decide whether the run should produce transient JSON output only, an explicit output file, or a canonical retained benchmark record write.
4. Execute the governed benchmark run.
   - Run `watchtower-core benchmark run` from `core/python` with the selected suite, baseline, and output options.
   - Let the benchmark runner control telemetry modes and subprocess isolation instead of wrapping the commands in ad hoc shell timers or local profiling helpers.
   - Treat missing telemetry files, non-zero subprocess exits, suite mismatch, command mismatch, or schema-validation failures as hard benchmark failures rather than partial evidence.
5. Assess the benchmark evidence.
   - Review the per-command medians, telemetry-on versus telemetry-off deltas, ratios, top nested operations, and any failed or noisy command step.
   - Distinguish observed benchmark results from bounded inference about root cause, optimization priority, or release risk.
   - If the benchmark exposes likely code, suite, or contract drift, route that follow-up into the narrower implementation, review, validation, or governed-artifact workflows instead of hiding the issue inside benchmark prose.
6. Close out the benchmark task.
   - If the task intended to retain new benchmark evidence, confirm the record was written to the canonical retained family and query it back through the governed lookup surface.
   - Record the exact suite ID, baseline record ID when used, run overrides when used, materially significant deltas, and any environment caveats that limit comparability.
   - If the result is inconclusive because the suite changed, parity failed, or the environment moved materially, say so explicitly and do not present the run as a valid regression proof.

## Data Structure
- Benchmark objective and in-scope suite ID
- Execution contract, including working directory, warmup runs, measured runs, telemetry modes, and retained-record write intent
- Baseline linkage, including prior record ID or path, suite-ID parity status, and command-ID parity status
- Run evidence, including per-command medians, telemetry deltas, ratios, top nested operations, and any hard-failure state
- Interpretation boundary, including observed facts, bounded inference, and unresolved comparability caveats

## Outputs
- A governed benchmark run result in human or JSON form, plus any explicit output file requested by the task
- An optional retained benchmark record under the canonical benchmark-record family when the task requests durable evidence
- An explicit current-versus-baseline comparison result when valid baseline parity exists
- Follow-up implementation, validation, or reconciliation work when the benchmark reveals unresolved drift or regression risk

## Done When
- The in-scope benchmarking question has been answered with governed benchmark evidence or an explicit blocker.
- Any requested retained benchmark record has been written and re-queried, or the reason it was not written is explicit.
- The result distinguishes measured facts from interpretation and names any remaining parity or environment gap that still limits confidence.
