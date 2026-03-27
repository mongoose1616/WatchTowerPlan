# Path And ID Generation Plan

## Purpose

Lock the v1 normalization, path-fallback, and typed-ID rules for CTF work items and reusable knowledge so scaffolded implementation does not need to re-derive naming behavior from conflicting Step 1 iterations.

## Current Contract Basis

- `STEP1_FINAL_v2.md`
  - `Q03`: keep the challenge path platform-aware and use a placeholder such as `unknown_platform` when source platform is missing
  - `Q34`: core owns generic slug/id machinery while pack rules define normalization and typed namespace policy
  - later path refinement: snake_case files and paths, dotted ids, readable stable paths, and platform-aware collision avoidance
- `STEP1_FINAL.md`
  - repeats the same `Q34` authority split and the same path-stability guidance
  - later path refinement introduces optional-segment collapse when `platform` or `event` is missing
- `STEP1_FINAL_v3.md`
  - preserve snake_case paths and files, dotted ids where the artifact family expects them, and repository-relative POSIX stored paths
  - typed slug and id-generation policy should be published explicitly in pack schemas and helpers
- `STEP1_PACK_SCAFFOLD_SPEC_v1.md`
  - keeps the current-compatible v1 baseline on `offensive_security/` plus the fixed canonical challenge root `offensive_security/ctf/<platform>/<event>/<challenge>/`
- shared naming authority:
  - `/home/j/WatchTowerPlan/core/docs/standards/metadata/naming_and_ids_standard.md`

## Deconfliction Outcome

- keep the scaffold-spec and v3 current-compatible challenge-root shape for v1:
  - `offensive_security/ctf/<platform>/<event>/<challenge>/`
- keep the fixed scaffold-compatible challenge-root shape for v1 and use placeholders when `platform` or `event` is missing at intake:
  - `unknown_platform`
  - `unknown_event`
- treat the later optional-segment collapse model from `STEP1_FINAL.md` and `STEP1_FINAL_v2.md` as a deferred future normalization target rather than the v1 implementation rule;
- keep the shared naming posture:
  - lowercase ASCII
  - readable deterministic identifiers
  - snake_case repository filenames and path segments
  - dotted typed machine ids

## Locked V1 Slug Normalization Rules

- use lowercase ASCII only for path segments, filenames, and typed concept slugs;
- use snake_case for challenge path segments, knowledge filenames, and other repository-managed path-level slugs;
- convert whitespace, hyphen, slash, and punctuation separators to `_`;
- collapse repeated `_` runs to one `_`;
- trim leading and trailing `_`;
- if normalization produces an empty result, use the family fallback slug instead of inventing a UUID.

## Locked V1 Fallback Slugs

- missing `platform` segment: `unknown_platform`
- missing `event` segment: `unknown_event`
- missing challenge title after normalization: `unnamed_challenge`
- missing reusable-knowledge title after normalization:
  - `unnamed_command`
  - `unnamed_tool`
  - `unnamed_protocol`
  - `unnamed_reference`
  - `unnamed_tactic`
  - `unnamed_playbook`

## Locked V1 Typed ID Rules

- generic slug/id helpers should live in shared core where possible, but the offsec pack owns the rule set that feeds those helpers;
- slugs derive from the locked path normalization rules above;
- ids derive from typed dotted namespace rules and are not the same thing as visible titles or stored paths;
- do not encode mutable lifecycle state, timestamps, owner fields, or review state into ids;
- keep pack traceability through the locked `pack_id`, the pack field on indexes, and the owning workspace root rather than repeating `pack.offensivesecurity` inside every work-item id.

Locked v1 work-item ids:

- `challenge_id = challenge.<platform_slug>.<event_slug>.<challenge_slug>`
- `knowledge_id = knowledge.<family>.<knowledge_slug>` for non-nested families
- `knowledge_id = knowledge.<family>.<context_slug>.<knowledge_slug>` when the family naturally lives beneath a stable parent context such as tactic-nested playbooks

Locked examples:

- `challenge.hack_the_box.season_8.underpass`
- `challenge.unknown_platform.picoctf_2026.format_string_lab`
- `knowledge.command.nmap_version_scan`
- `knowledge.playbook.web_sql_injection.web_sql_injection_boolean_blind`

## Locked V1 Path Rules

- always create challenge roots at:
  - `offensive_security/ctf/<platform_slug>/<event_slug>/<challenge_slug>/`
- in v1, never omit the `platform` or `event` segment from the canonical challenge root;
- when source metadata is missing, use the locked placeholder slug in the path and mirror that same segment in `challenge_id`;
- preserve known source values separately in metadata while placeholder paths are still in use;
- when better platform or event metadata becomes available later, run a governed path-and-id migration that renames the challenge root to the corrected canonical path and rewrites the affected known refs atomically;
- knowledge paths remain:
  - `offensive_security/knowledge/commands/<knowledge_slug>.md`
  - `offensive_security/knowledge/tools/<knowledge_slug>.md`
  - `offensive_security/knowledge/protocols/<knowledge_slug>.md`
  - `offensive_security/knowledge/references/<knowledge_slug>.md`
  - `offensive_security/knowledge/tactics/<knowledge_slug>/overview.md`
  - `offensive_security/knowledge/tactics/<tactic_slug>/playbooks/<knowledge_slug>.md`

## Stability And Collision Rules

- once a challenge root is created, its canonical path and `challenge_id` remain stable until a governed metadata-correction migration runs;
- when placeholder segments such as `unknown_platform` or `unknown_event` are replaced with better metadata, automatically rename the challenge root and update the canonical `challenge_id` through one governed migration operation rather than leaving the placeholder root permanently canonical;
- if a normalized challenge slug collides with an existing sibling root under the same `<platform>/<event>/`, append a numeric suffix:
  - `<challenge_slug>_2`
  - `<challenge_slug>_3`
- apply the same numeric-suffix rule to knowledge slugs inside the same family root when a collision occurs;
- mirror any collision suffix into the derived typed id so path and id remain aligned;
- migration must rewrite known machine refs, rendered links, internal doc links, indexes, and machine records in one governed operation rather than tolerating parallel canonical paths;
- future alias support remains optional and is not required by the v1 baseline.

## Metadata Follow-Through

- `challenge_metadata` must carry the canonical `challenge_id`, `platform_slug`, `event_slug`, and `challenge_slug`;
- `challenge_metadata` must also preserve the operator-facing source labels separately from the normalized path slugs;
- when placeholders are used, metadata should make that explicit through the normalized slug fields and the raw source fields rather than relying on path text alone;
- when a governed rename replaces placeholder segments or corrects other canonical slugs, the normalized slug fields and canonical id fields must be updated together as part of the same migration;
- `knowledge_index` and rendered knowledge views should treat `knowledge_id` as the stable machine key and `canonical_path` as the stable navigation surface.

## Remaining Future Extension

- optional-segment challenge-path collapse remains a deferred post-v1 design option if shared helper behavior and path-migration tooling ever make it worthwhile;
- if that future change lands, it must ship with:
  - explicit migration rules
  - alias or redirect handling for old ids or paths if needed
  - synchronized updates to `path_pattern_registry`, query helpers, indexes, and rendered views
