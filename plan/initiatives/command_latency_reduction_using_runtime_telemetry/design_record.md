# Command Latency Reduction Using Runtime Telemetry Design Record

## Summary
Uses the new local runtime telemetry to profile, prioritize, and reduce command latency across host, reusable core, and pack-owned paths.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/command_latency_reduction_using_runtime_telemetry/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Recommended Design
- Use one evidence loop for every performance slice:
  1. collect runtime telemetry and a stable benchmark baseline
  2. identify the slowest operation kinds and command paths
  3. reduce one bounded hotspot family
  4. rerun the same benchmark set
  5. either keep the change with evidence or reject it
- Organize the work by runtime seam rather than by file count:
  - host startup and selected-pack loading
  - reusable-core loaders, validators, and sync or query services
  - pack-owned `plan` orchestration and derived-surface rebuilds
- Avoid mixing large semantic refactors with performance work unless the telemetry proves the larger change is necessary.

## Benchmark Set
- Baseline commands should include:
  - `watchtower-core doctor`
  - `watchtower-core pack list --format json`
  - `watchtower-core pack validate --pack plan --format json`
  - `watchtower-core plan sync coordination --write --format json`
  - one representative plan read path
  - one representative plan write path beyond pure sync when useful
- Each command should be measured with 5-run medians and supporting per-run telemetry JSONL evidence.

## Hotspot Families
- Host and loader startup
  - parser build
  - argv parse
  - selected-pack discovery and activation
  - pack settings and manifest loading
- Reusable-core execution
  - schema and validator reuse
  - sync harness shared-state buildup
  - validation-suite and pack-contract work
  - query or rendered-surface loading paths
- Pack-owned orchestration
  - plan coordination refresh
  - task mutation write paths
  - closeout and tracker rebuild flows
  - workspace aggregation or snapshot loading

## Design Constraints
- Use telemetry to reduce latency, not to justify hidden caches with unclear invalidation rules.
- Prefer explicit cache reuse only when the invalidation boundary is obvious and testable.
- Keep optimization local to the hotspot. Do not spread global mutable state or hidden singletons just to shave small amounts of time.
- Preserve deterministic write behavior for sync, validation, and closeout flows.

## Expected Deliverables
- One documented baseline benchmark set.
- One hotspot inventory ranked by measured impact.
- One or more bounded optimization slices with benchmark deltas.
- Targeted regression tests or benchmark guards for the highest-value paths.
- One closeout summary describing what improved, what did not, and what remains worth doing.
