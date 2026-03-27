# WatchTower CTF Cold-Start Runbook

## Summary

This runbook is the first-ready-task start surface for a cold-start engineer. It exists because Phase 0 should not require a reader to reconstruct the exact read order, review questions, command proof, or outcome-recording path from several different support docs.

## Cold-Start Findings

- Before this runbook, the exact Phase 0 read order was split across `README.md`, live task state, `implementation_slice.md`, and `phase_output_manifest.md`.
- Before this runbook, the place to record a no-change conclusion versus a baseline delta was implicit rather than stated directly.
- Remaining material guesswork after this runbook: none. Only trigger-based later revisits in `conditional_revisit_queue.md` remain intentionally deferred.

## Read Order

1. Read `README.md` to map the initiative root and confirm the package boundary.
2. Read `.wt/tasks/phase_0_shared_contract_adoption_and_alignment/task.json` to lock the current task scope, governing docs, and done-when posture.
3. Read `implementation_slice.md`:
   - `Engineer Handoff Entry Order`
   - `phase.0` Shared Contract Adoption
4. Read `phase_output_manifest.md`:
   - `phase.0` Shared Contract Adoption And Alignment
5. Read `phase_closeout_checklists.md`:
   - `phase.0` Shared Contract Adoption And Alignment
6. Read `engineer_ambiguity_kill_sheet.md`, `conditional_revisit_queue.md`, and `contradiction_sweep_ledger.md` before changing any preserved baseline.
7. Reopen `decision_notes.md` only when a locked default, live delta, or deferred trigger is actually implicated.

## Questions To Answer

- Is the current-compatible identity still `pack_slug = offensivesecurity`, `pack_id = pack.offensivesecurity`, and `command_namespace = offsec`?
- Is the donor-versus-recipient split still the same: planning and preservation stay in this repo, while implementation starts later in `/home/j/WatchTower`?
- Do the canonical docs still agree on source-of-truth order and target-repo assumptions?
- Does coordination still point to the same first real next action and phase chain?
- Is any new live-contract delta required before `/home/j/WatchTower` mutation begins?
- Do `README.md`, this runbook, `phase_output_manifest.md`, and `phase_closeout_checklists.md` agree on the Phase 0 handoff posture?

## Command Anchors

- `cd /home/j/WatchTowerPlan/core/python`
- `uv run watchtower-core validate acceptance --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`
- `uv run watchtower-core plan query trace --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`
- `uv run watchtower-core plan query readiness --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`
- `uv run watchtower-core plan query coordination --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`

## Where To Record Outcomes

- If the baseline identity, authority order, or donor/recipient split is wrong, update `initiative_brief.md`, `design_record.md`, and `implementation_slice.md` in the same change set.
- If a locked default or live delta changes, update `decision_notes.md` and add or refresh the matching entry in `contradiction_sweep_ledger.md` or `conditional_revisit_queue.md` when applicable.
- If only the engineer start path was ambiguous, update `README.md`, this runbook, `phase_output_manifest.md`, and `phase_closeout_checklists.md` together.
- If machine acceptance or evidence drifted, update the acceptance contract, durable validation evidence, and initiative validation bundle together, then rerun `sync all`, `confirm-inputs`, and `approve`.
- If no baseline change is needed, leave canonical docs unchanged. The proof is that these surfaces still agree and the query or validation outputs still confirm the same current baseline.

## Done When

- The first-ready-task read order is explicit rather than inferred.
- The required Phase 0 questions can be answered without reopening the donor mirror by default.
- The place to record either a baseline delta or a no-change conclusion is explicit.
- Phase 1 can start without hidden baseline ambiguity.
