# Plan Python Package Dependency Cleanup Design Record

## Summary
Make plan/python an installable workspace package and remove the last repo-local import shim from reusable core.

## Design Direction
- `watchtower_plan` remains the approved plan-owned boundary under `plan/python/src/watchtower_plan/`.
- `plan/python/` gains its own package metadata so the shared `core/python/` workspace can install it instead of discovering it through `sys.path` mutation.
- The shared environment contract stays centered on `core/python/.venv/`; `plan/python/` participates as an installed package, not as a second workspace with its own environment.

## Key Decisions
- Prefer a real editable local package dependency over any new bootstrap helper, wrapper module, or hidden path mutation.
- Keep `watchtower_core` fail-closed: reusable package roots should not own repository-specific path discovery for plan-domain code.
- Keep the dependency direction narrow. `watchtower_core` may consume the installed `watchtower_plan` package where repo-local orchestration is intentional, but the package boundary itself should not be hidden inside reusable core.

## Validation Strategy
- Prove `watchtower-core` CLI and validation entrypoints still work with the installed plan package.
- Re-run focused boundary, sync, validation, and endstate residue tests on the final tree.
- Run `watchtower-core validate all --format json` after the package-install wiring lands.
