# First-Party Root Pack Roots

## Summary
Implement first-party root-pack discovery and default-pack resolution so copied repositories can host packs at <slug>/ without donor assumptions.

## Identity
- `initiative_id`: `initiative.first_party_root_pack_roots`
- `trace_id`: `trace.first_party_root_pack_roots`
- `scope_type`: `pack_wide`

## Problem Statement
The current pack-loading contract is still too loose around pack-root discovery. Shared runtime code can find `pack_settings.json` by broad globbing, but it does not define a deterministic preference for first-party root packs such as `plan/` or `oversight/`, and the default-pack fallback still behaves like an incidental repo scan instead of an explicit contract. That ambiguity makes copy-forward adoption harder to reason about and keeps the current internal `plan/` layout looking more special than it should.

## Goals
- Make first-party root packs such as `plan/` a supported, explicit discovery mode in reusable core.
- Keep `packs/<slug>/` as a supported secondary convention without making it the only discovery shape.
- Make default-pack resolution prefer the explicit registry default when available and use deterministic manifest discovery only as fallback.
- Prove the resulting behavior with `plan` as the first-party/root-pack test pack.

## In Scope
- Reusable-core pack-settings discovery and default-pack fallback behavior.
- Shared pack-root discovery helpers that need to know about direct root packs and `packs/*` pack roots.
- Targeted host and validation tests that prove root-pack behavior with manifest-backed fixtures.
- Same-change documentation updates if the runtime contract wording changes materially.

## Out Of Scope
- Removing the shared `core/python` workspace registration contract for hosted packs.
- General manifest-driven source import of pack Python packages when they are not installed into the shared workspace.
- Rewriting `pack_registry.json` or `core/python/pyproject.toml` to remove the current repository's `plan` entry in this slice.
- Full downstream repository remediation for `WatchTowerOversight` or future consuming repos.

## Success Criteria
- The reusable-core loader prefers the registry default pack when one is declared and valid.
- When no registry default can be used, deterministic fallback discovery prefers direct root packs such as `plan/` before nested `packs/*` pack roots.
- Root-pack discovery and defaulting are covered by targeted tests that use `plan` as the first-party/root-pack proof pack.
- Validation and host behavior remain green for the existing repository layout after the change.

## Initial Task Set
- `task.first_party_root_pack_roots.bootstrap_first_party_root_pack_roots`: Bootstrap First-Party Root Pack Roots live initiative package.
