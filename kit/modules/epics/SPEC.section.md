# Module `epics` — SPEC section (insert into SPEC.md if module enabled)

## Epics

An epic groups stories that serve one goal. Each epic used in a story's `epic:` field
has one file `epics/<epic>.md`, where `<epic>` is exactly the value of that field.

### Frontmatter

```yaml
---
id: auth                 # = the file name and the stories' `epic:` value
title: "Accounts"        # human-readable, ≤ 8 words
order: 1                 # position in the roadmap; lower comes first
status: active           # planned | active | done | dropped
updated: "2026-11-24"    # ISO 8601
---
```

| Status | Meaning |
|---|---|
| `planned` | Written, not started. A new epic is born here. |
| `active` | At least one of its stories is being worked on, or next in line. |
| `done` | Every exit criterion is met. |
| `dropped` | Abandoned — kept for history, like an `archived` story. |

### Sections

- `## Goal` (required) — why the epic exists, in two or three sentences.
- `## Exit criteria` (required) — a checklist (`- [ ]` / `- [x]`) of observable
  conditions. The epic is `done` when every box is ticked.
- `## Out of scope` (optional) — what a reader could expect here and will not find.
- `## Notes` (optional) — decisions, open questions, links.

The epic file does **not** list its stories: they are found by their `epic:` field.

### Lint

`lint_stories.py --epics-dir=epics` checks that every story's `epic` has a file, and
that every epic file is well-formed (frontmatter keys, `status`, `order`, the two
required sections). Without `--epics-dir`, epics are not checked.
