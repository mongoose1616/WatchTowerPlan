# Command Latency Reduction Using Runtime Telemetry Decision Notes

## Summary
Locks the execution decisions for the telemetry-driven latency-reduction tranche.

## Locked Decisions
- Use the existing local runtime telemetry as the first profiling source. Do not start with speculative refactors.
- Optimize operator-visible command latency first, not test-suite runtime as an independent goal.
- Keep the command benchmark set stable through the initiative so before-versus-after comparisons stay meaningful.
- Favor bounded fixes at public service seams over large cross-boundary rewrites.
- Keep stdout payload contracts, exit codes, and pack-boundary behavior stable while optimizing.
- Treat telemetry-on performance as the primary user experience target; telemetry-off comparison is supporting evidence, not the goal state.
- Preserve host versus reusable-core versus pack-owned ownership boundaries even when an optimization crosses those seams.

## Ranking Rules
- Highest priority goes to commands that are both slow and frequently used by operators.
- Next priority goes to commands whose hot paths are shared by many other commands.
- Lower priority goes to one-off or rare commands unless they block normal plan execution workflows.

## Deferral Rules
- If telemetry shows a hotspot is real but the required fix would be a large architecture change, capture it as an explicit deferred item rather than forcing it into this tranche.
- If a perceived hotspot cannot be reproduced in the benchmark set, do not optimize it in this initiative without new evidence.

## Evidence Rules
- Every substantive optimization slice must capture:
  - baseline timings
  - final timings
  - the specific hotspot or operation names reduced
  - any regression risk or residual long-tail cost
