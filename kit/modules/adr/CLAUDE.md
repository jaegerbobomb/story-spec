# Module `adr` — CLAUDE fragment

> Activated by `modules: [adr]`. Imported into `CLAUDE.dist.md`.

## When to write an ADR

Record an **architecture decision** (Architecture Decision Record) whenever a choice:

- is **structural** and **costly to reverse** (stack, bounded context boundary, exchange
  format, persistence choice, cross-cutting convention); or
- **supersedes** an earlier decision.

Do not create an ADR for local implementation details (those stay in the story/SPEC).

## Procedure

1. Sequential number `NNNN` (4 digits, never reused).
2. `docs/adr/NNNN-slug.md` from `modules/adr/templates/NNNN-title.md` (lightweight MADR format).
3. Initial status `proposed` → `accepted` after validation. A superseded decision moves to
   `superseded` with a link to the ADR that replaces it.
4. **Link from impacted stories**: add `adr: [NNNN]` to the story's frontmatter
   (field provided by this module), or cite the ADR under `## Notes`.

Shortcut: the **`adr-new`** skill scaffolds the file, assigns the number and pre-fills the
frontmatter.

## ADR statuses

`proposed` → `accepted` → (`superseded` | `deprecated`). `rejected` for a proposal that was not
adopted (kept for the record).
