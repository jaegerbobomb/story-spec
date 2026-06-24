# Module `adr` — SPEC section (insert into SPEC.md if module enabled)

## Architecture Decision Records

Architecture decisions live in `docs/adr/NNNN-slug.md` (lightweight MADR format, cf.
`modules/adr/templates/NNNN-title.md`).

- **Single source** of structural decisions: what is in an `accepted` ADR is authoritative.
  `SPEC.md` describes the current state; ADRs describe **why** we got there and the history.
- Sequential `NNNN` numbering, never reused; an ADR is never deleted — it is
  `superseded`/`deprecated`.
- A story can reference its decisions via the frontmatter field `adr: [NNNN, …]`.
- Index: `docs/adr/README.md` (generatable table, status + title + date).
