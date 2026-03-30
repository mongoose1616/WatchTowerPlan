# `core/control_plane/records/benchmarks`

## Description
`This directory holds committed durable benchmark records captured by the reusable-core benchmarking runtime. Use it for reviewable performance baselines and follow-up comparisons, not for transient telemetry JSONL output or ad hoc local profiling notes.`

## Notes
- Portable customer exports intentionally omit this retained-record family. A staged handoff bundle may therefore contain only `README.md` here.
- The canonical governing contract for these records is `core/docs/standards/engineering/performance_benchmarking_standard.md`.

## Files
| Path | Description |
|---|---|
| `core/control_plane/records/benchmarks/README.md` | Describes the purpose of the benchmark-record directory and its retained-history boundary. |
| `core/control_plane/records/benchmarks/benchmark_core_cli_representative_v1_20260329_baseline.json` | Baseline retained benchmark record for the governed reusable-core CLI representative suite captured on `2026-03-30T02:55:43Z`. |
