# Core Portability Follow-up Root Pack And Query Typing

## Summary
Cleans up copied-core portability debt in shared help, command docs, tests, and host query typing without changing WatchTowerPlan's current steady-state plan workspace contract.

## Identity
- `initiative_id`: `initiative.core_portability_followup_root_pack_and_query_typing`
- `trace_id`: `trace.core_portability_followup_root_pack_and_query_typing`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.core_portability_followup_root_pack_and_query_typing.bootstrap_core_portability_follow_up_root_pack_and_query_typing`: Bootstrap Core Portability Follow-up Root Pack And Query Typing live initiative package.

## Problem
- The copied-core assessment against `WatchTowerOversight` still identifies a small reusable-core portability tail even after the earlier copied-core hardening landed.
- The most actionable remaining shared-core issues are:
  - host help and command docs still use `packs/<slug>` examples as if that were the only supported hosted-pack topology
  - several shared-core tests still prove only the externalized `packs/<slug>` shape instead of the supported first-party root-pack shape
  - the host query handler layer is still red under `mypy` because payload render helpers accept `object` and then access typed attributes without typed boundaries
- At the same time, several assessment findings are not bugs in `WatchTowerPlan/core`; they are current repo facts such as the active `plan` pack, the current `watchtower-plan` shared workspace entry, and the live `watchtower-core plan ...` command family. This initiative must not destabilize those current contracts while cleaning up reusable-core portability debt.

## Desired Outcome
- Shared core documents and CLI help present first-party root packs such as `oversight/` as the default example shape for copied-core adoption.
- Shared-core tests prove root-pack support directly, while keeping one explicit externalized-pack path where the externalized topology is the subject under test.
- `mypy core/python/src/watchtower_host/cli/query_*.py` passes cleanly through explicit typed handler boundaries.
- The final change improves donor-core portability for copied-core consumers without changing the current `WatchTowerPlan` steady-state pack registry, command index, or workspace contract.

## In Scope
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/parser.py`
- `core/python/src/watchtower_host/cli/validate_family.py`
- `core/python/src/watchtower_host/cli/query_records_handlers.py`
- `core/python/src/watchtower_host/cli/query_knowledge_handlers.py`
- `core/python/src/watchtower_host/cli/query_discovery_handlers.py`
- core-owned command docs and authoring guidance that still hardcode `packs/oversight` as the only example topology
- shared-core tests and fixture helpers that should now default to first-party root-pack proof instead of only externalized-pack proof

## Out Of Scope
- Removing `plan` from `WatchTowerPlan` steady-state control-plane surfaces, docs, or shared workspace metadata
- Replacing the current `watchtower-plan` local workspace dependency in `core/python/pyproject.toml`
- Reworking the full shared-core test suite to remove every `watchtower_plan` import in this slice
- Any `WatchTowerOversight`-owned fixes outside the copied donor `core/`

## Operator Requirements
- Copied-core adopters must be able to read `watchtower-core` help and core-owned docs and see a supported root-pack example without inferring that `packs/<slug>` is mandatory.
- Shared-core validation and query commands must continue to work unchanged in `WatchTowerPlan`.
- Type-checking the touched host query handler files must pass without introducing casts that hide contract drift.

## Acceptance Criteria
- Root command help and hosted-pack family help no longer present `packs/oversight` as the only example pack root.
- The core-owned `pack` command docs and authoring reference describe first-party root packs explicitly and keep externalized packs as an allowed topology instead of the only one.
- Shared-core tests cover first-party root pack paths for scaffold/bootstrap or contract validation paths touched in this slice.
- `./core/python/.venv/bin/python -m mypy core/python/src/watchtower_host/cli/query_records_handlers.py core/python/src/watchtower_host/cli/query_knowledge_handlers.py core/python/src/watchtower_host/cli/query_discovery_handlers.py` passes.
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json` passes after the doc changes.

## Non Goals
- This initiative does not try to make `WatchTowerPlan/core` donor-neutral by removing all `plan` references. Current repo facts remain documented where they are materially true.
- This initiative does not change runtime pack discovery behavior that is already working from the earlier copied-core hardening tranche.
