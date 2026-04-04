# `watchtower_core.telemetry`

## Summary
Local, fail-open runtime telemetry for `watchtower-core` command execution. This package owns per-invocation JSONL sink creation, nested operation timing, and concise stderr summaries without changing stdout command contracts.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `create_telemetry_session`, `telemetry_operation`, `add_operation_attributes`, `TelemetryConfig`, `resolve_telemetry_root`, `TelemetryCleanupService`, and `TelemetryDeleteRequest`
- `Non-Goals`: OpenTelemetry exporters, remote collectors, W3C trace propagation, metrics backends, deliberate benchmark methodology, or durable governed benchmark storage.

## Runtime Contract
- Telemetry is default-on and local only.
- Set `WATCHTOWER_TELEMETRY=off` to disable all runtime telemetry.
- Set `WATCHTOWER_TELEMETRY_STDERR=off` to keep JSONL output but suppress the one-line stderr summary.
- Set `WATCHTOWER_TELEMETRY_DIR=<path>` to override the sink directory.
- Default sink location is `<machine_root>/runtime/telemetry/<yyyy>/<mm>/<dd>/`.
- Use `watchtower-core telemetry delete` for dry-run-first cleanup instead of ad hoc filesystem deletion.
- Runtime telemetry is operational machine state, not a governed durable artifact family.
- Deliberate retained benchmark evidence belongs to `watchtower_core.benchmarking`, not to this package.

## Related Surfaces
- `core/docs/standards/engineering/runtime_telemetry_standard.md`
- `core/python/src/watchtower_host/README.md`
