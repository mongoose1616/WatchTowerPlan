# `watchtower_core.benchmarking`

## Summary
Reusable fail-closed benchmarking helpers for deliberate, repeatable shared-core performance measurement. This package owns governed suite loading, fresh subprocess execution, telemetry-on and telemetry-off timing, retained benchmark record generation, and benchmark query alignment.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `BenchmarkRunner`, `BenchmarkRunRequest`, and `BenchmarkRunResult`
- `Non-Goals`: This package does not own default-on runtime telemetry, ad hoc profiling helpers, remote metrics export, or pack-local benchmarking policy.

## Runtime Contract
- Benchmarking is deliberate and fail-closed rather than default-on and fail-open.
- Benchmark commands run in fresh serialized subprocesses from the governed working directory declared by the benchmark suite registry.
- Telemetry-on runs must emit exactly one JSONL file per measured subprocess so nested operation hotspots can be derived deterministically.
- Benchmark outputs validate against the governed benchmark-record schema before optional retained record writes.

## Related Surfaces
- `core/docs/standards/engineering/performance_benchmarking_standard.md`
- `core/control_plane/registries/benchmark_suite_registry.json`
- `core/control_plane/records/benchmarks/`
- `core/python/src/watchtower_core/telemetry/README.md`
