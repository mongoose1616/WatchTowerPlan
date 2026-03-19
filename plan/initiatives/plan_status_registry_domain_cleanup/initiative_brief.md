# Plan Status Registry Domain Cleanup

## Summary
Removes legacy challenge-specific status leakage from the shared status registry and reconciles the authoritative requirements notes to the current pack-facing interface state.

## Scope
- Clean the shared `core/control_plane/registries/status_registry.json` surface so it no longer hard-codes `challenge` families or solution-centric terminal values.
- Keep the vocabulary generic for pack-facing reuse instead of introducing plan-only status names into the shared registry.
- Reconcile `requirements.md` so the status-registry row and adjacent pack-facing interface notes match the implemented artifact-index and status surfaces.

## Identity
- `initiative_id`: `initiative.plan_status_registry_domain_cleanup`
- `trace_id`: `trace.plan_status_registry_domain_cleanup`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_status_registry_domain_cleanup.generalize_shared_status_vocabulary`: Replace the legacy challenge-scoped blocked and terminal status entries with plan-domain-neutral status vocabulary.
- `task.plan_status_registry_domain_cleanup.add_focused_status_registry_coverage`: Lock the cleaned status-registry shape through targeted pack-context or loader coverage.
- `task.plan_status_registry_domain_cleanup.reconcile_requirements_notes`: Update requirements.md so the status-registry and artifact-index leakage notes reflect the current implemented state.
