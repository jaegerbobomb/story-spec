# Module `github-piloting` — CLAUDE fragment

> Live tracking of the backlog on GitHub, complementing the `stories/` files (durable spec).

## Two levels

| Level | Where | Role |
|---|---|---|
| Durable spec | `stories/S<NNN>.md` | definition, criteria, status |
| Live tracking | GitHub `[Epic]` issues + sub-issues | cross-session tracking, ordering, log |

## Conventions

- **One epic = one batch of workstreams** (often aligned to a milestone). It carries: a task list of
  the remaining work, a reminder of the conventions, and a **session log** (one line per session:
  merged PRs + version).
- **One sub-issue = one story** (`S<NNN>`): condensed spec + link to the `stories/` file
  (no duplication) + Definition of Done.
- **Starting the next task**: open the active epic → first open sub-issue → read
  the story → `in_progress` → branch from `main` → ship (PR, merge on green checks,
  `close #NNN`, story `done`, bump) → check off the sub-issue + add a line to the log.
- **Auto-close**: `fix #NNN`/`close #NNN` in the commit body.

## Guardrail

Never include a chat session link in a GitHub artifact (commit, PR, comment).
