# Command Latency Baseline

## Summary
- Captured on `2026-03-22T19:07:45Z`.
- Each command was measured for `5` telemetry-on runs and `5` telemetry-off runs.
- Timing captures used `WATCHTOWER_TELEMETRY_STDERR=off` so console noise did not affect the measurements.
- The representative extra write path, `watchtower-core plan task create --write --format json`, was measured in an isolated temporary repo copy so the live `plan` workspace stayed clean.

## Stable Benchmark Set
- `watchtower-core doctor`
- `watchtower-core pack list --format json`
- `watchtower-core pack validate --pack plan --format json`
- `watchtower-core plan query coordination --format json`
- `watchtower-core plan sync coordination --write --format json`
- `watchtower-core plan task create --write --format json` in an isolated repo copy

## Command Medians
| Command | Telemetry Off Median (ms) | Telemetry On Median (ms) | Delta (ms) | Ratio |
| --- | ---: | ---: | ---: | ---: |
| `plan task create --write --format json` | `3036.407` | `3037.702` | `1.295` | `1.0004` |
| `plan query coordination --format json` | `1363.112` | `1379.610` | `16.498` | `1.0121` |
| `plan sync coordination --write --format json` | `1307.377` | `1329.894` | `22.517` | `1.0172` |
| `pack validate --pack plan --format json` | `1005.442` | `1003.199` | `-2.243` | `0.9978` |
| `doctor` | `497.233` | `500.166` | `2.933` | `1.0059` |
| `pack list --format json` | `467.623` | `432.497` | `-35.126` | `0.9249` |

## Findings
1. `watchtower-core plan task create --write --format json` is the dominant measured hotspot at about `3.04s`. The nested telemetry shows `plan_task_create` itself at a `2391 ms` median, followed by `sync_harness run_specs` at `499 ms`, then `initiative-index` at `103 ms`, `coordination-index` at `95 ms`, and `task-index` at `82 ms`.
2. `watchtower-core plan query coordination --format json` is the slowest read path at about `1.38s`. The current nested telemetry only exposes `parser_build` at `73 ms` and active-pack import/load at about `15 ms`, which means most of the remaining read-path cost sits inside plan-owned query or workspace loading that is not yet surfaced at a finer operation boundary.
3. `watchtower-core plan sync coordination --write --format json` is the next material write hotspot at about `1.33s`. The measured nested work is `sync_command` at `975 ms`, `sync_harness run_specs` at `827 ms`, `initiative-index` at `410 ms`, `coordination-index` at `110 ms`, and `task-index` at `82 ms`.
4. `watchtower-core pack validate --pack plan --format json` remains a real reusable-core hotspot at about `1.00s`. The dominant nested operation is `pack_contract_validation validate` at a `568 ms` median.
5. Host startup by itself is not the current first-order problem. The largest parser-build median visible in the benchmark set is `73 ms`, and the pack runtime import/load tail is only about `14-15 ms` on the plan commands sampled here.
6. Telemetry overhead is operationally negligible for this command set. The worst measured telemetry-on ratio in the baseline is `1.0172`, and the write-heavy `plan task create` path is effectively flat at `1.0004`.

## Ranked Hotspot Inventory
1. `reduce_plan_command_latency`
   Focus first on `plan task create`, `plan query coordination`, and `plan sync coordination`.
   The current evidence points to plan-owned orchestration and workspace/query state assembly rather than host startup.
2. `reduce_validation_and_pack_runtime_latency`
   Focus next on `pack validate --pack plan`.
   The measured hotspot is `pack_contract_validation validate`.
3. `reduce_host_and_loader_startup_latency`
   Keep this third unless deeper inspection of the plan read path shows hidden startup churn not exposed in the current telemetry.

## Notes
- The committed machine-readable companion for this baseline is `benchmark_baseline.json`.
- Raw telemetry JSONL files were generated during the measurement pass through a temporary override directory and intentionally were not committed because runtime telemetry is operational state, not a governed durable artifact family.
