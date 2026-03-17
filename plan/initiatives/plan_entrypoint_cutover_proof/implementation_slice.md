# Plan Entrypoint Cutover Proof Implementation Slice

## Summary
Proves the pack-wide capture-first flow for the plan authority cutover.

## Initial Work Breakdown
- `task.plan_entrypoint_cutover_proof.publish_plan_authority_entrypoints`
  - Add `plan/AGENTS.md`.
  - Add `plan/workflows/README.md` and `plan/workflows/AGENTS.md`.
  - Refresh `plan/README.md`, root `README.md`, and any adjacent workflow-orientation docs needed to route humans to the new `plan/**` authority entrypoints.
- `task.plan_entrypoint_cutover_proof.validate_packwide_proof_package`
  - Confirm the edited authored inputs into machine state.
  - Rebuild rendered plan surfaces and indexes after the entrypoint updates land.
  - Validate that the pack-wide initiative remains machine-valid with no stale rendered or aggregate surfaces.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
