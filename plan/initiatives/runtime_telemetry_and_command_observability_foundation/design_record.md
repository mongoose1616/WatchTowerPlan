# Runtime Telemetry And Command Observability Foundation Design Record

## Summary
Adds default-on local runtime telemetry, timing, and error tracing across host, reusable-core, and plan command paths without adopting OTEL yet.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/runtime_telemetry_and_command_observability_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Recommended Design
- Add a new reusable-core package `watchtower_core.telemetry` that owns configuration resolution, runtime run context, nested operation tracking, JSONL sink emission, stderr summary emission, and global fail-open disablement for one invocation.
- Start telemetry from the host CLI entrypoint so every normal command run is wrapped in one telemetry run.
- Pass the active telemetry session through explicit lightweight runtime context objects and helper functions rather than thread-local magic.
- Instrument only public service boundaries and orchestration seams:
  - host main parse and dispatch
  - shared CLI result emitters
  - sync harness run and per-target execution
  - validation entrypoints and pack-contract evaluation
  - pack integration import and runtime resolution
  - plan sync, initiative lifecycle, and task lifecycle orchestration
- Keep telemetry data model deliberately small:
  - `run_started`
  - `operation_result`
  - `run_finished`

## Event Model
- `run_started` fields:
  - `record_type`
  - `telemetry_run_id`
  - `command`
  - `argv`
  - `started_at`
  - `telemetry_path`
  - `pack_id` when known
- `operation_result` fields:
  - `record_type`
  - `telemetry_run_id`
  - `operation_id`
  - `parent_operation_id`
  - `operation_kind`
  - `operation_name`
  - `status`
  - `started_at`
  - `finished_at`
  - `duration_ms`
  - optional `attributes`
  - optional `error_type`
  - optional `error_message`
- `run_finished` fields:
  - `record_type`
  - `telemetry_run_id`
  - `command`
  - `status`
  - `started_at`
  - `finished_at`
  - `duration_ms`
  - `operation_count`
  - optional top-level `error_type`
  - optional top-level `error_message`

## Sink Resolution
- Resolve the sink directory in this order:
  1. `WATCHTOWER_TELEMETRY=off` disables telemetry entirely.
  2. `WATCHTOWER_TELEMETRY_DIR` overrides the sink root.
  3. Otherwise resolve active pack settings and use `<machine_root>/runtime/telemetry/<yyyy>/<mm>/<dd>/`.
- Use one JSONL file per invocation with a timestamped filename that includes PID and short run identifier.
- Create parent directories lazily.
- Add `**/.wt/runtime/` to the root `.gitignore`.

## Failure Handling
- Any failure creating the sink, serializing records, or writing the JSONL stream disables telemetry for the rest of that invocation.
- Command execution continues normally after the disablement path.
- Telemetry should not recursively instrument its own failures.

## Instrumentation Seams
- `watchtower_host.cli.main`: create the run context, wrap parse/dispatch/help/error paths, and emit the final stderr summary.
- `watchtower_core.cli.handler_common`: attach command metadata and operation boundaries without changing stdout behavior.
- `watchtower_core.sync.harness`: wrap aggregate run plus each target execution.
- `watchtower_core.validation.*`: wrap public validation entrypoints, suite execution, and contract evaluation.
- `watchtower_core.pack_integration.runtime`: wrap integration import and runtime resolution.
- `watchtower_plan.cli.*` and plan services: wrap read and write orchestration, not every low-level helper.

## Documentation And Contract Updates
- Add one new engineering standard for runtime telemetry.
- Update `engineering_stack_direction.md` so local runtime telemetry is now an active baseline while OTEL remains a reference-only future option.
- Update pack authoring guidance so copied or newly bootstrapped packs inherit the same runtime sink contract.
- Refresh affected READMEs and only the command docs that need to mention the cross-cutting stderr and runtime-sink behavior.

## Non-Goals
- No wire-format standardization beyond local JSONL records.
- No remote collection or telemetry query interface in this tranche.
- No cross-process propagation or external tracing headers.
