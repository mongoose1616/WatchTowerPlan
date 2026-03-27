# WatchTower CTF Phase Output Manifest

## Summary

This support surface translates the preserved phase plan into bounded engineer outputs. It does not replace `implementation_slice.md` or the live task graph. Use it as the execution companion when an engineer is starting, reviewing, or closing one preserved phase.

## How To Use This Manifest

1. Read `README.md`, `initiative_brief.md`, `design_record.md`, `decision_notes.md`, and `implementation_slice.md` first.
2. Open the matching live task record under `.wt/tasks/**/task.json`.
3. Use this manifest to confirm primary outputs, command anchors, validation proof, and closeout evidence before changing `/home/j/WatchTower`.
4. Use `phase_closeout_checklists.md` as the last short pass before calling a phase done.
5. Use `phase_test_matrix.md` when deciding which validators, smoke tests, and proof artifacts must exist for the current phase.
6. Update this file in the same change set whenever a phase output, validation expectation, or evidence requirement changes materially.

## `phase.0` Shared Contract Adoption And Alignment

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment`
- Primary outputs:
  - revalidated baseline identity, donor or recipient split, and current-compatible delta set in the canonical docs;
  - no unresolved ambiguity in read-first order, target-repo assumptions, or source-of-truth precedence; and
  - current support docs `README.md`, `phase_output_manifest.md`, `phase_closeout_checklists.md`, `starter_surface_blueprint.md`, `conditional_revisit_queue.md`, and `contradiction_sweep_ledger.md`.
- Current command and query anchors:
  - `cd /home/j/WatchTowerPlan/core/python`
  - `uv run watchtower-core validate acceptance --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`
  - `uv run watchtower-core plan query trace --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`
  - `uv run watchtower-core plan query coordination --trace-id trace.watchtower_ctf_implementation_package_preservation --format json`
- Mandatory evidence:
  - current acceptance contract and durable handoff-readiness evidence still validate;
  - coordination points to one real next engineer action; and
  - no new live-contract delta is required before recipient-repo mutation.
- Ready-to-close signal:
  - Phase 1 can start without baseline ambiguity or hidden prerequisite review.

## `phase.1` Recipient Scaffold And Bootstrap

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap`
- Primary outputs:
  - staged shared-core export prepared from the donor repo;
  - copied shared `core/` root in `/home/j/WatchTower`;
  - scaffolded `offensive_security/` root with starter docs, workflows, tracking, and python surfaces; and
  - shared registry and workspace wiring bootstrapped with starter workflow metadata replaced.
- Current command anchors:
  - `cd /home/j/WatchTowerPlan/core/python`
  - `uv run watchtower-core pack export --output-root <staged_export> --overwrite --format json`
  - copy the staged export into `/home/j/WatchTower`
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core pack scaffold --pack-slug offensivesecurity --pack-root offensive_security --command-namespace offsec --python-distribution watchtower-offensivesecurity --python-package watchtower_offensivesecurity --domain-root ctf --domain-root knowledge --format json`
  - `uv run watchtower-core pack bootstrap --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --replace-hosted-packs --write --format json`
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- Mandatory evidence:
  - scaffold, bootstrap, and validation outputs recorded in the challenge or implementation notes for the first target-repo slice;
  - required starter surfaces from `starter_surface_blueprint.md` exist at the offsec root; and
  - starter workflow metadata is removed before routing, route preview, or workflow indexing are trusted.
- Ready-to-close signal:
  - the recipient repo contains a bootstrap-valid offsec root with no hidden bring-up steps.

## `phase.2` Pack Machine Contract

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract`
- Primary outputs:
  - first offsec schema set for challenge, notes, event, session, environment, closeout, extraction, evidence, and discrepancy artifacts;
  - first offsec registry set for artifact families, documentation families, templates, human surfaces, rendered surfaces, authority routing, query families, event types, discrepancy types, severities, resolutions, and governance limits; and
  - pack validation-suite baseline and lifecycle or safety policy artifacts wired into the pack settings.
- Current command anchors:
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core validate schema --path <schema_path> --format json` for every newly authored `*.schema.json`
  - `uv run watchtower-core validate artifact --path <artifact_path> --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json` for each new registry or policy artifact
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- Mandatory evidence:
  - every new schema and registry file has an explicit validation pass;
  - `template_catalog`, `documentation_family_registry`, and `human_surface_policy_registry` are present before claiming documentation completeness; and
  - field-level contracts for `event_stream`, `artifact_index`, `challenge_metadata`, `notes_metadata`, `session_state`, and `environment_context` are recorded in code and reflected in docs;
  - the first machine surfaces are identifiable in `machine_surface_specimen_index.md`; and
  - the first registry set is materially aligned with `starter_registry_exemplars.md` or any intentional divergence is explained explicitly in docs and evidence.
- Ready-to-close signal:
  - Phase 3 can build runtime behavior without re-deriving schema or registry meaning from prose.

## `phase.3` Runtime, Query, Sync, And Workflow Seam

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam`
- Primary outputs:
  - pack-owned query family, sync targets, rendered-surface generation, and workflow metadata wired to real offsec artifacts;
  - authored `ROUTING_TABLE.md`, workflow modules, workflow roles, and namespace command docs aligned to the runtime; and
  - first thin real-CLI vertical slice from challenge intake through notes, event stream, artifact index, challenge index, and initial query commands, matching `vertical_slice_proof_spec.md`.
