# Artifact Payload Contracts Plan

## Purpose

Lock the field-level payload contracts for governed challenge artifacts and reusable knowledge artifacts so schema authoring and validator work do not need to re-derive Step 1 answers.

## Step 1 Basis

- `STEP1_FINAL_v2.md`
  - `R18-R22`: closeout, evidence, extraction, candidate representation, and shared reusable-knowledge envelope
  - `R39-R44`: family-specific knowledge payloads for command, tool profile, protocol, reference, tactic, and playbook artifacts
  - shared artifact primitives: `contract_version`, UTC timestamps, pack-relative paths, and structured checksums
  - canonical user-visible roots include `artifacts/` and tactic-nested playbooks
- `STEP1_FINAL.md`
  - confirms candidate-to-accepted promotion and the split between lifecycle `status` and `review_status`
- reference-pack precedent:
  - `plan` keeps raw evidence and governed evidence shells separate
  - both working packs treat artifact families and rendered views as governed machine surfaces rather than prose conventions

## Shared Artifact Payload Primitives

Apply these primitives to every governed JSON artifact family in v1:

- require `contract_version` as the cross-family version primitive;
- keep timestamps RFC 3339, UTC only, `Z` suffix, and whole-second precision;
- keep `path`, `rendered_view_path`, and any other stored `*_path` field pack-relative and POSIX-style;
- represent checksums as a structured object with `algorithm` and `value`;
- prefer authoritative artifact ids for cross-artifact references and let `artifact_index` resolve those ids to paths;
- treat `status`, `review_required`, `review_status`, `source`, `trust_state`, and `verification_status` as governed fields driven by registries or policy rather than ad hoc prose.

## Source, Trust, And Verification Baseline

Use one nested authoritative `source` object and separate trust/verification registries across governed artifact families.

Locked canonical `source` posture:

- require `source.summary`;
- allow standard optional fields:
  - `source.platform`
  - `source.event`
  - `source.url`
  - `source.ref`
  - `source.type`
- flatten `source_*` fields only in indexes and query-oriented surfaces; keep the authoritative record nested.

Locked `source.type` starter registry values:

- `derived_challenge_knowledge`
- `curated_reference`
- `local_taxonomy`
- `challenge_page`
- `challenge_prompt`
- `event_material`
- `official_standard`
- `official_docs`
- `vendor_docs`
- `high_quality_reference`
- `community_reference`
- `internal_observation`
- `local_file`
- `paste`

Locked `trust_state` starter registry values:

- `unknown`
- `unverified`
- `source_attested`
- `partially_verified`
- `verified`

Locked `verification_status` starter registry values:

- `not_reviewed`
- `inspected`
- `integrity_checked`
- `manually_confirmed`
- `reproduced`

Locked rules:

- `source.type` answers origin category, not full derivation history;
- derivation remains in lineage fields such as `challenge_id`, `closeout_id`, `extraction_id`, `source_artifact_refs`, and typed relations;
- `trust_state` and `verification_status` remain separate governed fields;
- allowed subsets may vary by artifact family, but the baseline registries stay shared.

## Challenge Artifact Contracts

### `ctf_closeout_record`

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/closeout_record.json`

Required fields in addition to the shared primitives:

- `closeout_id`
- `challenge_id`
- `closed_at`
- `outcome`
- `closed_by`
- `summary`
- `evidence_complete`
- `solution_present`
- `recap_present`
- `artifacts_indexed`
- `extraction_created`
- `session_id`
- `effective_mode`
- `interaction_mode`
- `closeout_reason`

Conditionally required fields:

- `unresolved_reason`
- `candidate_count`
- `review_required`
- `review_status`
- `key_pivot`

Locked defaults:

- use one shared closeout envelope rather than outcome-specific variants;
- use `outcome` instead of a separate `solved` boolean;
- starter `outcome` values are `solved`, `blocked_closeout`, `unresolved`, and `closed_without_attempt` if that later lands;
- `key_pivot` is the decisive change in approach or evidence, not a general timeline recap.

### `ctf_evidence_artifact`

Canonical governed collection path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/evidence/artifacts.json`

Canonical raw capture root:

- `offensive_security/ctf/<platform>/<event>/<challenge>/artifacts/`

