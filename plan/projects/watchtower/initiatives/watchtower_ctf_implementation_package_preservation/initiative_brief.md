# WatchTower CTF Implementation Package Preservation

## Summary

This initiative absorbs `/home/j/mvp_reference/CTF_implementation` into the governed WatchTower planning workspace so the implementation package survives independently of that external directory. The preserved initiative includes a validator-safe transformed mirror of all `62` source files, parity manifests that prove nothing was dropped, and canonical initiative documents that capture the package purpose, baseline, design rationale, implementation sequencing, and locked decisions needed to build WatchTower.

## Identity

- `initiative_id`: `initiative.watchtower_ctf_implementation_package_preservation`
- `trace_id`: `trace.watchtower_ctf_implementation_package_preservation`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `source_root`: `/home/j/mvp_reference/CTF_implementation`
- `target_repo`: `/home/j/WatchTower`
- `transformed_mirror_root`: `source_snapshot/CTF_implementation/`

## Problem Statement

- The CTF planning package is implementation-ready, but it currently lives outside the governed WatchTower project initiative tree.
- Deleting `/home/j/mvp_reference/CTF_implementation` before transfer would remove implementation-critical planning detail, including phase sequencing, contract baselines, locked defaults, research anchors, and Step 1 coverage evidence.
- A raw copy of the package into the initiative root would introduce unmanaged `*.json` files that the plan validator would attempt to treat as governed initiative artifacts.

## Goals

- Preserve every implementation-supporting detail from the source package inside this initiative.
- Keep the preserved package recoverable and auditable through source inventory, digests, and reversible JSON restoration.
- Normalize the source package into repo-native initiative surfaces so follow-on implementation can begin from this initiative alone.
- Keep the initiative approval and readiness path compatible with the current `plan/.wt` validation contract.
- Turn the preserved package into an engineer-ready same-initiative handoff surface with explicit trace, evidence, task, and human-surface starter expectations.
- Publish concrete engineer-support surfaces that make initiative navigation, phase outputs, starter human surfaces, starter registries, example machine artifacts, the first runtime proof path, promotion flow, and trigger-based later decisions explicit before `/home/j/WatchTower` execution starts.

## Non-Goals

- Do not mutate `/home/j/WatchTower` during this preservation initiative.
- Do not alter repo-wide readiness rules, artifact validation behavior, or validator selection.
- Do not replace the transformed mirror with a reauthored summary; the source snapshot remains the frozen provenance layer.

## Governing Inputs And Authority Order

1. Current repo machine-readable authority in `plan/.wt/**` and `core/control_plane/**`
2. Current foundations, standards, and command docs under `core/docs/**` and `plan/docs/**`
3. The imported CTF planning package preserved under `source_snapshot/CTF_implementation/**`
4. Step 1 workbook source precedence retained by the package:
   - `STEP1_FINAL_v3.md`
   - `STEP1_FINAL_v2.md`
   - `STEP1_FINAL.md`
   - `STEP1.md`
   - `STEP1_PACK_SCAFFOLD_SPEC_v1.md` as the runnable scaffold and bootstrap baseline
5. Working donor-pack references at `/home/j/WatchTowerPlan/plan` and `/home/j/WatchTowerOversight/oversight` as implementation-pattern references, not higher authority

## Verified Current Baseline

| Concern | Locked Baseline |
|---|---|
| package purpose | planning-only bundle for the first WatchTower offensive-security / CTF hosted pack |
| pack root | `offensive_security` |
| workspace root | `offensive_security/` |
| pack slug | `offensivesecurity` |
| pack id | `pack.offensivesecurity` |
| command namespace | `offsec` |
| domain roots | `ctf`, `knowledge` |
| canonical challenge path | `offensive_security/ctf/<platform>/<event>/<challenge>/` with stable placeholders such as `unknown_platform` and `unknown_event` |
| live shared-core additions to adopt | `governance_surface_map`, `path_pattern_registry`, `status_registry`, and `actor_registry` |
| locked v1 deferral | `workflow_catalog` remains a post-v1 deferral rather than a baseline requirement |
| destination repo state as of `2026-03-26` | `/home/j/WatchTower` contains only `.git` metadata and is treated as empty |