- Current command anchors:
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - run the first offsec namespace query and sync commands only after their command docs and validators exist
- Mandatory evidence:
  - route preview, workflow metadata, and authored workflow docs agree;
  - the first vertical slice proves the exact proof boundary, surface set, and failure exclusions in `vertical_slice_proof_spec.md`; and
  - command-doc entrypoints under `offensive_security/docs/commands/core_python/` resolve to the implemented namespace surfaces; and
  - the required tests and smoke proof in `phase_test_matrix.md` exist immediately after the slice works.
- Ready-to-close signal:
  - the pack has a real runtime seam with no placeholder-only query or workflow surfaces.

## `phase.4` Challenge Artifacts And Closeout

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout`
- Primary outputs:
  - governed `challenge.md`, `notes.md`, `closeout_record`, evidence inventory, discrepancy records, and closeout validation hooks;
  - deterministic artifact layout under `offensive_security/ctf/<platform>/<event>/<challenge>/`; and
  - closeout behavior that leaves `.wt_local/` in place and enforces discrepancy and no-closeout limits.
- Current command anchors:
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core validate artifact --path <artifact_path> --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- Mandatory evidence:
  - one real challenge root proves notes capture, evidence capture, discrepancy handling, and closeout rules together;
  - `challenge.md` body text stays source-faithful while governed front matter remains machine-valid; and
  - closeout cannot pass while a discrepancy carries `no_closeout`.
- Ready-to-close signal:
  - one bounded challenge lifecycle can run from intake through closeout without manual contract interpretation and the Phase 4 checklist passes cleanly.

## `phase.5` Knowledge Promotion And Retrieval

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval`
- Primary outputs:
  - reusable knowledge families, promotion policy, review posture, relation model, and deterministic retrieval behavior;
  - extraction output connected to closeout rather than to unscheduled periodic background promotion; and
  - knowledge queries that rank and explain results consistently.
- Current command anchors:
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core validate artifact --path <artifact_path> --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- Mandatory evidence:
  - promoted knowledge keeps challenge-specific detail stripped or explicitly quarantined;
  - typed relations remain authoritative on source artifacts, not only in derived indexes; and
  - retrieval ordering and review semantics are proven against at least one real extraction set; and
  - promotion flow matches `promotion_extraction_map.md` or the divergence is explained explicitly.
- Ready-to-close signal:
  - the pack can move from challenge closeout to reusable knowledge without weakening provenance, review, or retrieval determinism, and the Phase 5 checklist passes cleanly.

## `phase.6` Environment Adapters And Safety

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety`
- Primary outputs:
  - environment adapter protocol for local, VPN-reachable, SSH, and airgapped modes;
  - session-state and event-stream support for requested versus effective mode, confirmations, and transfers; and
  - fail-closed safety confirmation matrix and governance limits.
- Current command anchors:
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core validate artifact --path <artifact_path> --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- Mandatory evidence:
  - every environment mode has explicit allowed actions, refusal cases, confirmation gates, and transfer provenance;
  - full-auto observability is proven before unattended execution claims are accepted; and
  - actor-ref requirements fail closed where the preserved contract requires them.
- Ready-to-close signal:
  - environment and safety behavior is implementable from explicit policy and validator proof rather than from operator intuition, and the Phase 6 checklist passes cleanly.

## `phase.7` Release And Portability Proof

- Task: `task.watchtower_ctf_implementation_package_preservation.phase_7_release_and_portability_proof`
- Primary outputs:
  - customer-safe staged export proof for the finished offsec pack;
  - documented handoff modes for `core-only`, `core-plus-pack`, and `pack-only`; and
  - reproducible release or bootstrap rehearsal evidence.
- Current command anchors:
  - `cd /home/j/WatchTower/core/python`
  - `uv run watchtower-core pack list --format json`
  - `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
  - `uv run watchtower-core pack export --output-root <staged_export> --include-pack offensivesecurity --overwrite --format json`
  - `uv run watchtower-core release check --output-root <staged_export> --include-pack offensivesecurity --overwrite --format json`
- Mandatory evidence:
  - staged export proves portability rather than relying on a raw donor worktree;
  - the recipient bootstrap sequence is repeatable from documented commands and pack-owned surfaces; and
  - release proof records whether the handoff mode is repository bundle or pack-only bundle.
- Ready-to-close signal:
  - the pack can be exported, bootstrapped, validated, and handed off without donor-only residue or hidden cleanup steps, and the Phase 7 checklist passes cleanly.
