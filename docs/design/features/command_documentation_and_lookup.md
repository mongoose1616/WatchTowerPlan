# Command Documentation and Lookup Design

## Summary
This document defines the feature-level design for a human-readable command-page family under `docs/commands/` and a machine-readable command index under `core/control_plane/indexes/commands/`.

## Source Request
- User request for strong human-readable command documentation and an index that can look up commands and route to their man pages.

## Scope and Feature Boundary
- Covers the command-doc family, command-page template, and command-index artifact family.
- Covers the first command documentation for the `watchtower-core` CLI.
- Covers the relationship between human command pages and machine-readable command lookup.
- Does not implement richer CLI behavior beyond the current scaffolded command surface.
- Does not introduce shell completions, external man-page generation, or database-backed command search.

## Current-State Context
- `core/python/` now exists as the consolidated Python workspace and exposes a thin `watchtower-core` CLI with a `doctor` subcommand.
- The repository does not yet have a dedicated command-doc family under `docs/`.
- The repository does not yet publish a command-specific machine-readable index.
- Current command discovery would require reading package code or general workspace READMEs directly.

## Foundations References Applied
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md): keep discovery local, explicit, and inspectable rather than relying on hidden heuristics.
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md): keep core command surfaces operational and support-oriented rather than product-marketing surfaces.
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md): use Markdown for human guidance and JSON for machine-readable lookup surfaces.
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md): keep one canonical purpose per artifact and avoid parallel truth between docs and machine-readable indexes.

## Internal Standards and Canonical References Applied
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md)
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [command_reference_template.md](/home/j/WatchTowerPlan/docs/templates/command_reference_template.md)

## Design Goals and Constraints
- Give humans one obvious place to find command docs.
- Give automation one obvious place to look up available commands and route to their docs.
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

### Data and Interface Impacts
- Add command-document and command-index standards.
- Add a command-page template for future command docs.
- Add a published command-index schema, live command index, and valid or invalid examples.
- Update the repository path index so both humans and automation can find the new command-doc and command-index roots.

### Execution Flow
1. An engineer wants to discover or remember a command.
2. Human navigation starts at `docs/commands/` and the command-family README.
3. Machine lookup starts at the command index and resolves to the command page and source surface.
4. The engineer or agent reads the command page for synopsis, arguments, examples, and current behavior.
5. The command doc and index stay aligned in the same change set whenever the command surface changes.

### Invariants and Failure Cases
- Command pages remain the human-readable semantic surface.
- The command index remains lookup-oriented and must not replace the command docs.
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
- Future implementation planning can add command-generation helpers later, but only after the baseline doc and index shape stabilizes.
- Future command growth should add new docs and index entries rather than widening the first pages into catch-all command catalogs.

## Dependencies
- The `watchtower-core` CLI scaffold in `core/python/src/watchtower_core/cli/main.py`.
- The repository path index and schema catalog for adjacent machine-readable lookup.

## Risks
- If command docs are updated without the command index, machine lookup will drift quickly.
- If command pages are too sparse, engineers will fall back to reading code instead of using the docs.
- If command pages start mixing onboarding, design rationale, and command semantics heavily, the family will become hard to maintain.

## Open Questions
- When the CLI grows options and additional subcommands, should the command index grow lightweight option summaries, or should it remain command-level only?
- Should a later CLI feature generate the command index automatically from code and docs, or remain reviewed and maintained manually?

## References
- [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/design/features/core_python_workspace_and_harness.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md)
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md)

## Last Synced
- `2026-03-09`
