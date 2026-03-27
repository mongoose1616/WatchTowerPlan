# Phase 5: Build Knowledge, Promotion, And Retrieval

## Purpose

Define the reusable offensive-security corpus, promotion workflow, relation model, and retrieval behavior built from challenge-local work.

## In-Scope Surfaces

- knowledge families
- candidate handling
- promotion review
- retrieval ranking
- relation and cross-link model
- reusable templates and validation expectations

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- knowledge schema families:
  - `knowledge_tactic`
  - `knowledge_playbook`
  - `knowledge_tool_profile`
  - `knowledge_protocol`
  - `knowledge_reference`
  - `knowledge_command_pattern`
- canonical knowledge paths:
  - `offensive_security/knowledge/tactics/overview.md`
  - `offensive_security/knowledge/tactics/<tactic_slug>/overview.md`
  - `offensive_security/knowledge/tactics/<tactic_slug>/playbooks/<playbook_slug>.md`
  - `offensive_security/knowledge/protocols/<protocol_slug>.md`
  - `offensive_security/knowledge/tools/<tool_slug>.md`
  - `offensive_security/knowledge/references/<reference_slug>.md`
  - `offensive_security/knowledge/commands/<command_slug>.md`
- vocabulary and naming surfaces:
  - `offensive_security/docs/standards/metadata/offsec_glossary_standard.md`
  - `offensive_security/docs/references/offsec_glossary.md`
  - `offensive_security/.wt/registries/term_registry.json`
- one shared reusable-knowledge envelope plus family-specific payload contracts, with extracted candidates created directly in the target family at the canonical path
- `offensive_security/.wt/registries/relation_type_registry.json`
- `offensive_security/.wt/registries/promotion_policy_registry.json`
- promotion and review workflow tied to `knowledge_capture` and `challenge_closeout`

## Dependencies

- Phase 2 knowledge family schema planning
- Phase 4 extraction output and closeout behavior
- research anchors for ATT&CK, WSTG, and evidence/reporting patterns

## Upstream Assumptions

- shared core does not define offensive-security knowledge semantics
- relation/query/rendered-view helpers can be reused, but payload rules remain pack-owned

## Validation And Acceptance Criteria

- all knowledge families have explicit ownership, schema, and template direction
- the shared reusable-knowledge envelope and each family payload contract are explicit enough to author schemas without re-derivation
- playbooks remain nested beneath tactics
- extraction is explicitly requestable, runs automatically at closeout, and does not run as periodic active-phase promotion by default
- promotion is the governed act of changing `status: candidate -> accepted`, while `review_status` remains a separate controlled field
- reusable-knowledge lifecycle transitions are published explicitly in `status_transition_rules` and are not left to review-service inference
- typed relations are authoritative on the source artifact, use the locked starter relation vocabulary, and keep `related_artifact_ids` as a derived index-only navigation aid
- promotion policy entries declare source artifact kinds, target families, required provenance fields, review workflow, and mirror mode
- runtime auto-promotion remains disabled by default; if a narrow allowlist is later enabled, only `reference` and `tool_profile` are eligible in v1
- standalone references remain the exception case rather than the default home for reusable material
- glossary and term-registry governance are explicit enough to keep naming drift out of implementation
- retrieval ranking is deterministic and ordered by scope match, exact tool/protocol match, reusability, freshness, evidence quality, breadth, teacher-mode explanation boost, and final `knowledge_id` tie-break
- source clarification is limited to targeted provenance or scope questions when materially necessary; otherwise provisional values plus review or discrepancy handling must be used
- external references use one shared entry contract with required `url` and `reference_kind`, recommended `label`, and optional `is_primary` and `quality_notes`
- challenge-specific details are stripped or quarantined before promotion

## Risks And Unresolved Questions

- ATT&CK alignment must stay version-pinned and not overfit deprecated ATT&CK surfaces
- reference-family scope can bloat if cross-cutting versus embedded reference rules are weak
- family-specific relation subsets must stay disciplined so knowledge artifacts do not become generic graph hubs

## Exit Criteria

- the package provides a full reusable-knowledge and promotion plan from candidate extraction to canonical artifact retrieval
