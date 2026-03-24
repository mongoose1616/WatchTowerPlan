# Routing Table

Use this table to select the minimum workflow documents required for a request. Treat trigger keywords as examples and route from the full prompt context. Always load `modules/core.md`, then load only the modules and roles needed for the matched task type(s).

Workflow documents are available building blocks, but they are active only when the routing result selects them or an active route explicitly merges them.

Workflow roles may publish `Composes Modules` sections for auditability, but the routing table remains the authority for which workflow documents become active for one request.

If the request includes explicit commit intent, merge `modules/commit_closeout.md` into the dominant route or use the Commit Closeout route alone when commit creation is the only requested task.

| Task Type | Trigger Keywords (Examples) | Required Workflows |
|---|---|---|
| `<task type>` | `<keyword 1>, <keyword 2>, <keyword 3>` | `modules/core.md`, `modules/<workflow>.md`, `roles/<role>.md` |