Locked collection shape:

- one authoritative JSON collection with `entries[]`
- one current-state entry per `artifact_id`
- in-place updates keyed by `artifact_id`
- `created_at_utc` and `updated_at_utc` on each entry
- no embedded per-entry `change_log[]`; change history is mirrored into `event_stream`

Locked starter `artifact_kind` values:

- `command_output`
- `file_capture`
- `screenshot`
- `network_capture`
- `manual_note`
- `clipboard_capture`
- `transfer_bundle`

Required per-entry envelope fields in addition to the shared primitives:

- `artifact_id`
- `artifact_kind`
- `path`
- `title`
- `evidence_role`
- `challenge_id`
- `captured_at`
- `captured_by`
- `summary`
- `trust_state`
- `verification_status`
- `payload`

Conditionally required per-entry envelope fields:

- `claim_ref`
- `used_in_closeout`
- `source_ref`
- `environment_context_ref`
- `checksum`
- `session_id`
- `related_command_ref`
- `related_event_ref`
- `mime_type`
- `rendered_view_path`
- `transfer_ref`
- `interaction_mode`

Locked payload posture:

- keep one shared evidence envelope plus `artifact_kind`-specific payload subobjects;
- command-output payloads may carry fields such as `command`, `exit_code`, `stdout_ref`, `stderr_ref`, and `execution_context_type`;
- screenshot and network-capture payloads may carry capture-specific fields without polluting other artifact kinds;
- scripts, helper binaries, and downloaded executables stay under `artifact_kind = file_capture` and should use typed payload fields such as `file_role = generated_script | generated_binary | downloaded_binary`;
- `path` points to the canonical captured artifact or normalized derivative under the challenge root, not to an absolute filesystem location.

Locked defaults:

- raw files and pasted-output captures live under `artifacts/`, while `.wt_local/evidence/artifacts.json` stores the governed metadata and provenance inventory;
- reuse the pack provenance vocabularies from `decision.source_trust_model` for `trust_state` and `verification_status`;
- do not add a blanket `manually_transferred` boolean; transfer conditions are expressed through `transfer_ref`, `interaction_mode`, checksum when practical, and provenance fields.

