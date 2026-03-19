# Routing Table

Use this table to select the minimum workflow modules required for a request. Treat trigger keywords as examples and route from the full prompt context. Always load `modules/core.md`, then load only the modules needed for the matched task type(s).

Workflow modules are available building blocks, but they are active only when the routing result selects them or an active route explicitly merges them.

If the request includes explicit commit intent, merge `modules/commit_closeout.md` into the dominant route or use the Commit Closeout route alone when commit creation is the only requested task.

| Task Type | Trigger Keywords (Examples) | Required Workflows |
|---|---|---|
| `<task type>` | `<keyword 1>, <keyword 2>, <keyword 3>` | `modules/core.md`, `modules/<workflow>.md` |
