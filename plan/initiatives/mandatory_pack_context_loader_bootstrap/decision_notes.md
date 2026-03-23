# Mandatory Pack Context Loader Bootstrap Decision Notes

## Summary
Locks the architecture decisions for making effective pack bootstrap a mandatory shared-core first phase.

## Decision Set
- Shared core will use one canonical loader-owned effective pack activation path rather than a new parallel context abstraction.
- The typed `PackContext` remains the reusable-core authority for pack-aware governed surfaces, but callers that only need runtime identity or runtime-manifest metadata should stop at loader activation instead of requiring the full context.
- Default-pack governed surface access without prior effective pack bootstrap is a bug.
- Pack-aware host commands should prefer the effective pack context over persisted registry defaults when the runtime view has already discovered a usable repo-local pack.
- Validation and runtime tests should patch import or module-resolution boundaries directly when pack-module reloads are part of the scenario; collection-time module identity is not a stable contract.
- This tranche may touch plan-owned tests and fixture helpers when they are the neighbor surfaces masking or reintroducing shared-core pack-context bugs.

## Explicit Deferrals
- No new third-party dependencies.
- No redesign of pack runtime descriptor shape beyond what is needed to consume the loader-owned pack context.
- No Oversight-owned repository changes in this donor-core tranche.
