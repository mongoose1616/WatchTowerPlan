# Knowledge Taxonomy And Promotion Standard

## Purpose

Define how reusable offensive-security knowledge is organized, generalized, reviewed, and retrieved from challenge-local work.

## Rules

- keep one shared offensive-security corpus under `knowledge/`;
- top-level families are `tactics`, `protocols`, `tools`, `references`, and `commands`;
- `playbooks` stay nested under `tactics`;
- ship one canonical human-readable glossary standard, one pack-facing glossary surface, and one machine-readable `term_registry` for the pack vocabulary;
- the machine term registry must support deprecation and replacement behavior rather than acting as a passive synonym list;
- promotion is explicit and reviewable;
- promotion is the governed act of moving reusable knowledge from `status: candidate` to `status: accepted`; `promoted` stays human-facing language, not the canonical lifecycle value;
- reusable-knowledge lifecycle status uses `candidate`, `accepted`, `deprecated`, and `archived`;
- reusable-knowledge lifecycle transitions must follow the published `knowledge_state` entry in `status_transition_rules.json`, not ad hoc reviewer behavior;
- review progress stays separate from lifecycle status and uses a governed `review_status` vocabulary of `not_required`, `pending_review`, `in_review`, `approved`, `rejected`, and `approved_with_exception`, with per-family subsets allowed where needed;
- extraction is explicitly requestable at any time, runs automatically at closeout, and does not run as periodic active-phase background promotion by default;
- challenge-specific detail must be stripped or quarantined before canonical promotion;
- standalone references are reserved for cross-cutting, source-heavy, or weak-ownership material; smaller supporting reference matter should stay embedded in the owning tactic, protocol, or tool artifact;
- command artifacts are first-class reusable artifacts, but promotion is limited to normalized, safety-reviewed, broadly reusable command patterns;
- all knowledge families inherit one shared reusable-knowledge envelope before adding family-specific payload fields;
- relations between tactics, playbooks, tools, protocols, references, and command patterns must be typed and queryable;
- the starter relation vocabulary is `derived_from`, `supports`, `related_to`, `supersedes`, `belongs_to_tactic`, `uses_tool`, `uses_protocol`, `references`, `evidenced_by`, `produced_by_command`, `captured_in_event`, and `imported_via_transfer`;
- authoritative typed `relations[]` live on the source artifact, while index-level `related_artifact_ids` stay derived-only;
- those relations must stay sparse, typed, deterministic, and machine-queryable rather than turning references into graph hubs;
- promotion-policy entries must declare target family, allowed source artifact kinds, required provenance fields, required review workflow, mirror mode, and whether the family is eligible for operator-enabled auto-promotion;
- runtime auto-promotion remains off by default; if the operator explicitly enables a narrow allowlist in v1, only `reference` and `tool_profile` are eligible;
- retrieval ranking must stay deterministic with explicit tie-breakers after the main ranking inputs are applied;
- retrieval ranking order is scope match, exact tool/protocol match, reusability, freshness, evidence quality, breadth of applicability, teacher-mode explanation boost, then deterministic `knowledge_id` tie-break;
- source clarification is allowed only for targeted metadata questions that materially affect indexing, review, promotion, or closeout; otherwise the pack records provisional values and routes ambiguity into review or discrepancy handling;
- `external_references` entries require `url` and `reference_kind`, strongly recommend `label`, and may add `is_primary` and `quality_notes`;
- ATT&CK alignment is allowed and encouraged, but ATT&CK version must be pinned where used.

## Acceptance

- every knowledge family has a defined schema path, template direction, and promotion rule;
- candidate-stage knowledge is created directly in the target family at the canonical final path rather than through a separate candidate family;
- vocabulary governance has one canonical glossary path and one canonical machine registry path;
- retrieval ranking inputs and promotion criteria are explicit enough for deterministic implementation;
- relation semantics, clarification behavior, and external-reference citation rules are explicit enough to implement without re-derivation.
