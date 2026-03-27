# `watchtower_ctf_implementation_package_preservation`

## Start Here
| Need | Open |
|---|---|
| What this initiative is preserving and why it exists | `initiative_brief.md` |
| Why the package is split into mirror, canonical docs, and live task state | `design_record.md` |
| The engineer-facing phase plan, dependencies, and execution gates | `implementation_slice.md` |
| Locked defaults, live deltas, and explicit later revisits | `decision_notes.md`, `conditional_revisit_queue.md` |
| The quickest map of outputs, handoff aids, and phase closeout proof | `phase_output_manifest.md`, `phase_closeout_checklists.md` |
| Copy-ready starter docs and registry posture for `/home/j/WatchTower` | `starter_surface_blueprint.md`, `starter_registry_exemplars.md` |
| The first real runtime proof path | `vertical_slice_proof_spec.md` |
| Concrete example records, first machine surfaces, and per-phase test expectations | `artifact_specimens.md`, `machine_surface_specimen_index.md`, `phase_test_matrix.md` |
| Fast answers when an implementation choice feels ambiguous | `engineer_ambiguity_kill_sheet.md` |
| The closeout-to-knowledge promotion path | `promotion_extraction_map.md` |
| Resolved tensions and reconciled wording that engineers should not re-open casually | `contradiction_sweep_ledger.md` |
| Full frozen source provenance | `source_snapshot/CTF_implementation/`, `source_capture_notes.md`, `source_coverage_matrix.md` |
| Live machine state, current ready task, and initiative readiness | `.wt/`, `plan/.wt/indexes/coordination_index.json`, `plan/.wt/indexes/readiness_index.json` |

## Workspace Map
| Area | Role | Use It When |
|---|---|---|
| `initiative_brief.md`, `design_record.md`, `implementation_slice.md`, `decision_notes.md` | Canonical authored authority | You need the actual preserved implementation contract. |
| `phase_output_manifest.md` | Phase-by-phase output and evidence companion | You are preparing to start or close one phase. |
| `phase_closeout_checklists.md` | Short phase completion checks | You want a fast final pass before marking a phase done. |
| `starter_surface_blueprint.md`, `starter_registry_exemplars.md` | Copy-ready human-surface and registry starter kit | You are bootstrapping the first `offensive_security/` root in `/home/j/WatchTower`. |
| `vertical_slice_proof_spec.md` | Exact first real runtime proof | You are implementing or reviewing the first Phase 3 end-to-end slice. |
| `artifact_specimens.md`, `machine_surface_specimen_index.md`, `phase_test_matrix.md` | Example and validation kit | You need example records, first machine-surface expectations, or phase-specific proof obligations. |
| `engineer_ambiguity_kill_sheet.md`, `conditional_revisit_queue.md`, `contradiction_sweep_ledger.md` | Ambiguity control surfaces | You need to know what stays deferred, what is already reconciled, or what the default answer should be. |
| `promotion_extraction_map.md` | Knowledge-promotion execution companion | You are implementing or reviewing candidate extraction, review, or promotion behavior. |
| `source_snapshot/CTF_implementation/` | Immutable transformed mirror of the donor package | You need deeper donor narrative or exact original wording. |
| `source_original_inventory.txt`, `source_stored_inventory.txt`, `source_sha256.tsv`, `source_capture_notes.md`, `source_coverage_matrix.md` | Provenance and completeness proof | You need parity, restore, or coverage evidence. |
| `.wt/` | Initiative-local machine state | You are checking tasks, evidence bundles, or initiative state. |
| `plan.md`, `progress.md`, `summary.md` | Rendered initiative views | You want the current human-readable initiative status without reading machine JSON directly. |

## Notes
- This initiative is the engineer handoff package for the WatchTower offsec implementation, but it does not mutate `/home/j/WatchTower` by itself.
- Start with this `README.md`, then move to the four canonical docs. Use the support docs as execution aids, not as a second authority layer.
- The transformed mirror under `source_snapshot/CTF_implementation/` is frozen provenance. Update canonical docs or recapture explicitly; do not silently edit mirrored meaning in place.
- The real next engineer action is published by live task state, not by this `README.md`. Use `plan/.wt/indexes/coordination_index.json` and the ready Phase 0 task when checking current execution posture.