### `ctf_extraction_output`

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/extractions/<extraction_id>.json`

Required fields in addition to the shared primitives:

- `extraction_id`
- `challenge_id`
- `closeout_id`
- `created_at`
- `extracted_by`
- `status`
- `candidate_count`
- `families_found`
- `extraction_summary`
- `review_required`
- `review_status`

Conditionally required fields:

- `notes_ref`
- `recap_ref`
- `solution_ref`
- `candidate_refs`
- `accepted_refs`
- `rejected_refs`
- `supersedes`
- `superseded_by`
- `archived_at`
- `evidence_complete`
- `source_coverage`

Locked defaults:

- starter `status` values are `active`, `archived`, and `superseded`;
- `notes_ref`, `recap_ref`, `solution_ref`, and candidate or accepted reference fields point to artifact ids, not raw paths;
- `families_found` should use canonical family ids such as `command`, `tool_profile`, `protocol`, `reference`, `tactic`, and `playbook`;
- `source_coverage` records which closeout surfaces were actually considered.

## Reusable Knowledge Contracts

### Candidate Representation

Locked v1 model:

- do not create a separate long-lived `knowledge_candidate` family;
- create artifacts directly in the target family at the canonical final path;
- set `status: candidate` at extraction time;
- on approval, keep the same artifact id and change `status: accepted`;
- record the promotion event in `event_stream` and mirror the latest promotion state in `artifact_index`;
- keep review progress in `review_required` and `review_status`, not in extra lifecycle status labels.

Candidate-stage required fields in addition to the shared family envelope:

- `challenge_id`
- `closeout_id`
- `extraction_id`
- `source_artifact_refs`
- `review_required`
- `review_status`
- `challenge_local_detail_stripped`

Conditionally useful candidate fields:

- `generalization_notes`
- `evidence_refs`
- `redaction_notes`
- `safety_reviewed`
- `evidence_complete`
- `confidence`

### Shared Reusable-Knowledge Envelope

Applies to `command`, `tool_profile`, `protocol`, `reference`, `tactic`, and `playbook` families.

Always required shared fields in addition to the shared primitives:

- `artifact_id`
- `artifact_family`
- `title`
- `summary`
- `status`
- `review_required`
- `review_status`
- `source`
- `tags`

Conditionally required shared fields:

- `source_artifact_refs`
- `challenge_id`
- `closeout_id`
- `extraction_id`
- `related_artifact_ids`
- `external_references`
- `challenge_local_detail_stripped`
- `generalization_notes`
- `redaction_notes`
- `evidence_refs`
- `evidence_complete`
- `safety_reviewed`

Locked defaults:

- challenge-derived lineage fields are required when the artifact comes from challenge work;
- directly authored reusable knowledge does not need artificial challenge lineage fields;
- `external_references` is a shared cross-family field, not a separate per-family link invention;
- family-specific payloads sit on top of this shared baseline rather than replacing it.

## Family-Specific Knowledge Payloads

| Family | Canonical Path | Required Payload Fields | Conditionally Useful Fields | Locked Notes |
|---|---|---|---|---|
| `command` | `offensive_security/knowledge/commands/<command_slug>.md` | `command_template`, `placeholders`, `required_binary`, `supported_environment_types`, `shell_assumptions`, `safety_class`, `when_to_use`, `when_not_to_use` | `defaults`, `expected_signals`, `verification_notes`, `runtime_assumptions` | keep the payload compact; use typed relations for linked tools, protocols, tactics, and playbooks |
| `tool_profile` | `offensive_security/knowledge/tools/<tool_slug>.md` | `tool_binary`, `supported_environment_types`, `when_to_use`, `when_not_to_use`, `applicability_boundaries`, `strengths`, `limitations`, `prerequisites` | `install_or_presence_notes`, `common_command_patterns`, `option_guidance`, `safety_notes`, `expected_outputs`, `verification_notes` | tool profiles stay tool-focused and do not absorb playbook logic |
| `protocol` | `offensive_security/knowledge/protocols/<protocol_slug>.md` | `default_ports`, `transport`, `service_identity`, `when_to_use`, `when_not_to_use`, `operator_relevance`, `authentication_notes`, `enumeration_notes`, `attack_relevance` | `common_misconfigurations`, `supported_environment_types`, `prerequisites`, `limitations`, `expected_signals`, `verification_notes` | protocol artifacts stay operator-oriented rather than RFC-style dumps |
| `reference` | `offensive_security/knowledge/references/<reference_slug>.md` | `source_kind`, `source_author_or_publisher`, `publication_context`, `key_takeaways`, `operator_relevance`, `when_to_use`, `when_not_to_use`, `not_normative_for` | `source_quality_notes`, `trust_notes`, `verification_notes`, `distilled_notes` | references support other families and should not become the main normative guidance layer |
| `tactic` | `offensive_security/knowledge/tactics/<tactic_slug>/overview.md` | `mitre_alignment`, `goal`, `when_to_use`, `when_not_to_use`, `typical_inputs`, `typical_outputs`, `common_signals`, `playbook_overview`, `selection_guidance`, `limitations`, `common_misuse` | `parent_context`, `related_tactics`, `safety_notes` | tactics stay coarse and orienting; detailed procedure belongs in playbooks |
| `playbook` | `offensive_security/knowledge/tactics/<tactic_slug>/playbooks/<playbook_slug>.md` | `primary_tactic`, `objective`, `prerequisites`, `step_sequence`, `decision_points`, `expected_inputs`, `expected_outputs`, `verification_steps`, `stop_conditions` | `related_tactics`, `branch_conditions`, `fallbacks`, `typical_tools`, `safety_notes` | playbooks are procedure-first and reproducible; branching is structured, not narrative-only |

Additional canonical tactic navigation surface:

- `offensive_security/knowledge/tactics/overview.md`

## Deconfliction Notes

- keep `promotion` as the named action and governed acceptance event; do not use `promoted` as the canonical lifecycle status value;
- use `candidate`, `accepted`, `deprecated`, and `archived` as the reusable-knowledge lifecycle baseline, with review state carried separately in `review_status`;
- keep raw `artifacts/` as a capture container, but do not treat the container itself as an artifact family;
- prefer shared relation and provenance surfaces over family-specific link duplication.
