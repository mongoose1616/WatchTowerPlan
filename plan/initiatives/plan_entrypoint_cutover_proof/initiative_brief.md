# Plan Entrypoint Cutover Proof

## Summary
Proves the pack-wide capture-first flow for the plan authority cutover.

## Identity
- `initiative_id`: `initiative.plan_entrypoint_cutover_proof`
- `trace_id`: `trace.plan_entrypoint_cutover_proof`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_entrypoint_cutover_proof.publish_plan_authority_entrypoints`: Capture the pack-wide start-here surfaces for the new live plan authority.
- `task.plan_entrypoint_cutover_proof.validate_packwide_proof_package`: Prove the pack-wide initiative can reach ready_for_execution cleanly.

## Bounded Slice
- Add the missing human entrypoint surfaces under `plan/` that the requirements call out directly: `plan/AGENTS.md` and `plan/workflows/README.md` plus `plan/workflows/AGENTS.md`.
- Refresh `plan/README.md` so it routes humans to `plan_overview.md`, scope roots, and the new plan-domain workflow entrypoint.
- Refresh the thin root-facing router docs only where needed so they point humans at `plan/**` for live planning authority while the canonical routing table remains at the repo root during this migration step.
- Do not attempt the full workflow-root split in this slice; `workflows/ROUTING_TABLE.md` and the existing workflow modules remain the operative routing backend until a later migration tranche lands.
