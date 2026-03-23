# `plan/python/tests/integration`

## Description
`This directory contains the plan-owned integration suite for live workspace, initiative, task, query, sync, closeout, and other repo-local orchestration flows that are specific to watchtower_plan.`

## Notes
- These tests may import `watchtower_plan` directly and may exercise live `plan/` workspace state or plan-native command paths.
- Reusable-core integration tests that must stay portable across copied-core repositories belong under `core/python/tests/integration/` instead.
- Prefer `watchtower_plan.testing` helpers for repeated plan-owned setup instead of reintroducing donor-specific helpers into `core/python/tests/`.
