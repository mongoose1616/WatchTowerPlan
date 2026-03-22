# Runtime Telemetry And Command Observability Foundation Decision Notes

## Summary
Locks the initial runtime telemetry shape so implementation can proceed without re-opening the core design boundary during execution.

## Locked Decisions
1. Local backend only in this tranche.
- Use only standard-library facilities for timing, JSONL writing, IDs, stderr output, and environment configuration.
- Defer OTEL transport/export, W3C propagation, metrics, and remote collectors.

2. Default-on enablement.
- Telemetry is enabled by default for normal commands.
- Operators disable telemetry only with `WATCHTOWER_TELEMETRY=off`.

3. Environment variables instead of global CLI flags.
- Use `WATCHTOWER_TELEMETRY`, `WATCHTOWER_TELEMETRY_STDERR`, and `WATCHTOWER_TELEMETRY_DIR`.
- Do not add root parser flags such as `--telemetry` or `--no-telemetry` in this tranche.

4. Pack-machine-root sink.
- Default sink root is `<machine_root>/runtime/telemetry/`.
- The current proof-pack path is `plan/.wt/runtime/telemetry/`.
- Runtime telemetry is operational machine state, not a governed durable artifact family.

5. Fail-open behavior.
- Telemetry initialization or write failures must disable telemetry for the current run rather than failing the command.
- Telemetry code must not change command exit codes or stdout payload contracts.

6. Separate runtime telemetry identity from planning identity.
- Runtime telemetry uses `telemetry_run_id`, `operation_id`, and `parent_operation_id`.
- Planning `trace_id`, initiative slug, task id, and related pack metadata are optional context attributes only.

7. Structured stderr summaries only.
- Emit one concise run summary to stderr per top-level command when stderr telemetry is enabled.
- Keep detailed telemetry records in JSONL only.

## Deferred Decisions
- OTEL mapping strategy for the local event model.
- Whether to add durable promoted telemetry guidance after the runtime layer proves useful.
- Whether future packs should expose pack-local telemetry retention controls in their manifests or registries.
