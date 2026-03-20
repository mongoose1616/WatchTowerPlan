---
id: "ref.argparse_subcommands"
title: "argparse Subcommands Reference"
summary: "Distilled reference for building nested CLI subcommands with stable handler dispatch."
type: "reference"
status: "active"
tags:
  - "reference"
  - "python"
  - "argparse"
owner: "repository_maintainer"
updated_at: "2026-03-20T17:12:07Z"
audience: "shared"
authority: "reference"
---

# argparse Subcommands Reference

## Summary
This reference captures the `argparse` behavior that matters when one host CLI needs reusable root commands plus namespaced domain-pack command families.

## Purpose
Keep command registration and dispatch predictable while the repository moves from flat plan-centric commands to a host-plus-pack namespaced CLI.

## Scope
- Covers nested subparser registration, defaults-based handler dispatch, and help-structure choices.
- Covers repository-relevant decisions for namespaced command trees such as `watchtower-core plan query ...`.
- Does not replace the repository's CLI architecture standards or command docs.

## Canonical Upstream
- `https://docs.python.org/3/library/argparse.html` - Python standard-library reference for `argparse`.

## Related Standards and Sources
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [watchtower_core.md](/core/docs/commands/core_python/watchtower_core.md)

## Quick Reference or Distilled Reference
### Core Mechanics
| Mechanic | Practical Meaning | Notes |
|---|---|---|
| `add_subparsers()` | Creates a subcommand layer. | Use one layer per command boundary: root, pack namespace, then pack capability families. |
| `dest=` | Stores the chosen command name in the parsed namespace. | Keep names stable and explicit for diagnostics and tests. |
| `required=` | Forces one subcommand to be chosen. | Useful for inner command families when a bare namespace should not execute work. |
| `set_defaults(handler=...)` | Attaches the callable to execute after parsing. | Prefer explicit handler binding over large `if/elif` dispatch blocks. |
| formatter and epilog examples | Controls help readability. | Use it to keep deep command trees discoverable. |

### Rules or Decision Points
- Build the tree from stable boundaries: root shared commands, pack namespace, then pack capabilities such as `query`, `task`, `sync`, and `closeout`.
- Bind handlers at the narrowest practical parser node with `set_defaults(...)`.
- Keep the root parser pack-agnostic. Pack-specific help and examples belong under the pack namespace.
- Treat parser construction as composition logic, not reusable-core logic.
- Keep one registrar per command family so host registration and pack registration are both testable and diff-friendly.

### Decision Table
| Question | Preferred Answer | Why |
|---|---|---|
| Where should `plan` be registered? | As one namespace under the host root parser. | Keeps reusable root commands separate from pack runtime. |
| How should deep commands be dispatched? | Parser-bound handlers via `set_defaults(handler=...)`. | Avoids a central dispatch switch that must know every pack command. |
| Should pack examples appear in root help? | Only sparingly. | Root help should stay readable and reusable-core first. |
| Should inner families require a subcommand? | Yes for work-performing families. | Prevents ambiguous no-op invocations. |

### Pitfalls and Failure Modes
- Flattening every pack command into the root parser makes the host feel pack-specific and scales poorly.
- Reusing one `dest` name across multiple levels makes debugging parsed namespaces harder.
- Registering pack commands through side effects at import time makes collision checks and tests less deterministic.
- Putting domain logic into parser builders instead of separate handlers makes CLI refactors much harder.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [pyproject.toml](/core/python/pyproject.toml)
- [watchtower_core.md](/core/docs/commands/core_python/watchtower_core.md)
- [watchtower_core_plan.md](/core/docs/commands/core_python/watchtower_core_plan.md)

### Why It Matters Here
- The repository is moving toward `watchtower-core <pack> ...` namespacing, which depends on nested subparsers rather than more flat command families.
- This reference supports the host-runtime split by keeping CLI composition in one explicit layer and allowing pack command registration through typed integration hooks.

### If Local Policy Tightens
- Update the host-runtime standard, domain-pack authoring reference, and command docs in the same slice when parser conventions change.
- Update CLI tests when handler-binding or namespace structure rules change.

## Process or Workflow
1. Register shared root commands first.
2. Register one parser per pack namespace.
3. Register each pack capability family beneath that namespace with explicit handlers.
4. Keep help examples local to the parser layer that owns them.

## Examples
- `watchtower-core plan bootstrap`
- `watchtower-core plan query initiatives --format json`
- `watchtower-core pack validate --pack plan --format json`

## References
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)
- [watchtower_core.md](/core/docs/commands/core_python/watchtower_core.md)

## Notes
- Canonical upstream source was reviewed on 2026-03-20 during the host-pack boundary hard-cutover tranche.

## Updated At
- `2026-03-20T17:12:07Z`
