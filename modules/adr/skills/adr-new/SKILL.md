---
name: adr-new
description: >-
  Creates a new Architecture Decision Record. Use when the user decides something
  structural or costly to reverse (stack, context boundary, exchange format,
  persistence, cross-cutting convention), or supersedes an existing decision. Triggers:
  "let's settle that…", "new architecture decision", "ADR for…", "we're replacing the decision…".
---

# adr-new

Scaffolds an ADR conforming to the `adr` module.

## Steps

1. **Determine the number**: next `NNNN` = max of the existing numbers in `docs/adr/` + 1,
   on 4 digits. If `docs/adr/` does not exist, create it + start at `0001`.
2. **Slug**: short kebab-case derived from the title.
3. **Create** `docs/adr/NNNN-slug.md` from `modules/adr/templates/NNNN-title.md`,
   pre-filling: number, title, today's date, status `proposed`.
4. **Fill in** Context / Decision / Consequences / Alternatives from the exchange. Do not
   invent: if a section is unknown, ask **one** targeted question rather than padding.
5. **Link**: if stories are concerned, add `adr: [NNNN]` to their frontmatter (or note it
   under `## Notes`).
6. **Superseding**: if this ADR replaces another, move the old one to
   `superseded by ADR-NNNN` and cite it.
7. **Index**: update `docs/adr/README.md` (create the table if absent).

## Output

Path of the created file + reminder: status `proposed`, to move to `accepted` after validation.