## Source Package Scope And Inventory

The source package is preserved in full and accounted for through both the transformed mirror and support manifests.

| Source Family | File Count |
|---|---|
| `00_context` | `10` |
| `01_capability_map` | `3` |
| `02_phases` | `8` |
| `03_workflows` | `3` |
| `04_contracts` | `15` |
| `05_research` | `2` |
| `06_standards` | `4` |
| `07_guides` | `3` |
| `08_tracking` | `5` |
| `README.md` | `1` |
| `indexes` | `8` |

The package acceptance standard retained by this initiative requires:

- every required document to exist;
- every JSON file under the source `indexes/` family to parse cleanly;
- every workbook section `A-J`, every `Q01-Q70`, and every `R01-R90` to be mapped explicitly, with `R69-R72` recorded as absent from the source set;
- every non-`Q/R` Step 1 source range to be accounted for through the line-by-line audit and machine companion indexes; and
- all omissions, adaptations, supersessions, and deferrals to remain explicit.

## Engineer Handoff Starter Contract

The preserved package now carries the starter human-surface and authoring posture that engineers should use when `/home/j/WatchTower` implementation begins.

- The offsec machine-contract baseline must require pack-local `template_catalog`, `documentation_family_registry`, and `human_surface_policy_registry` surfaces before the pack is treated as documentation-complete.
- Required starter `README.md` roots are `offensive_security/`, `offensive_security/docs/`, `offensive_security/workflows/`, `offensive_security/docs/commands/core_python/`, `offensive_security/tracking/`, and `offensive_security/python/`.
- Required starter `AGENTS.md` roots are `offensive_security/`, `offensive_security/workflows/`, and `offensive_security/python/`.
- `offensive_security/docs/AGENTS.md` remains optional unless the docs subtree later needs local behavior that materially differs from the pack root rules.
- The carried-over root template posture is the current `plan` / `oversight` pattern:
  - `README.md` stays thin, navigational, and points readers to machine authority where applicable.
  - `AGENTS.md` stays narrow, local, and does not restate repository-wide rules.
- The carried-over pack-local best-practice posture is:
  - govern recurring surfaces through template and family registries instead of prose-only convention;
  - update docs plus indexes, registries, and rendered views in the same change set when one depends on the other;
  - keep rendered visibility surfaces named and registry-backed;
  - use evidence-first readiness and contradiction-sweep discipline for handoff claims;
  - reuse shared core before duplicating generic behavior into the pack; and
  - keep domain workflows, templates, terminology, and guidance pack-owned when they are not reusable-core concerns.

## Engineer Handoff Support Surfaces

The initiative now carries a larger support-doc set beside the four canonical authored docs. These files do not replace canonical authority or live task state, but they make a large preserved package substantially easier to navigate and execute.

- `README.md`: initiative-root navigation surface for the larger handoff package.
- `cold_start_runbook.md`: explicit first-ready-task read order, review questions, command anchors, and outcome-recording path for cold-start engineers.
- `phase_output_manifest.md`: per-phase outputs, command anchors, validation proof, and required evidence for the first WatchTower implementation pass.
- `phase_closeout_checklists.md`: short final-pass closeout checks for each preserved phase.
- `starter_surface_blueprint.md`: copy-ready README / AGENTS posture, required starter roots, and initial registry expectations derived from `plan` and `oversight`.
- `starter_registry_exemplars.md`: copy-ready machine-registry exemplars for the first offsec template, documentation-family, human-surface, rendered-surface, and authority-map artifacts.
- `vertical_slice_proof_spec.md`: the exact first Phase 3 runtime proof boundary, required surfaces, validation proof, and failure conditions.
- `artifact_specimens.md`: example-filled specimen records for the first challenge-local artifacts, `artifact_index`, and minimal authority/query-family registry artifacts.
- `phase_test_matrix.md`: a phase-to-validator, smoke-test, and proof-artifact matrix for the first implementation pass.
- `machine_surface_specimen_index.md`: the first expected `.wt/` and `.wt_local/` machine-surface inventory, with authority posture and specimen references.
- `engineer_ambiguity_kill_sheet.md`: a compact default-answer sheet for the most likely implementation ambiguities.
- `promotion_extraction_map.md`: the closeout-to-candidate-to-accepted knowledge flow for Phase 4 and Phase 5 work.
- `conditional_revisit_queue.md`: trigger-based later decisions that stay explicitly deferred unless execution evidence forces them back open.
- `contradiction_sweep_ledger.md`: resolved wording, contract, and state tensions that engineers should not reopen casually.

