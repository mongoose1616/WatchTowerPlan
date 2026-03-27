# WatchTower CTF Engineer Ambiguity Kill Sheet

## Summary

This support surface answers the most likely implementation ambiguities quickly. Use it when an engineer is tempted to improvise because the package feels broad.

## Default Answers

| Ambiguity | Default Action | Escalate Or Reopen Only If |
|---|---|---|
| Which surface is authoritative? | Use the four canonical docs plus live task state first, then the mirror for deeper source detail. | A canonical doc is missing a required implementation fact or a new live-contract delta must be recorded. |
| Should I reopen the donor mirror before writing code? | Reopen `04_contracts/` and `03_workflows/` only for deeper field-level or workflow-level detail. | Canonical docs and support docs still leave a specific behavior ambiguous. |
| Can I change the slug, pack id, or namespace because underscore-safe names seem nicer? | No. Keep `pack_slug = offensivesecurity`, `pack_id = pack.offensivesecurity`, and `command_namespace = offsec`. | Upstream slug handling changes and a new live-contract delta is recorded. |
| Should missing `platform` or `event` path segments collapse away? | No. Keep placeholder segments such as `unknown_platform` and `unknown_event` in v1. | Real intake evidence proves placeholder segments cause unacceptable churn and the revisit trigger is met. |
| Do I invent pack-local behavior when shared core already has something close? | No. Reuse shared core first and make pack-local code prove that the behavior is genuinely offsec-specific. | The shared surface cannot express the needed domain behavior without distortion. |
| What counts as the first real runtime proof? | The exact boundary in `vertical_slice_proof_spec.md`, not a looser “runtime seems to work” claim. | A deliberate live-contract delta changes the proof boundary. |
| Can a phase close based on prose confidence alone? | No. Use `phase_output_manifest.md`, `phase_test_matrix.md`, and `phase_closeout_checklists.md`. | A missing test or artifact is itself the blocker to closeout. |
| When do I reopen a deferred decision? | Only when the trigger in `conditional_revisit_queue.md` actually fires. | The trigger is real and implementation evidence shows the current default is no longer workable. |
| What do I do if source wording and canonical wording conflict? | Follow canonical docs plus `decision_notes.md` and `contradiction_sweep_ledger.md`. | The conflict reveals a genuinely new mismatch that needs a live-contract delta. |
| Should candidate knowledge appear in default retrieval? | No. Accepted knowledge is the default retrieval posture. | The operator explicitly asks for candidate or draft material. |
| Can closeout pass while a discrepancy carries `no_closeout`? | No. | The discrepancy is resolved or an allowed exception path is explicitly governed. |

## Fast Escalation Rules

- If the question is about phase order or closeout proof, do not improvise. Use the phase chain as written.
- If the question is about field names or cardinality, use the preserved field-level contracts before inventing a wrapper.
- If the question is about human-surface or registry shape, start from `starter_surface_blueprint.md` and `starter_registry_exemplars.md`.
- If the question is about knowledge promotion, start from `promotion_extraction_map.md` and the Phase 5 section of `implementation_slice.md`.
