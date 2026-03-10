---
trace_id: "trace.command_documentation_and_lookup"
id: "design.features.command_documentation_and_lookup"
title: "Command Documentation and Lookup Design"
summary: "Defines the feature-level design for a human-readable command-page family under docs/commands and a machine-readable command index under core/control_plane/indexes/commands."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T05:14:33Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/design/features/command_documentation_and_lookup.md"
  - "docs/commands/"
  - "core/control_plane/indexes/commands/command_index.v1.json"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "command docs design"
  - "command lookup design"
---

# Command Documentation and Lookup Design

## Record Metadata
- `Trace ID`: `trace.command_documentation_and_lookup`
- `Design ID`: `design.features.command_documentation_and_lookup`
- `Design Status`: `active`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `2026-03-10T05:14:33Z`

## Summary
This document defines the feature-level design for a human-readable command-page family under `docs/commands/` and a machine-readable command index under `core/control_plane/indexes/commands/`.

## Source Request
- User request for strong human-readable command documentation and an index that can look up commands and route to their man pages.

## Scope and Feature Boundary
- Covers the command-doc family, command-page template, and command-index artifact family.
- Covers the first command documentation for the `watchtower-core` CLI.
- Covers the relationship between human command pages and machine-readable command lookup.
- Does not define shell completions, external man-page generation, or richer command discovery beyond the current governed command-doc and command-index surfaces.
- Does not introduce database-backed command search.

## Current-State Context
- `core/python/` now exists as the consolidated Python workspace and exposes `watchtower-core` command families for `doctor`, `query`, `sync`, `closeout`, and `validate`.
- The repository now has a dedicated command-doc family under `docs/commands/`.
- The repository now publishes a governed command-specific machine-readable index at `core/control_plane/indexes/commands/command_index.v1.json`.
- Current command discovery can start from `docs/commands/`, the command index, or the repository path index rather than reading package code directly.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keep discovery local, explicit, and inspectable rather than relying on hidden heuristics.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): keep core command surfaces operational and support-oriented rather than product-marketing surfaces.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): use Markdown for human guidance and JSON for machine-readable lookup surfaces.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep one canonical purpose per artifact and avoid parallel truth between docs and machine-readable indexes.

## Internal Standards and Canonical References Applied
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command pages need a stable human-readable synopsis, options, examples, and behavior shape.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): command lookup needs a governed machine index with stable command identities and doc links.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): command examples and workspace assumptions should stay anchored to `core/python/`.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): command-doc and command-index surfaces need to remain discoverable through the repository path index.
- [command_reference_template.md](/home/j/WatchTowerPlan/docs/templates/command_reference_template.md): each command page should share the same predictable authoring shape.

## Design Goals and Constraints
- Give humans one obvious place to find command docs.
- Give automation one obvious place to look up available commands and route to their docs.
- Keep machine authority for the command surface in the registry-backed CLI parser tree while preserving command pages as the human-readable companion layer.
- Keep command docs and machine lookup synchronized in the same change set.
- Keep the first design modular enough that future commands can be added one page and one index entry at a time.
- Avoid duplicating full man-page content inside the machine-readable index.

## Options Considered
### Option 1
- Put all command guidance into workspace READMEs.
- Strengths: fewest files and minimal new structure.
- Tradeoffs or reasons not chosen: poor lookup granularity, weak routing for subcommands, and mixes onboarding with command semantics.

### Option 2
- Add `docs/commands/` for human pages and a dedicated command index for machine lookup.
- Strengths: clear split between human docs and machine routing, easy to grow as commands expand, and consistent with the existing docs plus control-plane model.
- Tradeoffs or reasons not chosen: requires a new standard, template, docs family, schema, and index artifact.

### Option 3
- Generate shell man pages directly from CLI definitions and skip repository-native docs.
- Strengths: command docs stay close to code and could scale well later.
- Tradeoffs or reasons not chosen: premature for the current command surface and weak for repo-native context such as workspace assumptions and source-surface links.

## Recommended Design
### Architecture
- Add a human-readable command-doc family under `docs/commands/`.
- Group command pages by command family, starting with `docs/commands/core_python/`.
- Add a machine-readable command index under `core/control_plane/indexes/commands/`.
- Keep command pages as the human man-page layer.
- Keep the command index as the routing and lookup layer that points to command pages and code surfaces.
- Use the registry-backed CLI parser tree as the machine source for command presence, hierarchy, synopsis, and output-format metadata.
- Keep command pages as required human-readable companion docs rather than the machine-authoritative source.

### Data and Interface Impacts
- Add command-document and command-index standards.
- Add a command-page template for future command docs.
- Add a published command-index schema, live command index, and valid or invalid examples.
- Update the repository path index so both humans and automation can find the new command-doc and command-index roots.

### Execution Flow
1. An engineer wants to discover or remember a command.
2. Human navigation starts at `docs/commands/` and the command-family README.
3. Machine lookup starts at the command index, which is rebuilt from the registry-backed CLI parser tree and resolves to the command page plus source surface.
4. The engineer or agent reads the command page for synopsis, arguments, examples, and current behavior.
5. The command doc and index stay aligned in the same change set whenever the command surface changes.

### Invariants and Failure Cases
- Command pages remain the human-readable semantic surface.
- The command index remains lookup-oriented and must not replace the command docs.
- Registry-backed CLI metadata is the machine authority for command existence and structure, while command pages remain the human-readable semantic companion surface.
- Every indexed command must have a command page.
- Subcommand entries must be tied to a stable parent command.
- Stale command docs or stale index entries are treated as documentation drift, not acceptable backlog.

## Affected Surfaces
- `docs/commands/`
- `docs/standards/documentation/command_md_standard.md`
- `docs/standards/data_contracts/command_index_standard.md`
- `docs/templates/command_reference_template.md`
- `core/control_plane/schemas/artifacts/command_index.v1.schema.json`
- `core/control_plane/indexes/commands/command_index.v1.json`

## Design Guardrails
- Keep one command or subcommand per command page.
- Keep the machine-readable index small and routing-oriented.
- Keep the first rollout tied to commands that actually exist in the repo today.
- Update command docs, command indexes, and command-family READMEs together.

## Implementation-Planning Handoff Notes
- The first command-doc rollout should document `watchtower-core` and `watchtower-core doctor`.
- Future implementation planning can add richer command-generation helpers later, but they should preserve the registry-backed authority split and companion command docs.
- Future command growth should add new docs and index entries rather than widening the first pages into catch-all command catalogs.

## Dependencies
- The `watchtower-core` CLI parser and registry surfaces under `core/python/src/watchtower_core/cli/`.
- The repository path index and schema catalog for adjacent machine-readable lookup.

## Risks
- If command docs are updated without the command index, machine lookup will drift quickly.
- If command pages are too sparse, engineers will fall back to reading code instead of using the docs.
- If command pages start mixing onboarding, design rationale, and command semantics heavily, the family will become hard to maintain.

## Open Questions
- When the CLI grows options and additional subcommands, should the command index grow lightweight option summaries, or should it remain command-level only?

## References
- [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_python_workspace_and_harness.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md)
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md)

## Updated At
- `2026-03-10T05:14:33Z`