The reusable parts of this support kit are also promoted into durable plan guidance and initiative templates so future execution-facing initiatives can adopt the same cold-start posture by default rather than rebuilding it from initiative-local precedent.

## Durable Requirements

- `req.watchtower_ctf_package_preservation.001`: preserve all `62` source files inside this initiative with deterministic stored paths and reversible JSON restoration.
- `req.watchtower_ctf_package_preservation.002`: preserve source provenance through `source_original_inventory.txt`, `source_stored_inventory.txt`, `source_sha256.tsv`, and `source_coverage_matrix.md`.
- `req.watchtower_ctf_package_preservation.003`: capture the current-compatible baseline identity, authority order, live contract deltas, and donor/recipient split in canonical initiative docs.
- `req.watchtower_ctf_package_preservation.004`: preserve both human-readable source docs and machine-companion indexes so implementation does not depend on reopening the external source directory.
- `req.watchtower_ctf_package_preservation.005`: keep the preserved package validator-safe by storing mirrored JSON as `.raw` files rather than raw initiative-root `*.json` artifacts.
- `req.watchtower_ctf_package_preservation.006`: leave this initiative sufficient to bootstrap and implement WatchTower in `/home/j/WatchTower` after approval, without executing that implementation here.
- `req.watchtower_ctf_package_preservation.007`: publish a complete machine-readable handoff trace chain for this initiative through stable requirement IDs, acceptance IDs, one initiative-local validation bundle, and traceability joins.
- `req.watchtower_ctf_package_preservation.008`: replace the bootstrap-only placeholder task posture with a phase-aligned same-initiative execution task chain that exposes the real next engineer action and its dependencies.
- `req.watchtower_ctf_package_preservation.009`: carry the current `plan` / `oversight` README, AGENTS, template-governance, and same-change-set best-practice posture into the preserved offsec implementation contract.
- `req.watchtower_ctf_package_preservation.010`: publish a phase execution manifest that maps every preserved phase to concrete outputs, command anchors, validation proof, and closeout evidence for `/home/j/WatchTower` implementation.
- `req.watchtower_ctf_package_preservation.011`: publish a starter surface blueprint that turns the required offsec README / AGENTS roots and registry expectations into copy-ready execution guidance.
- `req.watchtower_ctf_package_preservation.012`: publish a conditional revisit queue so non-blocking future decisions remain explicit, defaulted, and trigger-based rather than becoming hidden ambiguity during implementation.
- `req.watchtower_ctf_package_preservation.013`: publish starter registry exemplars so the first offsec control registries can be authored from current `plan` / `oversight` patterns without reconstructing field shapes from donor precedent manually.
- `req.watchtower_ctf_package_preservation.014`: publish a first vertical-slice proof spec so Phase 3 has one exact minimum end-to-end runtime proof instead of a vague "runtime works" claim.
- `req.watchtower_ctf_package_preservation.015`: publish per-phase closeout checklists so engineers can confirm completion and evidence expectations quickly before task closeout.
- `req.watchtower_ctf_package_preservation.016`: publish a contradiction-sweep ledger so already reconciled tensions stay explicit and do not drift back into implementation ambiguity.
- `req.watchtower_ctf_package_preservation.017`: publish an initiative-root `README.md` so this larger preserved initiative has a stable human navigation surface instead of forcing readers to infer structure from the file tree alone.
- `req.watchtower_ctf_package_preservation.018`: publish example-filled artifact specimens for the first governed challenge-local records plus minimal authority-map and query-family registry specimens.
- `req.watchtower_ctf_package_preservation.019`: publish a phase-to-test matrix so every phase has explicit validators, smoke proofs, and required proof artifacts.
- `req.watchtower_ctf_package_preservation.020`: publish a machine-surface specimen index so engineers can see the first expected `.wt/` and `.wt_local/` surfaces, their authority class, and their first owning phase in one place.
- `req.watchtower_ctf_package_preservation.021`: publish an engineer ambiguity kill sheet so the most likely implementation questions already have default answers before `/home/j/WatchTower` mutation starts.
- `req.watchtower_ctf_package_preservation.022`: publish a promotion and extraction map so Phase 5 knowledge work has an explicit path from closeout outputs to candidate and accepted reusable knowledge.
- `req.watchtower_ctf_package_preservation.023`: publish a cold-start runbook so the first ready task has an explicit read order, review question set, command proof path, and outcome-recording path.
- `req.watchtower_ctf_package_preservation.024`: promote the reusable engineer-handoff support pattern into plan-level standard, pattern, and initiative templates so future initiatives can adopt the same core support kit by default.

