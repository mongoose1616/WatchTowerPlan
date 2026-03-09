# Status Tracking Standard

## Summary
This standard defines the lifecycle status vocabulary for governed repository artifacts.

## Purpose
Keep lifecycle state small, stable, and unambiguous so governed artifacts can signal whether they are current, still in progress, or temporarily retained on the way to removal.

## Scope
- Applies to lifecycle status for governed documents and governed machine-readable artifacts.
- Covers the allowed lifecycle values, their meaning, and how they should be used.
- Does not define validation-result state, runtime execution state, queue state, or task-progress state.
- Does not apply to short directory `README.md` files or other simple orientation docs.

## Use When
- Adding a `status` field to a governed artifact.
- Reviewing whether a lifecycle value is appropriate.
- Deciding whether an artifact should be deprecated or deleted.

## Related Standards and Sources
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

## Guidance
- Use `status` only for lifecycle state of governed artifacts.
- Do not reuse this field for validation outcomes such as passed or failed checks.
- Do not reuse this field for runtime or orchestration states such as queued, running, blocked, or complete.
- Do not add lifecycle status to short directory `README.md` files or similar orientation documents.
- Use one shared lifecycle vocabulary across governed docs and governed machine-readable artifacts unless a later narrower standard justifies a stricter subset.
- The allowed lifecycle values are:
  - `draft`
  - `active`
  - `deprecated`
- Use lowercase strings exactly as written above.
- Prefer deletion over long-lived deprecation when an artifact no longer needs to exist.
- Use `deprecated` only when temporary retention is still necessary for migration, reference cleanup, or active consumers.
- If no consumer still needs the artifact, delete it instead of keeping it in a deprecated state.

## Structure or Data Model
### Lifecycle values
| Value | Meaning | Use When |
|---|---|---|
| `draft` | The artifact is still being developed and is not yet the normal canonical current artifact. | The artifact exists for active authoring or review and is not yet the settled supported version. |
| `active` | The artifact is the current supported artifact. | The artifact is the current intended version for normal use. |
| `deprecated` | The artifact is being retained temporarily but should be removed after references, consumers, or migrations are handled. | Immediate deletion is not yet safe or practical. |

### Exclusions
- Validation-result values such as `pass`, `fail`, `error`, or `warning` are not lifecycle status values.
- Runtime or execution values such as `queued`, `running`, `blocked`, `complete`, or `cancelled` are not lifecycle status values.
- Storage or historical labels such as `archived` or `historical` are not part of the current lifecycle vocabulary.

## Process or Workflow
1. Confirm that the artifact is a governed artifact rather than a simple orientation file.
2. Decide whether the artifact is still in authoring, is the current supported artifact, or is only being retained temporarily.
3. Assign `draft`, `active`, or `deprecated` accordingly.
4. If `deprecated` is being considered, confirm whether deletion is possible instead.
5. If deletion is not yet possible, keep `deprecated` temporary and remove the artifact once dependencies are cleared.

## Examples
- A new standard being refined before it becomes the current repository rule can use `draft`.
- A current reference or standard in normal use should use `active`.
- A governed artifact kept only while links, schemas, or consumers are being updated can use `deprecated`.
- A short directory `README.md` should not carry lifecycle status at all.

## Validation
- Governed artifacts that expose lifecycle status should use only `draft`, `active`, or `deprecated`.
- Reviewers should reject new status vocabularies unless a narrower governing standard explicitly introduces them.
- Reviewers should challenge `deprecated` artifacts that remain in place without a clear reason to retain them.
- Validation and runtime state fields should use separate names rather than overloading `status`.

## Change Control
- Update this standard when the repository changes the shared lifecycle vocabulary or its scope.
- Update front matter schemas and any governed artifact schemas in the same change set when lifecycle values change.
- Prefer deleting obsolete governed artifacts instead of expanding the deprecation taxonomy.

## References
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

## Notes
- This standard is intentionally narrow. It defines lifecycle status only.
- If the repository later needs validation-result vocabularies or execution-state vocabularies, those should be separate standards.

## Last Synced
- `2026-03-09`
