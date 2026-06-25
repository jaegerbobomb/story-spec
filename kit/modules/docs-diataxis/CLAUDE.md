# Module `docs-diataxis` — CLAUDE fragment

> Documentation discipline for the application built with story-spec: structure the
> product docs along the four [Diátaxis](https://diataxis.fr) modes.

## Rule

Project documentation lives under `docs/` and is organized by **purpose**, not by
feature:

| Mode | Answers | Goes in |
|---|---|---|
| Tutorial | "teach me, step by step" | `docs/tutorials/` |
| How-to | "help me do task X" | `docs/how-to/` |
| Reference | "tell me exactly" | `docs/reference/` |
| Explanation | "help me understand why" | `docs/explanation/` |

- When a `done` story introduces a **user-facing** capability, add or update the
  matching doc(s) in the **same PR** — at minimum a how-to or a reference entry.
- Never mix modes in one page (a tutorial is not a reference).
- The story file stays the spec; Diátaxis docs are the user-facing companion, never
  a paraphrase of the acceptance criteria.

Keeps product docs discoverable and in step with delivered stories.