## Acceptance Criteria

- `ac.watchtower_ctf_package_preservation.001`: the initiative mirror contains exactly `62` stored files corresponding to the `62` source files.
- `ac.watchtower_ctf_package_preservation.002`: the transformed mirror preserves source bytes exactly, as proven by `source_sha256.tsv` and restore proof for mirrored JSON files.
- `ac.watchtower_ctf_package_preservation.003`: every source file appears in `source_coverage_matrix.md` with a canonical target and explicit status.
- `ac.watchtower_ctf_package_preservation.004`: the canonical initiative docs absorb the package purpose, baseline, phase plan, exact workflow metadata rules, implementation-critical query/state/safety/citation rules, and the full locked decision register, with explicit reconciliation notes where preserved source surfaces use conflicting schema shorthand, while any remaining donor-package narrative detail is explicitly preserved as mirrored reference.
- `ac.watchtower_ctf_package_preservation.005`: after sync, confirm-inputs, and approval, the initiative reaches `ready_for_execution=true`.
- `ac.watchtower_ctf_package_preservation.006`: the traceability layer, initiative-local validation bundle, and validator references agree on this initiative’s requirement IDs, acceptance IDs, evidence IDs, and applicable validators without relying on retained shared-core acceptance artifacts.
- `ac.watchtower_ctf_package_preservation.007`: the active same-initiative task graph exposes one explicit phase-aligned execution chain with the first executable task `ready`, later tasks `planned`, and explicit dependencies, related IDs, and governing docs for every task.
- `ac.watchtower_ctf_package_preservation.008`: the canonical docs restate the required offsec README / AGENTS starter roots plus the adapted template-governance and best-practice posture needed to bootstrap the pack without inheriting ambiguity from the donor repositories.
- `ac.watchtower_ctf_package_preservation.009`: `phase_output_manifest.md` covers every preserved phase with primary outputs, current command anchors, validation proof, evidence capture, and ready-to-close signals.
- `ac.watchtower_ctf_package_preservation.010`: `starter_surface_blueprint.md` covers every required README / AGENTS starter root, the donor template posture, and the minimum registry baseline that should govern those human surfaces.
- `ac.watchtower_ctf_package_preservation.011`: `conditional_revisit_queue.md` lists each remaining non-blocking conditional decision with its current default, reopen trigger, owning phase, and keep-default behavior when the trigger does not fire.
- `ac.watchtower_ctf_package_preservation.012`: `starter_registry_exemplars.md` provides copy-ready exemplar entries for the first offsec `template_catalog`, `documentation_family_registry`, `human_surface_policy_registry`, `rendered_surface_registry`, and `authority_map`.
- `ac.watchtower_ctf_package_preservation.013`: `vertical_slice_proof_spec.md` defines the exact first real runtime proof path, required machine surfaces, validation proof, evidence capture, and explicit failure conditions for Phase 3.
- `ac.watchtower_ctf_package_preservation.014`: `phase_closeout_checklists.md` gives each preserved phase a concise closeout checklist that aligns with the task graph and phase output manifest.
- `ac.watchtower_ctf_package_preservation.015`: `contradiction_sweep_ledger.md` records the major resolved tensions across source mirror, canonical docs, and live task state with their current governing surfaces.
- `ac.watchtower_ctf_package_preservation.016`: the initiative root `README.md` provides a stable navigation surface for the larger preserved package and routes engineers to the canonical docs, support docs, provenance surfaces, and live machine state.
- `ac.watchtower_ctf_package_preservation.017`: `artifact_specimens.md` provides example-filled specimens for the first governed challenge-local records, `artifact_index`, and minimal authority/query-family registry surfaces.
- `ac.watchtower_ctf_package_preservation.018`: `phase_test_matrix.md` maps every preserved phase to explicit validators, smoke tests, and proof artifacts.
- `ac.watchtower_ctf_package_preservation.019`: `machine_surface_specimen_index.md` lists the first expected `.wt/` and `.wt_local/` surfaces with authority class, first owning phase, and specimen or contract anchors.
- `ac.watchtower_ctf_package_preservation.020`: `engineer_ambiguity_kill_sheet.md` gives compact default answers for the most likely implementation ambiguities and escalation conditions.
- `ac.watchtower_ctf_package_preservation.021`: `promotion_extraction_map.md` maps closeout outputs to extraction candidates, review gates, and accepted reusable knowledge targets with mandatory provenance.
- `ac.watchtower_ctf_package_preservation.022`: `cold_start_runbook.md` makes the first-ready-task read order, review questions, command anchors, and outcome-recording path explicit, and records any remaining cold-start guesswork.
- `ac.watchtower_ctf_package_preservation.023`: the reusable handoff-support posture is promoted into a durable plan standard, a reusable pattern, and initiative template-catalog entries plus templates for `README.md`, `phase_output_manifest.md`, `phase_closeout_checklists.md`, and `cold_start_runbook.md`.

