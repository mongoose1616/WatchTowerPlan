# Command Latency Closeout Benchmark

## Summary
- Captured on `2026-03-22T20:06:47Z` after the final correctness fix and the full optimization tranche.
- The benchmark set was rerun with `5` telemetry-on and `5` telemetry-off samples per command, with `WATCHTOWER_TELEMETRY_STDERR=off` so console summaries did not affect timing.
- The isolated `plan task create --write --format json` path was measured in temporary repo copies so the live `plan` workspace remained clean.

## Final Command Delta Against Baseline
| Command | Baseline Telemetry-On Median (ms) | Final Telemetry-On Median (ms) | Improvement (ms) | Improvement (%) |
| --- | ---: | ---: | ---: | ---: |
| `doctor` | `500.166` | `467.242` | `32.924` | `6.58` |
| `pack list --format json` | `432.497` | `426.752` | `5.745` | `1.33` |
| `pack validate --pack plan --format json` | `1003.199` | `793.701` | `209.498` | `20.88` |
| `plan query coordination --format json` | `1379.610` | `585.425` | `794.185` | `57.57` |
| `plan sync coordination --write --format json` | `1329.894` | `1237.850` | `92.044` | `6.92` |
| `plan task create --write --format json` | `3037.702` | `3000.961` | `36.741` | `1.21` |

## Final Telemetry-Off Medians
| Command | Baseline Telemetry-Off Median (ms) | Final Telemetry-Off Median (ms) | Improvement (ms) | Improvement (%) |
| --- | ---: | ---: | ---: | ---: |
| `doctor` | `497.233` | `466.499` | `30.734` | `6.18` |
| `pack list --format json` | `467.623` | `416.592` | `51.031` | `10.91` |
| `pack validate --pack plan --format json` | `1005.442` | `770.457` | `234.985` | `23.37` |
| `plan query coordination --format json` | `1363.112` | `590.099` | `773.013` | `56.71` |
| `plan sync coordination --write --format json` | `1307.377` | `1195.601` | `111.776` | `8.55` |
| `plan task create --write --format json` | `3036.407` | `2964.078` | `72.329` | `2.38` |

## Interpretation
- The dominant gains held where the baseline identified the real pain: plan query, plan task writes, and pack validation.
- The host and loader startup tranche still delivered measurable reductions, especially on raw startup-sensitive commands such as `doctor` and `pack list`.
- The final tree preserved the original stdout and exit-code contracts while reducing both reusable-core and plan-owned latency.
- The post-benchmark correctness fixes refreshed pack-loader state after write operations and restored the missing aggregate follow-up indexes for task writes. That narrowed the task-write gain substantially, but the final accepted tree still remained slightly better than baseline while removing stale discrepancy reads and closeout drift.

## Additional Signals
- Importing `watchtower_host.cli.main` dropped from about `115.858 ms` to `99.081 ms`.
- The final `watchtower-core validate all --skip-acceptance --format json` gate passed on the live repo, and the telemetry run recorded about `9856 ms` end-to-end.

## Notes
- The machine-readable companion for this note is `benchmark_closeout.json`.
- This closeout benchmark supersedes the intermediate per-task benchmark notes as the final accepted measurement set for the initiative.
