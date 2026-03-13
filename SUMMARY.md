# WatchTowerPlan Whole-Repo Summary

Review date: March 11, 2026

This document is the durable whole-repo assessment referenced by the root
entrypoints, the foundations layer, and several follow-up planning slices. It
captures the historical review context that motivated the earlier foundations,
planning-authority, and derived-status remediation work, while preserving a
lightweight current-state summary for contributors who need the broad picture
before opening deeper planning artifacts.

## Current Status

- `WatchTowerPlan` is the governed core and planning workspace for WatchTower,
  not the first operator-facing product repository.
- The repository remains healthy, validated, and intentionally machine-first in
  its control-plane design, but the cost of navigation across many governed
  surfaces is a continuing optimization concern.
- The most important historical coherence issues identified by this review have
  already been addressed through traced follow-up slices and should now be read
  as resolved findings rather than active defects.

## Historical Findings Referenced By Follow-Up Slices

### Foundation Scope And EntryPoints

- The original review found that the repository foundations mixed current
  repository scope with future product direction too loosely.
- That concern is why
  [repository_scope.md](docs/foundations/repository_scope.md) became the
  authoritative current-repository charter and why the root entrypoints were
  tightened around routing, coordination, and whole-repo review.
- Follow-up slices that cite this summary for foundation-scope drift are
  referring to that historical finding.

### Planning Authority And Machine Lookup

- The original review found that the planning domain had no single canonical
  machine planning join and no explicit machine authority answer for recurring
  planning questions.
- That concern motivated the planning-authority unification work and the
  addition of the canonical planning catalog plus
  `watchtower-core query authority`.
- Follow-up slices that cite this summary for planning-authority scatter are
  referring to that historical finding.

### Derived Initiative Status Semantics

- The original review found that initiative-family projections published a
  generic lifecycle `status` field that was easy for machine consumers to
  misread next to the initiative outcome state.
- That concern motivated the later derived-projection semantics alignment work
  that separated `artifact_status` from `initiative_status`.
- Follow-up slices that cite this summary for status ambiguity are referring to
  that historical finding.

## Verification Update

This summary was rechecked on March 11, 2026 against the live repository state
after the initial follow-up initiatives closed.

- No longer valid: the missing short repository-charter concern was addressed
  by [repository_scope.md](docs/foundations/repository_scope.md).
- No longer valid: the missing canonical machine planning-catalog concern was
  addressed by
  [planning_catalog.v1.json](core/control_plane/indexes/planning/planning_catalog.v1.json)
  and the corresponding query surfaces.
- No longer valid: the missing machine authority-map concern was addressed by
  the planning authority surfaces and `watchtower-core query authority`.
- Resolved after verification: the ambiguous initiative-family projection field
  named `status` was replaced by explicit `artifact_status` while preserving
  distinct `initiative_status` semantics in initiative and coordination query
  results.
- Remaining recommendations from the original review should be read as future
  optimization opportunities, not as open coherence defects blocking repo
  closeout.

## Evidence Base

The review that produced this summary used repository-local evidence only.

Primary evidence surfaces:

- [README.md](README.md)
- [AGENTS.md](AGENTS.md)
- [docs/foundations/README.md](docs/foundations/README.md)
- [docs/planning/coordination_tracking.md](docs/planning/coordination_tracking.md)
- [docs/standards/README.md](docs/standards/README.md)
- [workflows/ROUTING_TABLE.md](workflows/ROUTING_TABLE.md)
- [workflows/modules/README.md](workflows/modules/README.md)
- [docs/commands/core_python/README.md](docs/commands/core_python/README.md)
- [core/control_plane/README.md](core/control_plane/README.md)
- [core/python/README.md](core/python/README.md)

Command and validation evidence used at the time:

- `watchtower-core query coordination --format json`
- `watchtower-core doctor --format json`
- `watchtower-core validate all --format json`
- `pytest -q`
- `python -m mypy src`
- `ruff check .`

## Residual Recommendations

- Keep rationalizing entrypoints as the governed surface count grows so humans
  and agents do not need to open many adjacent docs before reaching the right
  authority.
- Prefer one primary machine authority for recurring questions when several
  projections exist.
- Continue treating documentation compactness and boundary clarity as system
  quality concerns, not just editorial polish.

## Notes

- This summary is a durable historical review artifact, not the live current
  work tracker. For current initiative state, start with
  [coordination_tracking.md](docs/planning/coordination_tracking.md) or
  `watchtower-core query coordination --format json`.
- When a planning slice cites this summary, it is usually referencing the
  historical review finding that motivated that slice, not claiming the finding
  is still unresolved.
