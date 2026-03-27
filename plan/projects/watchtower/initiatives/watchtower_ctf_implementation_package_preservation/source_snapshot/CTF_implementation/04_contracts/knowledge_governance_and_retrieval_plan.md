# Knowledge Governance And Retrieval Plan

## Purpose

Lock the pack-owned relation, promotion, retrieval, clarification, and external-reference contracts so Phase 5 implementation does not have to reinterpret Step 1 policy choices.

## Step 1 Basis

- `STEP1_FINAL.md`
  - `Q22`: explicit reviewable promotion metadata, default-empty auto-promotion allowlist, and narrower family allowlists even when broader automation exists
  - `Q45`: deterministic retrieval ranking posture
  - `R23`: starter relation-model vocabulary and source-artifact relation authority
- `STEP1_FINAL_v2.md`
  - `R27`: relation-type registry and per-family relation subsets
  - `R46`: source clarification policy
  - `R77`: shared `external_references` entry shape
- donor-pack precedent:
  - `WatchTowerPlan/plan/.wt/registries/promotion_policy_registry.json`
  - `WatchTowerPlan/plan/.wt/registries/relation_type_registry.json`
  - `WatchTowerPlan/plan/.wt/registries/source_type_registry.json`

## Relation Type Registry Contract

Canonical path:

- `offensive_security/.wt/registries/relation_type_registry.json`

Required root fields:

- `$schema`
- `id = registry.relation_type`
- `title`
- `status`
- `entries[]`

Required `entries[]` fields:

- `relation_type`
- `entry_status`
- `direction`
- `description`
- `allowed_source_families`
- `allowed_target_families`

Optional fields:

- `inverse_relation_type`
- `notes`
- `examples`

Locked starter relation types:

- `derived_from`
- `supports`
- `related_to`
- `supersedes`
- `belongs_to_tactic`
- `uses_tool`
- `uses_protocol`
- `references`
- `evidenced_by`
- `produced_by_command`
- `captured_in_event`
- `imported_via_transfer`

Locked rules:

- store authoritative typed `relations[]` on the source artifact rather than only in indexes;
- treat `related_artifact_ids` in indexes as derived navigation, not the primary relation authority;
- keep relation direction explicit and deterministic rather than inferring inverse meaning from prose;
- allow only per-family subsets declared in schemas or validators so command, tool, protocol, tactic, playbook, and reference artifacts do not become undisciplined graph hubs;
- keep relation values sparse and operator-meaningful rather than approximating a generic ontology.

## Promotion Policy Registry Contract

Canonical path:

- `offensive_security/.wt/registries/promotion_policy_registry.json`

Required root fields:

- `$schema`
- `id = registry.promotion_policy`
- `title`
- `status`
- `entries[]`

Required `entries[]` fields:

- `policy_id`
- `entry_status`
- `target_family`
- `allowed_source_artifact_kinds`
- `required_review_workflow`
- `required_provenance_fields`
- `mirror_mode`
- `auto_promotion_allowed`

Optional fields:

- `notes`
- `review_required_by_default`
- `minimum_review_status`
- `allowed_interaction_modes`
- `allowed_environment_types`

Locked starter target families:

- `tactic`
- `playbook`
- `tool_profile`
- `protocol`
- `reference`
- `command_pattern`

Locked starter `allowed_source_artifact_kinds` values:

- `challenge_notes`
- `challenge_recap`
- `challenge_solution`
- `evidence_artifact`
- `extraction_candidate`

Locked required provenance fields:

- `challenge_id`
- `closeout_id`
- `extraction_id`
- `source_artifact_refs`
- `evidence_refs`

Locked rules:

- use `workflow.offensivesecurity.ctf_reviewer` as the default review workflow for governed promotion;
- keep auto-promotion disabled by default at runtime even when a family is marked eligible in the registry;
- if the operator explicitly enables a narrow allowlist, only `reference` and `tool_profile` are eligible in v1;
- keep tactic, playbook, protocol, and command-pattern promotion review-heavy by default;
- use `mirror_mode` to declare whether source edits can update an accepted artifact in place, require a review branch, or force a new candidate review cycle.

## Retrieval Ranking Contract

Locked default retrieval posture:

- execution-time retrieval uses `status = accepted` artifacts by default;
- `candidate` artifacts are visible only when the operator explicitly asks for draft or review-state material;
- deterministic ranking is required for both CLI output and pack-internal retrieval helpers.

Locked ranking order:

1. scope match to the active challenge, tactic, or requested family
2. exact tool or protocol match over general tactic guidance
3. reusability level
4. freshness
5. evidence quality
6. breadth of applicability
7. teacher-mode explanation boost when `teacher` mode is active
8. deterministic tie-break by `knowledge_id`

Locked rules:

- do not let weakly scoped “general advice” outrank highly specific tool, protocol, or tactic matches;
- keep ranking signals auditable enough that a rendered explanation can show why one artifact outranked another;
- do not rely on opaque embedding-only ordering in v1.

## Retrieval Presentation And Family Semantics

Locked rules:

- `knowledge` remains the umbrella reusable-knowledge surface, while `commands` and `references` are filtered views over that same corpus rather than separate storage families;
- tactics remain a distinct conceptual layer rather than being treated as tool artifacts;
- playbooks remain distinct artifacts that belong to tactics rather than collapsing into tactic prose;
- commands remain distinct artifacts that use tools rather than collapsing into tool profiles;
- references remain distinct artifacts that support tactics, playbooks, tools, commands, or other reusable artifacts rather than collapsing into those families;
- when human `knowledge` output shows mixed families, the intended conceptual ladder is tactics first, then playbooks, then tools, then commands, then references;
- when filtered `commands` or `references` output becomes mixed across tools or supported families, conditional subgrouping may add structure, but those filtered surfaces remain flatter than umbrella `knowledge` by default;
- when ranking materially affects interpretation, `knowledge`, `commands`, and `references` may render a short “why this matched” explanation in human output.

## Candidate Visibility Rules

Locked rules:

- accepted artifacts remain the default retrieval posture for `knowledge`, `commands`, and `references`;
- if excluded candidate artifacts exist nearby, human output should note that those candidates were excluded by default and show the exact flag needed to include them;
- when candidate artifacts are explicitly included, human output must show a clear candidate cue so accepted and candidate material cannot be confused.

## Source Clarification Policy

Locked rules:

- allow targeted minimal clarification only when provenance, scope, classification, trust, environment, path, or id metadata materially affects indexing, review, promotion, closeout, safety, or canonical record creation;
- prefer one narrow clarification over broad questionnaires;
- in `assistant`, `teacher`, and `note_taker` modes, ask before governed record creation when materially missing metadata would change canonical behavior;
- in `full_auto`, do not interrupt for clarification; record the best provisional value justified by evidence, mark the affected record for `needs_review` or discrepancy handling when material ambiguity remains, and do not fabricate certainty;
- keep clarification events auditable through the event stream and the affected artifact updates.

## External References Schema

Locked shared entry shape:

- required:
  - `url`
  - `reference_kind`
- strongly recommended:
  - `label`
- optional:
  - `is_primary`
  - `quality_notes`

Locked starter `reference_kind` values:

- `official`
- `official_standard`
- `vendor`
- `high_quality_reference`
- `community`
- `archive`

Locked rules:

- keep `reference_kind` distinct from nested `source.type`;
- use `external_references` for reusable knowledge artifact citations, not for challenge-local raw provenance;
- pin ATT&CK and WSTG versions when those sources appear in external references or derived knowledge.
