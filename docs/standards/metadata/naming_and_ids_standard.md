# Naming and IDs Standard

## Summary
This standard defines how governed repository artifacts are named and how stable machine-usable identifiers are assigned.

## Purpose
Keep identifiers predictable enough for retrieval, validation, linking, registry use, and change review without making every artifact depend on path-only or prose-only identity.

## Scope
- Applies to stable machine-usable identifiers for governed documents and governed machine-readable artifacts.
- Covers document front matter `id` values, schema `$id` values, and filename conventions for published schemas and example artifacts.
- Does not define every visible title, heading, or free-form label used in the repository.

## Use When
- Assigning a new stable identifier to a governed artifact.
- Reviewing whether an identifier change is appropriate or unnecessarily breaking.
- Defining filenames for new schemas or example artifacts.

## Related Standards and Sources
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/README.md)
- [rfc_9562_uuid_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_9562_uuid_reference.md)
- [semantic_versioning_reference.md](/home/j/WatchTowerPlan/docs/references/semantic_versioning_reference.md)

## Guidance
- Treat the stable machine identifier as distinct from the path, visible title, and current lifecycle status.
- Assign one canonical machine identifier per governed artifact.
- Keep identifiers stable across edits that change wording, file placement, or explanatory content without changing artifact identity.
- Do not encode mutable metadata such as `status`, `owner`, `updated`, or `audience` into the identifier.
- Prefer readable deterministic identifiers for authored repository artifacts.
- Use lowercase ASCII for governed identifiers and filenames unless an external standard requires another form.
- Use UUIDs only when the identifier is generated, cross-system uniqueness matters, or a human-readable deterministic identifier is not sufficient.
- Do not use UUIDs for normal documentation IDs or published schema IDs.

## Structure or Data Model
### Identifier families
| Artifact Family | Identifier Form | Example | Notes |
|---|---|---|---|
| Governed document front matter | dotted family prefix + concept slug | `ref.front_matter` | Best for references, standards, workflows, and similar long-lived docs. |
| Published schema `$id` | `urn:watchtower:schema:` namespace + version token | `urn:watchtower:schema:interfaces:documentation:front-matter-base:v1` | Use for canonical schema identity rather than file paths. |
| Schema filename | snake case concept name + version + `.schema.json` | `reference_front_matter.v1.schema.json` | Version should be obvious in review. |
| Example filename | snake case concept name + optional case suffix + version + `.example.json` | `reference_front_matter_missing_tags.v1.example.json` | Use case suffix only when it improves clarity. |

### Document `id` rules
- Use the form `<family>.<concept_slug>`.
- The family prefix is lowercase alphanumeric.
- The concept slug uses lowercase alphanumeric tokens joined with underscores.
- The canonical pattern is `^[a-z][a-z0-9]*(\\.[a-z0-9]+(?:_[a-z0-9]+)*)+$`.
- Reserve currently approved document-family prefixes:
  - `ref` for reference documents
  - `std` for standards
  - `wf` for workflows
- Do not invent a new family prefix in ad hoc front matter. Standardize it first in this repository or in a narrower governing standard.
- Use the concept slug to describe the document topic, not the document state or file suffix.

### Schema `$id` rules
- Use URNs for published schema identifiers.
- The canonical form is `urn:watchtower:schema:<namespace segments>:<artifact-name>:v<major>`.
- Use lowercase kebab-case for namespace segments and the artifact name inside the schema URN.
- Use `:` to separate namespace segments and `-` to separate words inside a segment.
- Include a major-version token such as `v1` when the published contract version is part of the schema identity.
- Do not use relative paths, file paths, or git URLs as canonical schema identifiers.

### Filename rules
- Use lowercase snake_case for governed filenames unless an external standard requires otherwise.
- Keep filenames aligned with artifact purpose so reviewers can relate the file to the logical identifier quickly.
- Published schemas should use `.v<major>.schema.json`.
- Published examples should use `.v<major>.example.json`.
- Markdown document filenames should remain readable and path-stable, but the path is not the canonical machine identity.

### Version placement rules
- Keep full release-version semantics out of ordinary document IDs.
- For versioned published schemas and similarly versioned machine contracts, place the major compatibility boundary in the identifier and filename as `v<major>`.
- If an artifact needs richer semantic versioning, keep that in explicit metadata fields or release surfaces rather than overloading the base identifier.

## Process or Workflow
1. Decide whether the artifact needs a stable machine identifier or only a human-visible name.
2. Choose the correct identifier family for the artifact type.
3. Reuse the established prefix or namespace pattern for that family.
4. Keep the new identifier aligned with existing references, schemas, registries, and examples in the same change set.
5. Validate any machine-enforced profiles that constrain the identifier shape before treating the change as complete.

## Examples
- `ref.front_matter` is the stable document ID for the front matter reference.
- `std.front_matter` is the stable document ID for the front matter standard.
- `wf.documentation_generation` is the stable document ID for the documentation-generation workflow family.
- `urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1` is the canonical `$id` for the reference front matter schema.
- `reference_front_matter.v1.schema.json` is the corresponding schema filename.

## Validation
- Reviewers should reject identifier changes that do not reflect a real identity or compatibility change.
- Governed document `id` values should follow the documented dotted pattern and approved family prefixes.
- Published schema `$id` values should follow the documented URN pattern and stay unique within the repository.
- Filenames for schemas and examples should make artifact purpose and major version discoverable in review.
- Front matter and schema validation profiles should enforce identifier shape where that constraint already exists.

## Change Control
- Update this standard when the repository adds a new governed artifact family, changes approved family prefixes, or changes schema `$id` policy.
- Update companion standards and machine-validation schemas in the same change set when identifier rules become stricter.
- Record breaking schema identifier changes alongside the related compatibility and migration updates when that structure is in use.

## References
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [rfc_9562_uuid_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_9562_uuid_reference.md)
- [semantic_versioning_reference.md](/home/j/WatchTowerPlan/docs/references/semantic_versioning_reference.md)

## Notes
- This standard prefers stable readable identifiers for authored repository artifacts because they work better for review, retrieval, and traceability than opaque generated IDs.
- Future standards may define narrower rules for specific artifact families, but they should refine rather than weaken this baseline.

## Last Synced
- `2026-03-09`