## Risks And Dependencies

Primary dependencies preserved from the source package:

- current shared pack commands for `pack export`, `pack scaffold`, `pack bootstrap`, `pack validate`, and release proof;
- current shared governance surfaces for pack context, status vocabulary, actor vocabulary, and path rules;
- donor-pack implementation patterns from `plan` and `oversight`;
- research anchors from ATT&CK, OWASP WSTG, NIST guidance, and Diataxis, always subordinate to current repo truth.

Primary risks carried forward from the package:

- slug normalization drift could invalidate the current-compatible scaffold identity;
- Step 1 workbook assumptions can drift from live shared-core truth;
- workflow starter metadata could remain in place too long after scaffold;
- markdown docs and structured indexes can diverge if not synchronized in one change set;
- environment and safety behavior can be implemented unsafely if the Phase 6 contract is treated as optional.

## Execution Task Chain

- `task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment`: lock the live shared-contract baseline, donor/recipient split, and current-compatible identity before target-repo implementation starts.
- `task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap`: export, scaffold, bootstrap, and validate the first real `offensive_security/` root in `/home/j/WatchTower`.
- `task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract`: author the offsec schemas, registries, policies, and validation suite baseline.
- `task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam`: implement the runtime, query, sync, workflow, and rendered-view seam.
- `task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout`: implement challenge-local artifacts, evidence, discrepancy, and closeout behavior.
- `task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval`: implement knowledge families, promotion policy, and deterministic retrieval.
- `task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety`: implement environment adapters, transfer governance, and the safety confirmation matrix.
- `task.watchtower_ctf_implementation_package_preservation.phase_7_release_and_portability_proof`: prove staged export, bootstrap, validation, and release portability for the finished pack.
