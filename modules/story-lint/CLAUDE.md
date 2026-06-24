# Module `story-lint` — CLAUDE fragment

> The story file is the spec; CI enforces it. `scripts/lint_stories.py` validates
> every story — the "third audience: CI" applied to the spec itself.

## Rule

A story must be **well-formed before it is implemented**. Run
`python3 scripts/lint_stories.py --stories-dir=stories` before moving a story to
`in_progress`, and in CI on every PR:

- filename `S<NNN>-<kebab-slug>.md`, with `id` matching the filename;
- required frontmatter complete (`id, title, epic, depends_on, status, estimate, bdd`);
- valid `status` (6-state lifecycle) and `estimate`;
- `bdd: true` ⇒ at least one scenario with steps under `## Acceptance Criteria`;
- `updated` present (warning) and `depends_on` ids resolvable (warning).

Errors fail the run; `--strict` also fails on warnings. Fix lint errors before coding.
