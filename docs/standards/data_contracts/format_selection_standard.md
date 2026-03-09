# Format Selection Standard

## Summary
This standard defines how the repository chooses data and document formats for governed artifacts.

## Purpose
Keep format choices small, predictable, and aligned with the repository's authority model so human-facing guidance stays readable, machine-facing artifacts stay validatable, and operational data does not drift into opaque ad hoc storage.

## Scope
- Applies to durable formats used for governed documents, governed machine-readable artifacts, examples, and future operational records.
- Covers the repository-preferred formats and the decision rules for when each should be used.
- Does not define every serialization detail, schema rule, or storage configuration by itself.

## Use When
- Adding a new artifact type under `docs/`, `workflows/`, or `core/control_plane/`.
- Deciding whether a new machine-readable surface should be JSON, YAML, NDJSON, SQLite-backed, or something else.
- Reviewing whether an existing format choice is introducing avoidable complexity.

## Related Standards and Sources
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md)
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [rfc_8259_json_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_8259_json_reference.md)
- [yaml_1_2_2_reference.md](/home/j/WatchTowerPlan/docs/references/yaml_1_2_2_reference.md)
- [ndjson_spec_reference.md](/home/j/WatchTowerPlan/docs/references/ndjson_spec_reference.md)
- [sqlite_wal_reference.md](/home/j/WatchTowerPlan/docs/references/sqlite_wal_reference.md)
- [commonmark_reference.md](/home/j/WatchTowerPlan/docs/references/commonmark_reference.md)

## Guidance
- Prefer the simplest format that preserves determinism, reviewability, and clear source-of-truth boundaries.
- Keep human-facing guidance in Markdown.
- Keep governed machine-readable artifacts in JSON unless there is a concrete reason to choose another format.
- Use YAML sparingly and only where its authoring ergonomics clearly outweigh its complexity.
- Use NDJSON only for append-only line-oriented records where whole-document JSON is a poor fit.
- Use SQLite only when local durable state, indexing, or retrieval genuinely need an embedded queryable store.
- Do not use a more complex format just because tooling can parse it.
- Do not let a derived convenience format become a parallel source of truth.
- Prefer formats that diff cleanly in git and are easy to inspect in review.
- Avoid binary or opaque formats for canonical repository artifacts unless an external standard or hard requirement leaves no practical alternative.

## Structure or Data Model
### Preferred format map
| Use Case | Preferred Format | Notes |
|---|---|---|
| Human-facing guidance, standards, workflows, references, and templates | Markdown | Use CommonMark-compatible structure by default. |
| Canonical governed machine-readable artifacts under `core/control_plane/` | JSON | Best fit for schema validation, deterministic review, and machine consumption. |
| Parsed document metadata in Markdown files | YAML front matter | Use only for governed document families that need metadata. |
| Small simple human-authored metadata with explicit parser rules | YAML | Use sparingly and keep the allowed subset simple. |
| Append-only operational records or line-oriented event streams | NDJSON | Use only when append-only processing materially matters. |
| Local embedded retrieval, indexing, or durable runtime state | SQLite | Use only when file-based documents are no longer the right shape. |

### Repository-default decisions
- `docs/**`, `workflows/**`, and human-facing repository guidance should use Markdown.
- `core/control_plane/schemas/**` should use JSON.
- `core/control_plane/contracts/**`, `registries/**`, `policies/**`, `indexes/**`, `ledgers/**`, and governed examples should default to JSON.
- Documentation front matter should use YAML only for the parsed metadata block, not for the document body.
- Future append-only runtime or event records should prefer NDJSON over inventing a custom line format.
- Future local retrieval or runtime stores should stay out of the canonical versioned control plane and only use SQLite when query needs justify it.

### Decision rules
| Question | Preferred Direction | Reason |
|---|---|---|
| Is the artifact primarily read by humans as prose or guidance? | Markdown | Best review and authoring fit. |
| Is the artifact a canonical machine-readable contract or record? | JSON | Best validation and interoperability fit. |
| Is the artifact only a small metadata layer for a Markdown document? | YAML front matter | Keeps document and metadata together without making YAML the main authoring surface. |
| Is the artifact append-only and line-oriented? | NDJSON | Supports streaming and incremental processing cleanly. |
| Does the artifact need embedded querying, indexing, or transactional local state? | SQLite | Earn the complexity only when document files are no longer enough. |
| Does the only reason for choosing YAML over JSON come down to familiarity? | Use JSON instead | Keep machine contracts stricter and easier to validate. |

## Process or Workflow
1. Decide whether the artifact is human-facing guidance, canonical machine-readable authority, metadata, append-only operational data, or local queryable state.
2. Start with the repository default for that class of artifact.
3. Challenge any move away from Markdown for prose or away from JSON for governed machine artifacts.
4. If choosing YAML, NDJSON, or SQLite, record the concrete reason the default format is insufficient.
5. Keep schema, validation, and companion examples aligned with the chosen format in the same change set.

## Examples
- A new policy document under `core/control_plane/policies/` should be JSON, not YAML.
- A new standards document under `docs/standards/**` should be Markdown, not JSON or YAML.
- A governed reference document may use YAML front matter for metadata while keeping the body in Markdown.
- A future append-only validation-event log could use NDJSON if it is truly line-oriented and not canonical control-plane authority.
- A future local retrieval index may justify SQLite if file-based indexes become too limited.

## Validation
- Reviewers should challenge format choices that add complexity without a concrete benefit.
- Governed machine-readable artifacts should default to JSON unless an explicit exception is justified.
- YAML usage should stay limited and simple enough that readers do not need advanced YAML knowledge.
- NDJSON and SQLite should not be introduced as theoretical future-proofing without a real operational need.
- A new format choice should not blur the boundary between canonical authority, derived support data, and mutable runtime state.

## Change Control
- Update this standard when the repository changes its default format choices or adds a new approved format category.
- Update companion standards and references in the same change set when a format choice changes validation, schema, or storage rules.
- If a narrower standard adopts a different format for a specific artifact family, it must justify the exception explicitly.

## References
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md)
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [rfc_8259_json_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_8259_json_reference.md)
- [yaml_1_2_2_reference.md](/home/j/WatchTowerPlan/docs/references/yaml_1_2_2_reference.md)
- [ndjson_spec_reference.md](/home/j/WatchTowerPlan/docs/references/ndjson_spec_reference.md)
- [sqlite_wal_reference.md](/home/j/WatchTowerPlan/docs/references/sqlite_wal_reference.md)
- [commonmark_reference.md](/home/j/WatchTowerPlan/docs/references/commonmark_reference.md)

## Notes
- This standard deliberately keeps format choice separate from schema design, identifier policy, and runtime validation logic.
- The goal is not to ban every alternative format. The goal is to make deviations from the defaults explicit and justified.

## Last Synced
- `2026-03-09`
