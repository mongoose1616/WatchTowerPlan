# `core/python/tests/fixtures`

## Description
`This directory contains shared fixture data for Python tests when authored control-plane examples are not sufficient by themselves.`

## Files
| Path | Description |
|---|---|
| `core/python/tests/fixtures/README.md` | Describes the purpose of the Python test-fixtures directory. |
| `core/python/tests/fixtures/packs/fixture/` | Neutral synthetic fixture pack used to materialize temporary hosted-pack repos for shared-core validation scenarios. Tests should treat this as template data rather than as a required live-pack import contract. The materializer derives pack identity from the target pack root by default, so new shared-core tests should not hard-code `plan` or any other live pack unless the behavior under test truly requires that exact pack. |

## Guidance
- Shared-core tests should prefer these fixture-pack roots over direct dependence on one live donor pack root.
- If one scenario truly proves behavior unique to the live `plan/` pack, keep that proof under the owning pack root or gate it explicitly so copied shared-core suites still pass in repositories that do not carry `plan/`.
