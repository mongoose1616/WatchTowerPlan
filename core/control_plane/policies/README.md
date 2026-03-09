# `core/control_plane/policies`

## Description
`This directory holds machine-readable guardrails used by the helper and harness layers. Keep policy content explicit, testable, and separate from code paths that enforce it.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/policies/README.md` | Describes the purpose of the policies directory and its main policy families. |
| `core/control_plane/policies/validation/` | Validation gate policy and fail-closed requirements. |
| `core/control_plane/policies/execution/` | Execution-safety and command-scope guardrails. |
| `core/control_plane/policies/release/` | Release publication and evidence expectations. |
